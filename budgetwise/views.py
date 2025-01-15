from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from budgetwise.models import Transaction, Budget, SavingsGoal, Notification, Update, Profile, Category, ContactMessage
import io
import base64
import matplotlib.pyplot as plt
import matplotlib
import calendar
from django.utils.timezone import now

matplotlib.use('Agg')


def index(request):
    transactions = Transaction.objects.all()  # NOQA
    total_members = User.objects.count()
    paid_members = Profile.objects.filter(plan__in=["premium", "elite"]).count()  # NOQA

    context = {
        "total_members": total_members,
        "paid_members": paid_members,
        "transactions": transactions,
    }

    return render(request, "index.html", context)


def updates(request):
    all_updates = Update.objects.order_by("-release_date")  # NOQA
    latest_update = all_updates.first()
    archived_updates = all_updates[1:]

    context = {
        "latest_update": latest_update,
        "archived_updates": archived_updates,
    }
    return render(request, "base/updates.html", context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        ContactMessage.objects.create(name=name, email=email, message=message)  # NOQA
        messages.success(request, "Your message has been received. We will get back to you soon!")

    return render(request, "base/contacts.html")


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'The username "{username}" is already taken!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'A user with the email "{email}" is already registered!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'User "{username}" has been successfully registered!')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
    return render(request, 'base/register.html')


def login(request):
    context = {}
    return render(request, "registration/login.html", context)


