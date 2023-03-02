from xml.dom import ValidationErr
from django.shortcuts import render,redirect
from .forms import *

from .models import *
from django.contrib import messages
from uuid import uuid4
from django.shortcuts import render,redirect,get_object_or_404
#from invoice.models import AllifmaalDetailsModel,AllifmaalScopeModel
#from learningapp.models import SepcoLogoModel
from django.http.response import HttpResponse, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required 


# Create your views here.
def alwen_website(request):
    return render(request,'logistics/alwen-web.html')

@login_required(login_url='login:loginpage')

def logistics_dashboard(request):
    title="Main Dashabord"
    expenses=AlwenExpensesModel.objects.all()
    assets=AlwenAssetsModel.objects.all()
    fillups=AlwenFillUpsModel.objects.all()
    mileages=AlwenDailyMileageModel.objects.all()
    invoices=AlwenInvoicesModel.objects.all()
    vehicles=AlwenVehiclesModel.objects.all()
    #customers=CustomersModel.objects.all()
    cards=CardsModel.objects.all()
    posted_inv_totals=AlwenInvoicesModel.objects.order_by('-invoice_total').filter(posting_inv_status='posted')[:10]
    no_of_posted_invs=AlwenInvoicesModel.objects.filter(posting_inv_status='posted').count()
    no_of_pending_invs=AlwenInvoicesModel.objects.filter(posting_inv_status='waiting').count()

    no_of_customers=CustomersModel.objects.all().count()
    no_of_cars=AlwenVehiclesModel.objects.all().count()
    no_of_drivers=AlwenDriversModel.objects.all().count()
   
    mycustomers=CustomersModel.objects.all()
    customers=CustomersModel.objects.order_by('-name')[:6]
    context={
        "expenses":expenses,
        "assets":assets,
        "fillups":fillups,
        "mileages":mileages,
        "invoices":invoices,
       "customers":customers,
        "cards":cards,
        "no_of_pending_invs":no_of_pending_invs,
        "vehicles":vehicles,
        "mycustomers":mycustomers,
        "posted_inv_totals":posted_inv_totals,
        "no_of_posted_invs":no_of_posted_invs,
        "no_of_customers":no_of_customers,
        "no_of_cars":no_of_cars,
        "no_of_drivers":no_of_drivers,
        "title":title,
        

    }
    return render(request,'logistics/logistics-dashboard.html',context)
@login_required(login_url='login:loginpage')
def add_show_customers(request):
    title="Customers"
    customers=CustomersModel.objects.all()
    form=AddCustomerForm()
    vehicles = AlwenVehiclesModel.objects.all()
    total=AlwenVehiclesModel.objects.count()
    if request.method == 'POST':
        form=AddCustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect('logistics:logistics-customers')
    else:
        form=AddCustomerForm()
    context={
        "vehicles":vehicles,
        "form":form,
        "title":title,
        "total":total,
        "customers":customers,
    }
    return render(request,'logistics/customers/customers.html',context)

@login_required(login_url='login:loginpage')
def allifmaalcustomerdetails(request,pk):
    title="Customer Details"
    try:
        customer_detail=CustomersModel.objects.get(id=pk)
    except:
        messages.error(request, 'Something went wrong')
        return redirect('logistics:logistics-customers')

    context={
        "customer_detail":customer_detail,
        "title":title,

    }
    return render(request,'logistics/customers/customer-details.html',context)

@login_required(login_url='login:loginpage')
def delete_customer(request,pk):
    try:
        CustomersModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('logistics:logistics-customers')

    return redirect('logistics:logistics-customers')
@login_required(login_url='login:loginpage')
def update_customer(request,pk):
    title="Update Customer"
    update= CustomersModel.objects.get(id=pk)
    form = AddCustomerForm(instance=update)
   
    if request.method == 'POST':
        form = AddCustomerForm(request.POST, instance=update)
        if form.is_valid():
            form.save()
          
            return redirect('logistics:logistics-customers')#just redirection page

    context = {
		'form':form,
        "update":update,
        "title":title,
    }
    
    return render(request, 'logistics/customers/customers.html', context)#th
@login_required(login_url='login:loginpage')
def topUpCustomerAccount(request,pk):
    title="Top Up Customer Account"
    global customer,mycustid
    try:
        customer=CustomersModel.objects.get(id=pk)#very important to get id to go to particular shipment
        initial_balance=customer.balance#this gives the initial account
        mycustid=customer.id
    except:
        return HttpResponse("Sorry there is a problem ! ")
    
    
    form=AddCustomerPaymentForm()
    top_up_cust_account= get_object_or_404(CustomersModel, id=pk)


    topups= CustomerPaymentsModel.objects.filter(customer=customer)#this line helps to
    
    cust_acc_total = 0.0
    if len(topups) > 0:
        for payment in topups:
            amount= float(payment.amount) 
            cust_acc_total += amount

    
    add_item= None
    if request.method == 'POST':
        form=AddCustomerPaymentForm(request.POST)
        if form.is_valid():
            add_item= form.save(commit=False)
            add_item.customer=top_up_cust_account
            add_item.save()
            myamount=request.POST.get('amount')
           
            mycard=CustomersModel.objects.get(id=customer.id)# returns TO objects
            mycard.balance= int(initial_balance)+int(myamount)
            mycard.save()
            return redirect('logistics:topUpCustomerAccount',pk=mycustid)#just redirection page
    context={
        "form":form,  
        "customer":customer,
        "topups":topups,
        "cust_acc_total":cust_acc_total,
        "title":title,
       

    }
    return render(request, 'logistics/customers/customers-top-ups.html', context)#th


#######################################3 Carriers section #####################################3
@login_required(login_url='login:loginpage')
def add_show_carriers(request):
    title="Carriers"
    carriers=CarriersModel.objects.all()
    form=AddCarrierForm()
    if request.method == 'POST':
        form=AddCarrierForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect('logistics:logistics-carriers')
    else:
        form=AddCarrierForm()
    context={
        
        "form":form,
        "title":title,
        
        "carriers":carriers,
    }
    return render(request,'logistics/vehicles/carriers.html',context)
