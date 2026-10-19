from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from .models import Users,Category,Expenses,Budget,Income
from decimal import Decimal, InvalidOperation
from datetime import date
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from datetime import date as date_type
import json
import calendar
# Create your views here.
def home(request):
    return render(request,'home.html')

def register(request):
    if request.method == "POST":
        un = request.POST.get('un', '').strip()
        mail = request.POST.get('mail', '').strip().lower()
        pwd = request.POST.get('pwd', '')
        cpwd = request.POST.get('cpwd', '')
        if not un or not mail or not pwd:
            return render(request,'register.html',{'error': 'All fields are required.'})
        if Users.objects.filter(email__iexact=mail).exists():
            return render(request,'register.html',{'error': 'Email is already registered.'})
        if pwd != cpwd:
            return render(request,'register.html',{'error': 'Passwords do not match.'})
        Users.objects.create(username=un,email=mail,password=make_password(pwd))
        return redirect('login')
    return render(request, 'register.html')

def signin(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')
        pwd = request.POST.get('pwd')
        user = Users.objects.filter(email=mail).first()
        if user and check_password(pwd, user.password):
            request.session['userid'] = user.id
            request.session['username'] = user.username
            return redirect('dashboard')
        else:
            return render(request,'login.html',{'error': 'Invalid email or password'})
    return render(request, 'login.html')

def logout(request):
    request.session.flush()
    return redirect('home')

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = Users.objects.filter(email=email).first()
        if not user:
            messages.error(request, "Email is not registered.")
            return redirect("forgot_password")
        request.session["reset_email"] = email
        return redirect("reset_password")
    return render(request, "forgot_password.html")

def reset_password(request):
    email = request.session.get("reset_email")
    if not email:
        messages.error(request, "Please enter your email first.")
        return redirect("forgot_password")
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("reset_password")
        user = Users.objects.get(email=email)
        user.password = make_password(password)
        user.save()
        del request.session["reset_email"]
        messages.success(request, "Password reset successfully. Please login.")
        return redirect("login")
    return render(request, "reset_password.html")


def dashboard(request):
    if 'userid' not in request.session:
        return redirect('login')
    user_id = request.session['userid']
    today = timezone.localdate()
    total_income = (Income.objects.filter(user_id=user_id).aggregate(total=Sum('amount'))['total']or Decimal('0.00'))
    expenses = Expenses.objects.filter(user_id=user_id)
    total_expenses = (expenses.aggregate(total=Sum('amount'))['total']or Decimal('0.00'))
    monthly_expenses = (
        expenses.filter(
            date__year=today.year,
            date__month=today.month
        ).aggregate(total=Sum('amount'))['total']
        or Decimal('0.00'))
    monthly_report = (
        expenses.filter(date__year=today.year)
        .values('date__month')
        .annotate(total=Sum('amount'))
        .order_by('date__month'))
    monthly_totals = {item['date__month']: float(item['total'])for item in monthly_report}
    chart_labels = [calendar.month_name[month]for month in range(1, 13)]
    chart_values = [monthly_totals.get(month, 0)for month in range(1, 13)]
    balance = total_income - total_expenses
    total_categories = Category.objects.count()
    return render(request, 'dashboard.html', {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'monthly_expenses': monthly_expenses,
        'total_categories': total_categories,
        'balance': balance,
        'chart_labels': chart_labels,
        'chart_values': chart_values,})

def add_category(request):
    if 'userid' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        if name:
            Category.objects.create(name=name, desc=desc)
            return redirect('add_category')
    return render(request, 'add_category.html')

def edit_category(request):
    if 'userid' not in request.session:
            return redirect('login')
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        category.name = request.POST.get('name')
        category.desc = request.POST.get('desc')
        category.save()
        messages.success(request, 'Category updated successfully!')
        return redirect('category_list')
    category_id = request.GET.get('id')
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'edit_category.html', {'category': category})


def delete_category(request, id):
    if 'userid' not in request.session:
        return redirect('login')
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        if Expenses.objects.filter(category=category).exists():
            messages.error(request,'Cannot delete this category because expenses use it.')
            return redirect('category_list')
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    return render(request,'delete_category.html',{'category': category})

