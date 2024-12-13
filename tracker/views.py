from django.shortcuts import render,redirect
from .models import Transaction
from django.db.models import Sum
# Create your views here.
from django.contrib import messages

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
        
        Transaction.objects.create(description=description,amount=amount)
    messages.info(request,"")
    context = {
        'trasactions':Transaction.objects.all(),
        'balance':Transaction.objects.all().aggregate(balance=Sum('amount'))['balance'] or 0,
        'income':Transaction.objects.filter(amount__gte=0).aggregate(income=Sum('amount'))['income'] or 0,
        'expense':Transaction.objects.filter(amount__lte=0).aggregate(expense=Sum('amount'))['expense'] or 0,
    }
    return render(request,'index.html',context)

def deleteTransaction(request, uuid):
    Transaction.objects.get(uuid=uuid).delete()
    return redirect('/')