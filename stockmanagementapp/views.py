from ctypes import Union
from typing import NewType
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages

from allifmaalapp.models import *

from stockmanagementapp.models import PhysicalStockModel#this is important for the pagination
from .forms import *
from uuid import uuid4
from .resources import PhysicalStockResource
import csv
from django.contrib.auth.models import User

#start of important imports for converting html page to pdf
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import *
from django.shortcuts import get_object_or_404
#end of important imports for converting html page to pdf
from logistics.models import AlwenAssetsModel


# Create your views here.
###################################### DASHBOARD SECTION#################################################33.
def stock_dashboard(request):
    title="Inventory dashboard"
    total_stock=PhysicalStockModel.objects.all().count()
    stock=PhysicalStockModel.objects.all()
    total_stores=StoresModel.objects.all().count()
    payments=AllifCustomerPaymentsModel.objects.all()
    expenses=AllifmaalExpensesModel.objects.all()
    assets=AlwenAssetsModel.objects.all()
    customers=AllifmaalCustomersModel.objects.all()
    mycontext={
        "title":title,
        "total_stock":total_stock,
        "stock":stock,
        "total_stores":total_stores,
        "payments":payments,
        "expenses":expenses,
        "assets":assets,
        "customers":customers,
    }

    return render (request,'dashboard/stock-dashboard.html',mycontext)
def error_page(request):
    context={

    }
    return render(request,'error/error-page.html',context)
def stock(request):
    title="Physical Stock Management System "
    header="Inventory Management System"
    form =AddPhysicalProductForm(request.POST or None)
    
    physical_products=PhysicalStockModel.objects.all()
    
    if form.is_valid():
        form.save()
        messages.success(request, 'Stock added successfully')
        form=AddPhysicalProductForm()
    else:
       form.non_field_errors
    
    pagination=Paginator(PhysicalStockModel.objects.all(),10)
    page=request.GET.get('page')
    physical_products=pagination.get_page(page)
    page_num="a"*physical_products.paginator.num_pages

    context = {
        "title":title,
        "form":form,
        "physical_products":physical_products,
        "header":header,
        "page_num":page_num,
      
    }

    return render(request,'stock/stock.html',context)

#this view is for showing the full details of a stock item/line
def productFullDetails(request,pk):
    title="Product details"
    product =PhysicalStockModel.objects.get(id=pk)
    context={"product":product,"title":title,}
    return render(request,"stock/productDetails.html",context)


def deletePhysicalStockItem(request,pk):
    try:
        PhysicalStockModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('stockmanagementapp:stock')

    return redirect('stockmanagementapp:stock')

    
#@allowed_users(allowed_roles=['admin'])
def updatePhysicalStock(request, pk):
    updateStockItem= PhysicalStockModel.objects.get(id=pk)
    form = AddPhysicalProductForm(instance= updateStockItem)#insert the content of the table stored in the selected id in the update form
    #we could have used the add customer form but the validation will refuse us to update since fields may exist
    if request.method == 'POST':
        form = AddPhysicalProductForm(request.POST, instance= updateStockItem)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock item updated successfully')
            return redirect('stockmanagementapp:stock')#just redirection page
    context = {
		'form':form,
        "updateStockItem":updateStockItem,
    }
    return render(request,'stock/updatePhysicalStock.html',context)

def issueOrReceiveItems(request, pk):
    header="Receive or issue stock items "
    item =PhysicalStockModel.objects.get(id=pk)

    context = {
        "header":header,

		"item": item,

	}
    return render(request,'stock/issueOrReceivePhysicalStock.html',context)


def issuePhysicalStockItems(request, pk):
    item =PhysicalStockModel.objects.get(id=pk)
    form = IssuePhysicalItemsForm(request.POST or None, instance=item)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receivedQuantity=0
        instance.quantity -= instance.issuedQuantity#deduct the issued items from those in stock
        instance.issuedBy=str(request.user)
        instance.save()

        # 7th August 2021...start of my own code trying to store the issued items in their own database called IssuedPhysicalStockTable
        items =PhysicalStockModel.objects.get(id=pk)
        form = IssuePhysicalItemsForm(request.POST or None, instance=items)
        issued=IssuedPhysicalStockModel(description=instance.description,issuedQuantity=instance.issuedQuantity, issuedTo=instance.issuedTo)
        issued.save()
        #end of the above 7th August 2021

        return redirect('stockmanagementapp:stock')

    context = {
		"title": 'Issue ' + str(item.partNumber),
		"item": item,
		"form": form,
	}
    return render(request,'stock/issueOrReceivePhysicalStock.html',context)