def add_expense(request):
    if 'userid' not in request.session:
        return redirect('login')
    categories = Category.objects.all()
    if request.method == 'POST':
        description = request.POST.get('description', '').strip()
        amount_text = request.POST.get('amount', '')
        category_id = request.POST.get('category')
        expense_date = request.POST.get('date')
        payment_method = request.POST.get('payment_method')
        try:
            amount = Decimal(amount_text)
            parsed_date = date.fromisoformat(expense_date)
            if not amount.is_finite() or amount <= 0:
                raise ValueError
            if len(description) > 200 or not description:
                raise ValueError
        except (InvalidOperation, ValueError, TypeError):
            return render(request, 'add_expense.html', {'categories': categories,
                'error': 'Please enter valid expense details.'})
        category = Category.objects.filter(id=category_id).first()
        if not category or not payment_method:
            return render(request, 'add_expense.html', {'categories': categories,
                'error': 'Please select a valid category and payment method.'})
        Expenses.objects.create(
            user_id=request.session['userid'],
            category=category,
            amount=amount,
            description=description,
            date=parsed_date,
            payment_method=payment_method
        )
        return redirect('dashboard')
    return render(request, 'add_expense.html', {'categories': categories})

def expenses_list(request):
    if 'userid' not in request.session:
        return redirect('login')
    user_id = request.session['userid']
    expenses = Expenses.objects.filter(user_id=user_id).select_related('category').order_by('-date')
    search = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    if search:
        expenses = expenses.filter(description__icontains=search)
    if category_id:
        expenses = expenses.filter(category_id=category_id)
    if start_date:
        expenses = expenses.filter(date__gte=start_date)
    if end_date:
        expenses = expenses.filter(date__lte=end_date)
    categories = Category.objects.all()
    return render(request, 'expenses_list.html', {
        'expenses': expenses,
        'categories': categories,
        'search': search,
        'selected_category': category_id,
        'start_date': start_date,
        'end_date': end_date,})
    
def category_list(request):
    if 'userid' not in request.session:
        return redirect('login')
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def edit_expense(request, id):
    if 'userid' not in request.session:
        return redirect('login')
    expense = get_object_or_404(Expenses,id=id,user_id=request.session['userid'])
    categories = Category.objects.all()
    if request.method == 'POST':
        description = request.POST.get('description', '').strip()
        amount_text = request.POST.get('amount', '').strip()
        category_id = request.POST.get('category')
        expense_date = request.POST.get('date', '')
        payment_method = request.POST.get('payment_method', '').strip()
        try:
            amount = Decimal(amount_text)
            parsed_date = date.fromisoformat(expense_date)
            if not amount.is_finite() or amount <= 0:
                raise ValueError
            if not description or len(description) > 200:
                raise ValueError
        except (InvalidOperation, ValueError, TypeError):
            return render(request, 'edit_expense.html', {
                'expense': expense,
                'categories': categories,
                'error': 'Please enter valid expense details.'})
        category = Category.objects.filter(id=category_id).first()
        if not category or not payment_method or len(payment_method) > 30:
            return render(request, 'edit_expense.html', {
                'expense': expense,
                'categories': categories,
                'error': 'Select a valid category and payment method.'})
        expense.description = description
        expense.amount = amount
        expense.category = category
        expense.date = parsed_date
        expense.payment_method = payment_method
        expense.save()
        return redirect('expenses_list')
    return render(request, 'edit_expense.html', {
        'expense': expense,
        'categories': categories})

def delete_expense(request, id):
    if 'userid' not in request.session:
        return redirect('login')
    expense = get_object_or_404(Expenses,id=id,user_id=request.session['userid'])
    if request.method == 'POST':
        expense.delete()
        return redirect('expenses_list')
    return render(request, 'delete_expense.html',{'expense': expense})

