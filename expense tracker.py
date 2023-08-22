# expenses/models.py
from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)
    date = model.DateField()

    def __str__(self):
        return f"${self.amount} - {self.description}"

# expenses/views.py
from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    total_spent = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request,'expenses/expense_list.html', {'expenses': expenses, 'total_spent': total_spent})

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
        else:
        form = ExpenseForm()

    return render(request, 'expenses/add_expense.html', {'form': form})     
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
@login_required
def monthly_report(request):
    current_month = timezone.now().month
    expenses = Expense.objects.filter(user=request.user, date__month=current_month)
    total_spent = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'expenses/monthly_report.html', {'expenses': expenses, 'total_spent': total_spent})

# expenses/forms.py
from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description', 'date']

<!-- monthly_report.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Expense Tracker - Monthly Report</title>
</head>
<body>
    <h1>Monthly Report - {{ current_month }}</h1>
    <p>Total Spent: ${{ total_spent }}</p>
    <ul>
        {% for expense in expenses %}
            <li>{{ expense }}</li>
        {% endfor %}
    </ul>
    <a href="{% url 'expense_list' %}">Back to Expense List</a>
</body>
</html>

# expenses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('add/', views.add_expense, name='add_expense'),
    path('monthly_report/', views.monthly_report, name='monthly_report'),
]

# expense_tracker/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('expenses.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

# settings.py
LOGIN_REDIRECT_URL = 'expense_list'
LOGOUT_REDIRECT_URL = 'login'