from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import shortuuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'   # SQLite file: urls.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Get base URL from environment variables
BASE_URL = os.getenv('BASE_URL', 'http://localhost:5001')  # default localhost agar env nahi mila

# Database Model
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_id = db.Column(db.String(6), unique=True, nullable=False)
    long_url = db.Column(db.Text, nullable=False)
    clicks = db.Column(db.Integer, default=0)

# Create all tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.json
    long_url = data.get('long_url')
    if not long_url:
        return jsonify({"error": "URL is required"}), 400

    short_id = shortuuid.ShortUUID().random(length=6)

    new_url = URL(short_id=short_id, long_url=long_url)
    db.session.add(new_url)
    db.session.commit()

    return jsonify(short_url=f"{BASE_URL}/{short_id}")

@app.route('/<short_id>')
def redirect_url(short_id):
    url = URL.query.filter_by(short_id=short_id).first()
    if url:
        url.clicks += 1
        db.session.commit()
        return redirect(url.long_url)
    return "URL not found", 404

if __name__ == "__main__":
    app.run(debug=True, port=5001)