@login_required
def profile(request):
    """View and update user profile."""
    if request.method == "POST":
        profile = request.user.profile  # NOQA

        if 'remove_picture' in request.POST:
            if profile.profile_picture.name != 'profile_pictures/default.png':  # NOQA
                profile.profile_picture.delete(save=False)  # NOQA
            profile.profile_picture = 'profile_pictures/default.png'

        profile.currency = request.POST.get("currency", profile.currency)

        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

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

    budgets = Budget.objects.filter(user=user) # NOQA
    transactions = Transaction.objects.filter(user=user).order_by('-date') # NOQA
    savings_goals = SavingsGoal.objects.filter(user=user) # NOQA
    notifications = Notification.objects.filter(user=user, is_read=False) # NOQA

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

    transactions = Transaction.objects.filter(user=user, date__year=year)  # NOQA

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

    income_bars = ax.bar(x, income_data, width=width, label='Income', color='#4CAF50', alpha=1.0, edgecolor='#4CAF50')
    expense_bars = ax.bar([i + width for i in x], expense_data, width=width, label='Expense', color='#F44336',
                          alpha=1.0, edgecolor='#F44336')

    for bar in income_bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, f"{bar.get_height():.2f}", ha='center',
                va='bottom', fontsize=7)
    for bar in expense_bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, f"{bar.get_height():.2f}", ha='center',
                va='bottom', fontsize=7)

    ax.set_xticks([i + width / 2 for i in x])
    ax.set_xticklabels(months, ha='center', fontsize=8)
    ax.set_title(f"Monthly Income and Expenses - {year}", fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel("Month", fontsize=10, labelpad=10)
    ax.set_ylabel("Amount", fontsize=10, labelpad=10)
    ax.legend(fontsize=10, loc='upper right', frameon=True, edgecolor='black')

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

    years = Transaction.objects.filter(user=user).dates('date', 'year')  # NOQA

    transactions = Transaction.objects.filter(user=user, date__year=selected_year).order_by('date')  # NOQA
    transactions_by_month = []
    for month in range(1, 13):
        month_transactions = transactions.filter(date__month=month)
        month_name = calendar.month_name[month]
        transactions_by_month.append({
            "month": month_name,
            "transactions": month_transactions,
        })

    context = {
        'monthly_chart': monthly_chart,
        'monthly_net_data': monthly_net_data,
        'selected_year': selected_year,
        'years': [year.year for year in years],
        'transactions_by_month': transactions_by_month,
    }
    return render(request, "base/analytics.html", context)


@login_required
def membership(request):
    """Display membership plans."""
    return render(request, "base/membership.html")


def error_404(request, exception=None):  # NOQA
    """Render a custom 404 page."""
    return render(request, 'errors/404.html', status=404)


def error_500(request, exception=None):  # NOQA
    """Render a custom 500 page."""
    return render(request, 'errors/500.html', status=500)


@login_required
def change_plan(request, plan):
    """Change the user's membership plan."""
    valid_plans = ['free', 'premium', 'elite']
    if plan in valid_plans:
        profile = request.user.profile  # NOQA
        profile.plan = plan
        profile.save()
        messages.success(request, f"Your plan has been updated to {plan.capitalize()}!")
    else:
        messages.error(request, "Invalid plan selection.")
    return redirect('membership')


@login_required
def all_transactions(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')  # NOQA
    return render(request, 'crud/all_transactions.html', {'transactions': transactions})


@login_required
def add_transaction(request):
    if request.method == "POST":
        category_id = request.POST.get("category")
        type = request.POST.get("type")  # NOQA
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        description = request.POST.get("description", "")

        if not category_id or not type or not amount or not date:
            messages.error(request, "All fields except description are required.")
            return redirect("add_transaction")

        try:
            category = Category.objects.get(id=category_id)  # NOQA
            amount = float(amount)
        except (Category.DoesNotExist, ValueError):  # NOQA
            messages.error(request, "Invalid category or amount.")
            return redirect("add_transaction")

        Transaction.objects.create(  # NOQA
            user=request.user,
            category=category,
            type=type,
            amount=amount,
            date=date,
            description=description,
        )
        messages.success(request, "Transaction added successfully!")
        return redirect("dashboard")

    categories = Category.objects.all()  # NOQA
    return render(request, "crud/create_transaction.html", {"categories": categories})


@login_required
def add_saving_goal(request):
    if request.method == "POST":
        name = request.POST.get("name")
        target_amount = request.POST.get("target_amount")
        transaction_ids = request.POST.getlist("transactions")
        due_date = request.POST.get("due_date")

        if not name or not target_amount:
            messages.error(request, "Name and target amount are required.")
            return redirect("add_saving_goal")

        try:
            target_amount = float(target_amount)
        except ValueError:
            messages.error(request, "Invalid target amount.")
            return redirect("add_saving_goal")

        savings_goal = SavingsGoal.objects.create(  # NOQA
            user=request.user,
            name=name,
            target_amount=target_amount,
            due_date=due_date,
        )

        if transaction_ids:
            try:
                transactions = Transaction.objects.filter(id__in=transaction_ids, user=request.user)  # NOQA
                savings_goal.transactions.add(*transactions)
            except Exception:  # NOQA
                messages.error(request, "An error occurred while assigning transactions.")
                return redirect("add_saving_goal")

        messages.success(request, "Savings goal added successfully!")
        return redirect("dashboard")

    available_transactions = Transaction.objects.filter(user=request.user).exclude(savings_goals__isnull=False)  # NOQA
    return render(request, "crud/create_saving_goal.html", {"available_transactions": available_transactions})


@login_required
def add_budget(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        description = request.POST.get("description", "")
        month = request.POST.get("month")
        year = request.POST.get("year")

        if not amount or not month or not year:
            messages.error(request, "All fields except description are required.")
            return redirect("add_budget")

        try:
            amount = float(amount)
            month = int(month)
            year = int(year)
        except (Category.DoesNotExist, ValueError):  # NOQA
            messages.error(request, "Invalid input.")
            return redirect("add_budget")

        Budget.objects.create(  # NOQA
            user=request.user,
            amount=amount,
            description=description,
            month=month,
            year=year,
        )
        messages.success(request, "Budget added successfully!")
        return redirect("dashboard")

    categories = Category.objects.all()  # NOQA
    return render(request, "crud/create_budget.html", {"categories": categories})


@login_required
def budget_manage(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)

    if request.method == "POST":
        if "edit" in request.POST:
            try:
                budget.amount = float(request.POST["amount"])
                budget.description = request.POST["description"]
                budget.month = int(request.POST["month"])
                budget.year = int(request.POST["year"])
                budget.save()
                messages.success(request, "Budget updated successfully!")
            except ValueError:
                messages.error(request, "Invalid input.")
            return redirect("dashboard")

        elif "delete" in request.POST:
            budget.delete()
            messages.success(request, "Budget deleted successfully!")
            return redirect("dashboard")

    categories = Category.objects.all()  # NOQA
    return render(request, "crud/budget_manage.html", {"budget": budget, "categories": categories})


@login_required
def saving_goal_manage(request, saving_goal_id):
    saving_goal = get_object_or_404(SavingsGoal, id=saving_goal_id, user=request.user)

    if request.method == "POST":
        transaction_id = request.POST.get("transaction_id")
        if "assign_transaction" in request.POST:
            try:
                transaction = Transaction.objects.get(id=transaction_id, user=request.user, type="income")
                saving_goal.transactions.add(transaction)
                messages.success(request, "Income transaction assigned to savings goal successfully!")
            except Transaction.DoesNotExist:
                messages.error(request, "Invalid or non-income transaction.")
        elif "remove_transaction" in request.POST:
            try:
                transaction = Transaction.objects.get(id=transaction_id, user=request.user)
                saving_goal.transactions.remove(transaction)
                messages.success(request, "Transaction removed from savings goal successfully!")
            except Transaction.DoesNotExist:
                messages.error(request, "Invalid transaction.")
        elif "delete_goal" in request.POST:
            saving_goal.delete()
            messages.success(request, "Savings goal deleted successfully!")
            return redirect("dashboard")

        saving_goal.refresh_from_db()
        return redirect("saving_goal_manage", saving_goal_id=saving_goal.id)

    available_transactions = Transaction.objects.filter(
        user=request.user, type="income"
    ).exclude(savings_goals=saving_goal)

    return render(request, "crud/saving_goal_manage.html", {
        "saving_goal": saving_goal,
        "available_transactions": available_transactions,
    })


@login_required
def transaction_manage(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)

    if request.method == 'POST':
        if 'edit' in request.POST:
            try:
                transaction.category_id = request.POST['category']

                amount = request.POST.get('amount', '0')
                if not amount.strip():
                    amount = '0'
                transaction.amount = float(amount)

                transaction.description = request.POST['description']

                date = request.POST.get('date')
                if date:
                    transaction.date = date
                else:
                    raise ValueError("Date is required.")

                transaction.save()
                messages.success(request, "Transaction updated successfully!")
                return redirect('dashboard')

            except ValueError as e:
                messages.error(request, f"Error: {e}")
                return redirect('transaction_manage', transaction_id=transaction.id)
            except Exception as e:
                messages.error(request, f"An unexpected error occurred. Please try again. {e}")
                return redirect('transaction_manage', transaction_id=transaction.id)

        elif 'delete' in request.POST:
            transaction.delete()
            messages.success(request, "Transaction deleted successfully!")
            return redirect('dashboard')

    context = {
        'transaction': transaction,
        'categories': Category.objects.all(),  # NOQA
    }
    return render(request, 'crud/transaction_manage.html', context)


@login_required
def mark_all_notifications_as_read(request):
    """Mark all notifications as read for the current user."""
    notifications = Notification.objects.filter(user=request.user, is_read=False)  # NOQA
    notifications.update(is_read=True)
    messages.success(request, "All notifications marked as read.")
    return redirect('dashboard')