def receivePhysicalStockItems(request, pk):
    item= PhysicalStockModel.objects.get(id=pk)
    form = ReceivePhysicalItemsForm(request.POST or None, instance=item)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issuedQuantity=0
        instance.quantity +=instance.receivedQuantity
        instance.receiveBy=str(request.user)
        instance.save()

         # 7th August 2021...start of my own code trying to store the issued items in their own database called IssuedPhysicalStockTable
        query_table_content =PhysicalStockModel.objects.get(id=pk)
        form = ReceivePhysicalItemsForm(request.POST or None, instance=query_table_content)
        issued=IssuedPhysicalStockModel(description=instance.description,receivedQuantity=instance.receivedQuantity)
        issued.save()
        #end of the above 7th August 2021

        query_table_content =PhysicalStockModel.objects.get(id=pk)
        form = ReceivePhysicalItemsForm(request.POST or None, instance=query_table_content)
       
        return redirect('stockmanagementapp:stock')
    context = {
			"title": 'Receive ' + str(item.partNumber),
			"item": item,
			"form": form,
			#"username": 'Receive By: ' + str(request.user),
		}
    return render(request,'stock/issueOrReceivePhysicalStock.html',context)

def issuedPhysicalStockHistory(request):
    title="Stock history"
    issuedItem=IssuedPhysicalStockModel.objects.all()
    context={"issuedItem":issuedItem,"title":title,}

    return render(request,"stock/issued_stock_history.html",context)

def deletePhysicalStockHistory(request,pk):
    try:
        IssuedPhysicalStockModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('stockmanagementapp:issued-stock-history')

    return redirect('stockmanagementapp:issued-stock-history')

def purchase_orders_list(request):
    mypos=PurchaseOrdersModel.objects.all()
    context={
        "mypos":mypos,

    }
    return render(request,'stock/po-list.html',context)

def create_new_po(request):

    last_po = PurchaseOrdersModel.objects.all().order_by('id').last()
    last_obj=PurchaseOrdersModel.objects.last()
    if last_obj:
        
        last_obj_id=last_obj.id
        last_obj_incremented=last_obj_id+1
   
    #purchaseNumber= 'LPO/AMEL-'+str(uuid4()).split('-')[1]
        purchaseNumber= 'LPO/AMEL/'+str(uuid4()).split('-')[1]+'/'+str(last_obj_incremented)
        print(purchaseNumber)
    else:
        
       purchaseNumber= 'LPO/AMEL/'+str(uuid4()).split('-')[1]
        #purchaseNumber= 'LPO/AMEL-'+str(uuid4()).split('-')[1]+'/'+str("Reset")

    newPurchaseOrder= PurchaseOrdersModel.objects.create(po_number=purchaseNumber)
    newPurchaseOrder.save()
    return redirect('stockmanagementapp:purchase-orders')

def delete_po(request,pk):
    PurchaseOrdersModel.objects.get(id=pk).delete()
    return redirect("stockmanagementapp:purchase-orders")


def add_po_details(request,pk):
    po_details=PurchaseOrdersModel.objects.filter(id=pk)
    try:
        my_po_id=PurchaseOrdersModel.objects.get(id=pk)
        
    except:
        messages.error(request, 'Something went wrong and could not get the invoice')
        return redirect("stockmanagementapp:purchase-orders")

    po_Items = PurchaseOrderItemsModel.objects.filter(po_item_con=my_po_id)#this line helps to
    #show items that belong to that particular invoice in that particular invoice
    inv_id= get_object_or_404(PurchaseOrdersModel, id=pk)#this helps to fill that select field and invoice fields and content
    
    form=addPODetailForm(instance=my_po_id)
    if request.method == 'POST':
        #add_shipment_items_form=AddShippmentItemsForm(request.POST)
        form=addPODetailForm(request.POST,request.FILES,instance=my_po_id)
        if form.is_valid():
            form.save()
            print(request.POST)
            print("I have saved and itts correct")
            return redirect('stockmanagementapp:add_po_items_allif',pk=pk)#just redirection page

        
    shipment_context={
        
        "form":form,
        "po_Items":po_Items,
        "po_details":po_details,
        
        

    }
    return render(request, 'stock/add-po-details.html', shipment_context)#th


