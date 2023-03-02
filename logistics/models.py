from django.db import models
from django.utils import timezone
from django.template.defaultfilters import register, slugify
from uuid import uuid4
#from hrmapp.models import HRMModel
from django.http.response import HttpResponse

#from matplotlib.pyplot import cla
#Choice field
class CustomersModel(models.Model):

    Country = [
    ('Somalia', 'Somalia'),
     ('Somaliland', 'Somaliland'),
    ('Kenya', 'Kenya'),
     ('UAE', 'UAE'),
     ('Ethiopia', 'Ethiopia'),
     ('Other', 'Other'),
    ]
    name = models.CharField(null=True, blank=True, max_length=20)
    phone = models.CharField(null=True, blank=True, max_length=30)
    email= models.CharField(null=True, blank=True, max_length=100)
    country = models.CharField(choices=Country, blank=True, max_length=30)
    city= models.CharField(null=True, blank=True, max_length=30)
    address = models.CharField(null=True, blank=True, max_length=30)
    balance=models.DecimalField(max_digits=10,blank=True,null=True,decimal_places=2,default=0)
    contact = models.CharField(null=True, blank=True, max_length=30)
   

    def __str__(self):
        return '{}'.format(self.name)
        
class CustomerPaymentsModel(models.Model):
    
    customer= models.ForeignKey(CustomersModel,related_name="custpaymentreltedname",on_delete=models.SET_NULL,blank=True,null=True)
    amount= models.DecimalField(max_digits=10,blank=True,null=True,decimal_places=2,default=0)
    date=models.DateField(auto_now=True)
    comments=models.CharField(max_length=15,blank=True,null=True, default='comment')
    
    def __str__(self):
        return '{}'.format(self.customer)

primary_meter_options = (
		('Kilometers', 'Kilometers'),
		('Miles', 'Miles'),
	)
vehicle_type_options = (
		('Truck', 'Truck'),
		('Car', 'Car'),
        ('Pickup','Pickup'),
        ('Bus', 'Bus'),
        ('Trailer', 'Trailer'),
        ('Van','Van'),
        ('Tow Truck','Tow Truck'),
        ('Motorcycle','Motorcycle'),
	)
vehicle_status_options = (
		('Active', 'Active'),
		('Inactive', 'Inactive'),
	)
oil_options = (
		('Petrol', 'Petrol'),
		('Diesel', 'Diesel'),
        ('Electric', 'Electric')
	)

payment_options = (
		('KES', 'KES'),
		('USD', 'USD'),
        ('EURO', 'EURO')
	)

class AlwenDriversModel(models.Model):
  
    name= models.CharField(max_length=10,blank=True,null=True)
    photo=models.FileField(upload_to='logistics/images/vehicles/%Y/',null=True, blank=True)#save according to year
    driver_license=models.FileField(upload_to='logistics/images/vehicles/%Y/',blank=True,null=True)
    driver_id=models.FileField(upload_to='logistics/images/vehicles/%Y/',blank=True,null=True)
   
   
    def __str__(self):
        return '{}'.format(self.name)
    #below calculates the total selling price for the model
    
class AlwenVehiclesModel(models.Model):
    vehicle_image=models.ImageField(upload_to='logistics/images/vehicles/%Y/',null=True, blank=True)#save according to year
    vehicle_name = models.CharField(max_length=30, blank=True, null=True)
    vehicle_make = models.CharField(max_length=30, blank=True, null=True)
    vehicle_model = models.CharField(max_length=30, blank=True, null=True)
    year = models.CharField(max_length=30, blank=True, null=True)
    
    starting_odometer = models.IntegerField(default=0,blank=True,null=True)
    primary_meter = models.CharField(max_length=30, blank=True, null=True,choices=primary_meter_options,default='Kilometers')
    vehicle_type = models.CharField(max_length=30, blank=True, null=True,choices=vehicle_type_options)
    vehicle_status = models.CharField(max_length=30, blank=True, null=True,choices=vehicle_status_options)
    mydocument=models.FileField(upload_to='myfiles/',null=True, blank=True)
    oil_type= models.CharField(max_length=30, blank=True, null=True,choices=oil_options)
    oil_capacity=models.CharField(blank=True,null=True,max_length=30)
    #operator=models.CharField(blank=True,null=True,max_length=250)
    operator=models.ForeignKey(AlwenDriversModel,on_delete=models.SET_NULL,blank=True,null=True)
    fuel_usage= models.IntegerField(null=True, blank=True,default=0)
    
    comments=models.CharField(blank=True,null=True,max_length=30)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    
    def __str__(self):
    	return str(self.vehicle_name)# this will show up in the admin area