@login_required(login_url='login:loginpage')
def delete_carrier(request,pk):
    try:
        CarriersModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('logistics:logistics-carriers')

    return redirect('logistics:logistics-carriers')
@login_required(login_url='login:loginpage')
def update_carrier(request,pk):
    update= CarriersModel.objects.get(id=pk)
    form = AddCarrierForm(instance=update)
   
    if request.method == 'POST':
        form = AddCarrierForm(request.POST, instance=update)
        if form.is_valid():
            form.save()
          
            return redirect('logistics:logistics-carriers')#just redirection page

    context = {
		'form':form,
        "update":update,
    }
    return render(request, 'logistics/vehicles/carriers.html', context)#th

##################################3 shipment section ######################
@login_required(login_url='login:loginpage')
def shipments_list(request):
    title="Shipements"
    shipments=ShipmentsModel.objects.all()
    shipment_context={
        "shipments":shipments,
        "title":title,

    }
    return render(request, 'logistics/shipments/shipments-list.html', shipment_context)#th
@login_required(login_url='login:loginpage')
def create_blank_shipment(request):
    shipmentNo= 'AN/SH/'+str(uuid4()).split('-')[1]
    new_shipment= ShipmentsModel.objects.create(shipment_number=shipmentNo)
    new_shipment.save()
    print(new_shipment)
    return redirect('logistics:logistics-shipments-list')
@login_required(login_url='login:loginpage')
def shipment_summary(request,pk):
    title="Shipment Summary"
    myshipment=ShipmentsModel.objects.get(id=pk)
    context={
        "myshipment":myshipment,
        "title":title,
    }
    return render(request,'logistics/shipments/shipments-list.html', context)


@login_required(login_url='login:loginpage')
def delete_shipment(request,pk):
    try:
        ShipmentsModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('logistics:logistics-shipments-list')

    return redirect('logistics:logistics-shipments-list')
@login_required(login_url='login:loginpage')
def add_shipment_details(request,pk):
    title="Add Shipment Details"
    shipments=ShipmentsModel.objects.filter(id=pk)
    try:
        my_invoice_id=ShipmentsModel.objects.get(id=pk)
        print(my_invoice_id)
    except:
        messages.error(request, 'Something went wrong and could not get the invoice')
        return redirect("logistics:logistics-shipments-list")

    inv_Items = ShipmentItemsModel.objects.filter(shipment_items_connector=my_invoice_id)#this line helps to
    #show items that belong to that particular invoice in that particular invoice
    inv_id= get_object_or_404(ShipmentsModel, id=pk)#this helps to fill that select field and invoice fields and content
    
    add_shipment_form=AddShippmentForm(instance=my_invoice_id)
    
   
    
    if request.method == 'POST':
        #add_shipment_items_form=AddShippmentItemsForm(request.POST)
        add_shipment_form=AddShippmentForm(request.POST,instance=my_invoice_id)
        if add_shipment_form.is_valid():
            add_shipment_form.save()
            print(request.POST)
            print("I have saved and itts correct")
            return redirect('logistics:add-items-to-shipment',pk=pk)#just redirection page

        
    shipment_context={
        
        "add_shipment_form":add_shipment_form,
        "inv_Items":inv_Items,
        "shipments":shipments,
        "title":title,
        

    }
    return render(request, 'logistics/shipments/add-shipment-details.html', shipment_context)#th
@login_required(login_url='login:loginpage')
def add_show_shipment_items(request,pk):
    title="Add Shipment Items"
    ourshipment =ShipmentsModel.objects.get(id=pk)#very important to get id to go to particular shipment
    
    add_shipment_items_form=AddShippmentItemsForm()
    add_Shipment= get_object_or_404(ShipmentsModel, id=pk)
    add_item= None
    if request.method == 'POST':
        add_shipment_items_form=AddShippmentItemsForm(request.POST)
        if add_shipment_items_form.is_valid():
            add_item= add_shipment_items_form.save(commit=False)
            add_item.shipment_items_connector =add_Shipment
            add_item.save()
           # return HttpResponse(post)
            return redirect('logistics:add-items-to-shipment',pk=pk)#just redirection page

    shipment_context={
   
            "add_shipment_items_form":add_shipment_items_form,
            "title":title,
            "ourshipment":ourshipment,
            "add_Shipment":add_Shipment, 
            "title":title,   
    }
    return render(request, 'logistics/shipments/add-items-to-shipment.html', shipment_context)#th
@login_required(login_url='login:loginpage')
def parcel_details(request,pk):
    title="Parcel Details"
    my_parcel=ShipmentItemsModel.objects.get(id=pk)
    context={
        "my_parcel":my_parcel,
        "title":title,
    }
    return render(request,'logistics/shipments/parcel-details.html', context)
@login_required(login_url='login:loginpage')
def delete_shipment_item(request,pk):
    
    try:
        ShipmentItemsModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('logistics:logistics-shipments-list')

    return redirect('logistics:logistics-shipments-list')
@login_required(login_url='login:loginpage')
def update_shipment_item(request,pk):
    title="Update Shipment"
    update= ShipmentItemsModel.objects.get(id=pk)
    add_shipment_items_form= AddShippmentItemsForm(instance=update)
   
    if request.method == 'POST':
        add_shipment_items_form= AddShippmentItemsForm(request.POST, instance=update)
        if add_shipment_items_form.is_valid():
            add_shipment_items_form.save()
          
            return redirect('logistics:logistics-shipments-list')#just redirection page
            return redirect('logistics:update-shipment-item',pk=pk)#you can aslo redirect to the same page

    context = {
		'add_shipment_items_form':add_shipment_items_form,
        "update":update,
        "title":title,
    }
    
    return render(request, 'logistics/shipments/update-shipment-item.html', context)#th





@login_required(login_url='login:loginpage')
def logistics(request):
    return render(request,'logistics/index.html')

@login_required(login_url='login:loginpage')
def vehicles(request):
    title="vehicles"
    form=AddVehicleDetailsForm(request.POST, request.FILES)
    vehicles = AlwenVehiclesModel.objects.all()
    total=AlwenVehiclesModel.objects.count()
    if request.method == 'POST':
        form=AddVehicleDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect('logistics:vehicles')
    else:
        form=AddVehicleDetailsForm()
    context={
        "vehicles":vehicles,
        "form":form,
        "title":title,
        "total":total,
    }
    return render(request,'logistics/vehicles.html',context)
