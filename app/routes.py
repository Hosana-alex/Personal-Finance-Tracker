from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models import User, Income, Expense, SavingsGoal
from app.expert_system import FinancialAdvisor, FinancialProfile
from datetime import datetime, date
from flask import Blueprint

routes = Blueprint('routes', __name__)

# Home Route

from collections import defaultdict
from datetime import datetime

def calculate_overspent_days(expenses, daily_budget):
    """Count how many days the user spent more than their daily budget, ignoring one-time expenses."""
    daily_totals = defaultdict(float)

    for expense in expenses:
        if hasattr(expense, 'expense_type') and expense.expense_type == 'one-time':
            continue  # Ignore one-time expenses
        day = expense.date_added.date()
        daily_totals[day] += expense.amount

    overspent_days = sum(1 for total in daily_totals.values() if total > daily_budget)
    return overspent_days

def calculate_luxury_spending_ratio(expenses):
    """Calculate the percentage of expenses spent on luxuries, ignoring one-time expenses."""
    luxury_categories = ["Entertainment", "Shopping", "Other"]

    luxury_total = 0
    total_expenses = 0

    for exp in expenses:
        if hasattr(exp, 'expense_type') and exp.expense_type == 'one-time':
            continue
        total_expenses += exp.amount
        if exp.category in luxury_categories:
            luxury_total += exp.amount

    if total_expenses == 0:
        return 0

    return (luxury_total / total_expenses) * 100

def check_emergency_buffer(total_income, total_expenses):
    """Check if at least 10% of income remains as a financial buffer."""
    buffer = total_income - total_expenses
    return buffer >= (0.10 * total_income)

def calculate_goal_progress(goal, savings):
    """Calculate the percentage progress toward the user's savings goal."""
    if not goal:
        return 0.0

    progress = (savings / goal.goal_amount) * 100
    return float(min(progress, 100))  # Cap at 100% and ensure it's float

def detect_spending_trend(previous_month_savings, current_month_savings):
    """Detect whether financial behavior is improving, worsening, or stable."""
    if previous_month_savings is None:
        return 'stable'

    if current_month_savings > previous_month_savings:
        return 'improving'
    elif current_month_savings < previous_month_savings:
        return 'worsening'
    else:
        return 'stable'

def calculate_emergency_buffer_amount(income, expenses):
    """Calculate emergency buffer as a percentage of income."""
    buffer = income - expenses
    if income == 0:
        return 0.0
    return buffer / income  # returns a percentage (e.g., 0.15 for 15%)

def calculate_salary_burn_rate(total_expenses, day_of_month):
    """Estimate salary burn rate by mid-month."""
    if day_of_month < 1:
        return 0.0
    mid_month_day = 15
    days_so_far = min(day_of_month, mid_month_day)
    expected_expense_rate = total_expenses / days_so_far if days_so_far > 0 else 0
    return expected_expense_rate / (total_expenses / 30) * 100 if total_expenses else 0

def detect_luxury_expense_growth(previous_luxury_spending, current_luxury_spending):
    """Detect if luxury spending is increasing, stable, or decreasing."""
    if previous_luxury_spending is None:
        return 'stable'
    if current_luxury_spending > previous_luxury_spending:
        return 'increasing'
    elif current_luxury_spending < previous_luxury_spending:
        return 'decreasing'
    else:
        return 'stable'

def calculate_overspending_streak(expenses, daily_budget):
    """Calculate the longest overspending streak, ignoring one-time expenses."""
    streak = 0
    max_streak = 0
    daily_totals = defaultdict(float)

    for expense in expenses:
        if hasattr(expense, 'expense_type') and expense.expense_type == 'one-time':
            continue
        day = expense.date_added.date()
        daily_totals[day] += expense.amount

    for total in daily_totals.values():
        if total > daily_budget:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 0

    return max_streak

def dummy_goal_achievement_streak():
    """Placeholder for now. (Optionally implement real monthly tracking later.)"""
    return 0
def evaluate_goal_health(goal, savings):
    """Evaluate if the user is on track to meet their savings goal."""
    if not goal:
        return "No savings goal set."

    today = datetime.utcnow().date()
    total_days = (goal.due_date - goal.date_set.date()).days  # Use date_set correctly
    days_passed = (today - goal.date_set.date()).days         # Use date_set here too

    if total_days <= 0:
        return "Invalid goal dates."

    expected_savings_by_now = (goal.goal_amount / total_days) * days_passed

    if expected_savings_by_now <= 0:
        return "Goal period has not started yet."

    if savings >= goal.goal_amount:
        return "Goal already achieved! Congratulations!"

    if savings >= expected_savings_by_now:
        return "On track to meet your goal. Keep it up!"

    savings_gap = expected_savings_by_now - savings

    if savings_gap <= (0.1 * goal.goal_amount):
        return "Slightly behind your goal. Minor adjustment needed."
    elif savings_gap <= (0.3 * goal.goal_amount):
        return "Warning: You are behind on your savings goal. Consider saving more aggressively."
    else:
        return "Critical: You are far behind on your goal. Immediate action required to catch up!"


