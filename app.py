from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_jwt_extended.jwt_manager import JWTManager
from flask_jwt_extended.utils import create_access_token, get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, datetime
import os
import json
from dotenv import load_dotenv
from ai_service import generate_travel_plan, generate_destination, generate_itinerary
import logging
from logging.handlers import RotatingFileHandler

# Load environment variables
load_dotenv()

# Configure logging
if not os.path.exists('logs'):
    os.makedirs('logs')
file_handler = RotatingFileHandler('logs/travelplanner.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)

app = Flask(__name__)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('TravelPlanner startup')

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///travelplanner.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Initialize extensions
CORS(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    travel_plans = db.relationship('TravelPlan', backref='user', lazy=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def __init__(self, email, password, full_name):
        self.email = email
        self.password = password
        self.full_name = full_name

class TravelPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    destination = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    preferences = db.Column(db.JSON, nullable=False)
    itinerary = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_public = db.Column(db.Boolean, default=False)
    likes = db.Column(db.Integer, default=0)

    def __init__(self, user_id, title, destination, start_date, end_date, budget, preferences, itinerary=None, is_public=False):
        self.user_id = user_id
        self.title = title
        self.destination = destination
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.preferences = preferences
        self.itinerary = itinerary
        self.is_public = is_public

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('travel_plan.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, plan_id):
        self.user_id = user_id
        self.plan_id = plan_id

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    app.logger.error(f'Server Error: {error}')
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "Request entity too large"}), 413

# Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }), 200

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ('email', 'password', 'full_name')):
            return jsonify({"error": "Missing required fields"}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already registered"}), 400
        
        user = User(
            email=data['email'],
            password=data['password'],  # In production, hash the password
            full_name=data['full_name']
        )
        
        db.session.add(user)
        db.session.commit()
        
        app.logger.info(f'New user registered: {user.email}')
        
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "message": "User registered successfully",
            "token": access_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name
            }
        }), 201
    except Exception as e:
        app.logger.error(f'Error in signup: {str(e)}')
        db.session.rollback()
        return jsonify({"error": "Registration failed"}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ('email', 'password')):
            return jsonify({"error": "Missing email or password"}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or user.password != data['password']:  # In production, verify hashed password
            return jsonify({"error": "Invalid credentials"}), 401
        
        app.logger.info(f'User logged in: {user.email}')
        
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "message": "Login successful",
            "token": access_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name
            }
        }), 200
    except Exception as e:
        app.logger.error(f'Error in login: {str(e)}')
        return jsonify({"error": "Login failed"}), 500

@app.route('/api/plans', methods=['POST'])
@jwt_required()
def create_plan():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not all(k in data for k in ('title', 'destination', 'start_date', 'end_date', 'budget', 'preferences')):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Generate AI-powered travel plan
        ai_plan = generate_travel_plan(data['preferences'])
        
        plan = TravelPlan(
            user_id=current_user_id,
            title=data['title'],
            destination=data['destination'],
            start_date=datetime.fromisoformat(data['start_date']),
            end_date=datetime.fromisoformat(data['end_date']),
            budget=data['budget'],
            preferences=data['preferences'],
            itinerary=ai_plan,
            is_public=data.get('is_public', False)
        )
        
        db.session.add(plan)
        db.session.commit()
        
        app.logger.info(f'New travel plan created: {plan.title} by user {current_user_id}')
        
        return jsonify({
            "message": "Plan created successfully",
            "plan": {
                "id": plan.id,
                "title": plan.title,
                "destination": plan.destination,
                "start_date": plan.start_date.isoformat(),
                "end_date": plan.end_date.isoformat(),
                "budget": plan.budget,
                "preferences": plan.preferences,
                "itinerary": plan.itinerary,
                "created_at": plan.created_at.isoformat(),
                "is_public": plan.is_public
            }
        }), 201
    except Exception as e:
        app.logger.error(f'Error creating plan: {str(e)}')
        db.session.rollback()
        return jsonify({"error": "Failed to create plan"}), 500

@app.route('/api/plans', methods=['GET'])
@jwt_required()
def get_plans():
    try:
        current_user_id = get_jwt_identity()
        plans = TravelPlan.query.filter_by(user_id=current_user_id).all()
        
        return jsonify([{
            "id": plan.id,
            "title": plan.title,
            "destination": plan.destination,
            "start_date": plan.start_date.isoformat(),
            "end_date": plan.end_date.isoformat(),
            "budget": plan.budget,
            "preferences": plan.preferences,
            "itinerary": plan.itinerary,
            "created_at": plan.created_at.isoformat(),
            "updated_at": plan.updated_at.isoformat(),
            "is_public": plan.is_public,
            "likes": plan.likes
        } for plan in plans]), 200
    except Exception as e:
        app.logger.error(f'Error fetching plans: {str(e)}')
        return jsonify({"error": "Failed to fetch plans"}), 500

