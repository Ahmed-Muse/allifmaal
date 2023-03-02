from turtle import title
from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from uuid import uuid4
from django.http.response import HttpResponse, JsonResponse
#from invoice.models import AllifmaalDetailsModel,AllifmaalScopeModel
#from learningapp.models import SepcoLogoModel
from django.http.response import HttpResponse, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from decimal import Decimal
from django.db.models import Count,Min,Max,Avg,Sum
from django.contrib.auth.decorators import login_required 
# Create your views here.


@login_required(login_url='login:loginpage')
def allifmaalmaindashboard(request):
    #quit()
    #fileHandle=open('testing.txt')
    #ts=fileHandle.read()
    #print(len(ts))
    prospects=AllifmaalQuotesModel.objects.filter(prospect="Likely").order_by('-total','-date')[:15]
    posted_invoices=AllifmaalInvoicesModel.objects.filter(posting_inv_status="posted").order_by('-invoice_total','-date')[:15]
    no_of_prospects=AllifmaalQuotesModel.objects.filter(prospect="Likely").count()
    
    total_value_of_prospects=AllifmaalQuotesModel.objects.filter(prospect="Likely").aggregate(Sum('total'))['total__sum']
    total_value_of_latest_posted_invoices=AllifmaalInvoicesModel.objects.filter(posting_inv_status="posted").aggregate(Sum('invoice_total'))['invoice_total__sum']
    
    debtors=AllifmaalCustomersModel.objects.filter(balance__gt=2).order_by('-balance')[:7]
    creditors=AllifmaalSuppliersModel.objects.filter(balance__gt=2).order_by('-balance')[:8]
    creditors_total_balance=AllifmaalSuppliersModel.objects.filter(balance__gt=2).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
    debtor_total_balance=AllifmaalCustomersModel.objects.filter(balance__gt=2).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
    gold_customers=AllifmaalCustomersModel.objects.all().order_by('-turnover')[:15]
    main_assets=AllifmaalAssetsModel.objects.filter(value__gt=0).order_by('-value')[:10]
    
    assets_tot_val=AllifmaalChartOfAccountsModel.objects.filter(code__lte=19999).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
    gold_customers_turnover=AllifmaalCustomersModel.objects.all().aggregate(Sum('turnover'))['turnover__sum']
    context={
        "prospects":prospects,
        "creditors_total_balance":creditors_total_balance,
        "no_of_prospects":no_of_prospects,
        "total_value_of_prospects":total_value_of_prospects,
        "posted_invoices":posted_invoices,
        "total_value_of_latest_posted_invoices":total_value_of_latest_posted_invoices,
        "debtors":debtors,
        "creditors":creditors,
        "gold_customers":gold_customers,
        "main_assets":main_assets,
        "debtor_total_balance":debtor_total_balance,
        "assets_tot_val":assets_tot_val,
        "gold_customers_turnover":gold_customers_turnover,
       

    }
    return render(request,'allifmaalapp/dashboard/allifmaaldashboard.html',context)


######################3 COMPANY DETAILS ###################3lll
def titlefunction(request,mytitle):
    amel="Allifmaal Engineering Limited"
    print(mytitle)
    return amel
def allifmaal_settings_details(request):
    
    title="Allifmaal Details"
    titlefunction(request,mytitle=title)

    CompanySettingDetails= AllifmaalDetailsModel.objects.all()

    form=AddAllifmaalDetailsForm(request.POST, request.FILES)
    
    if request.method == 'POST':
        form=AddAllifmaalDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect('allifmaalapp:allifmaal_settings_details')
    else:
        form=AddAllifmaalDetailsForm()
    
    ################ start ... below functions are just for learning purposes for *args and **kwargs
    def allif_inner_non_keyword_args_function(*numbers,**mywords):
        product=1
        sentence=''
        key_and_value=[]
        for number in numbers:
            product*=number
        print(product)
        for words in mywords.values():
            sentence+=words
        print(sentence)
        for key,value in mywords.items():#items gives both keys and values
            key_and_value.append("{} uses {}".format(key, value))
        print(key_and_value)
        product_and_words=str(product)+sentence
        return product_and_words
    allif_inner_non_keyword_args_function(10,50,10,a='kwargs ',b='contain a ',c='key-value-pair')#be sure the calling of the function to be at the same level as its declaration in identation

    def printingData(standard_args, *args, **kwargs):
        print("I am ", standard_args)
        for arg in args:
            print("I am arg: ", arg)
        for keyWord in kwargs.items():
            print("I am kwarg: ", keyWord)
    
    printingData('007', 'agent', firstName='Allifmaal', lastName='Engineering')

    ################ end #############################

    context={
        "title":title,
        "form":form,
        "CompanySettingDetails":CompanySettingDetails,

    }
    return render(request,'allifmaalapp/settings/allifmaal-settings-details.html',context)

def update_allifmaal_company_details(request,pk):
    title="Update Company Details"
    update= AllifmaalDetailsModel.objects.get(id=pk)
    form = AddAllifmaalDetailsForm(instance=update)
   
    if request.method == 'POST':
        form = AddAllifmaalDetailsForm(request.POST,request.FILES, instance=update)
        if form.is_valid():
            form.save()
          
            return redirect('allifmaalapp:allifmaal_settings_details')

    context = {
		'form':form,
        "update":update,
        "title":title,
    }
    
    return render(request,'allifmaalapp/settings/allifmaal-settings-details.html',context)
def delete_allifmaal_company_detail(request,pk):
    AllifmaalDetailsModel.objects.get(id=pk).delete()
    return redirect('allifmaalapp:allifmaal_settings_details')


def allifmaal_scope_details(request):
    title="Allifmaal Scope Details"

    AllifScopeDetails= AllifmaalScopeModel.objects.all()

    form=AddAllifmaalScopeForm(request.POST)
    
    if request.method == 'POST':
        form=AddAllifmaalScopeForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('allifmaalapp:allifmaal_scope_details')
    else:
        form=AddAllifmaalScopeForm()
    context={
        "title":title,
        "form":form,
        "AllifScopeDetails":AllifScopeDetails,

    }
    return render(request,'allifmaalapp/settings/allifmaal-scope-details.html',context)



def update_allifmaal_scope_details(request,pk):
    
    title="Update Company Scope Details"
    update= AllifmaalScopeModel.objects.get(id=pk)
    form =AddAllifmaalScopeForm(instance=update)
   
    if request.method == 'POST':
        form = AddAllifmaalScopeForm(request.POST,instance=update)
        if form.is_valid():
            form.save()
          
            return redirect('allifmaalapp:allifmaal_scope_details')

    context = {
		'form':form,
        "update":update,
        "title":title,
    }
    
    return render(request,'allifmaalapp/settings/allifmaal-scope-details.html',context)
def delete_allifmaal_scope_detail(request,pk):
    AllifmaalScopeModel.objects.get(id=pk).delete()
    return redirect('allifmaalapp:allifmaal_scope_details')


################################### SUPPLIERS ###############################3
def allifmaal_suppliers(request):
    title="Allifmaal Suppliers"
    suppliers=AllifmaalSuppliersModel.objects.all()
    print(suppliers)
    form=AddAllifmaalSupplierForm()
    
    if request.method == 'POST':
        form=AddAllifmaalSupplierForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect('allifmaalapp:allifmaal_suppliers')
    else:
        form=AddAllifmaalSupplierForm()
    context={
        
        "form":form,
        "title":title,
        
        "suppliers":suppliers,
    }
    return render(request,'allifmaalapp/suppliers/allifmaal-suppliers.html',context)



def show_allifmaal_supplier_details(request,pk):
    title="Supplier Details"
    try:
        Supplier_detail=AllifmaalSuppliersModel.objects.get(id=pk)
    except:
        messages.error(request, 'Something went wrong')
        return redirect('allifmaalapp:allifmaal_suppliers')

    context={
        "Supplier_detail":Supplier_detail,
        "title":title,

    }
    return render(request,'allifmaalapp/suppliers/allifmaal-supplier-details.html',context)
    


def delete_allifmaal_supplier(request,pk):
    try:
        AllifmaalSuppliersModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('allifmaalapp:allifmaal_suppliers')

    return redirect('allifmaalapp:allifmaal_suppliers')

def update_allifmaal_supplier(request,pk):
    title="Update Supplier Details"
    update= AllifmaalSuppliersModel.objects.get(id=pk)
    form = AddAllifmaalSupplierForm(instance=update)
   
    if request.method == 'POST':
        form = AddAllifmaalSupplierForm(request.POST, instance=update)
        if form.is_valid():
            form.save()
          
            return redirect('allifmaalapp:allifmaal_suppliers')

    context = {
		'form':form,
        "update":update,
        "title":title,
    }
    
    return render(request,'allifmaalapp/suppliers/allifmaal-suppliers.html',context)


##################################33 our customers ###################################3


def allifmaalcustomers(request):
    title="Allifmaal Customers"
    customers1=AllifmaalCustomersModel.objects.all()
    customers=AllifmaalCustomersModel.objects.annotate(Sum('turnover'))
    print(customers)
    form=AddAllifmaalCustomerForm()
    
    if request.method == 'POST':
        form=AddAllifmaalCustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect('allifmaalapp:allifmaalcustomers')
    else:
        form=AddAllifmaalCustomerForm()
    context={
        
        "form":form,
        "title":title,
        
        "customers":customers,
    }

   
    return render(request,'allifmaalapp/customers/allifmaal-customers-list.html',context)

def show_allifmaal_customer_details(request,pk):
    title="Customer Details"
    try:
        customer_detail=AllifmaalCustomersModel.objects.get(id=pk)
        related_invoices=AllifmaalInvoicesModel.objects.filter(customer=customer_detail)
        customer_payments=AllifmaalCustomerPaymentsModel.objects.filter(customer=customer_detail)
        related_quotes=AllifmaalQuotesModel.objects.filter(customer=customer_detail)
    except:
        messages.error(request, 'Something went wrong')
        return redirect('allifmaalapp:allifmaalcustomers')

    context={
        "customer_detail":customer_detail,
        "title":title,
        "related_invoices":related_invoices,
        "customer_payments":customer_payments,
        "related_quotes":related_quotes,

    }
    return render(request,'allifmaalapp/customers/allifmaal-customers-details.html',context)


def delete_allifmaal_customer(request,pk):
    try:
        AllifmaalCustomersModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('allifmaalapp:allifmaalcustomers')

    return redirect('allifmaalapp:allifmaalcustomers')

def update_allifmaal_customer(request,pk):
    title="Update Customer Details"
    update= AllifmaalCustomersModel.objects.get(id=pk)
    form = AddAllifmaalCustomerForm(instance=update)
   
    if request.method == 'POST':
        form = AddAllifmaalCustomerForm(request.POST, instance=update)
        if form.is_valid():
            form.save()
          
            return redirect('allifmaalapp:allifmaalcustomers')

    context = {
		'form':form,
        "update":update,
        "title":title,
    }
    
    return render(request,'allifmaalapp/customers/allifmaal-customers-list.html',context)
def AllifmaalCustomerPayments(request):
    payments=AllifmaalCustomerPaymentsModel.objects.all()
    lastestpayments=AllifmaalCustomerPaymentsModel.objects.order_by('-date')[:10]
    title="Customer Payments"

    context={
        
        "title":title,
        "payments":payments,
        "lastestpayments":lastestpayments,
       

    }
    return render(request, 'allifmaalapp/payment/customer-payments.html', context)#th