@login_required(login_url='login:loginpage')
def alwen_vehicle_details(request,pk):
    vehicle= AlwenVehiclesModel.objects.get(id=pk)
    title="Vehicle details"
    
    context={
        "title":title,
        "vehicle":vehicle,
    }
    return render(request,'logistics/vehicle-details.html',context)
@login_required(login_url='login:loginpage')
def delete_alwen_car(request,pk):
    car_id=AlwenVehiclesModel.objects.get(id=pk).delete()
    return redirect('logistics:vehicles')
@login_required(login_url='login:loginpage')
def delete_vehicle(request,pk):
    title="Delete vehicle"
    delete_vehicle=AlwenVehiclesModel.objects.get(id=pk)
    if request.method =="POST":
        delete_vehicle.delete()
        messages.success(request,'Item deleted successfully')
        return redirect('logistics:vehicles')
    context={
        "title":title,
        "delete_vehicle":delete_vehicle,
    }
    return render(request,'logistics/delete_vehicle.html',context)
@login_required(login_url='login:loginpage')
def update_vehicle_details(request, pk):
    title="Update record"
    vehicles= AlwenVehiclesModel.objects.get(id=pk)

    form = VehicleDetailsUpdateForm(instance=vehicles)#insert the content of the table stored in the selected id in the update form
    #we could have used the add customer form but the validation will refuse us to update since fields may exist
    if request.method == 'POST':
        form = VehicleDetailsUpdateForm(request.POST, instance=vehicles)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle updated successfully')
            return redirect('logistics:vehicles')
    context = {
		'form':form,
        "title":title,
        "vehicles":vehicles,
    }
    return render(request, 'logistics/update_vehicle.html', context)

@login_required(login_url='login:loginpage')
def dailyMileage(request):
    title="Daily Mileages"
    form=AddVehicleDailyMileageForm(request.POST, request.FILES)
    dailymileages= AlwenDailyMileageModel.objects.all()
    total=AlwenDailyMileageModel.objects.count()
    if request.method == 'POST':
        form=AddVehicleDailyMileageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect('logistics:dailyMileage')
    else:
        form=AddVehicleDailyMileageForm()
    context={
        "dailymileages":dailymileages,
        "form":form,
        "title":title,
        "total":total,
    }
    return render(request,'logistics/dailymileages.html',context)
@login_required(login_url='login:loginpage')
def delete_milleage(request,pk):
    car_id=AlwenDailyMileageModel.objects.get(id=pk).delete()
    return redirect('logistics:dailyMileage')
@login_required(login_url='login:loginpage')
def fill_ups(request):
    title="Daily Fill Ups"

    form=AddFillUpsForm(request.POST, request.FILES)
    fillups= AlwenFillUpsModel.objects.all()
    total=AlwenFillUpsModel.objects.count()
    if request.method == 'POST':
        form=AddFillUpsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            mycard=request.POST.get('card')
            my_car=request.POST.get('vehicle')
            liters=request.POST.get('quantity')
            unit_price=request.POST.get('unit_price')
            myfuelcost=int(liters)*int(unit_price)
            
           
            if mycard:
                ourcard=CardsModel.objects.get(id=mycard)
                initial_card_balance=ourcard.balance
                our_car=AlwenVehiclesModel.objects.get(id=my_car)
                carno=ourcard.number
                running_fuel_consumption=our_car.fuel_usage
                
            else:
                return redirect('logistics:fill_ups')
            
            if initial_card_balance>=myfuelcost:
                ourcard.balance=int(initial_card_balance)-int(myfuelcost)
                ourcard.save()
                our_car.fuel_usage=int(running_fuel_consumption)+ int(myfuelcost)
                our_car.save()
                
                return redirect('logistics:fill_ups')
            else:
                return HttpResponse("lacag maheysatid sxbow naga qaley!")
    else:
        form=AddFillUpsForm()
    context={
        "fillups":fillups,
        "form":form,
        "title":title,
        "total":total,
    }
    return render(request,'logistics/fill-ups.html',context)
@login_required(login_url='login:loginpage')
def alwen_fillups_details(request,pk):
    fillup=AlwenFillUpsModel.objects.get(id=pk)
    title="Fill Up Details"
    
    context={
        "title":title,
        "fillup":fillup,
    }
    return render(request,'logistics/fillups-details.html',context)
@login_required(login_url='login:loginpage')
def update_fillup(request, pk):
    title="Update record"
    fillup= AlwenFillUpsModel.objects.get(id=pk)

    form = AddFillUpsForm(instance=fillup)#insert the content of the table stored in the selected id in the update form
    #we could have used the add customer form but the validation will refuse us to update since fields may exist
    if request.method == 'POST':
        form = AddFillUpsForm(request.POST, instance=fillup)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fill up updated successfully')
            return redirect('logistics:fill_ups')
    context = {
		'form':form,
        "title":title,
        "vehicles":vehicles,
    }
    return render(request,'logistics/fill-ups.html',context)
@login_required(login_url='login:loginpage')
def delete_alwen_fillup(request,pk):
    AlwenFillUpsModel.objects.get(id=pk).delete()
    return redirect('logistics:fill_ups')
@login_required(login_url='login:loginpage')
def services(request):
    title="Services"
    services=AlwenServiceDetailsModel.objects.all()
    context={
        "services":services,
        "title":title,
    }

    return render(request, 'logistics/services.html', context)#th


@login_required(login_url='login:loginpage')
def create_service(request):
    service_no= 'SERVICE/ALWEN/'+str(uuid4()).split('-')[1]
    new_service= AlwenServiceDetailsModel.objects.create(service_number=service_no)
    new_service.save()
    
    return redirect('logistics:services')
@login_required(login_url='login:loginpage')
def delete_service(request,pk):
    AlwenServiceDetailsModel.objects.get(id=pk).delete()
    return redirect('logistics:services')