def add_po_items_allif(request,pk):
    title="Tasks"
    qaanshegto =PurchaseOrdersModel.objects.get(id=pk)#very important to get id to go to particular shipment
    form=addPOItemsForm()
    add_inv= get_object_or_404(PurchaseOrdersModel, id=pk)

    po_Items = PurchaseOrderItemsModel.objects.filter(po_item_con=qaanshegto)#this line helps to
    
    add_item= None
    if request.method == 'POST':
        form=addPOItemsForm(request.POST)
        if form.is_valid():
            add_item= form.save(commit=False)
            add_item.po_item_con=add_inv
            add_item.save()
           # return HttpResponse(post)
            return redirect('stockmanagementapp:add_po_items_allif',pk=pk)#just redirection page

    shipment_context={
   
            "form":form,
            "title":title,
            "qaanshegto":qaanshegto,
            "add_inv":add_inv,
            "po_Items":po_Items,
             
    }
    return render(request, 'stock/add-items-to-po.html', shipment_context)#t
def delete_po_item(request,pk):
    PurchaseOrderItemsModel.objects.get(id=pk).delete()
    return redirect("stockmanagementapp:purchase-orders")


def posting_po(request,pk):
    purchases=PurchaseOrdersModel.objects.filter(id=pk)#this is important to add the posting link to this page
    
    for item in purchases:
        myuplift=item.uplift######## this gives the uplift of the PO
        freightcost=item.shipping#######333 this gives the shipping cost of the PO
    try:
        myPO=PurchaseOrdersModel.objects.get(id=pk)
        thisistesting=myPO.purchaseordersmodel_set.all()
    except:
        messages.error(request, 'Something went wrong and could not get the invoice')

    poItems = PurchaseOrderItemsModel.objects.filter(po_item_con=myPO)#fi
    line_amount_sums=0
    for item in poItems:
        item_unit_cost=item.unitcost#this gets the unit cost of the individual items
        quantity=item.quantity#this gets the quantity of the individual items
        line_amount=item_unit_cost*quantity#this gives product of quantity and unit price per line
        line_amount_sums+=line_amount
        potential_selling_price=item_unit_cost*myuplift####### this gives the selling price
        products=PhysicalStockModel.objects.get(description=item.items)
        products.unitPrice=potential_selling_price
        products.quantity=item.quantity
        products.unitcost=item.unitcost
        products.save()
    
    total_PO_cost=line_amount_sums# this gives the sum of all the lines of the PO..

    ##########3######################### start of cost abortionment #########################################
    value=0
    for it in poItems:
        item_unit=it.unitcost
        quantity=it.quantity
        lamount=item_unit*quantity
        value+=lamount
        line_abortioned_cost=(lamount/total_PO_cost)*freightcost#abortioned cost per line
        per_unit_abortioned_cost=float(line_abortioned_cost/it.quantity)#this gives the abortioned cost per unit
        unit_total_cost=float(per_unit_abortioned_cost+it.unitcost)#this gives the unit total cost including FOB cost and abortioned freight cost
        line=PhysicalStockModel.objects.get(description=it.items)
        line.unitPrice=float(unit_total_cost*myuplift)
        line.unitcost= unit_total_cost
        line.save()
    ######################################## end of cost abortionment section #############################

    return redirect('stockmanagementapp:purchase-orders')

##################################3 file upload section##################33
def upload_file_view(request):
    form=AddCSVFileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form=AddCSVFileForm()
        obj=Csv.objects.get(activated=False)

        # now we need to read the data
        with open(obj.file_name.path,'r') as f:
            reader=csv.reader(f)
            for i, row in enumerate(reader):
                if i==0:
                    pass
                else:
                   
                    product=row[0].upper()
                    

                    #user=User.objects.get(username=row[1])
                    print(row)
                    print(type(row))
                    Sale.objects.create(
                        product=product,
                        quantity=int(row[1]),
                        #salesman=user,
                    )
        obj.activated=True
        obj.save()

    context={
        "form":form,
    }
    return render(request,'files/upload-file.html',context)

   
   #####################################################################################################3
   ################3 testing ##################
