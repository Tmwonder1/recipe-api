from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key-123'  # Change this in production
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    recipes = db.relationship('Recipe', backref='author', lazy=True)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(500), nullable=False)
    cuisine = db.Column(db.String(50), nullable=False)
    ratings = db.Column(db.String(100), default="")  # Comma-separated ratings
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username exists"}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created!"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200

@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    recipe_list = []
    for recipe in recipes:
        ratings = [int(r) for r in recipe.ratings.split(',') if r]
        recipe_list.append({
            "id": recipe.id,
            "name": recipe.name,
            "ingredients": recipe.ingredients.split(','),
            "cuisine": recipe.cuisine,
            "ratings": ratings,
            "average_rating": sum(ratings)/len(ratings) if ratings else 0
        })
    return jsonify({"recipes": recipe_list})

@app.route('/recipes', methods=['POST'])
@jwt_required()
def add_recipe():
    current_user_id = get_jwt_identity()
    data = request.json
    new_recipe = Recipe(
        name=data['name'],
        ingredients=','.join(data['ingredients']),
        cuisine=data['cuisine'],
        user_id=current_user_id
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({"message": "Recipe added!"}), 201

@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
@jwt_required()
def update_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404
    
    data = request.json
    recipe.name = data.get('name', recipe.name)
    recipe.ingredients = ','.join(data.get('ingredients', recipe.ingredients.split(',')))
    recipe.cuisine = data.get('cuisine', recipe.cuisine)
    db.session.commit()
    return jsonify({"message": "Recipe updated!"})

@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
@jwt_required()
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404
    
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"message": "Recipe deleted!"})

@app.route('/recipes/<int:recipe_id>/rate', methods=['POST'])
@jwt_required()
def rate_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404
    
    rating = request.json.get('rating')
    if not (1 <= rating <= 5):
        return jsonify({"error": "Rating must be 1-5"}), 400
    
    ratings = recipe.ratings.split(',')
    ratings.append(str(rating))
    recipe.ratings = ','.join(ratings)
    db.session.commit()
    return jsonify({"message": "Rating added!"})

@app.route('/recipes/search', methods=['GET'])
def search_recipes():
    query = request.args.get('q', '').lower()
    recipes = Recipe.query.filter(
        (Recipe.cuisine.ilike(f'%{query}%')) |
        (Recipe.ingredients.ilike(f'%{query}%'))
    ).all()
    recipe_list = []
    for recipe in recipes:
        ratings = [int(r) for r in recipe.ratings.split(',') if r]
        recipe_list.append({
            "id": recipe.id,
            "name": recipe.name,
            "ingredients": recipe.ingredients.split(','),
            "cuisine": recipe.cuisine,
            "ratings": ratings,
            "average_rating": sum(ratings)/len(ratings) if ratings else 0
        })
    return jsonify({"recipes": recipe_list})

if __name__ == '__main__':
    app.run(debug=True)