def calculate_recommended_budgets(goal, monthly_income):
    """Calculate recommended monthly and daily budget based on savings goal and income."""
    if not goal or not monthly_income:
        return None, None

    today = datetime.utcnow().date()
    total_days = (goal.due_date - goal.date_set.date()).days

    if total_days <= 0:
        return None, None

    daily_saving_target = goal.goal_amount / total_days
    monthly_saving_target = daily_saving_target * 30  # Approximate 30 days in a month

    # Prevent negative budgets
    recommended_monthly_budget = max(monthly_income - monthly_saving_target, 0)
    recommended_daily_budget = recommended_monthly_budget / 30

    return round(recommended_monthly_budget, 2), round(recommended_daily_budget, 2)





@routes.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))
    return redirect(url_for('routes.signup'))

@routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('routes.signup'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('routes.login'))

    return render_template('signup.html', page_title = "Sign Up")

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Login unsuccessful. Check username and password.', 'danger')

    return render_template('login.html', page_title = "Login")

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('routes.login'))


# Dashboard
@routes.route('/dashboard')
@login_required
def dashboard():
    # Calculate total income and expenses
    total_income = sum(income.amount for income in Income.query.filter_by(owner=current_user).all())
    total_expenses = sum(expense.amount for expense in Expense.query.filter_by(owner=current_user).all())

    # Fetch monthly income object
    monthly_income_obj = Income.query.filter_by(owner=current_user, income_type='monthly').first()
    monthly_income = monthly_income_obj.amount if monthly_income_obj else 0

    # Fetch user's savings goal
    goal = SavingsGoal.query.filter_by(owner=current_user).first()

    # Calculate recommended budgets
    recommended_monthly_budget, recommended_daily_budget = calculate_recommended_budgets(goal, monthly_income)

    # Calculate savings and savings_rate
    savings = total_income - total_expenses
    savings_rate = (savings / total_income) * 100 if total_income > 0 else 0

    # Evaluate goal health
    goal_progress = evaluate_goal_health(goal, savings)

    # Prepare recent transactions (latest 5 expenses)
    recent_transactions = Expense.query.filter_by(owner=current_user).order_by(Expense.date_added.desc()).limit(5).all()

    # Prepare pie chart data (expense breakdown)
    expense_summary = db.session.query(
        Expense.category,
        db.func.sum(Expense.amount)
    ).filter_by(owner=current_user).group_by(Expense.category).all()

    chart_labels = [item[0] for item in expense_summary]
    chart_data = [item[1] for item in expense_summary]

    # Render dashboard template
    return render_template('dashboard.html',
                           total_income=total_income,
                           total_expenses=total_expenses,
                           recommended_monthly_budget=recommended_monthly_budget,
                           recommended_daily_budget=recommended_daily_budget,
                           savings_rate=savings_rate,
                           goal_progress=goal_progress,
                           recent_transactions=recent_transactions,
                           chart_labels=chart_labels,
                           chart_data=chart_data,
                           goal = goal)



# Add Income
@routes.route('/add_income', methods=['GET', 'POST'])
@login_required
def add_income():
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        income_type = request.form.get('income_type')  # monthly or daily

        if amount and income_type:
            new_income = Income(amount=amount, income_type=income_type, owner=current_user)
            db.session.add(new_income)
            db.session.commit()
            flash('Income added successfully!', 'success')
            return redirect(url_for('routes.dashboard'))

        flash('Please fill all fields correctly.', 'danger')

    return render_template('add_income.html')

# Add Expense
@routes.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form.get('description', '')  # NEW: fetch description safely
        expense_type = request.form.get('expense_type', 'daily')  # Fetch expense type
        recurrence_interval = request.form.get('recurrence_interval', None)  # Fetch recurrence if present

        new_expense = Expense(
            amount=amount,
            category=category,
            description=description,
            owner=current_user,
            expense_type=expense_type,
            recurrence_interval=recurrence_interval
        )

        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('routes.dashboard'))

    return render_template('add_expense.html')



# Set Savings Goal (Optional)
@routes.route('/set_goal', methods=['GET', 'POST'])
@login_required
def set_goal():
    if request.method == 'POST':
        goal_amount = float(request.form.get('goal_amount'))
        due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%d').date()

        new_goal = SavingsGoal(goal_amount=goal_amount, due_date=due_date, owner=current_user)
        db.session.add(new_goal)
        db.session.commit()
        flash('Savings goal set successfully!', 'success')
        return redirect(url_for('routes.dashboard'))

    return render_template('set_goal.html')

