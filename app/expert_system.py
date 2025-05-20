from experta import KnowledgeEngine, Fact, Rule, Field, P

# ======= NEW EXPANDED FinancialProfile =======

class FinancialProfile(Fact):
    income = Field(float, mandatory=True)
    expenses = Field(float, mandatory=True)
    savings_rate = Field(float, mandatory=True)
    expense_rate = Field(float, mandatory=True)
    overspent_days = Field(int, mandatory=True)
    luxury_spending_ratio = Field(float, mandatory=True)
    emergency_buffer_present = Field(bool, mandatory=True)
    emergency_buffer_amount = Field(float, mandatory=True)  # NEW
    goal_progress = Field(float, mandatory=True)
    day_of_month = Field(int, mandatory=True)
    spending_trend = Field(str, mandatory=True)  # 'improving', 'worsening_slow', 'worsening_fast', 'stable'
    salary_burn_rate = Field(float, mandatory=True)  # NEW: % of salary spent halfway through the month
    luxury_expense_growth = Field(str, mandatory=True)  # NEW: 'increasing', 'stable', 'decreasing'
    overspending_streak = Field(int, mandatory=True)  # NEW: longest streak of overspending days
    goal_achievement_streak = Field(int, mandatory=True)  # NEW: consecutive months meeting goal (optional)

