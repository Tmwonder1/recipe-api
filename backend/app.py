import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import cloudinary
import cloudinary.uploader

load_dotenv()  # Load environment variables

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///recipes.db')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['CLOUDINARY_CLOUD_NAME'] = os.getenv('CLOUDINARY_CLOUD_NAME')
app.config['CLOUDINARY_API_KEY'] = os.getenv('CLOUDINARY_API_KEY')
app.config['CLOUDINARY_API_SECRET'] = os.getenv('CLOUDINARY_API_SECRET')

cloudinary.config(
    cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
    api_key=app.config['CLOUDINARY_API_KEY'],
    api_secret=app.config['CLOUDINARY_API_SECRET']
)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Database Models
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    profile_pic = db.Column(db.String(200))
    recipes = db.relationship('Recipe', backref='author', lazy=True)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(500), nullable=False)
    cuisine = db.Column(db.String(50), nullable=False)
    ratings = db.Column(db.String(100), default="")
    likes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# New Routes
@app.route('/profile/update', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    new_username = request.json.get('username', user.username)
    new_password = request.json.get('password', user.password)
    
    user.username = new_username
    user.password = new_password
    db.session.commit()
    
    return jsonify({"message": "Profile updated!"})

@app.route('/profile/upload', methods=['POST'])
@jwt_required()
def upload_profile_pic():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    file = request.files['file']
    upload_result = cloudinary.uploader.upload(file)
    user.profile_pic = upload_result['secure_url']
    db.session.commit()
    
    return jsonify({"profile_pic": user.profile_pic})

@app.route('/users/<int:user_id>/follow', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    user_to_follow = User.query.get(user_id)
    
    if not user_to_follow:
        return jsonify({"error": "User not found"}), 404
    
    current_user.followed.append(user_to_follow)
    db.session.commit()
    return jsonify({"message": f"Now following {user_to_follow.username}"})

@app.route('/recipes/<int:recipe_id>/like', methods=['POST'])
@jwt_required()
def like_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404
    
    recipe.likes += 1
    db.session.commit()
    return jsonify({"likes": recipe.likes})

# (Keep previous routes from earlier versions)