from django.shortcuts import render
from django.http import HttpResponse
from .resources import PersonResource,PhysicalStockResource
from tablib import Dataset
from .models import Person

def export_stock(request):
    person_resource = PhysicalStockResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="zamzam-stock.xls"'
    return response

def simple_reference_upload(request):#######3 this upload function is working well and can be used as reference
    persons=Person.objects.all()
    if request.method == 'POST':
        person_resource = PersonResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read(),format='xlsx')
        #print(imported_data)
        for data in imported_data:
            print(data[1])
            value = Person(
        		data[0],
        		data[1],
        		 data[2],
        		 data[3],
                data[4],
                #data[5],
                #data[6],
                 #data[7],
                  #data[8],
                 #data[9]
                
        		)
            value.save()       
        
        #result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        #if not result.has_errors():
        #    person_resource.import_data(dataset, dry_run=False)  # Actually import now
    context={
        "persons":persons,
    }

    return render(request, 'simpleupload/simple-upload.html',context)


def upload_stock(request):#######3 this upload function is working well and can be used as reference
    items=PhysicalStockModel.objects.all()
    try:
        if request.method == 'POST':
            person_resource = PhysicalStockResource()
            dataset = Dataset()
            new_persons = request.FILES['myfile']
            imported_data = dataset.load(new_persons.read(),format='xlsx')
            for data in imported_data:
                print(data[1])
                value = PhysicalStockModel(
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    
                    )
                value.save()       
        
            #result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

            #if not result.has_errors():
            #    person_resource.import_data(dataset, dry_run=False)  # Actually import now
    except:
        return HttpResponse("Sorry there was a problem! ")
    context={
        "items":items,
    }

    return render(request, 'stock/stock-upload.html',context)

###########################################################################################################
########################## below is for transfers of stores to other stores ###############################
def stores(request):
    stores=StoresModel.objects.all()
    add_store_form=AddStoreForm()
    if request.method=="POST":
        add_store_form=AddStoreForm(request.POST)
        if add_store_form.is_valid():
            add_store_form.save()
            return redirect("stockmanagementapp:stores")
    stores_context={
        "stores":stores,
        "add_store_form":add_store_form,

    }
    return render(request,'store/stores.html',stores_context)

def update_store(request,pk):
    update_store=StoresModel.objects.get(id=pk)
    add_store_form=AddStoreForm(instance=update_store)
    if request.method=="POST":
        add_store_form=AddStoreForm(request.POST,instance=update_store)
        if add_store_form.is_valid():
            add_store_form.save()

        return redirect("stockmanagementapp:stores")
    stores_context={
        "stores":stores,
        "add_store_form":add_store_form,

    }
    return render(request,'store/stores.html',stores_context)

def delete_store(request,pk):
    delete_store=StoresModel.objects.get(id=pk).delete()
    print(delete_store)
    return redirect("stockmanagementapp:stores")


def add_stock_to_store(request,pk):
    the_store=StoresModel.objects.get(id=pk)#this returns the name of the clicked store
    selected_store= get_object_or_404(StoresModel, id=pk)#this line returns also the name of the selected store
    add_stock_to_store_form= AddItemsToStoreForm()

    add_to_store= None
    if request.method == 'POST':
        add_stock_to_store_form=AddItemsToStoreForm(request.POST)
        if add_stock_to_store_form.is_valid():
            add_to_store=add_stock_to_store_form.save(commit=False)

            add_to_store.store = selected_store
           
            add_to_store.save()
            messages.success(request, 'Record added successfully...')
            add_stock_to_store_form=AddItemsToStoreForm()
            return redirect("stockmanagementapp:add-stock-to-store",pk=pk)
    context={
        "add_stock_to_store_form":add_stock_to_store_form,
        "the_store":the_store,
        
    }
    return render(request,'store/add-stock-store.html',context)
def delete_store_item(request,pk):
    StoreItemsModel.objects.get(id=pk).delete()
    return redirect("stockmanagementapp:stores")

def transfer_orders_list(request):
    transfers=TransferOrdersModel.objects.all()
   
    context={
        "transfers":transfers,

    }
    return render(request,'transfers/transfer-orders-list.html',context)