class AlwenDailyMileageModel(models.Model):
    vehicle=models.ForeignKey(AlwenVehiclesModel,on_delete=models.SET_NULL,blank=True,null=True,default=1)
    
    operator=models.ForeignKey(AlwenDriversModel,on_delete=models.SET_NULL,blank=True,null=True)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    starting_odometer=models.IntegerField(blank=True,null=True)
    ending_odometer=models.IntegerField(blank=True,null=True)
    notes=models.CharField(blank=True,null=True,max_length=20)

    def __str__(self):
    	return str(self.vehicle)#

class AlwenServiceDetailsModel(models.Model):
    service_number=models.CharField(max_length=30,blank=True,null=True)
    vehicle=models.ForeignKey(AlwenVehiclesModel,on_delete=models.SET_NULL,blank=True,null=True)
    date=models.DateField(blank=True,null=True,auto_now=True)
    odometer=models.IntegerField(blank=True,null=True)
   
    service_center= models.CharField(max_length=30, blank=True, null=True)

    service_cost=models.DecimalField(max_digits=10,blank=True,null=True,decimal_places=2,default=0)
    receipt=models.FileField(upload_to='myfiles/',blank=True,null=True)
    serviced_by=models.CharField(blank=True,null=True,max_length=20)
   
    notes=models.CharField(blank=True,null=True,max_length=20)

    def __str__(self):
        return str(self.service_number)#

class ServiceTasksModel(models.Model):
    task=models.CharField(max_length=20,blank=True,null=True)
    spares_cost=models.IntegerField(blank=True,null=True,default=0)
    labor_cost=models.IntegerField(blank=True,null=True,default=0)
    task_service_connector=models.ForeignKey(AlwenServiceDetailsModel,blank=True,null=True,on_delete=models.CASCADE,related_name='taskrelated')
    def __str__(self):
        return str(self.task)#
    
    @property
    def service_total_costs(self):
        service_total_cost=self.spares_cost+self.labor_cost
        return service_total_cost


class CarriersModel(models.Model):

    Carrier_Type= [
    ('Truck', 'Truck'),
	('Car', 'Car'),
    ('Pickup','Pickup'),
    ('Aeropplane','Aeropplane'),
    ('Ship','Ship'),
    ('Bus', 'Bus'),
    ('Trailer', 'Trailer'),
    ('Van','Van'),
    ('Bajaaj','Bajaaj'),
    ('Bike','Bike'),
    ('Other','Other'),
    
    ]
    Weight_Units=[
        ("KGs","KGs"),
        ("Ton","Ton"),
        ("Other","Other"),
    ]
    carrier= models.CharField(choices=Carrier_Type, blank=True, max_length=30)
    
    capacity = models.IntegerField(null=True, blank=True)
    unit= models.CharField(choices=Weight_Units,null=True, blank=True, max_length=20)
    
    owner = models.CharField(null=True, blank=True, max_length=30)
    phone = models.CharField(null=True, blank=True, max_length=30)
    email= models.CharField(null=True, blank=True, max_length=30)
    address = models.CharField(null=True, blank=True, max_length=30)
   
    def __str__(self):
        return '{}'.format(self.carrier)

class ShipmentsModel(models.Model):
    Shipment_Status=[
        ("Booked","Booked"),
        ("Loaded","Loaded"),
        ("Dispatched","Dispatched"),
        ("Enroute","Enroute"),
        ("Delivered","Delivered"),
        ("Unknown","Unknown"),
        ("Other","Other"),
    ]
    Transport_Mode=[
        ("Road","Road"),
        ("Air","Air"),
         ("Sea","Sea"),
    ]
    carrier= models.ForeignKey(AlwenVehiclesModel, blank=True, null=True, on_delete=models.SET_NULL,related_name='carrier_related')
    date= models.DateTimeField(null=True, blank=True)
    expected= models.DateTimeField(null=True, blank=True)
    status= models.CharField(choices=Shipment_Status,null=True, blank=True, max_length=20,default="Booked")
    origin= models.CharField(null=True, blank=True, max_length=20)
    destination= models.CharField(null=True, blank=True, max_length=20)
    via= models.CharField(choices=Transport_Mode,null=True, blank=True, max_length=20,default="Road")
    shipment_number= models.CharField(null=True, blank=True, max_length=20)
    comments=models.CharField(blank=True,null=True,max_length=30)
   
   
    
    def __str__(self):
         return '{}'.format(self.shipment_number)
    
   

    

