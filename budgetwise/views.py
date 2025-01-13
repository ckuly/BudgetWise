from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from budgetwise.models import Transaction, Category, Budget, SavingsGoal, Profile, Notification, AuditLog, Update
import io
import base64
import matplotlib.pyplot as plt
import matplotlib
import calendar
from django.utils.timezone import now

matplotlib.use('Agg')


def index(request):
    transactions = Transaction.objects.all()
    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    context = {
        'transactions': transactions,
        "num_visits": num_visits,
    }

    return render(request, "index.html", context)


def updates(request):
    all_updates = Update.objects.order_by("-release_date")
    latest_update = all_updates.first()
    archived_updates = all_updates[1:]

    context = {
        "latest_update": latest_update,
        "archived_updates": archived_updates,
    }
    return render(request, "updates.html", context)


def contacts(request):
    context = {}
    return render(request, "contacts.html", context)


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')


def login(request):
    context = {}
    return render(request, "registration/login.html", context)


def profile(request):
    context = {}
    return render(request, "profile.html", context)


@login_required
def dashboard(request):
    user = request.user

    budgets = Budget.objects.filter(user=user)
    transactions = Transaction.objects.filter(user=user).order_by('-date')  # Ordered by date
    savings_goals = SavingsGoal.objects.filter(user=user)
    notifications = Notification.objects.filter(user=user, is_read=False)
    audit_logs = AuditLog.objects.filter(user=user)

    context = {
        "budgets": budgets,
        "transactions": transactions,
        "savings_goals": savings_goals,
        "profile": user.profile,
        "notifications": notifications,
        "audit_logs": audit_logs,
    }

    return render(request, "dashboard.html", context)


def generate_monthly_chart(user, year):
    # Initialize data structure
    months = list(calendar.month_name)[1:]  # ['January', ..., 'December']
    income_data = [0] * 12
    expense_data = [0] * 12
    net_data = []  # To store net balance for each month

    # Query transactions for the specified year
    transactions = Transaction.objects.filter(user=user, date__year=year)

    # Aggregate income and expense by month
    for transaction in transactions:
        month_index = transaction.date.month - 1  # 0-based index
        if transaction.type == 'income':
            income_data[month_index] += transaction.amount
        elif transaction.type == 'expense':
            expense_data[month_index] += transaction.amount

    # Calculate net balance for each month
    for i in range(12):
        net_data.append({
            "month": months[i],
            "income": income_data[i],
            "expense": expense_data[i],
            "net": income_data[i] - expense_data[i],
        })

    # Generate the bar chart
    fig, ax = plt.subplots(figsize=(11, 5))
    width = 0.4
    x = range(12)

    income_bars = ax.bar(x, income_data, width=width, label='Income', color='#4CAF50', alpha=0.8, edgecolor='black')
    expense_bars = ax.bar([i + width for i in x], expense_data, width=width, label='Expense', color='#F44336', alpha=0.8, edgecolor='black')

    # Add values above the bars
    for bar in income_bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, f"{bar.get_height():.2f}", ha='center', va='bottom', fontsize=10)
    for bar in expense_bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, f"{bar.get_height():.2f}", ha='center', va='bottom', fontsize=10)

    # Customize the chart
    ax.set_xticks([i + width / 2 for i in x])
    ax.set_xticklabels(months, rotation=45, ha='right', fontsize=12)
    ax.set_title(f"Monthly Income and Expenses - {year}", fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel("Month", fontsize=14, labelpad=10)
    ax.set_ylabel("Amount (in your currency)", fontsize=14, labelpad=10)
    ax.legend(fontsize=12, loc='upper right', frameon=True, edgecolor='black', title='Legend', title_fontsize=12)

    # Add gridlines for readability
    ax.grid(True, which='major', linestyle='--', linewidth=0.5, alpha=0.7)

    # Set tight layout for proper spacing
    plt.tight_layout()

    # Save the chart to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close(fig)

    # Convert the image to base64
    chart_base64 = base64.b64encode(image_png).decode('utf-8')

    return chart_base64, net_data


@login_required
def analytics(request):
    user = request.user

    # Get the selected year from the request, default to the current year
    selected_year = request.GET.get('year', now().year)
    try:
        selected_year = int(selected_year)
    except ValueError:
        selected_year = now().year

    # Generate the monthly chart and net balances for the selected year
    monthly_chart, monthly_net_data = generate_monthly_chart(user, selected_year)

    # Get available years from the user's transactions
    years = Transaction.objects.filter(user=user).dates('date', 'year')

    context = {
        'monthly_chart': monthly_chart,
        'monthly_net_data': monthly_net_data,
        'selected_year': selected_year,
        'years': [year.year for year in years],
    }
    return render(request, "analytics.html", context)


def newsletter(request):
    context = {}
    return render(request, "newsletter.html", context)


def error_404(request, exception=None):
    """Render a custom 404 page."""
    return render(request, '404.html', status=404)


def error_500(request, exception=None):
    """Render a custom 500 page."""
    return render(request, '500.html', status=500)
