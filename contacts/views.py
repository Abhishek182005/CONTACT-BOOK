from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import connection
from .models import Book
from .forms import BookForm, SearchForm, ModifyForm

def ensure_database_exists():
    dbname = 'contact'
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbname}")
        cursor.execute(f"USE {dbname}")

def home(request):
    return render(request, "home.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")  # Single error message
            return redirect("login")
    else:
        return render(request, "login.html")

def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
            else:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password1,
                )
                user.save()
                messages.success(request, "User registered successfully")
                return redirect("login")
        else:
            messages.error(request, "Passwords do not match")
        return redirect("register")
    else:
        return render(request, "register.html")

@login_required(login_url="login")
def logout(request):
    auth_logout(request)
    return redirect("home")

@login_required(login_url="login")
def adder(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['Name']
            numbers = form.cleaned_data['NUMBERS']
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO contacts_book (Name, NUMBERS) VALUES (%s, %s)", [name, numbers])
            messages.success(request, "Contact added successfully")
            return redirect('adder')
    else:
        form = BookForm()
    return render(request, 'adder.html', {'form': form})

@login_required(login_url="login")
def shower(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT SNO, Name, NUMBERS FROM contacts_book")
        columns = [col[0] for col in cursor.description]
        books = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return render(request, 'shower.html', {'books': books})

@login_required(login_url="login")
def searcher(request):
    search_performed = False
    form = SearchForm()
    books = []

    if request.method == 'POST':
        search_performed = True
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            number = form.cleaned_data['number']
            number1 = str(number)
            with connection.cursor() as cursor:
                if name and number:
                    cursor.execute("SELECT SNO, Name, NUMBERS FROM contacts_book WHERE Name LIKE %s AND CAST(NUMBERS AS CHAR(10)) LIKE %s", ['%' + name + '%', '%' + number1 + '%'])
                elif name:
                    cursor.execute("SELECT SNO, Name, NUMBERS FROM contacts_book WHERE Name LIKE %s", ['%' + name + '%'])
                elif number:
                    cursor.execute("SELECT SNO, Name, NUMBERS FROM contacts_book WHERE CAST(NUMBERS AS CHAR(10)) LIKE %s", ['%' + number1 + '%'])
                books = cursor.fetchall()
    
    context = {
        'form': form,
        'books': books,
        'search_performed': search_performed,
    }
    return render(request, 'search_form.html', context)

def modifier(request):
    form = ModifyForm()
    books = []
    search_performed = False
    
    if request.method == 'POST':
        search_performed = True
        form = ModifyForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            number = form.cleaned_data['numbers']
            number1 = str(number)
            with connection.cursor() as cursor:
                if name and number:
                    cursor.execute("SELECT SNO, Name, NUMBERS FROM contacts_book WHERE Name LIKE %s AND CAST(NUMBERS AS CHAR(10)) LIKE %s", ['%' + name + '%', '%' + number1 + '%'])
                elif name:
                    cursor.execute("SELECT SNO, Name, NUMBERS FROM contacts_book WHERE Name LIKE %s", ['%' + name + '%'])
                elif number:
                    cursor.execute("SELECT SNO, Name, NUMBERS FROM contacts_book WHERE CAST(NUMBERS AS CHAR(10)) LIKE %s", ['%' + number1 + '%'])
                books = cursor.fetchall()
    elif request.method == 'GET' and 'sno' in request.GET:
        sno = request.GET['sno']
        book = get_object_or_404(Book, SNO=sno)
        form = ModifyForm(initial={'name': book.Name, 'numbers': book.NUMBERS})
        return render(request, 'modify_form.html', {'form': form, 'book': book})

    context = {
        'form': form,
        'books': books,
        'search_performed': search_performed,
    }
    return render(request, 'modify_form.html', context)

@login_required(login_url="login")
def modify_contact(request):
    if request.method == 'POST':
        sno = request.POST.get('sno')
        name = request.POST.get('name')
        numbers = request.POST.get('numbers')
        with connection.cursor() as cursor:
            if name:
                cursor.execute("UPDATE contacts_book SET Name = %s WHERE SNO = %s", [name, sno])
            if numbers:
                cursor.execute("UPDATE contacts_book SET NUMBERS = %s WHERE SNO = %s", [numbers, sno])
        messages.success(request, "Contact modified successfully")
        return redirect('modifier')

@login_required(login_url="login")
def deleter(request):
    if request.method == 'POST':
        sno = request.POST.get('sno')
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM contacts_book WHERE SNO = %s", [sno])
            cursor.execute("SET @sno = 0")
            cursor.execute("UPDATE contacts_book SET SNO = (@sno := @sno + 1)")
            cursor.execute("ALTER TABLE contacts_book AUTO_INCREMENT = 1")
        messages.success(request, "Contact deleted successfully")
        return redirect('modifier')