class ShipmentItemsModel(models.Model):
   
    Weight_Units=[
        ("KGs","KGs"),
        ("Ton","Ton"),
    ]
    Dimension_Units=[
        ("m","m"),
        ("cm","cm"),
        ("mm","mm"),
    ]
    Payment_Status=[
        ("Paid","Paid"),
        ("Unpaid","Unpaid"),
    ]
    Consignment_Status=[
        ("Received","Received"), ("Booked","Booked"), ("Loaded","Loaded"),
         ("Dispatched","Dispatched"), ("Enroute","Enroute"),
          ("Delivered","Delivered"),
    ]
    Transport_Mode=[
        ("Road","Road"),
        ("Air","Air"),
         ("Sea","Sea"),
    ]
    shipment_items_connector= models.ForeignKey(ShipmentsModel, blank=True, null=True, on_delete=models.CASCADE,related_name='shipmentanditemrelatedname')
    consigner= models.ForeignKey(CustomersModel, blank=True, null=True, on_delete=models.CASCADE,related_name='consignerrelated')
    consignee= models.ForeignKey(CustomersModel, blank=True, null=True, on_delete=models.CASCADE,related_name='consigneerelated')
    details=models.CharField(blank=True,null=True,max_length=20)
    address=models.CharField(blank=True,null=True,max_length=30)
    
    weight=models.IntegerField(blank=True,null=True)
    units=models.CharField(choices=Weight_Units,blank=True,null=True,max_length=20,default="KGs")
    lenth=models.IntegerField(blank=True,null=True)
    width=models.IntegerField(blank=True,null=True)
    height=models.IntegerField(blank=True,null=True)
    dimension_units=models.CharField(choices=Dimension_Units,blank=True,null=True,max_length=20,default="CM")
    received= models.DateTimeField(null=True, blank=True)
    value=models.CharField(blank=True,null=True,max_length=20)
    rate=models.CharField(blank=True,null=True,max_length=20)
    payer= models.ForeignKey(CustomersModel, blank=True, null=True, on_delete=models.CASCADE,related_name='payerrelated')
    payment=models.CharField(choices=Payment_Status,default='Unpaid',blank=True,null=True,max_length=20)
    status=models.CharField(choices=Consignment_Status,default='Received',blank=True,null=True,max_length=20)
    
    destination= models.CharField(null=True, blank=True, max_length=20)
    comments= models.CharField(null=True, blank=True, max_length=20)
    
   
    def __str__(self):
        return '{}'.format(self.details)

 



class AlwenAssetsModel(models.Model):
  
    description=models.CharField(max_length=30,blank=True,null=True)
    value=models.FloatField(max_length=20,blank=True,null=True,default=0)
    lifespan=models.CharField(max_length=10,blank=True,null=True)
    acquired= models.DateField(blank=True, null=True)

   
    
    def __str__(self):
        return str(self.description)


class AlwenExpensesModel(models.Model):
  
    description=models.CharField(max_length=25,blank=True,null=True)
    amount=models.FloatField(max_length=20,blank=True,null=True,default=0)
    comments=models.CharField(max_length=20,blank=True,null=True)
   
    
    def __str__(self):
        return str(self.description)



class AlwenJobsModel(models.Model):
    job_status=[
        ("open","open"),
        ("completed","completed"),
    ]
    #first_cust=CustomersModel.objects.filter()[0]
  
    job_number=models.CharField(max_length=20,blank=True,null=True)
    customer= models.ForeignKey(CustomersModel, blank=True, null=True, on_delete=models.SET_NULL,related_name='jobcustrelname')
    description=models.CharField(max_length=30,blank=True,null=True)
    vehicle=models.ForeignKey(AlwenVehiclesModel,on_delete=models.SET_NULL,blank=True,null=True)
    driver=models.ForeignKey(AlwenDriversModel,blank=True,null=True,on_delete=models.SET_NULL)
    opened_date=models.DateField(blank=True,null=True,auto_now_add=True)
    ending_date=models.DateField(blank=True,null=True,auto_now_add=False)
    starting_odometer=models.IntegerField(blank=True,null=True,default=0)
    ending_odometer=models.IntegerField(blank=True,null=True,default=0)
    status= models.CharField(max_length=20, blank=True, null=True,choices=job_status,default="open")
    refernce=models.CharField(max_length=20,blank=True,null=True)
    delivery=models.CharField(max_length=20,blank=True,null=True)
    
    comments=models.CharField(max_length=20,blank=True,null=True)
    uplift= models.FloatField(null=True, blank=True, default=1)
   
    def __str__(self):
        return str(self.job_number)
   

