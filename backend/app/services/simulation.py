from app.schemas.simulate import SimulateRequest, SimulateResponse, MonthRow


def run_simulation(req: SimulateRequest) -> SimulateResponse:
    amount   = req.loan_amount_uzs
    r        = (req.annual_rate_pct / 100) / 12
    n        = req.term_months
    income   = req.monthly_income_uzs
    expenses = req.monthly_expenses_uzs
    debt     = req.existing_debt_monthly_uzs

    # Annuity monthly payment
    if r > 0:
        payment = amount * r / (1 - (1 + r) ** (-n))
    else:
        payment = amount / n

    dti = (debt + payment) / max(income, 1)

    schedule = []
    balance = amount
    cumulative_interest = 0.0

    for month in range(1, n + 1):
        interest_part  = balance * r
        principal_part = payment - interest_part
        balance        = max(balance - principal_part, 0)
        cumulative_interest += interest_part
        disposable = income - expenses - debt - payment

        schedule.append(MonthRow(
            month=month,
            payment=round(payment, 2),
            principal=round(principal_part, 2),
            interest=round(interest_part, 2),
            balance=round(balance, 2),
            disposable_income=round(disposable, 2),
            cumulative_interest=round(cumulative_interest, 2),
        ))

    return SimulateResponse(
        monthly_payment=round(payment, 2),
        total_payment=round(payment * n, 2),
        total_interest=round(payment * n - amount, 2),
        dti_ratio=round(dti, 4),
        dti_warning=dti > 0.40,
        schedule=schedule,
    )