def AllifmaaltopUpCustomerAccount(request,pk):
    global customer,mycustid
    default_cash_accs=AllifmaalChartOfAccountsModel.objects.filter(description="Cash").first()
    default_cash_accs_2=AllifmaalChartOfAccountsModel.objects.filter(code__lte=19999)[3]
    form=AddAllifmaalCustomerPaymentForm(initial={'account':default_cash_accs})
  
    try:
        customer=AllifmaalCustomersModel.objects.get(id=pk)#very important to get id to go to particular shipment
        initial_balance=customer.balance#this gives the initial account
        mycustid=customer.id
        title="Receive Payment From "+ str(customer)
    except:
        return HttpResponse("Sorry there is a problem ! ")
    
    top_up_cust_account= get_object_or_404(AllifmaalCustomersModel, id=pk)


    topups= AllifmaalCustomerPaymentsModel.objects.filter(customer=customer)#this line helps to
    
    cust_acc_total = 0
    if len(topups) > 0:
        for payment in topups:
            amount= payment.amount
            cust_acc_total += amount

    
    add_item= None
    if request.method == 'POST':
        form=AddAllifmaalCustomerPaymentForm(request.POST)
        if form.is_valid():
            add_item= form.save(commit=False)
            add_item.customer=top_up_cust_account
            add_item.save()
            
            myamount=request.POST.get('amount')
           
            mycard=AllifmaalCustomersModel.objects.get(id=customer.id)# returns TO objects
            mycard.balance= Decimal(initial_balance)-Decimal(myamount)
            mycard.save()
            form=AddAllifmaalCustomerPaymentForm()
            #return redirect('allifmaalapp:AllifmaaltopUpCustomerAccount',pk=mycustid)#just redirection page
    
         ############# using for the chart of accounts ###########3
        received_amount=request.POST.get('amount')#this gives the amount in the field
        receive_to_acc=request.POST.get('account')
        
        receive_to_acc_queryset=AllifmaalChartOfAccountsModel.objects.get(id=receive_to_acc)
        
        receive_to_acc_initial_balance=receive_to_acc_queryset.balance
        
        receive_to_acc_queryset.balance=receive_to_acc_initial_balance+Decimal(received_amount)
        receive_to_acc_queryset.save()
        customer_advances=AllifmaalChartOfAccountsModel.objects.filter(description="Customer Advances").first()
        if customer_advances:
            cust_advances=AllifmaalChartOfAccountsModel.objects.filter(description="Customer Advances").first()
            initial_customer_advances_balances= cust_advances.balance
            cust_advances.balance=initial_customer_advances_balances+Decimal(myamount)
            #cust_advances.save()
        return redirect("allifmaalapp:AllifmaaltopUpCustomerAccount",pk=mycustid)
    

        ############# end using chart of accounts ##########3############
    context={
        "form":form,  
        "customer":customer,
        "topups":topups,
        "cust_acc_total":cust_acc_total,
        "title":title,
       

    }
    return render(request, 'allifmaalapp/payment/allifcustomers-top-ups.html', context)#th

def DeleteAllifmaalCustomerPayment(request,pk):
    AllifmaalCustomerPaymentsModel.objects.get(id=pk).delete()
    return redirect('allifmaalapp:AllifmaalCustomerPayments')

def AllifmaalCustomerPaymentDetails(request,pk):
    title="Payment Details "
    
    try:
        payment_id=AllifmaalCustomerPaymentsModel.objects.get(id=pk)
        ourid=payment_id.id
        
    except:
        messages.error(request, 'Something went wrong!')
       
   
    context={
        
        "title":title,
        "payment_id":payment_id,
        
    }
    return render(request,'allifmaalapp/payment/payment-details.html',context)



######################### QUOTATION #########################
def allifmaal_quotes(request):
    title="Quotations"
    no_of_quotes=AllifmaalQuotesModel.objects.all().count()
    no_of_prospects=AllifmaalQuotesModel.objects.filter(prospect="Likely").count()
    total_value_of_prospects=AllifmaalQuotesModel.objects.filter(prospect="Likely").aggregate(Sum('total'))['total__sum']
    quotes=AllifmaalQuotesModel.objects.all()
    prospects=AllifmaalQuotesModel.objects.filter(prospect='Likely')
    isticmaale=request.user
    print(isticmaale)
    context={
        "title":title,
        "quotes":quotes,
        "no_of_quotes":no_of_quotes,
        "prospects":prospects,
        "no_of_prospects":no_of_prospects,
        "total_value_of_prospects":total_value_of_prospects,
    }
    return render(request, 'allifmaalapp/quotes/allifquotes.html',context)
import datetime
def create_allifmaal_quote(request):
    current_datetime = datetime.datetime.now()
    Quote_year=current_datetime.year

    last_inv= AllifmaalQuotesModel.objects.all().order_by('id').last()
    last_obj=AllifmaalQuotesModel.objects.last()
    if last_obj:
        
        last_obj_id=last_obj.id
        last_obj_incremented=last_obj_id+1
        QuoteNumber= 'AM/SQ/'+str(last_obj_incremented)+'/'+str(Quote_year)
       
   
    #purchaseNumber= 'LPO/AMEL-'+str(uuid4()).split('-')[1]
        
    else:
       
        
        QuoteNumber= 'AM/SQ'+'/'+str(Quote_year)
        #QuoteNumber= 'AM/SQ/'+str(uuid4()).split('-')[1]
        #purchaseNumber= 'LPO/AMEL-'+str(uuid4()).split('-')[1]+'/'+str("Reset")

    newQuoteNumber= AllifmaalQuotesModel.objects.create(number=QuoteNumber)
    newQuoteNumber.save()
    return redirect('allifmaalapp:allifmaal_quotes')

def delete_allifmaal_quote(request,pk):
    AllifmaalQuotesModel.objects.get(id=pk).delete()
    return redirect('allifmaalapp:allifmaal_quotes')

def add_allifmaal_Quote_details(request,pk):
    title="Quote Details "
    
    try:
        Quote_id=AllifmaalQuotesModel.objects.get(id=pk)
        ourid=Quote_id.id
        
    except:
        messages.error(request, 'Something went wrong and could not get the Quote')
        return redirect('allifmaalapp:allifmaal_quotes')

    Quote_Items = AllifmaalQuoteItemsModel.objects.filter(allifquoteitemconnector=Quote_id)#this line helps to
    #show items that belong to that particular invoice in that particular invoice
    Qte_id= get_object_or_404(AllifmaalQuotesModel, id=pk)#this helps to fill that select field and invoice fields and content
    
    form=AddAllifmaalQuoteDetailsForm(instance=Quote_id)
   
    if request.method == 'POST':
        #add_shipment_items_form=AddShippmentItemsForm(request.POST)
        form=AddAllifmaalQuoteDetailsForm(request.POST,request.FILES,instance=Quote_id)
        if form.is_valid():
            form.save()
            #print(request.POST)
           
            return redirect('allifmaalapp:add_allifmaal_quote_items',pk=ourid)
    context={
        
        "form":form,
        "Quote_Items":Quote_Items,
       
        "Quote_id":Quote_id,
        "title":title,
        

    }
    return render(request,'allifmaalapp/quotes/quote-details.html',context)

