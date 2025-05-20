from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Expense Type Choices
EXPENSE_TYPE_CHOICES = ('daily', 'monthly', 'one-time', 'recurring')
RECURRENCE_CHOICES = ('weekly', 'biweekly', 'monthly')

# Tell Flask-Login how to load a user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationships
    incomes = db.relationship('Income', backref='owner', lazy=True)
    expenses = db.relationship('Expense', backref='owner', lazy=True)
    savings_goals = db.relationship('SavingsGoal', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}')"

# Income Model
class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    income_type = db.Column(db.String(10), nullable=False, default='monthly')  # 'monthly' or 'daily'
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Income('{self.amount}', '{self.income_type}', '{self.date_added}')"

# Expense Model


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # ===== New fields added here =====
    expense_type = db.Column(db.String(20), nullable=False, default='daily')  # NEW FIELD
    recurrence_interval = db.Column(db.String(20), nullable=True)  # NEW FIELD (optional)


# (Optional) Savings Goal Model
class SavingsGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal_amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    date_set = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"SavingsGoal('{self.goal_amount}', '{self.due_date}')"