def create_new_transfer_order(request):
    new_Trans_ord= 'TRANSORD/LOCAL/-'+str(uuid4()).split('-')[1]
    new_TO= TransferOrdersModel.objects.create(transfer_order_no=new_Trans_ord)
    new_TO.save()
    print(new_TO.transfer_order_no)
    return redirect('stockmanagementapp:transfer-orders')

def delete_transfer_order(request,pk):
    delete_trf=TransferOrdersModel.objects.get(id=pk).delete()
    return redirect("stockmanagementapp:transfer-orders")

def add_transfer_order_details(request,pk):
    trans_or=TransferOrdersModel.objects.get(id=pk)
    try:
        trans_ord_id=TransferOrdersModel.objects.get(id=pk)
    except:
        messages.error(request, 'Something went wrong and could not add details to the transfer order')
       
    transfer_order_related_objects= get_object_or_404(TransferOrdersModel, id=pk)
    
    add_to_details_form=AddTransferOderDetailsForm(instance=trans_ord_id)
    
    if request.method == 'POST':
        add_to_details_form=AddTransferOderDetailsForm(request.POST,instance=trans_ord_id)
        if add_to_details_form.is_valid():
            add_to_details_form.save()

            fields_content=request.POST
            print(fields_content)

            #return redirect('stockmanagementapp:add-items-to-transfer-order',pk=pk)
            return redirect('stockmanagementapp:add-details-to-transfer-order',pk=pk)
            
    context={
        "add_to_details_form":add_to_details_form,
        "trans_or":trans_or,
        "transfer_order_related_objects":transfer_order_related_objects,
    }
    return render(request,'transfers/add_to_details.html',context)

def add_items_to_transfer_order(request,pk):

    try:
        myTO=TransferOrdersModel.objects.get(id=pk)
    except:
        messages.error(request, 'Something went wrong and could not get the invoice')
    toItems = TransferOderItemsModel.objects.filter(testtoitemsconnector=myTO)#fi
    
    trans_id= get_object_or_404(TransferOrdersModel, id=pk)#this helps to fill that select field
    add_items_to_TO_Form=AddItemsToTransferOrderForm()
   
    if request.method == 'POST':
        add_items_to_TO_Form=AddItemsToTransferOrderForm(request.POST)
        
        if add_items_to_TO_Form.is_valid():
            poOrderItems = add_items_to_TO_Form.save(commit=False)
            poOrderItems.testtoitemsconnector= trans_id
            poOrderItems.save()
            return redirect("stockmanagementapp:add-items-to-transfer-order",pk=pk)
        
    context={
        "add_items_to_TO_Form":add_items_to_TO_Form,
       
        "toItems":toItems,
        "myTO":myTO,

    }
    return render(request,'transfers/add_items_to_transfer_order.html',context)
def delete_transfer_order_item(request,pk):
    TransferOderItemsModel.objects.get(id=pk).delete()
    return redirect('stockmanagementapp:transfer-orders')


