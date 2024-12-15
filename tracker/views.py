from django.shortcuts import render,redirect,HttpResponse
from .models import Transaction
from django.db.models import Sum,Q
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def registration(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user_obj = User.objects.filter(
            Q(email=email) | Q(username=username)
            )
        
        if user_obj.exists():
            messages.error(request, "Username or email already exists")
            return redirect("/registration/")
        user_obj = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
        )
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request,"User created")
        return redirect('/registration/')
        
    return render(request, 'registration.html')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user_obj = User.objects.filter(
            username=username
            )
        
        if not user_obj.exists():
            messages.error(request, "User not exists, create user")
            return redirect("/registration/")
        
        user_obj = authenticate(username=username,password=password)
        if user_obj is None:  
            messages.error(request, "Not a valid credential")
            return redirect("/login/")
        
        login(request,user_obj)
        return redirect("/")
    
    return render(request, 'login.html')
        
@login_required(login_url='/login/')
def logout_page(request):
    logout(request)
    messages.success(request,"User logout")
    return redirect('/login/')
    
@login_required(login_url='/login/')
def index(request):
    if request.method == "POST":
        description = request.POST.get('description')
        amount = request.POST.get('amount')
       
        
        if description is None:
            messages.error(request,"No description")
            return redirect('/')
        try:
            amount = float(amount)  # Convert to a number
        except ValueError:
            messages.error(request, "Amount is not a valid number.")
            return redirect('/')
        
        Transaction.objects.create(description=description,amount=amount,created_by=request.user)
    messages.info(request,"")
    context = {
        'trasactions':Transaction.objects.all(created_by=request.user),
        'balance':Transaction.objects.filter(created_by=request.user).aggregate(balance=Sum('amount'))['balance'] or 0,
        'income':Transaction.objects.filter(created_by=request.user,amount__gte=0).aggregate(income=Sum('amount'))['income'] or 0,
        'expense':Transaction.objects.filter(created_by=request.user,amount__lte=0).aggregate(expense=Sum('amount'))['expense'] or 0,
    }
    return render(request,'index.html',context)

@login_required(login_url='/login/')
def deleteTransaction(request, uuid):
    Transaction.objects.get(uuid=uuid).delete()
    return redirect('/')