from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

from config import Config
from db import db
from models.users import User
from models.plans import Plan
from models.subscriptions import Subscription
from models.usage import Usage
from models.discounts import Discount
from models.audit_logs import AuditLog
from models.alerts import Alert

from routes.admin_routes import admin_bp
from routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'], supports_credentials=True)
    
    # Register blueprints
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/user')
    
    # Create tables and insert demo data
    with app.app_context():
        db.create_all()
        create_demo_data()
    
    return app

def create_demo_data():
    """Create demo admin and user if they don't exist"""
    # Create demo admin user
    admin_user = User.query.filter_by(email='admin@example.com').first()
    if not admin_user:
        admin_user = User(
            name='Admin User',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin_user)
        print("Demo admin user created: admin@example.com / admin123")
    
    # Create demo regular user
    demo_user = User.query.filter_by(email='user@example.com').first()
    if not demo_user:
        demo_user = User(
            name='Demo User',
            email='user@example.com',
            password_hash=generate_password_hash('user123'),
            role='user'
        )
        db.session.add(demo_user)
        print("Demo user created: user@example.com / user123")
    
    # Create demo plans
    basic_plan = Plan.query.filter_by(name='Basic Plan').first()
    if not basic_plan:
        basic_plan = Plan(
            name='Basic Plan',
            description='Perfect for light users with basic data needs',
            monthly_price=29.99,
            monthly_quota_gb=10,
            is_active=True
        )
        db.session.add(basic_plan)
        print("Demo Basic Plan created")
    
    premium_plan = Plan.query.filter_by(name='Premium Plan').first()
    if not premium_plan:
        premium_plan = Plan(
            name='Premium Plan',
            description='Ideal for heavy users with unlimited data',
            monthly_price=59.99,
            monthly_quota_gb=100,
            is_active=True
        )
        db.session.add(premium_plan)
        print("Demo Premium Plan created")
    
    # Add more demo plans
    starter_plan = Plan.query.filter_by(name='Starter Plan').first()
    if not starter_plan:
        starter_plan = Plan(
            name='Starter Plan',
            description='Perfect for beginners with basic needs',
            monthly_price=9.99,
            monthly_quota_gb=2,
            is_active=True
        )
        db.session.add(starter_plan)
        print("Demo Starter Plan created")
    
    business_plan = Plan.query.filter_by(name='Business Plan').first()
    if not business_plan:
        business_plan = Plan(
            name='Business Plan',
            description='Designed for small businesses and teams',
            monthly_price=99.99,
            monthly_quota_gb=500,
            is_active=True
        )
        db.session.add(business_plan)
        print("Demo Business Plan created")
    
    enterprise_plan = Plan.query.filter_by(name='Enterprise Plan').first()
    if not enterprise_plan:
        enterprise_plan = Plan(
            name='Enterprise Plan',
            description='Unlimited data for large organizations',
            monthly_price=199.99,
            monthly_quota_gb=1000,
            is_active=True
        )
        db.session.add(enterprise_plan)
        print("Demo Enterprise Plan created")
    
    # Add more diverse demo plans
    student_plan = Plan.query.filter_by(name='Student Plan').first()
    if not student_plan:
        student_plan = Plan(
            name='Student Plan',
            description='Special discount for students with valid ID',
            monthly_price=14.99,
            monthly_quota_gb=5,
            is_active=True
        )
        db.session.add(student_plan)
        print("Demo Student Plan created")
    
    family_plan = Plan.query.filter_by(name='Family Plan').first()
    if not family_plan:
        family_plan = Plan(
            name='Family Plan',
            description='Perfect for families with multiple devices',
            monthly_price=79.99,
            monthly_quota_gb=200,
            is_active=True
        )
        db.session.add(family_plan)
        print("Demo Family Plan created")
    
    gamer_plan = Plan.query.filter_by(name='Gamer Plan').first()
    if not gamer_plan:
        gamer_plan = Plan(
            name='Gamer Plan',
            description='High-speed connection optimized for gaming',
            monthly_price=89.99,
            monthly_quota_gb=300,
            is_active=True
        )
        db.session.add(gamer_plan)
        print("Demo Gamer Plan created")
    
    professional_plan = Plan.query.filter_by(name='Professional Plan').first()
    if not professional_plan:
        professional_plan = Plan(
            name='Professional Plan',
            description='For remote workers and professionals',
            monthly_price=129.99,
            monthly_quota_gb=400,
            is_active=True
        )
        db.session.add(professional_plan)
        print("Demo Professional Plan created")
    
    unlimited_plan = Plan.query.filter_by(name='Unlimited Plan').first()
    if not unlimited_plan:
        unlimited_plan = Plan(
            name='Unlimited Plan',
            description='Truly unlimited data with no restrictions',
            monthly_price=149.99,
            monthly_quota_gb=9999,
            is_active=True
        )
        db.session.add(unlimited_plan)
        print("Demo Unlimited Plan created")
    
    # Create demo subscription for the user
    if demo_user and basic_plan:
        demo_subscription = Subscription.query.filter_by(user_id=demo_user.id).first()
        if not demo_subscription:
            demo_subscription = Subscription(
                user_id=demo_user.id,
                plan_id=basic_plan.id,
                status='active',
                start_date=datetime.now().date(),
                end_date=None,
                price_paid=29.99
            )
            db.session.add(demo_subscription)
            print("Demo subscription created for user")
    
    db.session.commit()
    print("Demo data setup completed!")
    
    # Create expiry alerts for active subscriptions
    create_expiry_alerts()

def create_expiry_alerts():
    """Create alerts for subscriptions expiring in 2 days"""
    from datetime import datetime, timedelta
    
    # Calculate date 2 days from now
    alert_date = datetime.now().date() + timedelta(days=2)
    
    # Find subscriptions expiring in 2 days
    expiring_subscriptions = Subscription.query.filter(
        Subscription.end_date == alert_date,
        Subscription.status == 'active'
    ).all()
    
    for subscription in expiring_subscriptions:
        # Check if alert already exists for this subscription
        existing_alert = Alert.query.filter_by(
            user_id=subscription.user_id,
            message__like='%Plan Expiring Soon%'
        ).first()
        
        if not existing_alert:
            alert = Alert(
                user_id=subscription.user_id,
                type='plan_expiry',
                message=f'Plan Expiring Soon: Your {subscription.plan.name} plan will expire on {subscription.end_date}. Please renew to continue service.',
                is_read=False
            )
            db.session.add(alert)
            print(f"Created expiry alert for user {subscription.user_id}")
    
    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)
