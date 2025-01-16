from budgetwise.models import Transaction
import io, base64
import matplotlib.pyplot as plt
import calendar
import matplotlib

matplotlib.use('Agg')


def generate_monthly_chart(user, year):
    months = list(calendar.month_name)[1:]
    income_data = [0] * 12
    expense_data = [0] * 12

    transactions = Transaction.objects.filter(user=user, date__year=year) # NOQA
    for transaction in transactions:
        month_index = transaction.date.month - 1
        amount = float(transaction.amount)
        if transaction.type == 'income':
            income_data[month_index] += amount
        elif transaction.type == 'expense':
            expense_data[month_index] += amount

    x = range(12)
    bar_width = 0.4
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(x, income_data, width=bar_width, label='Income', color='#87CEEB')
    ax.bar([i + bar_width for i in x], expense_data, width=bar_width, label='Expense', color='#4682B4')

    for i, (income, expense) in enumerate(zip(income_data, expense_data)):
        if income:
            ax.text(i, income, f"{income:.2f}", ha='center', va='bottom', fontsize=7)
        if expense:
            ax.text(i + bar_width, expense, f"{expense:.2f}", ha='center', va='bottom', fontsize=7)

    ax.set_xticks([i + bar_width / 2 for i in x])
    ax.set_xticklabels(months, fontsize=8)
    ax.set_title(f"Monthly Income and Expenses - {year}", fontsize=14, pad=20)
    ax.set_xlabel("Month", fontsize=10)
    ax.set_ylabel("Amount", fontsize=10)
    ax.legend(fontsize=10)

    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close(fig)

    net_data = [
        {"month": month, "income": income, "expense": expense, "net": income - expense}
        for month, income, expense in zip(months, income_data, expense_data)
    ]

    return chart_base64, net_data