def post_transfer_order(request,pk):############3 THIS IS WORKING
    myTO =TransferOrdersModel.objects.get(id=pk)
    trns_ord_id=myTO.id#returns the ID of the TO
    from_store_id=myTO.from_store#this returns the name of the transfering store
    to_store_id=myTO.to_store#returns the name of the receiving store
    from_items_stock=StoreItemsModel.objects.filter(store=from_store_id)#returns all the items of transfering store
    to_items_stock=StoreItemsModel.objects.filter(store=to_store_id)#returns all the items of receiving store
    testitems=TransferOderItemsModel.objects.filter(testtoitemsconnector=myTO)
    if testitems:

        for items in testitems:
            try:
                products=PhysicalStockModel.objects.get(id=items.item.description.id)#returns TO objects
                products.quantity= int(products.quantity - items.quantity)
                #products.save()
                
                products2=PhysicalStockModel.objects.get(description=items.item.description.description)# returns TO objects
                products2.quantity= int(products2.quantity - items.quantity)
                products2.save()

                from_store_transf_ord_items=StoreItemsModel.objects.get(store=from_store_id, description=items.item.description)# returns TO objects
                from_store_transf_ord_items.quantity=int(from_store_transf_ord_items.quantity - items.quantity)
                from_store_transf_ord_items.save()
                to_store_trans_ord_items=StoreItemsModel.objects.get(store=to_store_id, description=items.item.description)
                to_store_trans_ord_items.quantity=int(to_store_trans_ord_items.quantity + items.quantity)
                to_store_trans_ord_items.save()

                trans_ord_items_IDS=items.item.id#returns IDs of transfer order stock lines
                trans_ord_ref=TransferOrdersModel.objects.get(transfer_order_no=items.testtoitemsconnector.transfer_order_no)#returns TO ref
                my_TO_lines=StoreItemsModel.objects.filter(store=items.testtoitemsconnector.from_store)#returns queryset of all the items of the TO from the transfering store
                all_values=StoreItemsModel.objects.filter(store=items.testtoitemsconnector.from_store).values()#returns all values
                all_quantities=StoreItemsModel.objects.filter(store=items.testtoitemsconnector.from_store).values_list('quantity')#returns all quantities of transfering store
               
       
            except:
                return HttpResponse("Please ensure both stores are selected in the TRF and that all items are in both stores before posting this TRF...")
        
        print("___________________________________________________")
    else:
        return HttpResponse("Please add items to the transfer order first then post the transfer order...")
     
      
    transfer_order_stock_lines= TransferOderItemsModel.objects.filter(testtoitemsconnector=myTO)#fi
   
    common_items1 = from_items_stock.filter(
                       description__in=transfer_order_stock_lines.values_list('item', flat=True))
    common_items2 = transfer_order_stock_lines.filter(
                       item__in=from_items_stock.values_list('description', flat=True))
    
    try:
        from_store_id_needed=myTO.from_store.id#this returns the id of the transfering store
        to_store_id_needed=myTO.to_store.id#returns the id of the receiving store
        from_store_name=myTO.from_store.name#returns name of transfering store
        to_store_name=myTO.to_store.name#returns name of receiving store
    except:
        return HttpResponse("Please select both transfering and receiving stores in order to post the transfer order...")
    

    return redirect("stockmanagementapp:transfer-orders")