@app.route('/api/plans/<int:plan_id>', methods=['GET'])
@jwt_required()
def get_plan(plan_id):
    try:
        current_user_id = get_jwt_identity()
        plan = TravelPlan.query.get_or_404(plan_id)
        
        # Check if the plan belongs to the user or is public
        if plan.user_id != current_user_id and not plan.is_public:
            return jsonify({"error": "Access denied"}), 403
        
        return jsonify({
            "id": plan.id,
            "title": plan.title,
            "destination": plan.destination,
            "start_date": plan.start_date.isoformat(),
            "end_date": plan.end_date.isoformat(),
            "budget": plan.budget,
            "preferences": plan.preferences,
            "itinerary": plan.itinerary,
            "created_at": plan.created_at.isoformat(),
            "updated_at": plan.updated_at.isoformat(),
            "is_public": plan.is_public,
            "likes": plan.likes
        }), 200
    except Exception as e:
        app.logger.error(f'Error fetching plan {plan_id}: {str(e)}')
        return jsonify({"error": "Failed to fetch plan"}), 500

@app.route('/api/plans/<int:plan_id>', methods=['PUT'])
@jwt_required()
def update_plan(plan_id):
    try:
        current_user_id = get_jwt_identity()
        plan = TravelPlan.query.get_or_404(plan_id)
        
        # Check if the plan belongs to the user
        if plan.user_id != current_user_id:
            return jsonify({"error": "Access denied"}), 403
        
        data = request.get_json()
        
        if 'title' in data:
            plan.title = data['title']
        if 'destination' in data:
            plan.destination = data['destination']
        if 'start_date' in data:
            plan.start_date = datetime.fromisoformat(data['start_date'])
        if 'end_date' in data:
            plan.end_date = datetime.fromisoformat(data['end_date'])
        if 'budget' in data:
            plan.budget = data['budget']
        if 'preferences' in data:
            plan.preferences = data['preferences']
            # Regenerate itinerary if preferences change
            plan.itinerary = generate_travel_plan(data['preferences'])
        if 'is_public' in data:
            plan.is_public = data['is_public']
        
        db.session.commit()
        
        app.logger.info(f'Plan updated: {plan.title} by user {current_user_id}')
        
        return jsonify({
            "message": "Plan updated successfully",
            "plan": {
                "id": plan.id,
                "title": plan.title,
                "destination": plan.destination,
                "start_date": plan.start_date.isoformat(),
                "end_date": plan.end_date.isoformat(),
                "budget": plan.budget,
                "preferences": plan.preferences,
                "itinerary": plan.itinerary,
                "updated_at": plan.updated_at.isoformat(),
                "is_public": plan.is_public
            }
        }), 200
    except Exception as e:
        app.logger.error(f'Error updating plan {plan_id}: {str(e)}')
        db.session.rollback()
        return jsonify({"error": "Failed to update plan"}), 500

@app.route('/api/plans/<int:plan_id>', methods=['DELETE'])
@jwt_required()
def delete_plan(plan_id):
    try:
        current_user_id = get_jwt_identity()
        plan = TravelPlan.query.get_or_404(plan_id)
        
        # Check if the plan belongs to the user
        if plan.user_id != current_user_id:
            return jsonify({"error": "Access denied"}), 403
        
        db.session.delete(plan)
        db.session.commit()
        
        app.logger.info(f'Plan deleted: {plan.title} by user {current_user_id}')
        
        return jsonify({"message": "Plan deleted successfully"}), 200
    except Exception as e:
        app.logger.error(f'Error deleting plan {plan_id}: {str(e)}')
        db.session.rollback()
        return jsonify({"error": "Failed to delete plan"}), 500

@app.route('/api/plans/public', methods=['GET'])
def get_public_plans():
    try:
        plans = TravelPlan.query.filter_by(is_public=True).order_by(TravelPlan.likes.desc()).all()
        
        return jsonify([{
            "id": plan.id,
            "title": plan.title,
            "destination": plan.destination,
            "start_date": plan.start_date.isoformat(),
            "end_date": plan.end_date.isoformat(),
            "budget": plan.budget,
            "preferences": plan.preferences,
            "itinerary": plan.itinerary,
            "created_at": plan.created_at.isoformat(),
            "likes": plan.likes
        } for plan in plans]), 200
    except Exception as e:
        app.logger.error(f'Error fetching public plans: {str(e)}')
        return jsonify({"error": "Failed to fetch public plans"}), 500