# Create the main FinancialAdvisor engine
class FinancialAdvisor(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.advice = []
        self.score = 100
        self.category = ""
        self.persona = ""
        self.projection = ""

    # ===== Savings Rate Analysis Rules =====

    @Rule(FinancialProfile(savings_rate=P(lambda x: x < 2)))
    def savings_extremely_critical(self):
        self.advice.append("CRITICAL: Saving less than 2% of your income is financially dangerous!")
        self.score -= 40

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 2 and x < 5)))
    def savings_critical(self):
        self.advice.append("Very bad: Saving only 2%-5%. Major financial instability risk.")
        self.score -= 30

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 5 and x < 8)))
    def savings_very_low(self):
        self.advice.append("Very low savings (5%-8%). Immediate correction needed.")
        self.score -= 25

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 8 and x < 10)))
    def savings_low_borderline(self):
        self.advice.append("Borderline low savings (8%-10%). Still dangerous.")
        self.score -= 20

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 10 and x < 12)))
    def savings_better_but_risky(self):
        self.advice.append("Savings slightly better (10%-12%) but still risky. Improve more.")
        self.score -= 15

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 12 and x < 15)))
    def savings_moderate_risk(self):
        self.advice.append("Moderate risk: Saving between 12%-15%. You need stronger habits.")
        self.score -= 10

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 15 and x < 18)))
    def savings_decent(self):
        self.advice.append("Decent savings (15%-18%). Could still be improved slightly.")
        self.score -= 5

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 18 and x < 20)))
    def savings_okay(self):
        self.advice.append("Okay savings (18%-20%). Acceptable but strengthen for safety.")

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 20 and x < 25)))
    def savings_good(self):
        self.advice.append("Good savings discipline (20%-25%). Keep maintaining this momentum.")

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 25 and x < 30)))
    def savings_very_good(self):
        self.advice.append("Very good savings habit (25%-30%). Strong financial control!")

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 30 and x < 40)))
    def savings_excellent(self):
        self.advice.append("Excellent savings (30%-40%). Your financial future looks very secure!")

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 40 and x < 50)))
    def savings_outstanding(self):
        self.advice.append("Outstanding: Saving 40%-50% of your income! True financial independence ahead!")

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 50)))
    def savings_legendary(self):
        self.advice.append("LEGENDARY: Saving more than half your income! Future millionaire behavior.")

    # ===== Expense Rate Analysis Rules =====

    @Rule(FinancialProfile(savings_rate=P(lambda x: x < 2)))
    def savings_extremely_critical(self):
        self.advice.append("CRITICAL: Saving less than 2% of your income is financially dangerous!")
        self.score -= 40

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 2 and x < 5)))
    def savings_critical(self):
        self.advice.append("Very bad: Saving only 2%-5%. Major financial instability risk.")
        self.score -= 30

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 5 and x < 8)))
    def savings_very_low(self):
        self.advice.append("Very low savings (5%-8%). Immediate correction needed.")
        self.score -= 25

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 8 and x < 10)))
    def savings_low_borderline(self):
        self.advice.append("Borderline low savings (8%-10%). Still dangerous.")
        self.score -= 20

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 10 and x < 12)))
    def savings_better_but_risky(self):
        self.advice.append("Savings slightly better (10%-12%) but still risky. Improve more.")
        self.score -= 15

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 12 and x < 15)))
    def savings_moderate_risk(self):
        self.advice.append("Moderate risk: Saving between 12%-15%. You need stronger habits.")
        self.score -= 10

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 15 and x < 18)))
    def savings_decent(self):
        self.advice.append("Decent savings (15%-18%). Could still be improved slightly.")
        self.score -= 5

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 18 and x < 20)))
    def savings_okay(self):
        self.advice.append("Okay savings (18%-20%). Acceptable but strengthen for safety.")

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 20 and x < 25)))
    def savings_good(self):
        self.advice.append("Good savings discipline (20%-25%). Keep maintaining this momentum.")

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 25 and x < 30)))
    def savings_very_good(self):
        self.advice.append("Very good savings habit (25%-30%). Strong financial control!")

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 30 and x < 40)))
    def savings_excellent(self):
        self.advice.append("Excellent savings (30%-40%). Your financial future looks very secure!")

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 40 and x < 50)))
    def savings_outstanding(self):
        self.advice.append("Outstanding: Saving 40%-50% of your income! True financial independence ahead!")

    @Rule(FinancialProfile(savings_rate=P(lambda x: x >= 50)))
    def savings_legendary(self):
        self.advice.append("LEGENDARY: Saving more than half your income! Future millionaire behavior.")

    # ===== Budget Discipline Rules =====

    @Rule(FinancialProfile(overspent_days=P(lambda x: x >= 1 and x < 5)))
    def slight_overspending(self):
        self.advice.append("Slight overspending pattern detected. Monitor spending closely.")
        self.score -= 10

    @Rule(FinancialProfile(overspent_days=P(lambda x: x >= 5 and x < 10)))
    def moderate_overspending(self):
        self.advice.append("Moderate overspending across several days. Financial discipline slipping.")
        self.score -= 20

    @Rule(FinancialProfile(overspent_days=P(lambda x: x >= 10 and x < 15)))
    def severe_overspending(self):
        self.advice.append("Severe overspending streak detected. Major risk building.")
        self.score -= 35

    @Rule(FinancialProfile(overspent_days=P(lambda x: x >= 15 and x < 20)))
    def extreme_overspending(self):
        self.advice.append("Extreme overspending trend over many days. Crisis-level behavior.")
        self.score -= 50

    @Rule(FinancialProfile(overspent_days=P(lambda x: x >= 20)))
    def catastrophic_overspending(self):
        self.advice.append("Catastrophic loss of budget control. Financial collapse imminent.")
        self.score -= 70

    # ===== Daily Overspending Streak Detection =====

    @Rule(FinancialProfile(overspending_streak=P(lambda x: x >= 3 and x < 5)))
    def short_overspending_streak(self):
        self.advice.append("Short overspending streak (3-5 days). Break the bad habit early.")
        self.score -= 15

    @Rule(FinancialProfile(overspending_streak=P(lambda x: x >= 5 and x < 8)))
    def medium_overspending_streak(self):
        self.advice.append("Medium overspending streak (5-8 days). Warning signs flashing.")
        self.score -= 25

    @Rule(FinancialProfile(overspending_streak=P(lambda x: x >= 8)))
    def long_overspending_streak(self):
        self.advice.append("Long overspending streak (8+ days). Financial collapse accelerating.")
        self.score -= 45


    # ===== Emergency Buffer Rules =====

    # Emergency Buffer Amount Analysis
    @Rule(FinancialProfile(emergency_buffer_amount=P(lambda x: x < 0)))
    def negative_buffer(self):
        self.advice.append("Negative cash flow detected. Expenses exceed income!")
        self.score -= 50

    @Rule(FinancialProfile(emergency_buffer_amount=P(lambda x: x >= 0 and x < 0.05)))
    def critical_low_buffer(self):
        self.advice.append("Critical: Emergency buffer less than 5% of income. Very vulnerable to shocks.")
        self.score -= 30

    @Rule(FinancialProfile(emergency_buffer_amount=P(lambda x: x >= 0.05 and x < 0.10)))
    def very_low_buffer(self):
        self.advice.append("Very low emergency buffer (5%-10% of income). Danger zone.")
        self.score -= 20

    @Rule(FinancialProfile(emergency_buffer_amount=P(lambda x: x >= 0.10 and x < 0.20)))
    def low_buffer(self):
        self.advice.append("Low emergency buffer (10%-20%). Should be improved.")
        self.score -= 10

    @Rule(FinancialProfile(emergency_buffer_amount=P(lambda x: x >= 0.20)))
    def healthy_buffer(self):
        self.advice.append("Healthy emergency buffer (>20%). Good safety net maintained.")

    # Salary Burn Rate Analysis (by mid-month)
    @Rule(FinancialProfile(salary_burn_rate=P(lambda x: x > 80)))
    def catastrophic_salary_burn(self):
        self.advice.append("Catastrophic: Over 80% of salary burned by mid-month. Financial collapse imminent.")
        self.score -= 50

    @Rule(FinancialProfile(salary_burn_rate=P(lambda x: x > 60 and x <= 80)))
    def severe_salary_burn(self):
        self.advice.append("Severe salary burn (60%-80% spent by mid-month). High depletion risk.")
        self.score -= 30

    @Rule(FinancialProfile(salary_burn_rate=P(lambda x: x > 40 and x <= 60)))
    def moderate_salary_burn(self):
        self.advice.append("Moderate salary burn (40%-60% spent by mid-month). Caution needed.")

    @Rule(FinancialProfile(salary_burn_rate=P(lambda x: x <= 40)))
    def controlled_salary_burn(self):
        self.advice.append("Controlled salary burn (<40% spent by mid-month). Good management.")

    # ===== Luxury Spending Analysis Rules =====

    # Static Luxury Spending Levels
    @Rule(FinancialProfile(luxury_spending_ratio=P(lambda x: x > 60)))
    def luxury_extreme_addiction(self):
        self.advice.append("EXTREME luxury addiction detected (>60% of expenses on luxuries). Critical risk of financial instability.")
        self.score -= 40

    @Rule(FinancialProfile(luxury_spending_ratio=P(lambda x: x > 50 and x <= 60)))
    def luxury_heavy_addiction(self):
        self.advice.append("Heavy luxury spending habit (50%-60% of expenses). Major risk of lifestyle inflation.")
        self.score -= 30

    @Rule(FinancialProfile(luxury_spending_ratio=P(lambda x: x > 40 and x <= 50)))
    def luxury_high(self):
        self.advice.append("High luxury expenses (40%-50%). Caution: lifestyle may be inflating beyond control.")
        self.score -= 20

    @Rule(FinancialProfile(luxury_spending_ratio=P(lambda x: x > 30 and x <= 40)))
    def luxury_moderate_high(self):
        self.advice.append("Moderate-High luxury spending (30%-40%). Monitor non-essential purchases closely.")
        self.score -= 10

    @Rule(FinancialProfile(luxury_spending_ratio=P(lambda x: x > 20 and x <= 30)))
    def luxury_acceptable_range(self):
        self.advice.append("Luxury spending (20%-30%) within tolerable range. Stay disciplined.")

    # Luxury Spending Trend Detection
    @Rule(FinancialProfile(luxury_expense_growth='increasing'))
    def luxury_addiction_increasing(self):
        self.advice.append("ALERT: Luxury spending pattern is increasing over time. Risk of financial habits worsening.")
        self.score -= 20

    @Rule(FinancialProfile(luxury_expense_growth='stable'))
    def luxury_stable(self):
        self.advice.append("Luxury spending pattern is stable. Good discipline maintained.")

    @Rule(FinancialProfile(luxury_expense_growth='decreasing'))
    def luxury_improving(self):
        self.advice.append("Luxury spending is decreasing over time. Excellent financial behavior improvement.")

    # ===== Goal Achievement Rules =====

    @Rule(FinancialProfile(goal_progress=P(lambda x: x < 10)))
    def goal_no_progress(self):
        self.advice.append("Critical: Less than 10% of your savings goal achieved. Immediate action required.")
        self.score -= 30

    @Rule(FinancialProfile(goal_progress=P(lambda x: x >= 10 and x < 30)))
    def goal_low_progress(self):
        self.advice.append("Low progress towards savings goal (10%-30%). Increase your savings efforts.")
        self.score -= 20

    @Rule(FinancialProfile(goal_progress=P(lambda x: x >= 30 and x < 50)))
    def goal_moderate_progress(self):
        self.advice.append("Moderate savings goal progress (30%-50%). Keep pushing forward.")
        self.score -= 10

    @Rule(FinancialProfile(goal_progress=P(lambda x: x >= 50 and x < 70)))
    def goal_good_progress(self):
        self.advice.append("Good progress toward savings goal (50%-70%). Stay focused!")

    @Rule(FinancialProfile(goal_progress=P(lambda x: x >= 70 and x < 90)))
    def goal_very_good_progress(self):
        self.advice.append("Very good savings goal achievement (70%-90%). Almost there!")

    @Rule(FinancialProfile(goal_progress=P(lambda x: x >= 90 and x <= 100)))
    def goal_almost_achieved(self):
        self.advice.append("Excellent: Near or complete achievement of savings goal. Outstanding!")

    @Rule(FinancialProfile(goal_progress=P(lambda x: x > 100)))
    def goal_exceeded(self):
        self.advice.append("WOW: You have exceeded your savings goal! True financial discipline.")


    # ===== Mid-Month Financial Health Rules =====

    @Rule(FinancialProfile(day_of_month=P(lambda d: d >= 15), expense_rate=P(lambda x: x > 80)))
    def mid_month_expenses_critical(self):
        self.advice.append("CRITICAL: By mid-month, over 80% of income spent. Immediate financial intervention required!")
        self.score -= 40

    @Rule(FinancialProfile(day_of_month=P(lambda d: d >= 15), expense_rate=P(lambda x: x > 60 and x <= 80)))
    def mid_month_expenses_high(self):
        self.advice.append("Warning: By mid-month, 60%-80% of income already spent. Risk of salary depletion before month-end.")
        self.score -= 25

    @Rule(FinancialProfile(day_of_month=P(lambda d: d >= 15), expense_rate=P(lambda x: x > 40 and x <= 60)))
    def mid_month_expenses_caution(self):
        self.advice.append("Caution: Mid-month expenses are 40%-60% of income. Monitor spending to stay on track.")

    @Rule(FinancialProfile(day_of_month=P(lambda d: d >= 15), expense_rate=P(lambda x: x <= 40)))
    def mid_month_expenses_healthy(self):
        self.advice.append("Good management: Less than 40% of income spent by mid-month. Financial discipline strong!")


    # ===== Spending Trend Rules =====

    @Rule(FinancialProfile(spending_trend='worsening_fast'))
    def spending_trend_worsening_fast(self):
        self.advice.append("CRITICAL: Spending habits are worsening rapidly. Financial collapse imminent if not corrected.")
        self.score -= 40

    @Rule(FinancialProfile(spending_trend='worsening_slow'))
    def spending_trend_worsening_slow(self):
        self.advice.append("Warning: Spending habits are slowly deteriorating. Early intervention needed.")
        self.score -= 20

    @Rule(FinancialProfile(spending_trend='stable'))
    def spending_trend_stable(self):
        self.advice.append("Spending habits are stable. Continue monitoring and maintaining discipline.")

    @Rule(FinancialProfile(spending_trend='improving'))
    def spending_trend_improving(self):
        self.advice.append("Excellent: Spending habits are improving over time. Keep reinforcing good behaviors!")


    # ===== Finalization: Financial Persona, Projection, Category =====

    def finalize(self):
        """Assign financial persona, category, and future projection after rules fire."""
        
        self.projection = "No projection available yet. "

        # Score to Category
        if self.score >= 90:
            self.category = "Elite"
        elif self.score >= 80:
            self.category = "Excellent"
        elif self.score >= 70:
            self.category = "Very Good"
        elif self.score >= 60:
            self.category = "Good"
        elif self.score >= 50:
            self.category = "Average"
        elif self.score >= 40:
            self.category = "At Risk"
        else:
            self.category = "Critical"

        # Persona Detection based on score
        if self.score >= 90:
            self.persona = "Strict Saver (Ultra Disciplined)"
        elif self.score >= 80:
            self.persona = "Strategic Investor (Goal-Oriented)"
        elif self.score >= 70:
            self.persona = "Balanced Planner (Well-Managed)"
        elif self.score >= 60:
            self.persona = "Conscious Spender (Stable but Watchful)"
        elif self.score >= 50:
            self.persona = "Casual Planner (Occasionally Careless)"
        elif self.score >= 40:
            self.persona = "Overspender (At Financial Risk)"
        elif self.score >= 30:
            self.persona = "Lifestyle Inflator (Dangerously Addicted to Luxury)"
        elif self.score >= 20:
            self.persona = "Paycheck-to-Paycheck Survivor (Financially Fragile)"
        elif self.score >= 10:
            self.persona = "Risk Taker (Negligent Financial Habits)"
        else:
            self.persona = "Financial Free-Faller (Critical Emergency)"

        # Future Projection Based on expense_rate
        if hasattr(self, 'expense_rate'):
            if self.expense_rate > 85:
                self.projection = "Extreme risk: Salary depletion imminent. Emergency measures needed."
            elif self.expense_rate > 70:
                self.projection = "High risk: Tight survival toward month-end. Significant discipline needed."
            elif self.expense_rate > 50:
                self.projection = "Moderate risk: Manageable if discipline improves."
            else:
                self.projection = "Healthy trajectory: Likely surplus at month-end."