def add_allifmaal_quote_items(request,pk):
    title="Add Quote Items "
    global qiimeeyn,qiimeynid
    #try:
    qiimeeyn =AllifmaalQuotesModel.objects.get(id=pk)#very important to get id to go to particular shipment
    qiimeynid=qiimeeyn.id
    #except:
        #return HttpResponse("Sorry there is a problem ! ")
   
    form=AddAllifmaalQuoteItemsForm()
    add_Qte_No= get_object_or_404(AllifmaalQuotesModel, id=pk)
    initial_invoice_total=qiimeeyn.total#this gives the initial invoice total
    if qiimeeyn.customer:
        mycust=qiimeeyn.customer#this gives the customer of the invoice
        customer_id=mycust.id#this gives the id of the customer specified in the invoice
        customer_account_balance=mycust.balance#this gets the account balance of the customer

    #try:
    Qte_Items = AllifmaalQuoteItemsModel.objects.filter(allifquoteitemconnector=qiimeeyn)#this line helps to
    invoiceTotal = 0
    if len(Qte_Items) > 0:
        for line in Qte_Items:
            quantityTimesUnitPrice = line.quantity*line.description.unitPrice
            invoiceTotal += quantityTimesUnitPrice
    
    myinvoice=AllifmaalQuotesModel.objects.get(id=qiimeynid)
    myinvoice.total=invoiceTotal
    myinvoice.save()
    #except:
        #return HttpResponse("There is a problem... seems you inserted a number beyond the range")


    add_item= None
    try:
        if request.method == 'POST':
            form=AddAllifmaalQuoteItemsForm(request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.allifquoteitemconnector=add_Qte_No
                add_item.save()
                # return HttpResponse(post)
                return redirect('allifmaalapp:add_allifmaal_quote_items',pk=qiimeynid)#just redirection page
    except:
        return HttpResponse("There is a problem... seems you inserted a number beyond the range")

    context={
   
            "form":form,
            
            "qiimeeyn":qiimeeyn,
            "add_Qte_No":add_Qte_No,
            "invoiceTotal":invoiceTotal,
            "Qte_Items":Qte_Items,
            "title":title, 
    }
    return render(request,'allifmaalapp/quotes/add-quote-items.html',context)

def delete_allifmaal_quote_item(request,pk):
    AllifmaalQuoteItemsModel.objects.get(id=pk).delete()
    #return redirect('logistics:add_invoice_items_alwen',pk=pk)#just redirection page
    return redirect('allifmaalapp:add_allifmaal_quote_items',pk=qiimeynid)

def allifmaal_quote_to_pdf(request,pk):
    system_user=request.user
    Quote_details=get_object_or_404(AllifmaalQuotesModel,id=pk)
    title="Quote "+str(Quote_details)
    try:
        allif_quote_number= AllifmaalQuotesModel.objects.get(id=pk)
    except:
        messages.error(request, 'Something went wrong')

    quoteItems = AllifmaalQuoteItemsModel.objects.filter(allifquoteitemconnector=allif_quote_number)

    invoiceTotal = 0
    if len(quoteItems) > 0:
       for x in quoteItems:
            y = (0 or x.quantity) * (0 or x.description.unitPrice)
            invoiceTotal += y

    template_path = 'allifmaalapp/quotes/allifmaal-quote-to-pdf.html'
    companyDetails=AllifmaalDetailsModel.objects.all()
    scopes=AllifmaalScopeModel.objects.all()
    
    context = {
    'Quote_details':Quote_details,
   "quoteItems":quoteItems,
   "companyDetails":companyDetails,
   "invoiceTotal":invoiceTotal,
   "scopes":scopes,
   "system_user":system_user,
   "title":title,
   
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Allifmaal-invoice.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    try:
        pisa_status = pisa.CreatePDF(
       html, dest=response)
    except:
        return HttpResponse("Something went wrong!")
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response

########################### END OF QUOTATION ###############

##########################3 INVOICES #######################333
def allifmaal_invoices(request):
    title="Allifmaal Invoices"
    invoices=AllifmaalInvoicesModel.objects.filter(posting_inv_status="waiting")
    last_invoices=AllifmaalInvoicesModel.objects.order_by('invoice_number')[:6]
    no_invoices=AllifmaalInvoicesModel.objects.all().count()
    
   
    latest_paid_invoices=AllifmaalInvoicesModel.objects.filter(invoice_status='Paid').order_by('-date')[:7]
    posted_invoices_total_value=AllifmaalInvoicesModel.objects.filter(posting_inv_status="posted").aggregate(Sum('invoice_total'))['invoice_total__sum']
    context={
        "invoices":invoices,
        "last_invoices":last_invoices,
        "title":title,
        "no_invoices":no_invoices,
        "posted_invoices_total_value":posted_invoices_total_value,
        "latest_paid_invoices":latest_paid_invoices,
        
    }

    return render(request,'allifmaalapp/invoices/invoices.html',context)

def create_allifmaal_invoice(request):

    last_inv= AllifmaalInvoicesModel.objects.all().order_by('id').last()
    last_obj=AllifmaalInvoicesModel.objects.last()
    if last_obj:
        
        last_obj_id=last_obj.id
        last_obj_incremented=last_obj_id+1
   
    #purchaseNumber= 'LPO/AMEL-'+str(uuid4()).split('-')[1]
        purchaseNumber= 'AM/INV/'+'/'+str(last_obj_incremented)
        print(purchaseNumber)
    else:
       
        
        purchaseNumber= 'AM/INV/'+str(uuid4()).split('-')[1]
        #purchaseNumber= 'LPO/AMEL-'+str(uuid4()).split('-')[1]+'/'+str("Reset")

    newPurchaseOrder= AllifmaalInvoicesModel.objects.create(invoice_number=purchaseNumber)
    newPurchaseOrder.save()
    return redirect('allifmaalapp:allifmaal_invoices')

def delete_allifmaal_invoice(request,pk):
    AllifmaalInvoicesModel.objects.get(id=pk).delete()
    return redirect('allifmaalapp:allifmaal_invoices')

def delete_allifmaal_posted_invoice(request,pk):
    AllifmaalInvoicesModel.objects.get(id=pk).delete()
    return redirect('allifmaalapp:allifpostedinvoices')

def add_allifmaal_invoice_details(request,pk):
    title="Invoice Details "
    inv_details=AllifmaalInvoicesModel.objects.filter(id=pk)
    try:
        my_inv_id=AllifmaalInvoicesModel.objects.get(id=pk)
        ourid=my_inv_id.id
        
    except:
        messages.error(request, 'Something went wrong and could not get the invoice')
        return redirect('allifmaalapp:allifmaal_invoices')

    service_Items = AllifmaalInvoiceItemsModel.objects.filter(allifinvitemconnector=my_inv_id)#this line helps to
    #show items that belong to that particular invoice in that particular invoice
    inv_id= get_object_or_404(AllifmaalInvoicesModel, id=pk)#this helps to fill that select field and invoice fields and content
    
    form=AddAllifmaalInvoiceDetailsForm(instance=my_inv_id)
   
    if request.method == 'POST':
        #add_shipment_items_form=AddShippmentItemsForm(request.POST)
        form=AddAllifmaalInvoiceDetailsForm(request.POST,request.FILES,instance=my_inv_id)
        if form.is_valid():
            form.save()
            print(request.POST)
            print("I have saved and itts correct")
            return redirect('allifmaalapp:add_allifmaal_invoice_items',pk=ourid)
    context={
        
        "form":form,
        "service_Items":service_Items,
       
        "my_inv_id":my_inv_id,
        "title":title,
        

    }
    return render(request,'allifmaalapp/invoices/invoice-details.html',context)
   


def add_allifmaal_invoice_items(request,pk):
    title="Add Invoice Items "
    global qaanshegto,myinvid
    try:
        qaanshegto =AllifmaalInvoicesModel.objects.get(id=pk)#very important to get id to go to particular shipment
        myinvid=qaanshegto.id
    except:
        return HttpResponse("Sorry there is a problem ! ")
   
    form=AddAllifmaalInvoiceItemsForm()
    add_inv= get_object_or_404(AllifmaalInvoicesModel, id=pk)
    initial_invoice_total=qaanshegto.invoice_total#this gives the initial invoice total
    if qaanshegto.customer:
        mycust=qaanshegto.customer#this gives the customer of the invoice
        customer_id=mycust.id#this gives the id of the customer specified in the invoice
        customer_account_balance=mycust.balance#this gets the account balance of the customer


    inv_Items = AllifmaalInvoiceItemsModel.objects.filter(allifinvitemconnector=qaanshegto)#this line helps to
    invoiceTotal = 0
    inv_items_total_cost=0
    if len(inv_Items) > 0:
        for line in inv_Items:
            quantityTimesUnitPrice = line.quantity * line.description.unitPrice
            invoiceTotal += quantityTimesUnitPrice
            total_cost=line.quantity* line.description.unitcost
            inv_items_total_cost+=total_cost
    
    myinvoice=AllifmaalInvoicesModel.objects.get(id=myinvid)
    myinvoice.invoice_total=invoiceTotal
    myinvoice.invoice_items_total_cost=inv_items_total_cost
    myinvoice.save()
    

    add_item= None
    amount=0
    if request.method == 'POST':
        form=AddAllifmaalInvoiceItemsForm(request.POST)
        if form.is_valid():
            add_item= form.save(commit=False)
            add_item.allifinvitemconnector=add_inv
            add_item.save()

            quantity=request.POST.get('quantity')
            description_id=int(request.POST.get('description'))
            invoiceitem=AllifmaalStocksModel.objects.get(pk=description_id)
            selling_price=invoiceitem.unitPrice
            amount=Decimal(selling_price)*Decimal(quantity)

           # return HttpResponse(post)
            return redirect('allifmaalapp:add_allifmaal_invoice_items',pk=myinvid)#just redirection page

    context={
   
            "form":form,
            
            "qaanshegto":qaanshegto,
            "add_inv":add_inv,
            "invoiceTotal":invoiceTotal,
            "inv_Items":inv_Items,
            "title":title,
            "amount":amount,
    }
    return render(request,'allifmaalapp/invoices/add-invoice-items.html',context)

def delete_allifmaal_invoice_item(request,pk):
    AllifmaalInvoiceItemsModel.objects.get(id=pk).delete()
    #return redirect('logistics:add_invoice_items_alwen',pk=pk)#just redirection page
    return redirect('allifmaalapp:add_allifmaal_invoice_items',pk=myinvid)

def post_allifmaal_invoice(request,pk):
    
    global qaanshegto,myinvid
    #try:
    qaanshegto =AllifmaalInvoicesModel.objects.get(id=pk)#very important to get id to go to particular shipment
    
    inv_items=AllifmaalInvoiceItemsModel.objects.filter(allifinvitemconnector=qaanshegto)

    if qaanshegto.customer:
        myinvid=qaanshegto.id
        inv_terms=qaanshegto.invoice_terms
        inv_total=qaanshegto.invoice_total# this gives invoice value
        inv_items_total_cost=qaanshegto.invoice_items_total_cost# this gives the total cost of all items in the invoice
        profit_or_lost=inv_total - inv_items_total_cost
        customer=qaanshegto.customer
        customer_id=customer.id
        if inv_terms=="Cash":
            for item in inv_items:
                inventory_acc_id=item.description.inventory_account.id
                expense_acc_id=item.description.expense_account.id
                income_acc_id=item.description.income_account.id
                
                invo_quantity=item.quantity # this gives the quantities in the invoice
                invoice_item_id=item.description.id #this gives the IDs of the invoice item in the main AllifmaalStocksModel database.
                
                products=AllifmaalStocksModel.objects.get(pk=invoice_item_id)
                initial_item_quantity=products.quantity
                products.quantity=initial_item_quantity-invo_quantity
            
                unitprice=products.unitPrice # this gives the item selling price
                unit_cost=products.unitcost # this gives the item selling price
                per_line_selling_price=unitprice*invo_quantity
                per_line_cost=unit_cost*invo_quantity
                weighted_unit_cost=products.unitcost
                per_line_cost_price=weighted_unit_cost*invo_quantity

                #.......... credit the inventory account ................
                initial_inv_acc_balance=products.inventory_account.balance
                products.inventory_account.balance=initial_inv_acc_balance - per_line_cost_price
            

                # .............debit the cash account ...............
                initial_cash_acc_balance=products.expense_account.balance
                products.expense_account.balance=initial_cash_acc_balance + per_line_selling_price
                products.save()

                # ....... debit the inventory account ..........
                inv_acc=AllifmaalChartOfAccountsModel.objects.get(pk=inventory_acc_id)
                initial_inv_bal=inv_acc.balance
                inv_acc.balance=initial_inv_bal-per_line_cost_price
                inv_acc.save()

                # ....... debit the cash account ..........
                cash_acc=AllifmaalChartOfAccountsModel.objects.get(pk=expense_acc_id)
                initial_cash_bal=cash_acc.balance
                cash_acc.balance=initial_cash_bal + per_line_selling_price
                #cash_acc.save()

                # ....... record the revenue in the income account ..........
                income_acc=AllifmaalChartOfAccountsModel.objects.get(pk=income_acc_id)
                initial_income_bal=income_acc.balance
                income_acc.balance=initial_income_bal + per_line_selling_price
                income_acc.save()

                # ....... record the Cost of goods sold ..........
                cost_goods_sold_acc_exist=AllifmaalChartOfAccountsModel.objects.filter(description="COGS").first()
                if cost_goods_sold_acc_exist:

                    cost_goods_sold_acc=AllifmaalChartOfAccountsModel.objects.filter(description="COGS").first()
                    initial_cost_of_goods_sold_balance=cost_goods_sold_acc.balance
                    cost_goods_sold_acc.balance=initial_cost_of_goods_sold_balance+per_line_cost
                    cost_goods_sold_acc.save()

                

            #increase customer turnover
            mycustomer=AllifmaalCustomersModel.objects.get(pk=customer_id)
            initial_customer_acc_turnover=mycustomer.turnover
            mycustomer.turnover=initial_customer_acc_turnover+inv_total
            initial_customer_acc_balance=mycustomer.balance
            mycustomer.balance=initial_customer_acc_balance+inv_total
            mycustomer.save()

            # ......... credit the equity account .........
            equity_acc=AllifmaalChartOfAccountsModel.objects.get(description="Equity")
            initial_equity_account_balance=equity_acc.balance
            equity_acc.balance=initial_equity_account_balance + profit_or_lost
            #equity_acc.save()

            ######## change invoice status
            qaanshegto.posting_inv_status="posted"
            qaanshegto.save()

        # ....... record the gross profit ..........
            gross_profit_acc_exist=AllifmaalChartOfAccountsModel.objects.filter(description="Gross Profit").first()
            if gross_profit_acc_exist:

                profit_and_loss_acc=AllifmaalChartOfAccountsModel.objects.filter(description="Gross Profit").first()
                initial_profit_and_loss_balance=profit_and_loss_acc.balance
                profit_and_loss_acc.balance=initial_profit_and_loss_balance+profit_or_lost
                profit_and_loss_acc.save()
                
            else:
                pass

        else:
            for item in inv_items:

                invo_quantity=item.quantity # this gives the quantities in the invoice
                
                invoice_item_id=item.description.id#this gives the IDs of the invoice item in the main AllifmaalStocksModel database.
                
                products=AllifmaalStocksModel.objects.get(pk=invoice_item_id)
                weighted_unit_price=products.unitPrice # this gives the item selling price
                per_line_selling_price=weighted_unit_price*invo_quantity
                initial_item_quantity=products.quantity
                products.quantity=initial_item_quantity-invo_quantity


                #.......... credit the inventory account ................
                initial_inv_acc_balance=products.inventory_account.balance
                products.inventory_account.balance=initial_inv_acc_balance - per_line_selling_price
                products.save()

                
                # ....... debit the inventory account ..........
                weighted_unit_cost=products.unitcost
                per_line_cost_price=weighted_unit_cost*invo_quantity
                inventory_acc_id=item.description.inventory_account.id
                inv_acc=AllifmaalChartOfAccountsModel.objects.get(pk=inventory_acc_id)
                initial_inv_bal=inv_acc.balance
                inv_acc.balance=initial_inv_bal-per_line_cost_price
                inv_acc.save()

                # ....... record the revenue in the income account ..........
                income_acc_id=item.description.income_account.id
                income_acc=AllifmaalChartOfAccountsModel.objects.get(pk=income_acc_id)
                initial_income_bal=income_acc.balance
                income_acc.balance=initial_income_bal + per_line_selling_price
                income_acc.save()


                # .............credit the customer account account ...............

            mycustomer=AllifmaalCustomersModel.objects.get(pk=customer_id)
            initial_customer_acc_balance=mycustomer.balance
            mycustomer.balance=initial_customer_acc_balance+inv_total

            initial_customer_acc_turnover=mycustomer.turnover
            mycustomer.turnover=initial_customer_acc_turnover+inv_total

            mycustomer.save()
        

            #.......... credit the equity account
            equity_acc=AllifmaalChartOfAccountsModel.objects.get(description="Equity")
            initial_equity_account_balance=equity_acc.balance
            equity_acc.balance=initial_equity_account_balance+ profit_or_lost
            equity_acc.save()

            ######## change invoice status
            qaanshegto.posting_inv_status="posted"
            qaanshegto.save()
    else:
        return HttpResponse("Please fill all the details before posting the invoice.")
        #client_detail, created = AllifPostedInvoicesModel.objects.get_or_create(customer=mycustomer,invoice_number=,invoice_total=)

    return redirect('allifmaalapp:add_allifmaal_invoice_items',pk=myinvid)

 
def allifpostedinvoices(request):
    title="Posted Invoices "
    #posted_invoices=AllifPostedInvoicesModel.objects.filter(posting_inv_status="posted")
    posted_invoices=AllifmaalInvoicesModel.objects.filter(posting_inv_status="posted")
    posted_invoices_count=AllifmaalInvoicesModel.objects.filter(posting_inv_status="posted").count()
    last_invoices=AllifmaalInvoicesModel.objects.filter(posting_inv_status="posted").order_by('-invoice_total')[:10]
    context={
        "posted_invoices":posted_invoices,
        "title":title,
        "last_invoices":last_invoices,
        "posted_invoices_count":posted_invoices_count,

    }
    return render(request,'allifmaalapp/invoices/posted-invoices.html',context)

def allifmaal_invoice_to_pdf(request,pk):
    system_user=request.user
    invoice_details=get_object_or_404(AllifmaalInvoicesModel,id=pk)
    title="Invoice "+str(invoice_details)
    try:
        inv_number= AllifmaalInvoicesModel.objects.get(id=pk)
    except:
        messages.error(request, 'Something went wrong')

    invoiceItems = AllifmaalInvoiceItemsModel.objects.filter(allifinvitemconnector=inv_number)

    invoiceTotal = 0
    if len(invoiceItems) > 0:
       for x in invoiceItems:
            y = (0 or x.quantity) *(0 or x.unit_price)
            invoiceTotal += y

    template_path = 'allifmaalapp/invoices/allifmaal-inv-to-pdf.html'
    companyDetails=AllifmaalDetailsModel.objects.all()
    scope=AllifmaalScopeModel.objects.all()
    
    context = {
    'invoice_details':invoice_details,
   "invoiceItems":invoiceItems,
   "companyDetails":companyDetails,
   "invoiceTotal":invoiceTotal,
   "scope":scope,
   "system_user":system_user,
   "title":title,
   
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Allifmaal-invoice.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    try:
        pisa_status = pisa.CreatePDF(
       html, dest=response)
    except:
        return HttpResponse("Something went wrong!")
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response

########################################################## EXPENSES ############################################3
def allifmaalExpenses(request):
    title="Expenses"
    coa_less_than_queryset=AllifmaalChartOfAccountsModel.objects.filter(code__lte=19999)
    myland=AllifmaalChartOfAccountsModel.objects.filter(description="Land").first()
    default_cash_accs_2=AllifmaalChartOfAccountsModel.objects.filter(code__lte=19999)[3]

    default_cash_accs=AllifmaalChartOfAccountsModel.objects.filter(description="Cash").first()
    my_expense_default=AllifmaalChartOfAccountsModel.objects.filter(code__gte=49999).first()
    form=AddAllifmaalExpensesForm(initial={'pay_from':default_cash_accs,'pay_to':my_expense_default})
  
    accs=AllifmaalGeneralLedgersModel.objects.all()
    chartaccs=AllifmaalChartOfAccountsModel.objects.all()
    expenses=AllifmaalExpensesModel.objects.all()
    gl=AllifmaalGeneralLedgersModel.objects.first()#this gives the first item in the list
    first_item_in_list=accs[0]

    if request.method =="POST":
        supplier=int(request.POST.get('supplier'))
        modeOfPayment=request.POST.get('mode')
        spent_amount=request.POST.get('amount')
        pay_from_account=request.POST.get('pay_from')
        supplier_account=request.POST.get('supplier')
        pay_to_account=request.POST.get('pay_to')
        form=AddAllifmaalExpensesForm(request.POST or None,request.FILES)
       
        
        if form.is_valid():
            form.save()
            form=AddAllifmaalExpensesForm(initial={'pay_from':default_cash_accs,'pay_to':my_expense_default})
    
        ############# using for the chart of accounts ###########3
        if modeOfPayment=="Cash":
            if pay_from_account and pay_to_account:
                spent_amount=Decimal(request.POST.get('amount'))#this gives the amount in the field
                pay_from_acc=request.POST.get('pay_from')
                pay_to_acc=request.POST.get('pay_to')
                
                pay_from_acc_queryset=AllifmaalChartOfAccountsModel.objects.get(id=pay_from_acc)
                pay_from_acc_initial_balance=pay_from_acc_queryset.balance
                pay_from_acc_queryset.balance=pay_from_acc_initial_balance-spent_amount
                pay_from_acc_queryset.save()

                pay_to_acc_queryset=AllifmaalChartOfAccountsModel.objects.get(id=pay_to_acc)
                exp_acc_initial_balance=pay_to_acc_queryset.balance
                pay_to_acc_queryset.balance=exp_acc_initial_balance+spent_amount
                pay_to_acc_queryset.save()

                mysupplier=AllifmaalSuppliersModel.objects.get(pk=supplier)
                initial_supp_turnover_balance=mysupplier.turnover
                mysupplier.turnover=initial_supp_turnover_balance+spent_amount
                

                initial_supp_balance=mysupplier.balance
                if initial_supp_balance>0:

                    mysupplier.balance=initial_supp_balance-spent_amount

                

                else:


                    chartaccs_values_list=AllifmaalChartOfAccountsModel.objects.all().values_list('description', flat=True)
                    if "Equity" in chartaccs_values_list:
                        myequityacc=AllifmaalChartOfAccountsModel.objects.get(description="Equity")
                        initial_equity_bal=myequityacc.balance
                        myequityacc.balance=initial_equity_bal-spent_amount
                        myequityacc.save()
                    

                    else:
                        pass
                mysupplier.save()

        else:
            supp=AllifmaalSuppliersModel.objects.get(pk=supplier)
            initial_supp_balance=Decimal(supp.balance)
            initial_sup_turnover_balance=Decimal(supp.turnover)
            supp.balance=initial_supp_balance+Decimal(spent_amount)
            supp.turnover=initial_sup_turnover_balance+Decimal(spent_amount)
            supp.save()

            pay_to_acc=request.POST.get('pay_to')
            pay_to_acc_queryset=AllifmaalChartOfAccountsModel.objects.get(id=pay_to_acc)
            exp_acc_initial_balance=pay_to_acc_queryset.balance
            pay_to_acc_queryset.balance=exp_acc_initial_balance+Decimal(spent_amount)
            pay_to_acc_queryset.save()

            chartaccs_values_list=AllifmaalChartOfAccountsModel.objects.all().values_list('description', flat=True)
            if "Equity" in chartaccs_values_list:
                myequityacc=AllifmaalChartOfAccountsModel.objects.get(description="Equity")
                initial_equity_bal=myequityacc.balance
                myequityacc.balance=initial_equity_bal-Decimal(spent_amount)
                myequityacc.save()
            else:
                pass
                

           
        
    exp=0
    total_exp=0
    for expense in expenses:
        exp+=expense.amount
    total_exp=exp
    mycontext={
        
        "form":form,
        "expenses":expenses,
        "total_exp":total_exp,
        "title":title,
    }
    return render (request,'allifmaalapp/expenses/allifmaalexpenses.html',mycontext)

def deleteAllifmaalExpense(request,pk):
    AllifmaalExpensesModel.objects.get(id=pk).delete()
    return redirect('allifmaalapp:allifmaalExpenses')


################################## TASKS ###########################################


def allifmaal_Tasks(request):
    title="To do list"
   
    form =AddAllifmaalTasksForm(request.POST or None)
   
    #tasks=TasksModel.objects.order_by('complete','dueDate')
    tasks=AllifmaalTasksModel.objects.order_by('dueDate').filter(status="incomplete")
    completed_tasks=AllifmaalTasksModel.objects.filter(status="complete")
    

    if form.is_valid():
        form.save()
        messages.success(request, 'Task added successfully')
        form=AddAllifmaalTasksForm()#this clears out the form after adding the product

    context = {
        "form":form,
        "tasks":tasks,
        "title":title,
        "completed_tasks":completed_tasks,
        
        
    }

    return render(request,'allifmaalapp/tasks/allifmaaltasks.html',context)

def markAllifmaalTaskComplete(request,pk):
    mark_complete=AllifmaalTasksModel.objects.get(id=pk)
    if mark_complete.status=="incomplete":
        mark_complete.status="complete"
        mark_complete.save()
       
    else:
        mark_complete.status="incomplete"
        mark_complete.save()
      
    return redirect('allifmaalapp:allifmaal_Tasks')
def allifmaalCompletedTasksList(request):
    title="Completed Tasks"
   
    #tasks=TasksModel.objects.order_by('complete','dueDate')
    tasks=AllifmaalTasksModel.objects.filter(status="incomplete")
    completed_tasks=AllifmaalTasksModel.objects.filter(status="complete")

    context = {
        
        "tasks":tasks,
        "title":title,
        "completed_tasks":completed_tasks,
        
        
    }

    return render(request,'allifmaalapp/tasks/allifmaal-completed-tasks.html',context)


#@allowed_users(allowed_roles=['admin'])  
def delete_allifmaal_task(request,pk):
    try:
        AllifmaalTasksModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('todoapp:to-do-list ')

    return redirect('allifmaalapp:allifmaal_Tasks')


def update_allifmaal_tasks(request, pk):
    update_task= AllifmaalTasksModel.objects.get(id=pk)
    form = AddAllifmaalTasksForm(instance=  update_task)
   
    if request.method == 'POST':
        form = AddAllifmaalTasksForm(request.POST, instance=  update_task)
        if form.is_valid():
            form.save()
          
            return redirect('allifmaalapp:allifmaal_Tasks')
    context = {
		'form':form,
        " update_task": update_task,
    }
    return render(request, 'todoapp/toDoList.html', context)#this is the main page rendered first

####################### ACCOUNTING MODULES ##################3
def allifmaalGeneralLedgers(request):
    title="Allifmaal General Ledgers"
    generalledgers=AllifmaalGeneralLedgersModel.objects.all()
    
   
    try:
        form=AddAllifmaalGeneralLedgerAccountForm()
        
        if request.method == 'POST':
            form = AddAllifmaalGeneralLedgerAccountForm(request.POST)
            try:
                if form.is_valid():
                    form.save()
                
                    return redirect('allifmaalapp:allifmaalGeneralLedgers')
                else:
                    return HttpResponse("There is a problem! Ensure description is not already existing")
            except:
                return HttpResponse("There is a problem! Ensure description is not already existing")
    except:
        return HttpResponse("There is a problem! Ensure description is not already existing")
        #messages.error()
   

    context={
        "generalledgers":generalledgers,
        "form":form,
        "title":title,
       
       

    }
    return render(request,'allifmaalapp/accounts/allifmaal_general_ledgers.html',context)

def AllifmaalGeneralLedgerDetails(request, pk):
    try:
        title="Allifmaal General Ledger Account Details"
        supplier_liabilities=AllifmaalSuppliersModel.objects.filter(balance__gte=1)
        gl_details= AllifmaalGeneralLedgersModel.objects.get(id=pk)
        related_accs=AllifmaalChartOfAccountsModel.objects.filter(category=gl_details)
        acc_balance=0
        for items in related_accs:
            acc_balance+=items.balance
            print(items)
        acc_total=acc_balance
        gl_details.balance=acc_total
        gl_details.save()

    except:
        return HttpResponse("There was a problem !")
    context = {
        "gl_details":gl_details,
        "related_accs":related_accs,
        "title":title,
        "acc_total":acc_total,
		
    }
    return render(request,'allifmaalapp/accounts/allifmal_gl_details.html',context)


def updateAllifmaalGeneralLedger(request, pk):
    update_gl= AllifmaalGeneralLedgersModel.objects.get(id=pk)
    form = AddAllifmaalGeneralLedgerAccountForm(instance=  update_gl)
   
    if request.method == 'POST':
        form = AddAllifmaalGeneralLedgerAccountForm(request.POST, instance=  update_gl)
        if form.is_valid():
            form.save()
          
            return redirect('allifmaalapp:allifmaalGeneralLedgers')
    context = {
		'form':form,
        " update_gl": update_gl,
    }
    return render(request,'allifmaalapp/accounts/allifmaal_general_ledgers.html',context)

def deleteAllifmaalGeneralLedgerAccount(request,pk):
    AllifmaalGeneralLedgersModel.objects.get(id=pk).delete()
    return redirect('allifmaalapp:allifmaalGeneralLedgers')


###################### chart of accounts  ######################3

def allifmaal_add_show_chart_of_account(request):
    title="Allifmaal Chart of accounts"
    supplier_liabilities=AllifmaalSuppliersModel.objects.filter(balance__gte=1)
    customer_debts=AllifmaalCustomersModel.objects.filter(balance__gte=1)
    customer_liab=AllifmaalCustomersModel.objects.filter(balance__lte=1)
    
    chart_of_accounts1=AllifmaalChartOfAccountsModel.objects.order_by("code").values()
    chart_of_accounts=AllifmaalChartOfAccountsModel.objects.all().order_by("code")
    coa_less_than_queryset=AllifmaalChartOfAccountsModel.objects.filter(code__lte=19999)
    
    coa_greater_than_queryset=AllifmaalChartOfAccountsModel.objects.filter(code__gte=19999)
    coa_greater_than_and_less_than_queryset=AllifmaalChartOfAccountsModel.objects.filter(code__gte=20000,code__lte=27000)

    assets=AllifmaalChartOfAccountsModel.objects.filter(code__lte=19999)
    liabilities=AllifmaalChartOfAccountsModel.objects.filter(code__gte=19999,code__lte=29999)
    equity=AllifmaalChartOfAccountsModel.objects.filter(code__gte=30000,code__lte=39999)

    
    #debts
    debts=0
    for debt in customer_debts:
        debts+=debt.balance
    total_debts=debts
    #supplier balances
    supp_bal=0
    for bal in supplier_liabilities:
        supp_bal+=bal.balance
    suppliers_balances=supp_bal

    # ASSETS
    total_assets_value=0
    for item in assets:
       
        
        total_assets_value+=item.balance
    Allifmaal_Assets_Value=total_assets_value
    

    #LIABILITIES
    total_liabilities_value=0
    for item in liabilities:
       
        total_liabilities_value+=item.balance
    Allifmaal_Liabilities_Value=total_liabilities_value
    #Customer LIABILITIES
    total_customer_advanced_payment_value=0
    for item in customer_liab:
       
        total_customer_advanced_payment_value+=(-1)*(item.balance)
    Allifmaal_Customers_Advanced_Payments=total_customer_advanced_payment_value
    
    
    #EQUITY
    total_equity_value=0
    for item in equity:
       
        total_equity_value+=item.balance
    Allifmaal_Equities_Value=total_equity_value
        
    
    form=AddAllifmaalChartOfAccountForm(request.POST, request.FILES)
    if request.method == 'POST':
        form=AddAllifmaalChartOfAccountForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect('allifmaalapp:allifmaal_add_show_chart_of_account')
    else:
        form=AddAllifmaalChartOfAccountForm()

    
    ourassets=total_debts+Allifmaal_Assets_Value
    liabandequ=Allifmaal_Equities_Value+Allifmaal_Liabilities_Value+suppliers_balances+Allifmaal_Customers_Advanced_Payments
    context={
        "chart_of_accounts":chart_of_accounts,
        "form":form,
        "title":title,
        "Allifmaal_Assets_Value":Allifmaal_Assets_Value,
        "Allifmaal_Liabilities_Value":Allifmaal_Liabilities_Value,
        "Allifmaal_Equities_Value":Allifmaal_Equities_Value,
        "suppliers_balances":suppliers_balances,
        "total_debts":total_debts,
        "ourassets":ourassets,
        "liabandequ":liabandequ,
        "Allifmaal_Customers_Advanced_Payments":Allifmaal_Customers_Advanced_Payments,
        
    }
    return render(request,'allifmaalapp/accounts/allifmaal-chart-of-accounts.html',context)

def synchacc(request):

    suplier_tot_liab=AllifmaalSuppliersModel.objects.filter(balance__gte=1).aggregate(Sum('balance'))['balance__sum']
    sup_bal=AllifmaalChartOfAccountsModel.objects.filter(description="Supplier Balances")
    if sup_bal:
        sup_balan=AllifmaalChartOfAccountsModel.objects.get(description="Supplier Balances")
        
        sup_balan.balance=suplier_tot_liab
        sup_balan.save()

    else:
        pass

    customer_adv_liab=AllifmaalCustomersModel.objects.filter(balance__lte=1).aggregate(Sum('balance'))['balance__sum']
    
    suplier_tot_liab=AllifmaalSuppliersModel.objects.filter(balance__gte=1).aggregate(Sum('balance'))['balance__sum']
    cust_adv=AllifmaalChartOfAccountsModel.objects.filter(description="Customer Advances")
    if cust_adv:
        cust_adv_pay=AllifmaalChartOfAccountsModel.objects.get(description="Customer Advances")
        
        cust_adv_pay.balance=customer_adv_liab
        cust_adv_pay.save()

    else:
        pass

    cust_tot_debt=AllifmaalCustomersModel.objects.filter(balance__gte=1).aggregate(Sum('balance'))['balance__sum']
    acc_receiv=AllifmaalChartOfAccountsModel.objects.filter(description="Accounts Receivable")
    if acc_receiv:
        accrec=AllifmaalChartOfAccountsModel.objects.get(description="Accounts Receivable")
        
        accrec.balance=cust_tot_debt
        accrec.save()

    else:
        pass
    return redirect('allifmaalapp:allifmaal_add_show_chart_of_account')

   

def allifmaal_delete_chart_of_account(request,pk):
    AllifmaalChartOfAccountsModel.objects.get(id=pk).delete()
    return redirect('allifmaalapp:allifmaal_add_show_chart_of_account')

def edit_chart_of_account(request, pk):
    update_account= AllifmaalChartOfAccountsModel.objects.get(id=pk)
    form = AddAllifmaalChartOfAccountForm(instance= update_account)
   
    if request.method == 'POST':
        form = AddAllifmaalChartOfAccountForm(request.POST, instance=update_account)
        if form.is_valid():
            form.save()
          
            return redirect('allifmaalapp:allifmaal_add_show_chart_of_account')
    context = {
		'form':form,
        "update_account": update_account,
    }
    return render(request,'allifmaalapp/accounts/allifmaal-chart-of-accounts.html',context)

def show_account_of_account_details(request,pk):
    title="Chart Of Account Details"
    exprelated=AllifmaalExpensesModel.objects.all()
    try:
        account_details=AllifmaalChartOfAccountsModel.objects.get(id=pk)
        
    except:
        messages.error(request, 'Something went wrong')
        return redirect('allifmaalapp:allifmaal_add_show_chart_of_account')
    payments=AllifmaalCustomerPaymentsModel.objects.all().filter(account=account_details)
    expenses_from_acc=AllifmaalExpensesModel.objects.all().filter(pay_from=account_details)
    expenses_to_acc=AllifmaalExpensesModel.objects.all().filter(pay_to=account_details)
    #assets=AllifmaalAssetsModel.objects.all().filter(asset_account=account_details)
    assets=AllifmaalAssetsModel.objects.all().filter(cost_account=account_details)
    asset=AllifmaalAssetsModel.objects.all().filter(asset_account=account_details)
    acc_receivables=AllifmaalCustomersModel.objects.filter(balance__gt=1)
    #asset_inv=AllifmaalPurchaseOrdersModel.objects.all().filter(asset_account=account_details)
    cash_posted_POs=AllifmaalPurchaseOrdersModel.objects.all().filter(payment_terms="Cash", posting_po_status="posted",total__gt=0)
    context={
        "account_details":account_details,
        "title":title,
        "exprelated":exprelated,
        "payments":payments,
        "expenses_from_acc":expenses_from_acc,
        "expenses_to_acc":expenses_to_acc,
        "assets":assets,
        "asset":asset,
        "cash_posted_POs":cash_posted_POs,
        "acc_receivables":acc_receivables,
        

    }
    return render(request,'allifmaalapp/accounts/account-details.html',context)


###################### Inventory #####################################
def allifmaal_inventory_category(request):
    title="Allifmaal Stock Category"
    categories=AllifmaalStockCategoriesModel.objects.all()

    form=AddAllifmaalStockCategoryForm()
   
    if request.method == 'POST':
        form=AddAllifmaalStockCategoryForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock category added successfully')
            form=AddAllifmaalStockCategoryForm()
    else:
       form.non_field_errors
   

    context = {
        "title":title,
        "form":form,
        "categories":categories,
       
      
    }
   

    return render(request,'allifmaalapp/inventory/inventory_categories.html',context)

def deleteStockCategory(request,pk): 
    try:
        AllifmaalStockCategoriesModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('allifmaalapp:allifmaal_inventory_category')

    return redirect('allifmaalapp:allifmaal_inventory_category')

    
#@allowed_users(allowed_roles=['admin'])
def allifmaalUpdateStockCategoryDetails(request, pk):
    title="Update stock category Details"
    updateStockItem=AllifmaalStockCategoriesModel.objects.get(id=pk)
    form =AddAllifmaalStockCategoryForm(instance= updateStockItem)#insert the content of the table stored in the selected id in the update form
    #we could have used the add customer form but the validation will refuse us to update since fields may exist
    if request.method == 'POST':
        form =AddAllifmaalStockCategoryForm(request.POST, instance= updateStockItem)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock item updated successfully')
            return redirect('allifmaalapp:allifmaal_inventory_category')
    context = {
		'form':form,
        "updateStockItem":updateStockItem,
        "title":title,
    }
    return render(request,'allifmaalapp/inventory/inventory_categories.html',context)

def allifmaalStockCategoryDetails(request,pk):
    title="Category details"
    cat =AllifmaalStockCategoriesModel.objects.get(id=pk)
    category_items= AllifmaalStocksModel.objects.filter(category=cat)#this line helps to
    related_inventory_quantity_sum=AllifmaalStockCategoriesModel.objects.filter(description=cat).aggregate(Sum('catinvtconrlnm__quantity'))#
    no_of_items_in_cat=AllifmaalStockCategoriesModel.objects.filter(description=cat).aggregate(Count('catinvtconrlnm__description'))
    print(no_of_items_in_cat)
   
    context={"cat":cat,"title":title,
    "category_items":category_items,}
    return render(request,'allifmaalapp/inventory/allifstockcategorydetails.html',context)


def allifmaal_inventory(request):
    title="Allifmaal Stock"
    stocks2=AllifmaalStocksModel.objects.all().order_by('-category').annotate(Sum('quantity'))
    stocks=AllifmaalStocksModel.objects.all().order_by('-category').annotate(Sum('quantity'))
    number_of_categories= AllifmaalStocksModel.objects.annotate(Count('category'))
    test1=AllifmaalStockCategoriesModel.objects.first()
    
    #test2=AllifmaalStockCategoriesModel.objects.annotate(Min('AllifmaalStocksModel__quantity'))
    #categories = AllifmaalStockCategoriesModel.objects.prefetch_related('allifmaalStocksModel_set').all()
    
    

    sales=AllifmaalChartOfAccountsModel.objects.all().filter(description="Sales").first()
    inventory=AllifmaalChartOfAccountsModel.objects.all().filter(description="Inventory").first()
    assets_queryset=AllifmaalChartOfAccountsModel.objects.filter(code__lte=19999).first()
    form=AddAllifmaalStockForm(initial={'expense_account':assets_queryset,'inventory_account':inventory,'income_account':sales})
   
    if request.method == 'POST':
        form=AddAllifmaalStockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock added successfully')
            form=AddAllifmaalStockForm()
    else:
       form.non_field_errors
    

    ######################## statics start ###########################
    stock_avg_qty=AllifmaalStocksModel.objects.aggregate(Avg('quantity'))
    sum_of_stock_quantities=AllifmaalStocksModel.objects.aggregate(Sum('quantity'))
    average_quantities_greater_than=AllifmaalStocksModel.objects.filter(quantity__gte=100).aggregate(Avg('quantity'))
    related_inventory_quantity_sum=AllifmaalStockCategoriesModel.objects.aggregate(Sum('catinvtconrlnm__quantity'))#double underscore and relatd name

   
    gives_dictionary=AllifmaalStocksModel.objects.values()
    gives_dictionary_of_quantities=AllifmaalStocksModel.objects.values('quantity')

    #starting with lowest, below gives each quantity value and how many times it occured
    quantity_value_and_frequency=AllifmaalStocksModel.objects.values('quantity').annotate(Count('quantity'))
    test1=AllifmaalStocksModel.objects.values('category').annotate(Count('quantity'))
    cat_and_sum_quantities=AllifmaalStocksModel.objects.values('category').annotate(wadartuwaa=Sum('quantity'))
    testing=AllifmaalStocksModel.objects.values('category').annotate(Sum('quantity')).order_by("-quantity")
    mycat=AllifmaalStocksModel.objects.values('category')
    print(cat_and_sum_quantities)
    
    
    
    

    ###################### end ######################
   

    context = {
        "title":title,
        "form":form,
        "stocks":stocks,
        "cat_and_sum_quantities":cat_and_sum_quantities,
       
      
    }
   

    return render(request,'allifmaalapp/inventory/inventory.html',context)



#this view is for showing the full details of a stock item/line
def allifmaalProductFullDetails(request,pk):
    title="Product details"
    product =AllifmaalStocksModel.objects.get(id=pk)
    context={"product":product,"title":title,}
    return render(request,'allifmaalapp/inventory/allifproductdetails.html',context)


def deleteStockItem(request,pk):
    try:
        AllifmaalStocksModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('allifmaalapp:allifmaal_inventory')

    return redirect('allifmaalapp:allifmaal_inventory')

    
#@allowed_users(allowed_roles=['admin'])
def allifmaalUpdateStockDetails(request, pk):
    title="Update Item Details"
    updateStockItem=AllifmaalStocksModel.objects.get(id=pk)
    form =AddAllifmaalStockForm(instance= updateStockItem)#insert the content of the table stored in the selected id in the update form
    #we could have used the add customer form but the validation will refuse us to update since fields may exist
    if request.method == 'POST':
        form =AddAllifmaalStockForm(request.POST, instance= updateStockItem)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock item updated successfully')
            return redirect('allifmaalapp:allifmaal_inventory')
    context = {
		'form':form,
        "updateStockItem":updateStockItem,
        "title":title,
    }
    return render(request,'allifmaalapp/inventory/inventory.html',context)


############ stock taking ##############
def physicalInventory(request):
    title="Physical Inventory"
    stocks=AllifmaalStocksModel.objects.all().filter(quantity__gte=1)

    total_cost=0
    total_value=0
    for items in stocks:
        total_cost+=items.unitcost*items.quantity
        total_value+=items.unitPrice*items.quantity
    total_cost_of_available_stock=total_cost
    total_value_of_available_stock=total_value

        

    context={
        "stocks":stocks,
        "total_cost_of_available_stock":total_cost_of_available_stock,
        "total_value_of_available_stock":total_value_of_available_stock,
        "title":title,

    }
    return render(request,'allifmaalapp/inventory/physicalinventory.html',context)



############################# STOCK PURCHASE ORDERS #####################################

def AllifmaalPurchaseOrders(request):
    title="Purchase Orders"
    mypos=AllifmaalPurchaseOrdersModel.objects.all()
    context={
        "mypos":mypos,
        "title":title,

    }
    return render(request,'allifmaalapp/inventory/allifmaalPurchaseOrders.html',context)

def Allifmaal_create_new_purchase_order(request):

    last_po = AllifmaalPurchaseOrdersModel.objects.all().order_by('id').last()
    last_obj=AllifmaalPurchaseOrdersModel.objects.last()
    if last_obj:
        
        last_obj_id=last_obj.id
        last_obj_incremented=last_obj_id+1
   
    #purchaseNumber= 'LPO/AMEL-'+str(uuid4()).split('-')[1]
        purchaseNumber= 'AM/PO/'+str(last_obj_incremented)
        print(purchaseNumber)
    else:
        
       purchaseNumber= 'LPO/AMEL/'+str(uuid4()).split('-')[1]
        #purchaseNumber= 'LPO/AMEL-'+str(uuid4()).split('-')[1]+'/'+str("Reset")

    newPurchaseOrder= AllifmaalPurchaseOrdersModel.objects.create(po_number=purchaseNumber)
    newPurchaseOrder.save()
    return redirect('allifmaalapp:AllifmaalPurchaseOrders')

def AllifmaalDeletePO(request,pk):
    AllifmaalPurchaseOrdersModel.objects.get(id=pk).delete()
    return redirect('allifmaalapp:AllifmaalPurchaseOrders')


def Allifmaal_Add_PO_Details(request,pk):
    title="Add Purchase Order Details"
    po_details=AllifmaalPurchaseOrdersModel.objects.filter(id=pk)
    try:
        my_po_id=AllifmaalPurchaseOrdersModel.objects.get(id=pk)
        po_terms=my_po_id.payment_terms
        
    except:
        messages.error(request, 'Something went wrong!')
        return redirect("allifmaalapp:Allifmaal_Add_PO_items",id=my_po_id)

    po_Items = AllifmaalPurchaseOrderItemsModel.objects.filter(po_item_con=my_po_id)#this line helps to
    #show items that belong to that particular invoice in that particular invoice
    inv_id= get_object_or_404(AllifmaalPurchaseOrdersModel, id=pk)#this helps to fill that select field and invoice fields and content
    misc_costs=AllifmaalPurchaseOrderMiscCostsModel.objects.filter(po_misc_cost_con=my_po_id)

    misc_cost_items=0
    for cost in misc_costs:
        misc_cost_items+=cost.amount
    total_misc_cost=misc_cost_items
    my_po_id.shipping=total_misc_cost
    my_po_id.save()
    form=AddAllifmaalPurchaseOrderDetailsForm(instance=my_po_id)
    if request.method == 'POST':
        #add_shipment_items_form=AddShippmentItemsForm(request.POST)
        form=AddAllifmaalPurchaseOrderDetailsForm(request.POST,request.FILES,instance=my_po_id)
        if form.is_valid():
            form.save()
           
           
            return redirect('allifmaalapp:AllifmaalPurchaseOrders')

        
    context={
        
        "form":form,
        "po_Items":po_Items,
        "po_details":po_details,
        "title":title,
        "my_po_id": my_po_id,
        
        

    }
    return render(request,'allifmaalapp/inventory/addPurchaseOrdersDetails.html',context)


def Allifmaal_Add_PO_items(request,pk):
    title="Add items to the purchase order"
    Allif_PO=AllifmaalPurchaseOrdersModel.objects.get(id=pk)#very important to get id to go to particular shipment
    form=AddAllifmaalPurchaseOrderItemsForm()
    add_inv= get_object_or_404(AllifmaalPurchaseOrdersModel, id=pk)

    po_Items = AllifmaalPurchaseOrderItemsModel.objects.filter(po_item_con=Allif_PO)#this line helps to
    
    add_item= None
    if request.method == 'POST':
        form=AddAllifmaalPurchaseOrderItemsForm(request.POST)
        if form.is_valid():
            add_item= form.save(commit=False)
            add_item.po_item_con=add_inv
            add_item.save()
           # return HttpResponse(post)
            return redirect('allifmaalapp:Allifmaal_Add_PO_items',pk=pk)#just redirection page
    po_total=0
    for items in po_Items:
        po_total+=items.quantity*items.unitcost
    po_new_amount=po_total
    Allif_PO.total=po_new_amount
    Allif_PO.save()

    context={
   
            "form":form,
            "title":title,
            "Allif_PO":Allif_PO,
            "add_inv":add_inv,
            "po_Items":po_Items,
             
    }
    return render(request,'allifmaalapp/inventory/add_po_items.html',context)
def delete_allifmaal_po_item(request,pk):
    AllifmaalPurchaseOrderItemsModel.objects.get(id=pk).delete()
    return redirect('allifmaalapp:AllifmaalPurchaseOrders')

def Allifmaal_Add_PO_Misc_Cost(request,pk):
    title="Add misc. costs to the purchase order"
    Allif_PO=AllifmaalPurchaseOrdersModel.objects.get(id=pk)#very important to get id to go to particular shipment
    form=AddAllifmaalPurchaseOrderMiscCostForm()
    add_cost= get_object_or_404(AllifmaalPurchaseOrdersModel, id=pk)

    po_Misc_Costs_Items = AllifmaalPurchaseOrderMiscCostsModel.objects.filter(po_misc_cost_con=Allif_PO)#this line helps to
    
    add_item= None
    if request.method == 'POST':
        form=AddAllifmaalPurchaseOrderMiscCostForm(request.POST)
        if form.is_valid():
            add_item= form.save(commit=False)
            add_item.po_misc_cost_con=add_cost
            add_item.save()
           # return HttpResponse(post)
            return redirect('allifmaalapp:Allifmaal_Add_PO_Misc_Cost',pk=pk)#just redirection page

    context={
   
            "form":form,
            "title":title,
            "Allif_PO":Allif_PO,
            "add_cost":add_cost,
            "po_Misc_Costs_Items":po_Misc_Costs_Items,
             
    }
    return render(request,'allifmaalapp/inventory/add_po_misc_costs.html',context)

def delete_allifmaal_po_misc_cost(request,pk):
    AllifmaalPurchaseOrderMiscCostsModel.objects.get(id=pk).delete()
    return redirect('allifmaalapp:AllifmaalPurchaseOrders')



def AllifmaalPOPosting(request,pk):
    
    try:
        myPO=AllifmaalPurchaseOrdersModel.objects.get(id=pk)
        purch_ord_terms=myPO.payment_terms#this gives the selected PO terms
        po_amount=myPO.total
        applied_uplift=myPO.uplift
        po_supplier=myPO.supplier
        supplier_id=po_supplier.id
        
    except:
        return HttpResponse("Something went wrong... have you filled the PO details ?")

    
    ################# ...start of  misc costs...credit the service provider account....###################
    misc_costs=AllifmaalPurchaseOrderMiscCostsModel.objects.filter(po_misc_cost_con=myPO)
    total_misc_cost=0
    for cost in misc_costs:
        spent_amount=cost.amount
        total_misc_cost+=cost.amount
        misc_cost_supplier_id=int(cost.supplier.id)
        misc_cost_supplier=AllifmaalSuppliersModel.objects.get(pk=misc_cost_supplier_id)# The misc cost service supplier
        supplier_acc_balance=misc_cost_supplier.balance
        misc_cost_supplier.balance=supplier_acc_balance+spent_amount
        misc_cost_supplier.save()
   

    ################### end of misc costs ###############
   
    total_incurred_misc_cost=myPO.shipping
    poItems = AllifmaalPurchaseOrderItemsModel.objects.filter(po_item_con=myPO)# this gives the list of items of this PO
    if purch_ord_terms=="Cash":
        if myPO.posting_po_status=="waiting":
            myPO.posting_po_status="posted"
            myPO.save()
        else:
            myPO.posting_po_status="waiting"
            myPO.save()

        for item in poItems:
            item_unit_cost=item.unitcost#this gets the new unit buying price of the individual items from the po
            # apportioned unit cost = ((unit cost)/total_PO_value)*total_misc_cost
            apportioned_misc_unit_cost=(item_unit_cost/po_amount)*total_incurred_misc_cost
            actual_item_unit_cost=apportioned_misc_unit_cost+item_unit_cost

           #we need to calculate the weighted unit cost
            products=AllifmaalStocksModel.objects.get(description=item.items)
            quantity=item.quantity#this gets the quantity of the individual items
            existing_item_unit_quantity=item.items.quantity# this gives the quantities for existing items in the system
            total_inv_quantity=existing_item_unit_quantity+quantity# this gives the sum of existing quantities and those in the po.
            existing_item_unit_cost=item.items.unitcost# this gives the unit cost for existing items in the system
            weighted_new_unit_cost=(existing_item_unit_cost*existing_item_unit_quantity+quantity*actual_item_unit_cost)/Decimal(total_inv_quantity)
            products.unitcost=weighted_new_unit_cost
            products.quantity=total_inv_quantity


            # deal with buying price --- get weighted buying price
            existing_item_unit_buying_price=item.items.buyingPrice
            weighted_new_buying_price=(existing_item_unit_buying_price*existing_item_unit_quantity+quantity*item_unit_cost)/total_inv_quantity
            products.buyingPrice=weighted_new_buying_price

            # .... set the selling price .......
            products.unitPrice=applied_uplift*weighted_new_unit_cost
            products.save()

            #....... debit item inventory account .............
            inventory_acc_id=item.items.inventory_account.id
            inventory_acc=AllifmaalChartOfAccountsModel.objects.get(pk=inventory_acc_id)
            item_initial_inventory_account_balance=inventory_acc.balance
            item_new_inventory_account_balance = item_initial_inventory_account_balance + actual_item_unit_cost*quantity
            inventory_acc.balance=item_new_inventory_account_balance
            inventory_acc.save()

             #icrease the supplier turn over account
            supplier_acc=AllifmaalSuppliersModel.objects.get(pk=supplier_id)
            initial_supplier_turnover=supplier_acc.turnover
            supplier_acc.turnover=initial_supplier_turnover+quantity*item_unit_cost
            supplier_acc.save()

            # __________________________ reduce the cash accpunt __________________________________
            expense_acc_id=item.items.expense_account.id
            exp_acc=AllifmaalChartOfAccountsModel.objects.get(pk=expense_acc_id)
            initial_cash_account_balance=exp_acc.balance
            new_cash_acc_balance = initial_cash_account_balance-item_unit_cost*quantity
            exp_acc.balance=new_cash_acc_balance
            exp_acc.save()

           
        
    else:
        for item in poItems:
            item_unit_cost=item.unitcost#this gets the new unit buying price of the individual items from the po
            apportioned_misc_unit_cost=(item_unit_cost/po_amount)*total_incurred_misc_cost
            actual_item_unit_cost=apportioned_misc_unit_cost+item_unit_cost
            quantity=item.quantity#this gets the quantity of the individual items
            existing_item_unit_quantity=item.items.quantity# this gives the quantities for existing items in the system
            total_inv_quantity=existing_item_unit_quantity+quantity
            #credit the supplier account balance
            supplier_acc=AllifmaalSuppliersModel.objects.get(pk=supplier_id)
            initial_supplier_balance=supplier_acc.balance
            initial_supplier_turnover=supplier_acc.turnover
            supplier_acc.balance=initial_supplier_balance+quantity*item_unit_cost
            supplier_acc.turnover=initial_supplier_turnover+quantity*item_unit_cost
            supplier_acc.save()


            products=AllifmaalStocksModel.objects.get(description=item.items)
            products.quantity=total_inv_quantity
            existing_item_unit_cost=item.items.unitcost#
            weighted_new_unit_cost=(existing_item_unit_cost*existing_item_unit_quantity+quantity*actual_item_unit_cost)/total_inv_quantity
            products.unitcost=weighted_new_unit_cost
            products.quantity=total_inv_quantity

            # deal with buying price --- get weighted buying price
            existing_item_unit_buying_price=item.items.buyingPrice
            weighted_new_buying_price=(existing_item_unit_buying_price*existing_item_unit_quantity+quantity*item_unit_cost)/total_inv_quantity
            products.buyingPrice=weighted_new_buying_price
            # .... set the selling price .......
            products.unitPrice=applied_uplift*weighted_new_unit_cost
            products.save()

            #....... debit item inventory account .............
            inventory_acc_id=item.items.inventory_account.id
            inventory_acc=AllifmaalChartOfAccountsModel.objects.get(pk=inventory_acc_id)
            item_initial_inventory_account_balance=inventory_acc.balance
            item_new_inventory_account_balance = item_initial_inventory_account_balance + actual_item_unit_cost*quantity
            inventory_acc.balance=item_new_inventory_account_balance
            inventory_acc.save()

            accs_payable=AllifmaalChartOfAccountsModel.objects.filter(description="Supplier balances").first()
            if accs_payable:
                payables=AllifmaalChartOfAccountsModel.objects.filter(description="Supplier balances").first()
                initial_liab_balances= payables.balance
                payables.balance=initial_liab_balances+quantity*item_unit_cost
                #payables.save()
    

    return redirect('allifmaalapp:AllifmaalPurchaseOrders')



##########################################################3  HRM #######################
def hrm(request):
    title="Allifmaal Human Resource Management"
    header="Allifmaal HRM Management System"
    form =AddStaffForm()
    
    staff=AllifmaalHumanResourcesModel.objects.all()
    staffSearch=AllifmaalHumanResourcesModel.objects.all()
    latestAddedStaff = AllifmaalHumanResourcesModel.objects.order_by('-dateJoined')[:2]#the minus means start with the latest addition
    
    if request.method == 'POST':
        form =AddStaffForm(request.POST,request.FILES)
        if form.is_valid():
           
            form.save()
            form=AddStaffForm()
            salaries=AllifmaalHumanResourcesModel.objects.all()
            salaries_due=0
            for salary in salaries:
                salaries_due+=salary.salary
            wages_payables=salaries_due

            wages=AllifmaalChartOfAccountsModel.objects.filter(description="Salaries").first()
            if wages:
                wage=AllifmaalChartOfAccountsModel.objects.get(description="Salaries")
                wage.balance=wages_payables
                wage.save()
            return redirect("allifmaalapp:human-resource")
        else:
            form.non_field_errors
    #pagination=Paginator(AllifmaalHumanResourcesModel.objects.all(),1)
    #page=request.GET.get('page')
    #physical_products=pagination.get_page(page)
    #page_num="a"*physical_products.paginator.num_pages

     # start of the search form part.............................
    #staffsearchform = StaffSearchForm(request.POST or None)#this is for the search
    #if request.method == 'POST':
        #staff = HRMModel.objects.filter(firstName__icontains=staffsearchform['firstName'].value())
     #End of search
    
   
  

    context = {
        "title":title,
        "form":form,
       
        "header":header,
        "staff":staff,
        #"page_num":page_num,
        "latestAddedStaff":latestAddedStaff,
        "staffSearch":staffSearch,
        #"staffsearchform":staffsearchform,
       
      
    }

    return render(request,'allifmaalapp/hrm/hrm.html',context)

def deleteStaff(request,pk):
    try:
        AllifmaalHumanResourcesModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('allifmaalapp:human-resource')

    return redirect('allifmaalapp:human-resource')

    
#@allowed_users(allowed_roles=['admin'])
def updateStaffDetails(request, pk):
    title="Update Staff Details"
    updateStockItem= AllifmaalHumanResourcesModel.objects.get(id=pk)
    form = AddStaffForm(instance= updateStockItem)#insert the content of the table stored in the selected id in the update form
    #we could have used the add customer form but the validation will refuse us to update since fields may exist
    if request.method == 'POST':
        form = AddStaffForm(request.POST, instance= updateStockItem)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock item updated successfully')
            return redirect('allifmaalapp:human-resource')#just redirection page
    context = {
		'form':form,
        "updateStockItem":updateStockItem,
        "title":title,
    }
    return render(request,'allifmaalapp/hrm/updateStaffDetails.html',context)


def staff_Details(request,pk):
    title="Employee Details"
    employee_details=AllifmaalHumanResourcesModel.objects.get(id=pk)
   
    context={
    
        "employee_details":employee_details,
        "title":title,
     

    }
    return render(request,'allifmaalapp/hrm/staffDetails.html',context)

############# assets

def AllifmaalAssets(request):
    title="Allifmaal Assets"
    assets=AllifmaalAssetsModel.objects.all()
    
    assets_queryset=AllifmaalChartOfAccountsModel.objects.filter(code__lte=19999)
    cash=AllifmaalChartOfAccountsModel.objects.filter(code__lte=19999).first()
    default_cash_accs=AllifmaalChartOfAccountsModel.objects.filter(description="Cash").first()
   
    form=AddAllifmaalAssetsForm(initial={'cost_account':cash,'asset_account':assets_queryset})
    
    
    if request.method =="POST":
        form=AddAllifmaalAssetsForm(request.POST or None,request.FILES)
        if form.is_valid():
            form.save()
            form=AddAllifmaalAssetsForm()

            supplier_id=request.POST.get('supplier')
            payment_option=request.POST.get('payment_terms')
            asset_value_acc_id=int(request.POST.get('asset_account'))
            cost_value_acc_id=int(request.POST.get('cost_account'))
            quantity=Decimal(request.POST.get('quantity'))
            unit_cost=Decimal(request.POST.get('value'))
            total_cost=Decimal(quantity*unit_cost)

            if payment_option=="Cash":
                cash_acc_selected=AllifmaalChartOfAccountsModel.objects.get(description="Cash")#this is hard-coding the db filter
                cost_acc_selected=AllifmaalChartOfAccountsModel.objects.get(pk=cost_value_acc_id)
                initial_cash_balance=cost_acc_selected.balance
                cost_acc_selected.balance=Decimal(initial_cash_balance)-total_cost
                cost_acc_selected.save()

                asset_acc=AllifmaalChartOfAccountsModel.objects.get(pk=asset_value_acc_id)
                initial_asset_balance=Decimal(asset_acc.balance)
                asset_acc.balance=initial_asset_balance+total_cost
                asset_acc.save()
                
                supplier_acc=AllifmaalSuppliersModel.objects.get(pk=supplier_id)
                initial_supplier_turnover=supplier_acc.turnover
                supplier_acc.turnover=initial_supplier_turnover+total_cost
                supplier_acc.save()
                
            else:
                    #increase account payables by the PO total amount
                asset_acc=AllifmaalChartOfAccountsModel.objects.get(pk=asset_value_acc_id)
                initial_asset_balance=asset_acc.balance
                asset_acc.balance=initial_asset_balance+total_cost
                asset_acc.save()
               
                cash_acc=AllifmaalChartOfAccountsModel.objects.filter(description="Accounts Payable_testingonlhy").first()
                if cash_acc:
                    
                    initial_cash_balance=cash_acc.balance
                    cash_acc.balance=initial_cash_balance+total_cost
                    cash_acc.save()
                    
                else:
                    supplier=AllifmaalSuppliersModel.objects.get(pk=supplier_id)
                    initial_supplier_balance=supplier.balance
                    initial_supplier_turnover=supplier.turnover
                    supplier.balance=initial_supplier_balance+total_cost
                    supplier.turnover=initial_supplier_turnover+total_cost
                    supplier.save()

    totalassets=0
    for asset in assets:
        totalassets+=asset.value
    allifmaal_assets=totalassets
    context={
        
        "form":form,
        "assets":assets,
        "allifmaal_assets":allifmaal_assets,
        "title":title,
        
    }
    return render(request,'allifmaalapp/assets/allifmaalassets.html',context)
    

def DeleteAllifmaalAsset(request,pk):
    delete_asset=AllifmaalAssetsModel.objects.get(id=pk)
    assetAcc_id=delete_asset.asset_account.id
    assetCostAcc_id=delete_asset.cost_account.id
    asset_quantity=delete_asset.quantity
    asset_value=delete_asset.value
    total_asset_value=asset_quantity*asset_value
    terms=delete_asset.payment_terms
    supplier=delete_asset.supplier
    if terms=="Cash":
        assetAcc=AllifmaalChartOfAccountsModel.objects.get(id=assetAcc_id)
        asset_acc_initial_balance=assetAcc.balance
        assetAcc.balance=asset_acc_initial_balance-total_asset_value
        assetAcc.save()

        AssetCostAccount=AllifmaalChartOfAccountsModel.objects.get(id=assetCostAcc_id)
        cost_acc_initial_balance=AssetCostAccount.balance
        AssetCostAccount.balance=cost_acc_initial_balance+total_asset_value
        AssetCostAccount.save()
        supplier_initial_turnover=supplier.turnover
        supplier.turnover=supplier_initial_turnover-total_asset_value
        supplier.save()
        delete_asset.delete()

    else:
        assetAcc=AllifmaalChartOfAccountsModel.objects.get(id=assetAcc_id)
        asset_acc_initial_balance=assetAcc.balance
        assetAcc.balance=asset_acc_initial_balance-total_asset_value
        assetAcc.save()

        supplier_initial_turnover=supplier.turnover
        supplier.turnover=supplier_initial_turnover-total_asset_value

        supplier_initial_balance=supplier.balance
        supplier.balance=supplier_initial_balance-total_asset_value
        supplier.save()
        delete_asset.delete()
        
    return redirect('allifmaalapp:AllifmaalAssets')

###################### BANK SECTION #########################
def AllifmaalBanks(request):
    title="Allifmaal Banks"
    banks=AllifmaalBanksModel.objects.all()
    tot_bal=AllifmaalBanksModel.objects.filter(balance__gt=0).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
    form=AddAllifmaalBankForm()
    if request.method =="POST":
        form=AddAllifmaalBankForm(request.POST or None,request.FILES)
        if form.is_valid():
            form.save()
            form=AddAllifmaalBankForm()
            return redirect("allifmaalapp:AllifmaalBanks")
    context={
        "title":title,
        "form":form,
        "banks":banks,
        "tot_bal":tot_bal,

    }
    return render(request,'allifmaalapp/banks/allifmaalbanks.html',context)

def deleteBank(request,pk):
    try:
        AllifmaalBanksModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('allifmaalapp:AllifmaalBanks')

    return redirect('allifmaalapp:AllifmaalBanks')

    
#@allowed_users(allowed_roles=['admin'])
def updateBankDetails(request, pk):
    updateStockItem= AllifmaalBanksModel.objects.get(id=pk)
    form = AddAllifmaalBankForm(instance= updateStockItem)#insert the content of the table stored in the selected id in the update form
    #we could have used the add customer form but the validation will refuse us to update since fields may exist
    if request.method == 'POST':
        form = AddAllifmaalBankForm(request.POST, instance= updateStockItem)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bank updated successfully')
            return redirect('allifmaalapp:AllifmaalBanks')#just redirection page
    context = {
		'form':form,
        "updateStockItem":updateStockItem,
    }
    return render(request,'allifmaalapp/banks/allifmaalbanks.html',context)


def ShowBankDetails(request,pk):
    title="Bank Details"
    bankdetails=AllifmaalBanksModel.objects.get(id=pk)
   
    context={
    
        "bankdetails":bankdetails,
        "title":title,
     

    }
    return render(request,'allifmaalapp/banks/allifmaalbanksdetails.html',context)


def AllifmaalBankDeposits(request):
    title="Allifmaal Bank Deposits"
    deposits=AllifmaalBankDepositsModel.objects.all()
    tot_bal=AllifmaalBankDepositsModel.objects.filter(amount__gt=0).order_by('-amount').aggregate(Sum('amount'))['amount__sum']
    
    form=AddAllifmaalBankDepositForm()
    if request.method =="POST":
        form=AddAllifmaalBankDepositForm(request.POST or None,request.FILES)
        if form.is_valid():
            form.save()
            form=AddAllifmaalBankDepositForm()
           
            bank_id=int(request.POST.get('bank'))
            amount=Decimal(request.POST.get('amount'))
            print(bank_id,amount)
            bank=AllifmaalBanksModel.objects.get(pk=bank_id)
            initial_bank_ac_balance=bank.balance
            bank.balance=Decimal(initial_bank_ac_balance)+amount
            bank.save()
            print(bank)

            #return redirect("allifmaalapp:AllifmaalBankDeposits")
    context={
        "title":title,
        "form":form,
        "deposits":deposits,
        "tot_bal":tot_bal,

    }
    return render(request,'allifmaalapp/banks/allifmaalbankdeposits.html',context)

def deleteBankDeposit(request,pk):
    try:
        AllifmaalBankDepositsModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('allifmaalapp:AllifmaalBankDeposits')

    return redirect('allifmaalapp:AllifmaalBankDeposits')

    
#@allowed_users(allowed_roles=['admin'])
def updateBankDepositDetails(request, pk): 
    deposit= AllifmaalBankDepositsModel.objects.get(id=pk)
    form =AddAllifmaalBankDepositForm(instance=deposit)#insert the content of the table stored in the selected id in the update form
    #we could have used the add customer form but the validation will refuse us to update since fields may exist
    if request.method == 'POST':
        form =AddAllifmaalBankDepositForm(request.POST, instance=deposit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bank updated successfully')
            return redirect('allifmaalapp:AllifmaalBankDeposits')#just redirection page
    context = {
		'form':form,
        "deposit":deposit,
    }
    return render(request,'allifmaalapp/banks/allifmaalbankdeposits.html',context)


def ShowBankDepositDetails(request,pk):
    title="Bank Deposit Details"
    details=AllifmaalBankDepositsModel.objects.get(id=pk)
   
    context={
    
        "details":details,
        "title":title,
     

    }
    return render(request,'allifmaalapp/banks/allifmaalbankdepositdetails.html',context)



def AllifmaalBankWithdrawls(request):
    title="Allifmaal Bank Withdrawals"
    withdrawals=AllifmaalBankWithdrawalsModel.objects.all()
    tot_bal=AllifmaalBankWithdrawalsModel.objects.filter(amount__gt=0).order_by('-amount').aggregate(Sum('amount'))['amount__sum']
    
    form=AddAllifmaalBankWithdrawalForm()
    if request.method =="POST":
        form=AddAllifmaalBankWithdrawalForm(request.POST or None,request.FILES)
        if form.is_valid():
            form.save()
            form=AddAllifmaalBankWithdrawalForm()
            bank_id=int(request.POST.get('bank'))
            amount=Decimal(request.POST.get('amount'))
            bank=AllifmaalBanksModel.objects.get(pk=bank_id)
            initial_bank_ac_balance=bank.balance
            init_bal=Decimal(initial_bank_ac_balance)
            if init_bal>amount:
                bank.balance= init_bal-amount
                bank.save()
                
            else:
                return HttpResponse("You do not have enough money in the account")
    context={
        "title":title,
        "form":form,
        "withdrawals":withdrawals,
        "tot_bal":tot_bal,

    }
    return render(request,'allifmaalapp/banks/allifmaalbankwithdrawals.html',context)

def deleteBankWithdrawal(request,pk):
    try:
        AllifmaalBankWithdrawalsModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('allifmaalapp:AllifmaalBankWithdrawls')

    return redirect('allifmaalapp:AllifmaalBankWithdrawls')

    
#@allowed_users(allowed_roles=['admin'])
def updateBankWithdrawalDetails(request, pk):
    updated_query= AllifmaalBankWithdrawalsModel.objects.get(id=pk)
    form =AddAllifmaalBankWithdrawalForm(instance=updated_query)#insert the content of the table stored in the selected id in the update form
    #we could have used the add customer form but the validation will refuse us to update since fields may exist
    if request.method == 'POST':
        form =AddAllifmaalBankWithdrawalForm(request.POST, instance=updated_query)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bank updated successfully')
            return redirect('allifmaalapp:AllifmaalBankWithdrawls')#just redirection page
    context = {
		'form':form,
        
    }
    return render(request,'allifmaalapp/banks/allifmaalbankwithdrawals.html',context)


def ShowBankWithdrawalDetails(request,pk): 
    title="Bank Withdrawal Details"
    query_details=AllifmaalBankWithdrawalsModel.objects.get(id=pk)
   
    context={
    
        "query_details":query_details,
        "title":title,
     

    }
    return render(request,'allifmaalapp/banks/allifmaalbankwithdrawdetails.html',context)


###################### profit and loss section ###################3
def profitAndLoss(request):
    title="Profit And Loss"
    try:
        totalsales=AllifmaalInvoicesModel.objects.filter(posting_inv_status='posted').order_by('-invoice_total').aggregate(Sum('invoice_total'))['invoice_total__sum']
        totalrevenue=AllifmaalChartOfAccountsModel.objects.filter(code__lt=49999,code__gt=39999).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
        
        totalgoodscost=AllifmaalInvoicesModel.objects.filter(posting_inv_status='posted').order_by('-invoice_items_total_cost').aggregate(Sum('invoice_items_total_cost'))['invoice_items_total_cost__sum']
        grossprofitorloss=totalsales-totalgoodscost
        #totalexpenses=totalgoodscost=AllifmaalExpensesModel.objects.all().order_by('-amount').aggregate(Sum('amount'))['amount__sum']
        totexpenses=AllifmaalChartOfAccountsModel.objects.filter(code__lt=59999,code__gt=49999).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
        netprofitorloss=grossprofitorloss-totexpenses

        totalrevenue=AllifmaalChartOfAccountsModel.objects.filter(code__lt=49999,code__gt=39999).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
        
        #order_by('-amount').aggregate(Sum('amount'))['amount__sum']
        
        exps=AllifmaalChartOfAccountsModel.objects.filter(code__lt=59999,code__gt=49999)
    except:
        return HttpResponse("No invoices posted yet")
    
    
    context={
        "title":title,
        "totalsales":totalsales,
        "totalgoodscost":totalgoodscost,
        "grossprofitorloss":grossprofitorloss,
        "netprofitorloss":netprofitorloss,
       
        "totexpenses":totexpenses,
        "totalrevenue":totalrevenue,

    }
    return render(request,'allifmaalapp/profitandloss/profitandloss.html',context)


def moneyWithdrawalFromCompany(request):
    title="Cash Withdrawals"
    withdrawals=MoneyDrawingModel.objects.all()
    tot_bal=MoneyDrawingModel.objects.filter(amount__gt=0).order_by('-amount').aggregate(Sum('amount'))['amount__sum']
    print(withdrawals)
    form=AddMoneyDrawingForm()
    if request.method =="POST":
        form=AddMoneyDrawingForm(request.POST or None,request.FILES)
        if form.is_valid():
            form.save()
            form=AddMoneyDrawingForm()
            
            acc_id=int(request.POST.get('fromacc'))
            nature_id=int(request.POST.get('account'))
            amount=Decimal(request.POST.get('amount'))
            cashacc=AllifmaalChartOfAccountsModel.objects.get(pk=acc_id)
            initial_ac_balance=cashacc.balance
            init_bal=Decimal(initial_ac_balance)
            cashacc.balance= init_bal-amount
            cashacc.save()

            naturecc=AllifmaalChartOfAccountsModel.objects.get(pk=nature_id)
            initial_nat_ac_balance=naturecc.balance
            init_nature_bal=Decimal(initial_nat_ac_balance)
            naturecc.balance= init_nature_bal+amount
            naturecc.save()

            ############# subtract from the equity account also #####
            #equitycc=AllifmaalChartOfAccountsModel.objects.get(description="Equity")
            #initial_equity_ac_balance=equitycc.balance
            #init_equ_bal=Decimal(initial_equity_ac_balance)
            #equitycc.balance= init_equ_bal-amount
            #equitycc.save()
                
           
            return redirect('allifmaalapp:moneyWithdrawalFromCompany')
    context={
        "title":title,
        "form":form,
        "withdrawals":withdrawals,
        "tot_bal":tot_bal,

    }
    return render(request,'allifmaalapp/dividends/moneywithdrawals.html',context)

def deleteMoneyWithdrawal(request,pk):
    try:
        MoneyDrawingModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('allifmaalapp:moneyWithdrawalFromCompany')

    return redirect('allifmaalapp:moneyWithdrawalFromCompany')

    
#@allowed_users(allowed_roles=['admin'])
def updateMoneyWithdrawalDetails(request, pk):
    updated_query=MoneyDrawingModel.objects.get(id=pk)
    form =AddMoneyDrawingForm(instance=updated_query)#insert the content of the table stored in the selected id in the update form
    #we could have used the add customer form but the validation will refuse us to update since fields may exist
    if request.method == 'POST':
        form =AddMoneyDrawingForm(request.POST, instance=updated_query)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully')
            return redirect('allifmaalapp:moneyWithdrawalFromCompany')#just redirection page
    context = {
		'form':form,
        
    }
    return render(request,'allifmaalapp/dividends/moneywithdrawals.html',context)



#####################3333 FOR LEARNING ONLY ############3
def forlearningonly(request):
    learns=ForLearningOnlyModel.objects.all()
    form=AddItemLearningForm()
    if request.method=="POST":
        form=AddItemLearningForm(request.POST or None)
        if form.is_valid():
            form.save()
            
        return redirect('allifmaalapp:forlearningonly')
    context={
        "learns":learns,
        "form":form,
    }
    return render(request,'allifmaalapp/learn/dropdown_auto_fill_form_field.html',context)

def autofill_form_field_when_dropdown_selected(request):

    if request.method=="GET":

        selectedoption=request.GET.get('allifidforselecteditem')

        selecteditemid=AllifmaalStocksModel.objects.get(pk=selectedoption)
     
        doc_data={
        "id":selecteditemid.id,
        "unitPrice":selecteditemid.unitPrice,
        }
        
        return JsonResponse(doc_data)

def delete_autofill_form_field_when_dropdown(request,pk):
    try:
        ForLearningOnlyModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('allifmaalapp:forlearningonly')

    return redirect('allifmaalapp:forlearningonly')

    
#@allowed_users(allowed_roles=['admin'])
def edit_autofill_form_field_when_dropdown(request, pk):
    updateStockItem= ForLearningOnlyModel.objects.get(id=pk)
    form = AddItemLearningForm(instance= updateStockItem)#insert the content of the table stored in the selected id in the update form
    #we could have used the add customer form but the validation will refuse us to update since fields may exist
    if request.method == 'POST':
        form = AddItemLearningForm(request.POST, instance= updateStockItem)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock item updated successfully')
            return redirect('allifmaalapp:forlearningonly')#just redirection page
    context = {
		'form':form,
        "updateStockItem":updateStockItem,
    }
    return render(request,'allifmaalapp/learn/dropdown_auto_fill_form_field.html',context)

        
########################### for learning ###################
def amtestingdynamicforms(request):
    
    return render(request,'mydynamicformtest.html')

    
   