def allifmaal_purchase_order_pdf(request,pk):
    system_user=request.user
    invoice_details=get_object_or_404(TransferOrdersModel,id=pk)
    try:
        inv_number= TransferOrdersModel.objects.get(id=pk)
    except:
        messages.error(request, 'Something went wrong')

    transfer_order_items= TransferOderItemsModel.objects.filter(testtoitemsconnector=inv_number)
    
    template_path = 'transfers/po-pdf.html'
    companyDetails=AllifmaalDetailsModel.objects.all()
    scope=AllifmaalScopeModel.objects.all()
    
    context = {
    'invoice_details':invoice_details,
    "transfer_order_items":transfer_order_items,
    "companyDetails":companyDetails,
    "scope":scope,
   
   "system_user":system_user,
   "inv_number":inv_number,
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



####################################################333 sales section #########################################

def enterprise_resource_management(request):
    total_stock=PhysicalStockModel.objects.all().count()
    stock=PhysicalStockModel.objects.all()
    total_stores=StoresModel.objects.all().count()
    payments=AllifCustomerPaymentsModel.objects.all()
    expenses=AllifmaalExpensesModel.objects.all()
    assets=AlwenAssetsModel.objects.all()
    customers=AllifmaalCustomersModel.objects.all()
    context={
        
        "total_stock":total_stock,
        "stock":stock,
        "total_stores":total_stores,
        "payments":payments,
        "expenses":expenses,
        "assets":assets,
        "customers":customers,
    }
    
    return render(request,'erm/erm-dashboard.html',context)
def allif_invoices_list(request):
    invoices=AllifInvoicesModel.objects.all()
    posted_true=AllifInvoicesModel.objects.filter(posted=True)
    inv_items=AllifInvoiceItemsModel.objects.all()
    am=0
    for item in inv_items:
        am+=item.selling_price
       
        #print(item.price)
    grand_sum_all_invoices=am
    
    sepco_inv_context={
        "invoices":invoices,
        "grand_sum_all_invoices":grand_sum_all_invoices,
        "posted_true":posted_true,

    }
    return render(request,'invoices/invoices_list.html',sepco_inv_context)

def AllifNewInvoice(request):
    last_po = AllifInvoicesModel.objects.all().order_by('id').last()
    last_obj=AllifInvoicesModel.objects.last()
    if last_obj:
        
        last_obj_id=last_obj.id
        last_obj_incremented=last_obj_id+1
   
    #purchaseNumber= 'LPO/AMEL-'+str(uuid4()).split('-')[1]
        invNumber= 'INV/AMEL/'+str(uuid4()).split('-')[1]+'/'+str(last_obj_incremented)
        
    else:
        
       invNumber= 'INV/AMEL/'+str(uuid4()).split('-')[1]
        #purchaseNumber= 'LPO/AMEL-'+str(uuid4()).split('-')[1]+'/'+str("Reset")

    newInvNo= AllifInvoicesModel.objects.create(number=invNumber)
    newInvNo.save()
    return redirect('stockmanagementapp:allif_invoices_list')

def AllifDeleteInvoice(request,pk):
    AllifInvoicesModel.objects.get(id=pk).delete()
    return redirect("stockmanagementapp:allif_invoices_list")



def AllifInvDetails(request,pk):
    invoices=AllifInvoicesModel.objects.filter(id=pk)
    try:
        my_invoice_id=AllifInvoicesModel.objects.get(id=pk)
        
    except:
        #messages.error(request, 'Something went wrong and could not get the invoice')
        return redirect("stockmanagementapp:allif_invoices_list")

    inv_Items = AllifInvoiceItemsModel.objects.filter(invitemcon=my_invoice_id)#this line helps to
    #show items that belong to that particular invoice in that particular invoice
    inv_id= get_object_or_404(AllifInvoicesModel, id=pk)#this helps to fill that select field and invoice fields and content
    
    invform=AddAllifInvoiceForm(instance=my_invoice_id)

    if request.method == 'POST':
        #add_shipment_items_form=AddShippmentItemsForm(request.POST)
        invform=AddAllifInvoiceForm(request.POST,instance=my_invoice_id)
        if invform.is_valid():
            invform.save()
            print(request.POST)
            print("I have saved and itts correct")
            return redirect('stockmanagementapp:AllifAddItemsInvoice',pk=pk)#just redirection page
    context={
        
        "invform":invform,
        "inv_Items":inv_Items,
        "invoices":invoices,
        "my_invoice_id":my_invoice_id,
        

    }
    return render(request, 'invoices/addinvdetails.html', context)#th

def AllifAddItemsInvoice(request,pk):
    invoices=AllifInvoicesModel.objects.filter(id=pk)
    try:
        my_invoice_id=AllifInvoicesModel.objects.get(id=pk)
    except:
        messages.error(request, 'We are really sorry, something went wrong!')
        return redirect("stockmanagementapp:error_page")

    inv_Items = AllifInvoiceItemsModel.objects.filter(invitemcon=my_invoice_id)
    inv_id= get_object_or_404(AllifInvoicesModel, id=pk)

    itemsform= AddAllifInvoiceItemsForm()
    invoiceTotal = int(0)
    if len(inv_Items) > 0:
        for product in inv_Items:
            quantityTimesUnitPrice = product.quantity * product.description.unitPrice
            invoiceTotal += quantityTimesUnitPrice
   
    if request.method == 'POST':
        itemsform= AddAllifInvoiceItemsForm(request.POST)

        if itemsform.is_valid():
            additems= itemsform.save(commit=False)
            additems.invitemcon= inv_id
            additems.save()
            return redirect('stockmanagementapp:AllifAddItemsInvoice',pk=pk)
       
    context={
        
        "itemsform":itemsform,
        "inv_id":inv_id,
        "inv_Items":inv_Items,
        "invoiceTotal":invoiceTotal,
        "invoices":invoices,
        "my_invoice_id":my_invoice_id,
    }
    return render(request,'invoices/addItemsInvoice.html',context)
def delete_invoice_item(request,pk):
    AllifInvoiceItemsModel.objects.get(id=pk).delete()
    return redirect("stockmanagementapp:allif_invoices_list")

def allif_invoice_posting_view(request,pk):
    try:
        myInv =AllifInvoicesModel.objects.get(id=pk)
        print(myInv.posted)
        mycustomer=myInv.customer
    
    except:
        messages.error(request, 'Something went wrong')
        return redirect('stockmanagementapp:error_page')
        
    InvPharmItems = AllifInvoiceItemsModel.objects.filter(invitemcon=myInv)#fi

    invoiceTotal = int(0)
    if len(InvPharmItems) > 0:
        for product in InvPharmItems:
            quantityTimesUnitPrice = product.quantity * product.description.unitPrice
            invoiceTotal += quantityTimesUnitPrice
    
    if myInv.status=='Paid':
   
        for items in InvPharmItems:
            products=PhysicalStockModel.objects.get(id=items.description.id)
            if items.description.quantity>items.quantity:
                stock_quantities=items.description.quantity
                invoice_quantities=items.quantity
                products.quantity= int(items.description.quantity - items.quantity)
                products.save()
                myInv.posted=True
                myInv.save()
                posted_inv, created = AllifPostedSalesInvoicesModel.objects.get_or_create(inv_no=myInv,customer=mycustomer,inv_total_value=invoiceTotal)
            else: 
                message=messages.error(request, 'Something went wrong')
                return HttpResponse("Quantities in stock are not enough to enable posting")
                return redirect('stockmanagementapp:allif_invoices_list')
    
    if myInv.status=='Current':
        for items in InvPharmItems:
            products=PhysicalStockModel.objects.get(id=items.description.id)
            products.quantity= int(items.description.quantity + items.quantity)
            #products.save()
            
    
    return redirect('stockmanagementapp:allif_posted_invoices_list')

def allif_posted_invoices_list(request):
    posted_invoices=AllifPostedSalesInvoicesModel.objects.all()
    context={
        "posted_invoices":posted_invoices,
    }
    return render(request,'invoices/posted-invoices.html',context)
    
def Allif_delete_posted_invoice(request,pk):
    AllifPostedSalesInvoicesModel.objects.get(id=pk).delete()
    return redirect('stockmanagementapp:allif_posted_invoices_list')

def AllifInvpdf(request,pk):
    system_user=request.user
    invoice_details=get_object_or_404(AllifInvoicesModel,id=pk)
    try:
        inv_number= AllifInvoicesModel.objects.get(id=pk)
    except:
        #messages.error(request, 'Something went wrong')
         return redirect("stockmanagementapp:allif_invoices_list")

    invoiceItems = AllifInvoiceItemsModel.objects.filter(invitemcon=inv_number)
    
    
    invoiceTotal = 0.0
    if len(invoiceItems) > 0:
       for x in invoiceItems:
            y = float(x.quantity) * float(x.description.unitPrice)
            invoiceTotal += y
    template_path = 'invoices/allif-inv-pdf.html'
    companyDetails=AllifmaalDetailsModel.objects.all()
    scope=AllifmaalScopeModel.objects.all()
    sepcologo=AllifmaalDetailsModel.objects.all()
    context = {
    'invoice_details':invoice_details,
   "invoiceItems":invoiceItems,
   "companyDetails":companyDetails,
   "invoiceTotal":invoiceTotal,
   "scope":scope,
   "system_user":system_user,
   "sepcologo":sepcologo,
   "inv_number":inv_number,
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Allif-invoice.pdf"'
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

def allif_add_show_expenses(request):
    expenses=AllifExpensesModel.objects.all()

    form=AllifAddExpensesForm(request.POST or None)
    if request.method =="POST":
        form=AllifAddExpensesForm(request.POST or None,request.FILES)
        if form.is_valid():
            form.save()
            form=AllifAddExpensesForm()
    
    payments=AllifExpensesModel.objects.all()
    value=0
    for amount in payments:
        value+=amount.amount
    total=value
    mycontext={
        
        "form":form,
        "expenses":expenses,
        "total":total,
        "value":value,
    }
    return render (request,'expenses/expenses.html',mycontext)


def deleteAllifExpenses(request,pk):
    AllifExpensesModel.objects.get(id=pk).delete()
    return redirect("stockmanagementapp:allif_add_show_expenses")

def allif_customerPayments(request):
    payments=AllifCustomerPaymentsModel.objects.all()
    balances=AllifCustomersBalanceModel.objects.all()

    value=0
    for amount in payments:
        value+=amount.amount
    total=value

    form=AllifAddCustomerPaymentsForm()
    if request.method=="POST":
        form=AllifAddCustomerPaymentsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("stockmanagementapp:allif_customerPayments")
    context={
        "form":form,
        "payments":payments,
        "total":total,
        "balances":balances,
        
    }

    return render(request,'erm/allif-payments.html',context)

def deleteAllifPayment(request,pk):
    AllifCustomerPaymentsModel.objects.get(id=pk).delete()
    return redirect("stockmanagementapp:allif_customerPayments")























    
    