@login_required(login_url='login:loginpage')
def add_service_details(request,pk):
    title="Add Service Details"
    services=AlwenServiceDetailsModel.objects.filter(id=pk)
    try:
        my_service_id=AlwenServiceDetailsModel.objects.get(id=pk)
        
    except:
        messages.error(request, 'Something went wrong and could not get the invoice')
        return redirect("logistics:services")

    service_Items = ServiceTasksModel.objects.filter(task_service_connector=my_service_id)#this line helps to
    #show items that belong to that particular invoice in that particular invoice
    inv_id= get_object_or_404(AlwenServiceDetailsModel, id=pk)#this helps to fill that select field and invoice fields and content
    
    form=AddServiceDetailsForm(instance=my_service_id)
    
    
    if request.method == 'POST':
        #add_shipment_items_form=AddShippmentItemsForm(request.POST)
        form=AddServiceDetailsForm(request.POST,request.FILES,instance=my_service_id)
        if form.is_valid():
            form.save()
            print(request.POST)
            print("I have saved and itts correct")
            return redirect('logistics:add_show_service_tasks',pk=pk)#just redirection page

        
    shipment_context={
        
        "form":form,
        "service_Items":service_Items,
        "services":services,
        "my_service_id":my_service_id,
        "title":title,
        

    }
    return render(request, 'logistics/add-service-details.html', shipment_context)#th
