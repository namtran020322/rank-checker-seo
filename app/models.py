from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    searches = db.relationship('KeywordSearch', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class KeywordSearch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(200), nullable=False)
    target_url = db.Column(db.String(500), nullable=False)  # Thêm trường URL cần kiểm tra
    country = db.Column(db.String(2), nullable=False)
    device = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    results = db.relationship('SearchResult', backref='search', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    target_url_rank = db.Column(db.Integer)  # Thêm trường lưu thứ hạng của URL mục tiêu

class SearchResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search_id = db.Column(db.Integer, db.ForeignKey('keyword_search.id'), nullable=False)
    rank = db.Column(db.Integer)
    title = db.Column(db.String(500))
    link = db.Column(db.String(500))
    snippet = db.Column(db.Text)
    is_target = db.Column(db.Boolean, default=False)  # Đánh dấu nếu đây là URL mục tiêu