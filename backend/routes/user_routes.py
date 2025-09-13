from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.users import User
from models.plans import Plan
from models.subscriptions import Subscription
from models.audit_logs import AuditLog
from db import db
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/signup', methods=['POST'])
def user_signup():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if not all([name, email, password]):
            return jsonify({'error': 'Name, email, and password are required'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 400
        
        # Create new user
        new_user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            role='user'
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Log the signup action
        audit_log = AuditLog(
            user_id=new_user.id,
            action='user_signup',
            table_name='users',
            record_id=new_user.id,
            new_values={'email': email, 'name': name},
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'user': new_user.to_dict(),
            'redirect_url': '/user/dashboard'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/login', methods=['POST'])
def user_login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user
        user = User.query.filter_by(email=email, role='user').first()
        
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Log the login action
        audit_log = AuditLog(
            user_id=user.id,
            action='user_login',
            table_name='users',
            record_id=user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user.to_dict(),
            'redirect_url': '/user/dashboard'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Plans and Subscriptions routes
@user_bp.route('/plans', methods=['GET'])
def get_plans():
    try:
        plans = Plan.query.filter_by(is_active=True).all()
        return jsonify({
            'success': True,
            'plans': [plan.to_dict() for plan in plans]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/plans/<int:plan_id>', methods=['GET'])
def get_plan_details(plan_id):
    try:
        plan = Plan.query.get(plan_id)
        if not plan:
            return jsonify({'error': 'Plan not found'}), 404
        
        return jsonify({
            'success': True,
            'plan': plan.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/my-plan', methods=['GET'])
def get_my_plan():
    try:
        # Get user from request headers or session
        user_id = request.headers.get('User-ID')
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        # Get user's active subscription
        subscription = Subscription.query.filter_by(
            user_id=user_id, 
            status='active'
        ).first()
        
        if not subscription:
            return jsonify({
                'success': True,
                'has_plan': False,
                'message': 'No active plan found'
            }), 200
        
        # Get plan details
        plan = Plan.query.get(subscription.plan_id)
        
        return jsonify({
            'success': True,
            'has_plan': True,
            'subscription': subscription.to_dict(),
            'plan': plan.to_dict() if plan else None
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/purchase-plan', methods=['POST'])
def purchase_plan():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        plan_id = data.get('plan_id')
        
        if not user_id or not plan_id:
            return jsonify({'error': 'User ID and Plan ID are required'}), 400
        
        # Validate user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        # Validate plan exists
        plan = Plan.query.get(plan_id)
        if not plan:
            return jsonify({'error': 'Plan not found'}), 404
            
        # Check if user already has an active subscription
        existing_subscription = Subscription.query.filter_by(
            user_id=user_id, 
            status='active'
        ).first()
        
        if existing_subscription:
            # Cancel existing subscription
            existing_subscription.status = 'cancelled'
            existing_subscription.end_date = datetime.now().date()
        
        # Create new subscription
        new_subscription = Subscription(
            user_id=user_id,
            plan_id=plan_id,
            status='active',
            start_date=datetime.now().date(),
            end_date=None,
            price_paid=plan.monthly_price
        )
        
        db.session.add(new_subscription)
        
        # Log the purchase
        audit_log = AuditLog(
            user_id=user_id,
            action='plan_purchased',
            table_name='subscriptions',
            record_id=new_subscription.id,
            new_values={'plan_id': plan_id, 'price_paid': float(plan.monthly_price)},
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Plan purchased successfully',
            'subscription': new_subscription.to_dict(),
            'plan': plan.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/cancel-plan', methods=['POST'])
def cancel_plan():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
            
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        # Find active subscription
        active_subscription = Subscription.query.filter_by(
            user_id=user_id,
            status='active'
        ).first()
        
        if not active_subscription:
            return jsonify({'error': 'No active subscription found'}), 404
            
        # Cancel the subscription
        active_subscription.status = 'cancelled'
        active_subscription.end_date = datetime.now().date()
        
        # Create alert for plan cancellation
        from models.alerts import Alert
        alert = Alert(
            user_id=user_id,
            type='system',
            message=f'Plan Cancelled: Your {active_subscription.plan.name} plan has been cancelled. You will continue to have access until {active_subscription.end_date}.',
            is_read=False
        )
        db.session.add(alert)
        
        # Log the cancellation
        audit_log = AuditLog(
            user_id=user_id,
            action='plan_cancelled',
            table_name='subscriptions',
            record_id=active_subscription.id,
            old_values={'status': 'active'},
            new_values={'status': 'cancelled', 'end_date': active_subscription.end_date.isoformat()},
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Plan cancelled successfully',
            'subscription': active_subscription.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/alerts', methods=['GET'])
def get_user_alerts():
    try:
        user_id = request.headers.get('User-ID')
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
            
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        from models.alerts import Alert
        alerts = Alert.query.filter_by(user_id=user_id).order_by(Alert.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'alerts': [alert.to_dict() for alert in alerts]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/alerts/<int:alert_id>/read', methods=['PUT'])
def mark_alert_read(alert_id):
    try:
        user_id = request.headers.get('User-ID')
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
            
        from models.alerts import Alert
        alert = Alert.query.filter_by(id=alert_id, user_id=user_id).first()
        
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
            
        alert.is_read = True
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Alert marked as read'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Placeholder routes for future development
@user_bp.route('/dashboard', methods=['GET'])
def user_dashboard():
    return jsonify({'message': 'User dashboard - to be implemented'}), 200

@user_bp.route('/subscriptions', methods=['GET', 'POST'])
def my_subscriptions():
    return jsonify({'message': 'My subscriptions - to be implemented'}), 200

@user_bp.route('/recommendations', methods=['GET'])
def plan_recommendations():
    return jsonify({'message': 'Plan recommendations - to be implemented'}), 200

@user_bp.route('/usage', methods=['GET'])
def usage_history():
    return jsonify({'message': 'Usage history - to be implemented'}), 200

@user_bp.route('/billing', methods=['GET'])
def billing():
    return jsonify({'message': 'Billing - to be implemented'}), 200