# View Expense History
@routes.route('/history')
@login_required
def history():
    expenses = Expense.query.filter_by(owner=current_user).order_by(Expense.date_added.desc()).all()
    return render_template('history.html', expenses=expenses)
# Analysis (AI Expert System)
@routes.route('/analysis', methods=['GET', 'POST'])
@login_required
def analysis():
    # Get expense filter from the form if POST, else default to 'all'
    expense_filter = request.form.get('expense_filter', 'all')

    # Fetch all user's expenses
    all_expenses = Expense.query.filter_by(owner=current_user).all()

    # Apply filtering based on user selection
    if expense_filter == 'daily':
        expenses = [exp for exp in all_expenses if exp.expense_type == 'daily']
    elif expense_filter == 'monthly':
        expenses = [exp for exp in all_expenses if exp.expense_type == 'monthly']
    elif expense_filter == 'one-time':
        expenses = [exp for exp in all_expenses if exp.expense_type == 'one-time']
    else:
        expenses = all_expenses  # No filtering

    # If no expenses after filtering, avoid proceeding
    if not expenses:
        flash('No expenses found for the selected filter. Please add expenses first.', 'danger')
        return redirect(url_for('routes.dashboard'))

    # Calculate totals from filtered expenses
    total_income = sum(income.amount for income in Income.query.filter_by(owner=current_user).all())
    total_expenses = sum(expense.amount for expense in expenses)

    if total_income == 0:
        flash('Please add income first before running analysis.', 'danger')
        return redirect(url_for('routes.dashboard'))

    savings = total_income - total_expenses
    savings_rate = (savings / total_income) * 100 if total_income else 0
    expense_rate = (total_expenses / total_income) * 100 if total_income else 0

    # Fetch monthly income for daily budget
    monthly_income = Income.query.filter_by(owner=current_user, income_type='monthly').first()
    daily_budget = monthly_income.amount / 30 if monthly_income else 0

    # Fetch savings goal if set
    goal = SavingsGoal.query.filter_by(owner=current_user).first()
    goal_health_message = evaluate_goal_health(goal, savings)

    # Calculate dynamic fields
    overspent_days = calculate_overspent_days(expenses, daily_budget)
    luxury_spending_ratio = calculate_luxury_spending_ratio(expenses)
    emergency_buffer_present = check_emergency_buffer(total_income, total_expenses)
    emergency_buffer_amount = calculate_emergency_buffer_amount(total_income, total_expenses)
    salary_burn_rate = calculate_salary_burn_rate(total_expenses, datetime.now().day)
    previous_luxury_spending = None  # Placeholder
    luxury_expense_growth = detect_luxury_expense_growth(previous_luxury_spending, luxury_spending_ratio)
    overspending_streak = calculate_overspending_streak(expenses, daily_budget)
    goal_progress = calculate_goal_progress(goal, savings)
    goal_achievement_streak = dummy_goal_achievement_streak()
    day_of_month = datetime.now().day
    spending_trend = 'stable'  # Placeholder

    # ========== SAFETY HELPERS ==========
    def safe_value(val, fallback=0.01):
        try:
            v = float(val)
            if v == 0 or v is None:
                return fallback
            return v
        except:
            return fallback

    def safe_int_value(val, fallback=0):
        try:
            v = int(float(val))  # Convert to float first, then int
            return v
        except:
            return fallback

    # Fix values
    overspent_days = safe_int_value(overspent_days)
    overspending_streak = safe_int_value(overspending_streak)
    goal_achievement_streak = safe_int_value(goal_achievement_streak)

    # ========== DECLARE TO ADVISOR ==========
    advisor = FinancialAdvisor()
    advisor.reset()
    advisor.declare(FinancialProfile(
        income=total_income,
        expenses=total_expenses,
        savings_rate=safe_value(savings_rate),
        expense_rate=safe_value(expense_rate),
        overspent_days=overspent_days,
        luxury_spending_ratio=safe_value(luxury_spending_ratio),
        emergency_buffer_present=emergency_buffer_present,
        emergency_buffer_amount=safe_value(emergency_buffer_amount),
        goal_progress=safe_value(goal_progress),
        day_of_month=day_of_month,
        spending_trend=spending_trend,
        salary_burn_rate=safe_value(salary_burn_rate),
        luxury_expense_growth=luxury_expense_growth,
        overspending_streak=overspending_streak,
        goal_achievement_streak=goal_achievement_streak
    ))
    advisor.run()
    advisor.finalize()

    # ========== RESULTS ==========
    results = {
        "savings": savings,
        "savings_rate": savings_rate,
        "expense_rate": expense_rate,
        "score": advisor.score,
        "category": advisor.category,
        "persona": advisor.persona,
        "advice": advisor.advice,
        "projection": advisor.projection,
        "goal_health_message": goal_health_message
    }

    return render_template('analysis.html', results=results)

