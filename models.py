from . import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    twofactor = db.Column(db.String(11), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    is_admin = db.Column(db.Boolean)

    def get_id(self):
        return self.id

    def get_is_admin(self):
        return self.is_admin

    def set_is_admin(self, priv_mod):
        self.is_admin = priv_mod

    def __repr__(self):
        return f"Username('{self.username}')"

class LoginHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    login_time = db.Column(db.String(20), nullable=False)
    logout_time = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"LoginHistory('{self.user_id}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    results = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.user_id}')"