def budget_view(request):
    if 'userid' not in request.session:
        return redirect('login')
    today = timezone.localdate()
    user_id = request.session['userid']
    budget, created = Budget.objects.get_or_create(
        user_id=user_id,
        month=today.month,
        year=today.year,
        defaults={'amount': 0}
    )
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return render(request, 'budget.html', {
                'budget': budget,
                'error': 'Enter a valid budget greater than zero.'
            })
        budget.amount = amount
        budget.save()
        return redirect('budget')
    spent = Expenses.objects.filter(
        user_id=user_id,
        date__year=today.year,
        date__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or 0
    remaining = budget.amount - spent
    return render(request, 'budget.html', {'budget': budget,'spent': spent,'remaining': remaining,})

def add_income(request):
    if 'userid' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        source = request.POST.get('source', '').strip()
        amount = request.POST.get('amount')
        description = request.POST.get('description', '').strip()
        date = request.POST.get('date')
        try:
            amount = Decimal(amount)
            date_type.fromisoformat(date)
            if amount <= 0 or not source:
                raise ValueError
        except (InvalidOperation, ValueError, TypeError):
            return render(request,'add_income.html',{'error': 'Enter a valid source, amount, and date.'})
        Income.objects.create(
            user_id=request.session['userid'],
            source=source,
            amount=amount,
            description=description,
            date=date)
        return redirect('income_list')
    return render(request, 'add_income.html')

def income_list(request):
    if 'userid' not in request.session:
        return redirect('login')
    incomes = Income.objects.filter(user_id=request.session['userid']).order_by('-date')
    return render(request,'income_list.html',{'incomes': incomes})

def edit_income(request, id):
    if 'userid' not in request.session:
        return redirect('login')
    income = get_object_or_404(Income,id=id,user_id=request.session['userid'])
    if request.method == 'POST':
        source = request.POST.get('source', '').strip()
        amount = request.POST.get('amount')
        description = request.POST.get('description', '').strip()
        date = request.POST.get('date')
        try:
            amount = Decimal(amount)
            date_type.fromisoformat(date)
            if amount <= 0 or not source:
                raise ValueError
        except (InvalidOperation, ValueError, TypeError):
            return render(request, 'edit_income.html', {'income': income,'error': 'Enter a valid source, amount, and date.'})
        income.source = source
        income.amount = amount
        income.description = description
        income.date = date
        income.save()
        return redirect('income_list')
    return render(request, 'edit_income.html',{'income': income})


def delete_income(request, id):
    if 'userid' not in request.session:
        return redirect('login')
    income = get_object_or_404(Income,id=id,user_id=request.session['userid'])
    if request.method == 'POST':
        income.delete()
        return redirect('income_list')
    return render(request, 'delete_income.html', {'income': income})

def expense_report(request):
    if 'userid' not in request.session:
        return redirect('login')
    user_id = request.session['userid']
    report = (Expenses.objects.filter(user_id=user_id).values('category__name').annotate(total=Sum('amount')).order_by('-total'))
    labels = []
    values = []
    for item in report:
        labels.append(item['category__name'] or 'Uncategorized')
        values.append(float(item['total']))
    context = {'report': report,'chart_labels': json.dumps(labels),'chart_values': json.dumps(values),}
    return render(request, 'expense_report.html', context)

def monthly_expense_report(request):
    if 'userid' not in request.session:
        return redirect('login')
    today = date.today()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))
    if month < 1 or month > 12 or year < 2000 or year > 2100:
        month = today.month
        year = today.year
    user_id = request.session['userid']
    expenses = Expenses.objects.filter(
        user_id=user_id,
        date__month=month,
        date__year=year)
    total = expenses.aggregate(total=Sum('amount'))['total'] or 0
    report = (expenses.values('category__name').annotate(total=Sum('amount')).order_by('-total'))
    months = [(i, calendar.month_name[i]) for i in range(1, 13)]
    years = range(max(2000, today.year - 5), today.year + 2)
    return render(request, 'monthly_expense_report.html', {
        'report': report,
        'total': total,
        'selected_month': month,
        'selected_year': year,
        'months': months,
        'years': years,})