class AlwenJobItemsModel(models.Model):
  
    description=models.ForeignKey(AlwenExpensesModel, blank=True, null=True, on_delete=models.CASCADE,related_name='desrlnm')
    quantity=models.FloatField(max_length=20,blank=True,null=True,default=0)
    unit_cost=models.FloatField(max_length=20,blank=True,null=True,default=0)
    unit_price=models.FloatField(max_length=20,blank=True,null=True,default=0)
    selling_price=models.FloatField(max_length=20,blank=True,null=True,default=0)
    comments=models.CharField(max_length=20,blank=True,null=True,default="Comments")
    
    jobitemconnector= models.ForeignKey(AlwenJobsModel, blank=True, null=True, on_delete=models.CASCADE,related_name='itemjobconrelnme')
    
    def __str__(self):
        return str(self.description)
    @property
    def sellingamount(self):
        sellingamount=float(self.quantity) * float(self.unit_price)
        return sellingamount
    @property
    def lineamount(self):
        lineamount=int(self.quantity) * int(self.unit_cost)
        return lineamount
    
class AlwenJobItemsSellingModel(models.Model):
  
    description=models.CharField(max_length=30,blank=True,null=True)
    quantity=models.FloatField(max_length=20,blank=True,null=True,default=0)
    unit_cost=models.FloatField(max_length=20,blank=True,null=True,default=0)
    unit_price=models.FloatField(max_length=20,blank=True,null=True,default=0)
    jobitselcon= models.ForeignKey(AlwenJobsModel, blank=True, null=True, on_delete=models.CASCADE,related_name='jbitselrenm')
   
    def __str__(self):
        return str(self.description)
    @property
    def mylineamount(self):
        mylineamount=float(self.quantity) * float(self.unit_price)
        return mylineamount
    @property
    def linecost(self):
        linecost=int(self.quantity) * int(self.unit_cost)
        return linecost


########################################################################

class AlwenInvoicesModel(models.Model):
    paymentTerms = [
    ('Cash', 'Cash'),
    ('Deposit', 'Deposit'),
    ('15 days', '15 days'),
   
    ]
    invoiceStatus = [
    ('Paid', 'Paid'),
    ('Current', 'Current'),
    ('Overdue', 'Overdue'),
   
    ]
    Currency = [
    ('KES','KES'),
    ('$', 'USD'),
    ('£', 'EURO'),
    ]
    posting_status = [
    ('waiting','waiting'),
    ('posted', 'posted'),
   
    ]
    #testingfield= models.ForeignKey(PurchaseOrdersModel,related_name="testingfieldrelatedname",on_delete=models.CASCADE,blank=True,null=True)
    customer= models.ForeignKey(CustomersModel,related_name="alwrelatcustinvoice",on_delete=models.CASCADE,blank=True,null=True)
    invoice_number = models.CharField(null=True, blank=True, max_length=20)
    invoice_due_Date = models.DateField(null=True, blank=True)
    invoice_terms = models.CharField(choices=paymentTerms, default='Cash', max_length=20)
    invoice_status = models.CharField(choices=invoiceStatus, default='Current', max_length=20)
    invoice_currency = models.CharField(choices=Currency, default='$', max_length=20)
    invoice_comments=models.CharField(blank=True,null=True,default='invoice',max_length=20)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    job= models.ForeignKey(AlwenJobsModel, blank=True, null=True, on_delete=models.SET_NULL,related_name='jobinvrelnm')
    invoice_total=models.DecimalField(max_digits=10,blank=True,null=True,decimal_places=2,default=0)
    posting_inv_status=models.CharField(choices=posting_status, default='waiting', max_length=100,blank=True,null=True)

    def __str__(self):
        return '{}'.format(self.invoice_number)

   
class AlwenInvoiceItemsModel(models.Model):
  
    description= models.CharField(max_length=30,blank=True,null=True)
    quantity = models.IntegerField(null=True, blank=True,default=0)
    unit_price = models.IntegerField(null=True, blank=True,default=0)
    
    #Related Fields
    alinvcontr= models.ForeignKey(AlwenInvoicesModel, blank=True, null=True, on_delete=models.CASCADE,related_name='invitemrelated')
    
    
   
    def __str__(self):
        return '{}'.format(self.description)
    #below calculates the total selling price for the model
    @property
    def selling_price(self):
        selling_price=self.quantity * self.unit_price
        return selling_price