@login_required(login_url='login:loginpage')
def add_show_service_tasks(request,pk):
    title="Tasks"
    try:
        ourservice =AlwenServiceDetailsModel.objects.get(id=pk)#very important to get id to go to particular shipment

        form=AddServiceTasksForm()
        add_Service= get_object_or_404(AlwenServiceDetailsModel, id=pk)
        service_Items = ServiceTasksModel.objects.filter(task_service_connector=ourservice)
        serv_cost=0
        add_item= None
        if request.method == 'POST':
            form=AddServiceTasksForm(request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.task_service_connector =add_Service
                add_item.save()
                # return HttpResponse(post)
                for item in service_Items:
                    serv_cost+= item.service_total_costs
                    total_serv_cost=serv_cost
                    ourservice.service_cost=total_serv_cost
                    ourservice.save()
                return redirect('logistics:add_show_service_tasks',pk=pk)#just redirection page
    except:
        return redirect('logistics:services')

    #print(ourservice.service_cost)
    
    

    shipment_context={
   
            "form":form,
            "title":title,
            "ourservice":ourservice,
            "add_Service":add_Service,    
    }
    return render(request, 'logistics/add-tasks-to-service.html', shipment_context)#th
@login_required(login_url='login:loginpage')
def delete_service_task(request,pk):
    ServiceTasksModel.objects.get(id=pk).delete()
    return redirect('logistics:services')



############################################################# INVOICES ########################3
@login_required(login_url='login:loginpage')
def alwen_invoices(request):
    title="Invoices"
    invoices=AlwenInvoicesModel.objects.filter(posting_inv_status="waiting")
    last_invoices=AlwenInvoicesModel.objects.order_by('invoice_number')[:6]
    context={
        "invoices":invoices,
        "last_invoices":last_invoices,
        "title":title,
    }

    return render(request, 'logistics/alwen-invoices.html', context)#th
@login_required(login_url='login:loginpage')
def create_alwen_invoice(request):
    my_inv_no= 'AN/INV/'+str(uuid4()).split('-')[1]
    new_inv= AlwenInvoicesModel.objects.create(invoice_number=my_inv_no)
    new_inv.save()
   
    return redirect('logistics:alwen_invoices')


@login_required(login_url='login:loginpage')
def create_alwen_invoice_job(request,pk):
    myjob=AlwenJobsModel.objects.get(id=pk)
    print(myjob.id)
    inv_no= 'INV/ALWEN/'+str(uuid4()).split('-')[1]
    new_inv= AlwenInvoicesModel.objects.create(invoice_number=inv_no,job=myjob)
    myid=new_inv.id
    print(myid)
    new_inv.save()
    
    #return redirect('logistics:alwen_invoices')
    return redirect('logistics:add_invoice_details',pk=myid)
    return HttpResponse("yes")
@login_required(login_url='login:loginpage')
def delete_invoice(request,pk):
    AlwenInvoicesModel.objects.get(id=pk).delete()
    return redirect('logistics:alwen_invoices')
@login_required(login_url='login:loginpage')
def add_invoice_details(request,pk):
    title="Add Invoice Details"
    inv_details=AlwenInvoicesModel.objects.filter(id=pk)
    try:
        my_inv_id=AlwenInvoicesModel.objects.get(id=pk)
        
    except:
        messages.error(request, 'Something went wrong and could not get the invoice')
        return redirect("logistics:services")

    service_Items = AlwenInvoiceItemsModel.objects.filter(alinvcontr=my_inv_id)#this line helps to
    #show items that belong to that particular invoice in that particular invoice
    inv_id= get_object_or_404(AlwenInvoicesModel, id=pk)#this helps to fill that select field and invoice fields and content
    
    form=AddAlwenInvoiceDetailsForm(instance=my_inv_id)
    
   
    
    if request.method == 'POST':
        #add_shipment_items_form=AddShippmentItemsForm(request.POST)
        form=AddAlwenInvoiceDetailsForm(request.POST,request.FILES,instance=my_inv_id)
        if form.is_valid():
            form.save()
            print(request.POST)
            print("I have saved and itts correct")
            return redirect('logistics:add_invoice_items_alwen',pk=pk)#just redirection page

        
    shipment_context={
        
        "form":form,
        "service_Items":service_Items,
        "services":services,
        "my_inv_id":my_inv_id,
        "title":title,
        

    }
    return render(request, 'logistics/add-invoice-details.html', shipment_context)#th

@login_required(login_url='login:loginpage')
def add_invoice_items_alwen(request,pk):
    title="Add Invoice Items"
    global qaanshegto,myinvid
    try:
        qaanshegto =AlwenInvoicesModel.objects.get(id=pk)#very important to get id to go to particular shipment
        myinvid=qaanshegto.id
    except:
        return HttpResponse("Sorry there is a problem ! ")
   
    form=AddAlwenInvoiceItemsForm()
    add_inv= get_object_or_404(AlwenInvoicesModel, id=pk)
    initial_invoice_total=qaanshegto.invoice_total#this gives the initial invoice total
    if qaanshegto.customer:
        mycust=qaanshegto.customer#this gives the customer of the invoice
        customer_id=mycust.id#this gives the id of the customer specified in the invoice
        customer_account_balance=mycust.balance#this gets the account balance of the customer


    inv_Items = AlwenInvoiceItemsModel.objects.filter(alinvcontr=qaanshegto)#this line helps to
    invoiceTotal = 0.0
    if len(inv_Items) > 0:
        for line in inv_Items:
            quantityTimesUnitPrice = float(line.quantity) * float(line.unit_price)
            invoiceTotal += quantityTimesUnitPrice
    
    myinvoice=AlwenInvoicesModel.objects.get(id=myinvid)
    myinvoice.invoice_total=int(invoiceTotal)
    myinvoice.save()

    add_item= None
    if request.method == 'POST':
        form=AddAlwenInvoiceItemsForm(request.POST)
        if form.is_valid():
            add_item= form.save(commit=False)
            add_item.alinvcontr=add_inv
            add_item.save()
           # return HttpResponse(post)
            return redirect('logistics:add_invoice_items_alwen',pk=pk)#just redirection page

    shipment_context={
   
            "form":form,
            
            "qaanshegto":qaanshegto,
            "add_inv":add_inv,
            "invoiceTotal":invoiceTotal,
            "title":title,  
    }
    return render(request, 'logistics/add-items-to-invoice.html', shipment_context)#t
@login_required(login_url='login:loginpage')
def delete_invoice_items(request,pk):
    AlwenInvoiceItemsModel.objects.get(id=pk).delete()
    #return redirect('logistics:add_invoice_items_alwen',pk=pk)#just redirection page
    return redirect('logistics:add_invoice_items_alwen',pk=myinvid)
@login_required(login_url='login:loginpage')
def post_logistics_invoice(request,pk):
    global qaanshegto,myinvid
    try:
        qaanshegto =AlwenInvoicesModel.objects.get(id=pk)#very important to get id to go to particular shipment
        myinvid=qaanshegto.id
    except:
        return HttpResponse("Sorry there is a problem ! ")
   
    form=AddAlwenInvoiceItemsForm()
    add_inv= get_object_or_404(AlwenInvoicesModel, id=pk)

    initial_invoice_total=qaanshegto.invoice_total#this gives the initial invoice total
    if qaanshegto.customer:
        mycust=qaanshegto.customer#this gives the customer of the invoice
        customer_id=mycust.id#this gives the id of the customer specified in the invoice
        customer_account_balance=mycust.balance#this gets the account balance of the customer
    else:
        return redirect('logistics:add_invoice_items_alwen',pk=myinvid)
    


    inv_Items = AlwenInvoiceItemsModel.objects.filter(alinvcontr=qaanshegto)#this line helps to
    invoiceTotal = 0.0
    if len(inv_Items) > 0:
        for line in inv_Items:
            quantityTimesUnitPrice = float(line.quantity) * float(line.unit_price)
            invoiceTotal += quantityTimesUnitPrice
    myinvoice=AlwenInvoicesModel.objects.get(id=myinvid)
    myinvoice.posting_inv_status="posted"
    myinvoice.save()
    #myinvoice.invoice_total=int(invoiceTotal)
    
    inv_tot=qaanshegto.invoice_total
    macaamil=CustomersModel.objects.get(id=customer_id)
    macaamil.balance=int(customer_account_balance)-int(inv_tot)
    
    macaamil.save()
    #client_detail, created = AllifPostedInvoicesModel.objects.get_or_create(customer=mycustomer,invoice_number=,invoice_total=)

    return redirect('logistics:add_invoice_items_alwen',pk=myinvid)
@login_required(login_url='login:loginpage')
def allifpostedinvoices(request):
    title="Posted Invoices"
    #posted_invoices=AllifPostedInvoicesModel.objects.filter(posting_inv_status="posted")
    posted_invoices=AlwenInvoicesModel.objects.filter(posting_inv_status="posted")
    context={
        "posted_invoices":posted_invoices,
        "title":title,

    }
    return render(request, 'logistics/posted-invoices.html', context)#
@login_required(login_url='login:loginpage') 
def alwen_invoice_pdf(request,pk):
    title="Invoice PDF"
    system_user=request.user
    invoice_details=get_object_or_404(AlwenInvoicesModel,id=pk)
    try:
        inv_number= AlwenInvoicesModel.objects.get(id=pk)
    except:
        messages.error(request, 'Something went wrong')

    invoiceItems = AlwenInvoiceItemsModel.objects.filter(alinvcontr=inv_number)

    invoiceTotal = float(0.0)
    if len(invoiceItems) > 0:
       for x in invoiceItems:
            y = float(0 or x.quantity) * float(0 or x.unit_price)
            invoiceTotal += y

    template_path = 'logistics/invoice-pdf.html'
    companyDetails=AllifmaalDetailsModel.objects.all()
    scope=AllifmaalScopeModel.objects.all()
    alwenco=SepcoLogoModel.objects.all()
    context = {
    'invoice_details':invoice_details,
   "invoiceItems":invoiceItems,
   "companyDetails":companyDetails,
   "invoiceTotal":invoiceTotal,
   "scope":scope,
   "system_user":system_user,
   "alwenco":alwenco,
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

@login_required(login_url='login:loginpage')
def AlwenAssets(request):
    title="Alwen Assets"
    assets=AlwenAssetsModel.objects.all()
    
    
   
    form=AddAlwenAssetsForm(request.POST or None)
    if request.method =="POST":
        form=AddAlwenAssetsForm(request.POST or None,request.FILES)
        if form.is_valid():
            form.save()
            form=AddAlwenAssetsForm()
    totalassets=0
    for asset in assets:
        totalassets+=asset.value
    sepco_assets=totalassets
    mycontext={
        
        "form":form,
        "assets":assets,
        "sepco_assets":sepco_assets,
        "title":title,
        
    }
    return render (request,'logistics/alwen-assets.html',mycontext)
@login_required(login_url='login:loginpage')
def delete_asset(request,pk):
    AlwenAssetsModel.objects.get(id=pk).delete()
    return redirect('logistics:AlwenAssets')

########################################################## EXPENSES ############################################3
@login_required(login_url='login:loginpage')
def AlwenExpenses(request):
    title="Expenses"
    expenses=AlwenExpensesModel.objects.all()
    
   
    form=AddAlwenExpensesForm(request.POST or None)
    if request.method =="POST":
        form=AddAlwenExpensesForm(request.POST or None,request.FILES)
        if form.is_valid():
            form.save()
            form=AddAlwenExpensesForm()
    exp=0
    for expense in expenses:
        exp+=expense.amount
    total_exp=exp
    mycontext={
        
        "form":form,
        "expenses":expenses,
        "total_exp":total_exp,
        "title":title,
    }
    return render (request,'logistics/alwenexpenses.html',mycontext)
@login_required(login_url='login:loginpage')
def alwenDeleteExpense(request,pk):
    AlwenExpensesModel.objects.get(id=pk).delete()
    return redirect('logistics:AlwenExpenses')
@login_required(login_url='login:loginpage')
def alwen_jobs_list(request):
    title="Jobs"
    jobs=AlwenJobsModel.objects.all()
    context={
        "jobs":jobs,
        "title":title,

    }
    return render(request,'jobs/jobs.html',context)


import datetime
@login_required(login_url='login:loginpage')
def AllifNewJobs(request):
    current_datetime = datetime.datetime.now()
    job_year=current_datetime.year
    
    last_po = AlwenJobsModel.objects.all().order_by('id').last()
    last_obj=AlwenJobsModel.objects.last()
    if last_obj:
        
        last_obj_id=last_obj.id
        last_obj_incremented=last_obj_id+1
   
    #purchaseNumber= 'LPO/AMEL-'+str(uuid4()).split('-')[1]
        jobNo= 'AN/JB/'+str(uuid4()).split('-')[1]+'/'+str(last_obj_incremented)+'/'+str(job_year)
        
    else:
        
       jobNo= 'AN/JB/'+str(uuid4()).split('-')[1]
        #purchaseNumber= 'LPO/AMEL-'+str(uuid4()).split('-')[1]+'/'+str("Reset")

    newJobRef= AlwenJobsModel.objects.create(job_number=jobNo)
    newJobRef.save()
    return redirect('logistics:alwen_jobs_list')

@login_required(login_url='login:loginpage')
def delete_job(request,pk):
    AlwenJobsModel.objects.get(id=pk).delete()
    return redirect("logistics:alwen_jobs_list")

@login_required(login_url='login:loginpage')
def add_job_details(request,pk):
    title="Add Job Details"
    jobs=AlwenJobsModel.objects.filter(id=pk)
    distance_covered=ending_mileage=starting_mileage=0
    try:
        my_job_id=AlwenJobsModel.objects.get(id=pk)
        starting_mileage=my_job_id.starting_odometer
        ending_mileage=my_job_id.ending_odometer
        
        
    except:
        #messages.error(request, 'Something went wrong and could not get the invoice')
        return redirect("logistics:alwen_jobs_list")
    
    distance_covered=int(ending_mileage)-int(starting_mileage)
    job_Items = AlwenJobItemsModel.objects.filter(jobitemconnector=my_job_id)#this line helps to
    #show items that belong to that particular invoice in that particular invoice
    inv_id= get_object_or_404(AlwenJobsModel, id=pk)#this helps to fill that select field and invoice fields and content
    
    form=AddAlwenJobDetailsForm(instance=my_job_id)

    if request.method == 'POST':
        #add_shipment_items_form=AddShippmentItemsForm(request.POST)
        form=AddAlwenJobDetailsForm(request.POST,request.FILES,instance=my_job_id)
        if form.is_valid():
            form.save()
           
            return redirect('logistics:add_job_items',pk=pk)#just redirection page
            return redirect('logistics:add_job_details',pk=pk)#just redirection page
    
    context={
        
        "form":form,
        "job_Items":job_Items,
        "jobs":jobs,
        "my_job_id":my_job_id,
        "distance_covered":distance_covered,
        "title":title,
        

    }
    return render(request, 'jobs/addjobdetails.html', context)#th

@login_required(login_url='login:loginpage')
def add_job_items(request,pk):
    title="Add Job Items"
    jobs=AlwenJobsModel.objects.filter(id=pk)
    global my_job_id,myjobid
    for item in jobs:
        markup=item.uplift
        
    try:
        my_job_id=AlwenJobsModel.objects.get(id=pk)
        myjobid=my_job_id.id
    except:
        messages.error(request, 'We are really sorry, something went wrong!')
        return redirect("stockmanagementapp:error_page")

    job_Items = AlwenJobItemsModel.objects.filter(jobitemconnector=my_job_id)
    job_id= get_object_or_404(AlwenJobsModel, id=pk)

    invoiceTotal = int(0)
    if len(job_Items) > 0:
        for product in job_Items:
            quantityTimesUnitPrice = product.quantity * product.unit_cost
            invoiceTotal += quantityTimesUnitPrice

    form= AddAlwenJobItemsForm()
    if request.method == 'POST':
        form= AddAlwenJobItemsForm(request.POST)
        if form.is_valid():
            descrip=request.POST['description']
            des_same=request.POST.get('description')
            qty=request.POST['quantity']
            unitcost=request.POST['unit_cost']

            my_description= form.cleaned_data['description']
            my_qty= form.cleaned_data['quantity']
            my_unit_cost= form.cleaned_data['unit_cost']
            my_unit_price=int(my_unit_cost)*int(markup)
            additems= form.save(commit=False)
            additems.jobitemconnector= job_id
            additems.save()
            form=AddAlwenJobItemsForm()
           
            newOrder, created=AlwenJobItemsSellingModel.objects.get_or_create(description=my_description,unit_cost=my_unit_cost,quantity=my_qty, unit_price=my_unit_price,jobitselcon=my_job_id)
            #newOrder, created=AlwenJobItemsSellingModel.objects.get_or_create(description=descrip,unit_cost=unitcost,quantity=qty)
            #my_new_data=AlwenJobItemsSellingModel(description=my_description,unit_cost=my_unit_cost,quantity=my_qty, unit_price=amount,jobitselcon=my_job_id)
            #my_new_data.save()
            return redirect('logistics:add_job_items',pk=pk)

    context={
        
        "form":form,
        "job_id":job_id,
        "job_Items":job_Items,
        "invoiceTotal":invoiceTotal,
        "jobs":jobs,
        "my_job_id":my_job_id,
        "title":title,
    }
    return render(request,'jobs/addItemsToJob.html',context)
@login_required(login_url='login:loginpage')
def delete_job_items(request,pk):
    AlwenJobItemsModel.objects.get(id=pk).delete()
    return redirect("logistics:add_job_items",pk=myjobid)

@login_required(login_url='login:loginpage')
def allif_invoice_job(request,pk):
    title="Invoice PDF"
    system_user=request.user
    my_job_id=AlwenJobsModel.objects.get(id=pk)
    job_Items = AlwenJobItemsModel.objects.filter(jobitemconnector=my_job_id)
    myuplift=0

    form=AddAlwenJobDetailsForm(instance=my_job_id)

    if request.method == 'POST':
        #add_shipment_items_form=AddShippmentItemsForm(request.POST)
        form=AddAlwenJobDetailsForm(request.POST,request.FILES,instance=my_job_id)
        if form.is_valid():
            form.save()
    
    for item in job_Items:
        products=AlwenJobItemsModel.objects.get(id=item.id)
        item_unit_cost=item.unit_cost#this gets the unit cost of the individual items
        myuplift=my_job_id.uplift
        products.unit_price=item_unit_cost*myuplift
        products.selling_price=item_unit_cost*myuplift
        products.save()
    
    sellingjob=AlwenJobItemsSellingModel.objects.filter(jobitselcon=my_job_id)  
    invoiceTotal=0
    total_cost=0
    gross_profit=0
    profit_percentage=0
    if len(job_Items) > 0:
        for product in job_Items:
            quantityTimesUnitPrice = float(product.quantity * product.unit_price)
            invoiceTotal += quantityTimesUnitPrice
            linecost=float(product.quantity * product.unit_cost)
            total_cost+=linecost
    gross_profit=float(invoiceTotal-total_cost)
    if gross_profit:
        profit_percentage=float(gross_profit/total_cost)*100
    else:
        pass
        
    context={
        "my_job_id":my_job_id,
        "job_Items":job_Items,
        "myuplift":myuplift,
        "sellingjob":sellingjob,
        #"potential_selling_price":potential_selling_price,
        "invoiceTotal":invoiceTotal,
        "total_cost":total_cost,
        "gross_profit":gross_profit,
        "profit_percentage":profit_percentage,
        "form":form,
        "system_user":system_user,
        "title":title,
        
    }
    return render(request,'jobs/allif-invoice-job.html',context)
@login_required(login_url='login:loginpage')
def alwen_job_invoice_pdf(request,pk):
    title="Job Invoice Pdf"
    system_user=request.user
    my_job_id=AlwenJobsModel.objects.get(id=pk)
    job_Items = AlwenJobItemsModel.objects.filter(jobitemconnector=my_job_id)
    myuplift=0

    form=AddAlwenJobDetailsForm(instance=my_job_id)

    if request.method == 'POST':
        #add_shipment_items_form=AddShippmentItemsForm(request.POST)
        form=AddAlwenJobDetailsForm(request.POST,request.FILES,instance=my_job_id)
        if form.is_valid():
            form.save()
    
    for item in job_Items:
        products=AlwenJobItemsModel.objects.get(id=item.id)
        item_unit_cost=item.unit_cost#this gets the unit cost of the individual items
        myuplift=my_job_id.uplift
        products.unit_price=item_unit_cost*myuplift
        products.selling_price=item_unit_cost*myuplift
        products.save()
    
    sellingjob=AlwenJobItemsSellingModel.objects.filter(jobitselcon=my_job_id)  
    invoiceTotal=0
    total_cost=0
    gross_profit=0
    profit_percentage=0
    if len(job_Items) > 0:
        for product in job_Items:
            quantityTimesUnitPrice = float(product.quantity * product.unit_price)
            invoiceTotal += quantityTimesUnitPrice
            linecost=float(product.quantity * product.unit_cost)
            total_cost+=linecost
    gross_profit=float(invoiceTotal-total_cost)
    if gross_profit:
        profit_percentage=float(gross_profit/total_cost)*100
    else:
        pass
    template_path = 'jobs/job-invoice-pdf.html'
    companyDetails=AllifmaalDetailsModel.objects.all()
    scope=AllifmaalScopeModel.objects.all()
    alwenco=SepcoLogoModel.objects.all()
        
    context={
        "my_job_id":my_job_id,
        "job_Items":job_Items,
        "myuplift":myuplift,
        "sellingjob":sellingjob,
        #"potential_selling_price":potential_selling_price,
        "invoiceTotal":invoiceTotal,
        "total_cost":total_cost,
        "gross_profit":gross_profit,
        "profit_percentage":profit_percentage,
        "form":form,
        "companyDetails":companyDetails,
   
        "scope":scope,
        "system_user":system_user,
        "alwenco":alwenco,
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


@login_required(login_url='login:loginpage')
def allif_job_transaction_report_pdf(request,pk):
    title="Job Transactions Report Pdf"
    system_user=request.user
    my_job_id=AlwenJobsModel.objects.get(id=pk)
    job_Items = AlwenJobItemsModel.objects.filter(jobitemconnector=my_job_id)
    myuplift=0

    form=AddAlwenJobDetailsForm(instance=my_job_id)

    if request.method == 'POST':
        #add_shipment_items_form=AddShippmentItemsForm(request.POST)
        form=AddAlwenJobDetailsForm(request.POST,request.FILES,instance=my_job_id)
        if form.is_valid():
            form.save()
    
    for item in job_Items:
        products=AlwenJobItemsModel.objects.get(id=item.id)
        item_unit_cost=item.unit_cost#this gets the unit cost of the individual items
        myuplift=my_job_id.uplift
        products.unit_price=item_unit_cost*myuplift
        products.selling_price=item_unit_cost*myuplift
        products.save()
    
    sellingjob=AlwenJobItemsSellingModel.objects.filter(jobitselcon=my_job_id)  
    invoiceTotal=0
    total_cost=0
    gross_profit=0
    profit_percentage=0
    if len(job_Items) > 0:
        for product in job_Items:
            quantityTimesUnitPrice = float(product.quantity * product.unit_price)
            invoiceTotal += quantityTimesUnitPrice
            linecost=float(product.quantity * product.unit_cost)
            total_cost+=linecost
    gross_profit=float(invoiceTotal-total_cost)
    if gross_profit:
        profit_percentage=float(gross_profit/total_cost)*100
    else:
        pass
    template_path = 'jobs/job-transaction-report-pdf.html'
    companyDetails=AllifmaalDetailsModel.objects.all()
    scope=AllifmaalScopeModel.objects.all()
    alwenco=SepcoLogoModel.objects.all()
        
    context={
        "my_job_id":my_job_id,
        "job_Items":job_Items,
        "myuplift":myuplift,
        "sellingjob":sellingjob,
        #"potential_selling_price":potential_selling_price,
        "invoiceTotal":invoiceTotal,
        "total_cost":total_cost,
        "gross_profit":gross_profit,
        "profit_percentage":profit_percentage,
        "form":form,
        "companyDetails":companyDetails,
   
        "scope":scope,
        "system_user":system_user,
        "alwenco":alwenco,
        "title":title,
        
    }
    
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Job-Transactions.pdf"'
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
    


###################################### CHART OF ACCOUNTS #####################################
@login_required(login_url='login:loginpage')
def add_show_chart_of_account(request):
    title="Chart of accounts"
    chart_of_accounts=AllifChartOfAccountsModel.objects.all()
    form=AddAllifChartOfAccountForm(request.POST, request.FILES)
    if request.method == 'POST':
        form=AddAllifChartOfAccountForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect('logistics:add_show_chart_of_account')
    else:
        form=AddAllifChartOfAccountForm()
    context={
        "chart_of_accounts":chart_of_accounts,
        "form":form,
        "title":title,
        
    }
    return render(request,'accounts/chart-of-accounts.html',context)
@login_required(login_url='login:loginpage')
def delete_chart_of_account(request,pk):
    AllifChartOfAccountsModel.objects.get(id=pk).delete()
    return redirect('logistics:add_show_chart_of_account')


##############################################
@login_required(login_url='login:loginpage')
def add_show_drivers(request):
    title="Drivers"
    drivers=AlwenDriversModel.objects.all()
    form=AdddriversForm(request.POST, request.FILES)
    if request.method=="POST":
        form=AdddriversForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("logistics:add_show_drivers")
    
    mycontext={
        "form":form,
        "drivers":drivers,
        "title":title,
    
    }
    return render(request,'drivers/drivers.html',mycontext)
@login_required(login_url='login:loginpage')
def delete_driver(request,pk):
    
    try:
        AlwenDriversModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('logistics:add_show_drivers')

    return redirect('logistics:add_show_drivers')
@login_required(login_url='login:loginpage')
def update_driver(request,pk):
    title="Update Driver"
    update= AlwenDriversModel.objects.get(id=pk)
    form= AdddriversForm(instance=update)
   
    if request.method == 'POST':
        form= AdddriversForm(request.POST, instance=update)
        if form.is_valid():
            form.save()
          
            return redirect('logistics:add_show_drivers')#just redirection page

    context = {
		'form':form,
        "title":title,
        
    }
    
    return render(request, 'drivers/drivers.html', context)#th

    ################################ CARDS ########################################
@login_required(login_url='login:loginpage')
def cards(request):
    title="Cards"
    cards=CardsModel.objects.all()
    form=AddCardsForm()
    if request.method == 'POST':
        form= AddCardsForm(request.POST)
        if form.is_valid():
            form.save()
          
            return redirect('logistics:cards')#just redirection page
    
    context = {
		'form':form,
        "cards":cards, 
        "title":title,
        
    }
    return render(request,'cards/cards.html',context)
@login_required(login_url='login:loginpage')
def update_card(request,pk):
    title="Update Card"
    update= CardsModel.objects.get(id=pk)
    form= AddCardsForm(instance=update)
   
    if request.method == 'POST':
        form= AddCardsForm(request.POST, instance=update)
        if form.is_valid():
            form.save()
          
            return redirect('logistics:cards')#just redirection page

    context = {
		'form':form,
        "title":title,
        
    }
    
    return render(request, 'cards/cards.html', context)#th
@login_required(login_url='login:loginpage')   
def deleteCard(request,pk):
    CardsModel.objects.get(id=pk).delete()
    return redirect('logistics:cards')
@login_required(login_url='login:loginpage')
def topUpCard(request,pk):
    title="Top Up Card"
    try:
        card=CardsModel.objects.get(id=pk)#very important to get id to go to particular shipment
        initial_balance=card.balance#this gives the initial account
    except:
        return HttpResponse("Sorry there is a problem ! ")
    
    
    form=AddCardTopUpsForm()
    top_up_card= get_object_or_404(CardsModel, id=pk)


    topups= CardsTopUpsModel.objects.filter(card=card)#this line helps to
    print(card.id)
    card_total = 0.0
    if len(topups) > 0:
        for payment in topups:
            amount= float(payment.amount) 
            card_total += amount

    
    add_item= None
    if request.method == 'POST':
        form=AddCardTopUpsForm(request.POST)
        if form.is_valid():
            add_item= form.save(commit=False)
            add_item.card=top_up_card
            add_item.save()
            myamount=request.POST.get('amount')
           
            mycard=CardsModel.objects.get(id=card.id)# returns TO objects
            mycard.balance= int(initial_balance)+int(myamount)
            mycard.save()
            return redirect('logistics:topUpCard',pk=pk)#just redirection page

    context={
        "form":form,  
        "card":card,
        "topups":topups,
        "card_total":card_total,
        "title":title,
       

    }
    return render(request,'cards/cardtopups.html',context)
@login_required(login_url='login:loginpage')
def delete_top_up(request,pk):
    CardsTopUpsModel.objects.get(id=pk).delete()
    return redirect('logistics:cards')