@app.route('/api/plans/<int:plan_id>/like', methods=['POST'])
@jwt_required()
def like_plan(plan_id):
    try:
        plan = TravelPlan.query.get_or_404(plan_id)
        
        # Check if the plan is public
        if not plan.is_public:
            return jsonify({"error": "Can only like public plans"}), 403
        
        plan.likes += 1
        db.session.commit()
        
        app.logger.info(f'Plan liked: {plan.title}, new likes: {plan.likes}')
        
        return jsonify({
            "message": "Plan liked successfully",
            "likes": plan.likes
        }), 200
    except Exception as e:
        app.logger.error(f'Error liking plan {plan_id}: {str(e)}')
        db.session.rollback()
        return jsonify({"error": "Failed to like plan"}), 500

@app.route('/api/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    try:
        current_user_id = get_jwt_identity()
        favorites = Favorite.query.filter_by(user_id=current_user_id).all()
        
        plans = []
        for fav in favorites:
            plan = TravelPlan.query.get(fav.plan_id)
            if plan:
                plans.append({
                    "id": plan.id,
                    "title": plan.title,
                    "destination": plan.destination,
                    "start_date": plan.start_date.isoformat(),
                    "end_date": plan.end_date.isoformat(),
                    "budget": plan.budget,
                    "preferences": plan.preferences,
                    "itinerary": plan.itinerary,
                    "created_at": plan.created_at.isoformat(),
                    "is_public": plan.is_public,
                    "likes": plan.likes
                })
        
        return jsonify(plans), 200
    except Exception as e:
        app.logger.error(f'Error fetching favorites: {str(e)}')
        return jsonify({"error": "Failed to fetch favorites"}), 500

@app.route('/api/favorites/<int:plan_id>', methods=['POST'])
@jwt_required()
def add_favorite(plan_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Check if the plan exists and is public
        plan = TravelPlan.query.get_or_404(plan_id)
        if not plan.is_public:
            return jsonify({"error": "Can only favorite public plans"}), 403
        
        # Check if already favorited
        existing_favorite = Favorite.query.filter_by(user_id=current_user_id, plan_id=plan_id).first()
        if existing_favorite:
            return jsonify({"message": "Plan already in favorites"}), 200
        
        favorite = Favorite(user_id=current_user_id, plan_id=plan_id)
        db.session.add(favorite)
        db.session.commit()
        
        app.logger.info(f'Plan favorited: {plan.title} by user {current_user_id}')
        
        return jsonify({"message": "Plan added to favorites"}), 201
    except Exception as e:
        app.logger.error(f'Error adding favorite {plan_id}: {str(e)}')
        db.session.rollback()
        return jsonify({"error": "Failed to add favorite"}), 500

@app.route('/api/favorites/<int:plan_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite(plan_id):
    try:
        current_user_id = get_jwt_identity()
        
        favorite = Favorite.query.filter_by(user_id=current_user_id, plan_id=plan_id).first_or_404()
        db.session.delete(favorite)
        db.session.commit()
        
        app.logger.info(f'Favorite removed: plan {plan_id} by user {current_user_id}')
        
        return jsonify({"message": "Plan removed from favorites"}), 200
    except Exception as e:
        app.logger.error(f'Error removing favorite {plan_id}: {str(e)}')
        db.session.rollback()
        return jsonify({"error": "Failed to remove favorite"}), 500

@app.route('/api/destinations', methods=['GET'])
def get_destinations():
    try:
        budget = request.args.get('budget', 'medium')
        temperature = request.args.get('temperature', 'mild')
        purpose = request.args.get('purpose', 'leisure')
        duration = request.args.get('duration', '7 days')
        
        destination = generate_destination(budget, temperature, purpose, duration)
        
        return jsonify(destination), 200
    except Exception as e:
        app.logger.error(f'Error generating destinations: {str(e)}')
        return jsonify({"error": "Failed to generate destinations"}), 500

@app.route('/api/itineraries', methods=['GET'])
def get_itinerary():
    try:
        destination = request.args.get('destination', 'Paris')
        duration = request.args.get('duration', '7 days')
        budget = request.args.get('budget', 'medium')
        purpose = request.args.get('purpose', 'leisure')
        travelers = request.args.get('travelers', '2')
        preferences = request.args.get('preferences', '{}')
        
        try:
            preferences = json.loads(preferences)
        except json.JSONDecodeError:
            preferences = {}
        
        itinerary = generate_itinerary(destination, duration, budget, purpose, travelers, preferences)
        
        return jsonify(itinerary), 200
    except Exception as e:
        app.logger.error(f'Error generating itinerary: {str(e)}')
        return jsonify({"error": "Failed to generate itinerary"}), 500

# Serve static files in production
@app.route('/')
def serve_frontend():
    return send_from_directory('frontend/dist', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend/dist', path)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=os.getenv('DEBUG', 'True').lower() == 'true', port=5001) 