################################################## BELOW IS FOR CHART OF ACCOUNTS ######################

class AllifChartOfAccountsModel(models.Model):
    Financial_Statement= [
    ('Income Statement','Income Statement'),
    ('Balance Sheet', 'Balance Sheet'),
    
    ]
    Account_category= [
    ('Assets','Assets'),
    ('Liabilities', 'Liabilities'),
    ('Equity', 'Equity'),
    ('Revenue', 'Revenue'),
    ('Expenses', 'Expenses'),
    
    ]

    Account_nature= [
    ('Debit','Debit'),
    ('Credit', 'Credit'),
    ('Both', 'Both'),
    ]
    Account_Type= [
    ('Posting','Posting'),
    ('Heading', 'Heading'),
    ('Total', 'Total'),
    ('Begin-Total', 'Begin-Total'),
    ('End-Total', 'End-Total'),
    ]
  
    code=models.CharField(max_length=20,blank=True,null=True,unique=True)
    description=models.CharField(max_length=30,blank=True,null=True)
    statement=models.CharField(choices=Financial_Statement,max_length=20,blank=True,null=True)
    category=models.CharField(choices=Account_category,max_length=20,blank=True,null=True)
    nature=models.CharField(choices=Account_nature,max_length=20,blank=True,null=True)
    type=models.CharField(choices=Account_Type,max_length=20,blank=True,null=True)
    balance=models.FloatField(max_length=20,blank=True,null=True,default=0)
    
    def __str__(self):
        return str(self.code)

        ############################3 CARDS ###########################3

class CardsModel(models.Model):

    currency=[
        ('KES', 'KES'),
        ('$','USD'),
        ('€','EURO')
        ]
    name= models.CharField(max_length=15,blank=False,null=True)
    number= models.IntegerField(null=True, blank=False,default=0)
    balance= models.IntegerField(null=True, blank=True,default=0)
    comment= models.CharField(max_length=15,blank=True,null=True,default='No comment')
    currency=models.CharField(max_length=20,blank=True,null=True,choices=currency,default=1)
    
   
    def __str__(self):
        return '{}'.format(self.number)
    
    def deposit(self, myamount):
        self.balance += myamount
        self.save()
    
    def withdraw(self, myamount):
        if myamount > self.balance:
            return HttpResponse("NO SUFFICIENT MONEY")
        self.balance -= myamount
        self.save()

class CardsTopUpsModel(models.Model):
    
    card= models.ForeignKey(CardsModel,related_name="cardreltedname",on_delete=models.SET_NULL,blank=True,null=True)
    amount= models.IntegerField(null=True, blank=True,default=0)
    date=models.DateField(auto_now=True)
    comments=models.CharField(max_length=15,blank=True,null=True, default='comment')
    
    def __str__(self):
        return '{}'.format(self.card)
   
    
    
#####################################33  fill ups ##################################

class AlwenFillUpsModel(models.Model):
    vehicle=models.ForeignKey(AlwenVehiclesModel,on_delete=models.SET_NULL,blank=False,null=True)
    card=models.ForeignKey(CardsModel,on_delete=models.SET_NULL,blank=True,null=True)
    operator=models.ForeignKey(AlwenDriversModel,on_delete=models.SET_NULL,blank=True,null=True)
    date=models.DateField(blank=True,null=True,auto_now=True)
    odometer=models.IntegerField(blank=True,null=True)
    quantity=models.IntegerField(blank=False,null=False)
    unit_price=models.IntegerField(blank=False,null=False)
    oil_type= models.CharField(max_length=25, blank=True, null=True,choices=oil_options)
    station= models.CharField(max_length=25, blank=True, null=True)
    payment= models.CharField(max_length=25, blank=True, null=True,choices=payment_options)
    receipt=models.FileField(upload_to='myfiles/',blank=True,null=True)
    fuel_brand= models.CharField(max_length=25, blank=True, null=True)
    
   
    notes=models.CharField(blank=True,null=True,max_length=20)

    def __str__(self):
        return str(self.vehicle)#
    
    @property
    def fuelcost(self):
        total_fuel_cost=int(self.quantity) * int(self.unit_price)
        return total_fuel_cost



 
    


   
    

