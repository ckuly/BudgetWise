from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from budgetwise.models import Transaction, Budget, SavingsGoal, Notification, Update
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
    return render(request, "base/updates.html", context)


def contacts(request):
    context = {}
    return render(request, "base/contacts.html", context)


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
    return render(request, 'base/register.html')


def login(request):
    context = {}
    return render(request, "registration/login.html", context)


@login_required
def profile(request):
    """View and update user profile."""
    if request.method == "POST":
        # Get the user's profile
        profile = request.user.profile

        # Check if the user wants to remove the profile picture
        if 'remove_picture' in request.POST:
            profile.profile_picture.delete(save=False)  # Deletes the file from storage
            profile.profile_picture = 'profile_pictures/default.jpg'  # Reset to default

        # Update profile fields
        profile.currency = request.POST.get("currency", profile.currency)
        profile.timezone = request.POST.get("timezone", profile.timezone)

        # Update profile picture if provided
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        # Save changes
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    context = {
        "user": request.user,
    }
    return render(request, "base/profile.html", context)


@login_required
def dashboard(request):
    user = request.user

    budgets = Budget.objects.filter(user=user)
    transactions = Transaction.objects.filter(user=user).order_by('-date')  # Ordered by date
    savings_goals = SavingsGoal.objects.filter(user=user)
    notifications = Notification.objects.filter(user=user, is_read=False)

    context = {
        "budgets": budgets,
        "transactions": transactions,
        "savings_goals": savings_goals,
        "profile": user.profile,
        "notifications": notifications,
    }

    return render(request, "base/dashboard.html", context)


def generate_monthly_chart(user, year):
    months = list(calendar.month_name)[1:]
    income_data = [0] * 12
    expense_data = [0] * 12
    net_data = []

    transactions = Transaction.objects.filter(user=user, date__year=year)

    for transaction in transactions:
        month_index = transaction.date.month - 1
        if transaction.type == 'income':
            income_data[month_index] += transaction.amount
        elif transaction.type == 'expense':
            expense_data[month_index] += transaction.amount

    for i in range(12):
        net_data.append({
            "month": months[i],
            "income": income_data[i],
            "expense": expense_data[i],
            "net": income_data[i] - expense_data[i],
        })

    fig, ax = plt.subplots(figsize=(11, 5))
    width = 0.4
    x = range(12)

    income_bars = ax.bar(x, income_data, width=width, label='Income', color='#4CAF50', alpha=0.8, edgecolor='black')
    expense_bars = ax.bar([i + width for i in x], expense_data, width=width, label='Expense', color='#F44336',
                          alpha=0.8, edgecolor='black')

    for bar in income_bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, f"{bar.get_height():.2f}", ha='center',
                va='bottom', fontsize=10)
    for bar in expense_bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, f"{bar.get_height():.2f}", ha='center',
                va='bottom', fontsize=10)

    ax.set_xticks([i + width / 2 for i in x])
    ax.set_xticklabels(months, rotation=45, ha='right', fontsize=12)
    ax.set_title(f"Monthly Income and Expenses - {year}", fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel("Month", fontsize=14, labelpad=10)
    ax.set_ylabel("Amount (in your currency)", fontsize=14, labelpad=10)
    ax.legend(fontsize=12, loc='upper right', frameon=True, edgecolor='black', title='Legend', title_fontsize=12)

    ax.grid(True, which='major', linestyle='--', linewidth=0.5, alpha=0.7)

    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close(fig)

    chart_base64 = base64.b64encode(image_png).decode('utf-8')

    return chart_base64, net_data


@login_required
def analytics(request):
    user = request.user

    selected_year = request.GET.get('year', now().year)
    try:
        selected_year = int(selected_year)
    except ValueError:
        selected_year = now().year

    monthly_chart, monthly_net_data = generate_monthly_chart(user, selected_year)

    years = Transaction.objects.filter(user=user).dates('date', 'year')

    context = {
        'monthly_chart': monthly_chart,
        'monthly_net_data': monthly_net_data,
        'selected_year': selected_year,
        'years': [year.year for year in years],
    }
    return render(request, "base/analytics.html", context)


@login_required
def membership(request):
    """Display membership plans."""
    return render(request, "base/membership.html")


def newsletter(request):
    context = {}
    return render(request, "base/newsletter.html", context)


def error_404(request, exception=None):
    """Render a custom 404 page."""
    return render(request, 'errors/404.html', status=404)


def error_500(request, exception=None):
    """Render a custom 500 page."""
    return render(request, 'errors/500.html', status=500)


@login_required
def change_plan(request, plan):
    """Change the user's membership plan."""
    valid_plans = ['free', 'premium', 'elite']
    if plan in valid_plans:
        profile = request.user.profile
        profile.plan = plan
        profile.save()
        messages.success(request, f"Your plan has been updated to {plan.capitalize()}!")
    else:
        messages.error(request, "Invalid plan selection.")
    return redirect('membership')
