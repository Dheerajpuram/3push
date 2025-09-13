from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from models.users import User
from models.audit_logs import AuditLog
from db import db
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['POST'])
def admin_login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find admin user
        admin_user = User.query.filter_by(email=email, role='admin').first()
        
        if not admin_user or not check_password_hash(admin_user.password_hash, password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Log the login action
        audit_log = AuditLog(
            user_id=admin_user.id,
            action='admin_login',
            table_name='users',
            record_id=admin_user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': admin_user.to_dict(),
            'redirect_url': '/admin/dashboard'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Placeholder routes for future development
@admin_bp.route('/dashboard', methods=['GET'])
def admin_dashboard():
    return jsonify({'message': 'Admin dashboard - to be implemented'}), 200

@admin_bp.route('/plans', methods=['GET', 'POST'])
def manage_plans():
    return jsonify({'message': 'Manage plans - to be implemented'}), 200

@admin_bp.route('/discounts', methods=['GET', 'POST'])
def manage_discounts():
    return jsonify({'message': 'Manage discounts - to be implemented'}), 200

@admin_bp.route('/users', methods=['GET'])
def manage_users():
    return jsonify({'message': 'Manage users - to be implemented'}), 200

@admin_bp.route('/analytics', methods=['GET'])
def analytics():
    return jsonify({'message': 'Analytics - to be implemented'}), 200
