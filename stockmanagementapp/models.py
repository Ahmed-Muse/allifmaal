from django.db import models
from django.contrib.auth.models import User
from allifmaalapp.models import AllifmaalSuppliersModel,AllifmaalCustomersModel


# Create your models here.

class PhysicalStockModel(models.Model):
    #store=models.ForeignKey(StoresModel, blank=True, null=True, on_delete=models.CASCADE,related_name='storerelatedname')
    partNumber = models.CharField(max_length=255, blank=True, null=True,unique=False)# unique prevents data duplication
    description = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(blank=False,null=True)
    unitcost=models.FloatField(null=True,blank=True,default=0)
    
    unitPrice = models.IntegerField(blank=False, null=True,default=0)

    comments = models.CharField(max_length=255, blank=True, null=True)
    receivedQuantity = models.IntegerField(default=0,blank=True,null=True)
    receivedBy = models.CharField(max_length=50,blank=True,null=True)
    issuedQuantity = models.IntegerField(default=0,blank=True,null=True)
    issuedBy = models.CharField(max_length=50,blank=True,null=True)
    issuedTo = models.CharField(max_length=50,blank=True,null=True)
    createdBy = models.CharField(max_length=50,blank=True,null=True)
    reorderLevel = models.IntegerField(default='0',blank=True,null=True)

    #item physical attributes
    weight = models.CharField(max_length=50,blank=True,null=True)
    length = models.CharField(max_length=50,blank=True,null=True)
    width = models.CharField(max_length=50,blank=True,null=True)
    color = models.CharField(max_length=50,blank=True,null=True)
    expiryDate = models.CharField(max_length=50,blank=True,null=True)
    vendor = models.CharField(max_length=50,blank=True,null=True)
    timestamp = str(models.DateTimeField(auto_now_add=True, auto_now=False,blank=True,null=True))#if adding now, pick currrent data and if updating stick to the original date
    lastUpdated = str(models.DateTimeField(auto_now_add=False, auto_now=True,blank=True,null=True))
    
    def __str__(self):
    		return str(self.description) # this will show up in the admin area

#in the object below am trying to store the issue goods in their own model
class IssuedPhysicalStockModel(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True)
    issuedQuantity = models.IntegerField(default='0',blank=True,null=True)
    issuedTo = models.CharField(max_length=50,blank=True,null=True)
    receivedQuantity = models.IntegerField(default='0',blank=True,null=True)
    def __str__(self):
    	return self.issuedQuantity

#################################

class PurchaseOrdersModel(models.Model):
    po_number = models.CharField(null=True, blank=True, max_length=100)
    shipping=models.IntegerField(null=True, blank=True, default=0)
    uplift= models.FloatField(null=True, blank=True, default=1)
    comments = models.CharField(null=True, blank=True, max_length=100)
    
    def __str__(self):
        return str(self.po_number)

class PurchaseOrderItemsModel(models.Model):

    supplier= models.ForeignKey(AllifmaalSuppliersModel,related_name="supitemrelname",on_delete=models.CASCADE,blank=True,null=True)
    items= models.ForeignKey(PhysicalStockModel,related_name="poitemrelatedname",on_delete=models.CASCADE)
    quantity = models.FloatField(null=True, blank=True)
    unitcost=models.FloatField(null=True, blank=True, default=0)
    notes= models.CharField(null=True, blank=True,max_length=250)

    po_item_con= models.ForeignKey(PurchaseOrdersModel, blank=True, null=True, on_delete=models.CASCADE,related_name='poitrelname')
   
   
    def __str__(self):
        return '{}'.format(self.items)

###########################################3

class StoresModel(models.Model):
   
    name=models.CharField(max_length=30,null=True,blank=True)
    comments= models.CharField(max_length=30,null=True,blank=True)

    def __str__(self) :
        return self.name

class StoreItemsModel(models.Model):
    store=models.ForeignKey(StoresModel, blank=True, 
    null=True, on_delete=models.CASCADE,related_name='itemstorerelatname')

    description=models.ForeignKey(PhysicalStockModel,blank=True, 
    null=True, on_delete=models.CASCADE,related_name='storeitemrelated')

    quantity = models.IntegerField(blank=False,null=True)
    comments= models.CharField(max_length=30,null=True,blank=True)

    def __str__(self) :
        return str(self.description)

class TransferOrdersModel(models.Model):
    transfer_order_no=models.CharField(max_length=30,null=True,blank=True)
    from_store=models.ForeignKey(StoresModel, blank=True, 
    null=True, on_delete=models.CASCADE,related_name='from_store')

    to_store=models.ForeignKey(StoresModel, blank=True, 
    null=True, on_delete=models.CASCADE,related_name='to_store')
    
    comments= models.CharField(max_length=30,null=True,blank=True)
    def __str__(self) :
        return self.transfer_order_no

class TransferOderItemsModel(models.Model):
    item= models.ForeignKey(StoreItemsModel,related_name="toitemrelatedtest",on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    comments= models.CharField(null=True, blank=True,max_length=250)
    testtoitemsconnector= models.ForeignKey(TransferOrdersModel, blank=True, 
    null=True, on_delete=models.CASCADE,related_name='toitemrelatedtest')
    
   
   
    def __str__(self):
        return '{}'.format(self.item)


class AllifInvoicesModel(models.Model):
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
    #testingfield= models.ForeignKey(PurchaseOrdersModel,related_name="testingfieldrelatedname",on_delete=models.CASCADE,blank=True,null=True)
    customer= models.ForeignKey(AllifmaalCustomersModel,related_name="invcustrelname",on_delete=models.CASCADE,blank=True,null=True)
    number = models.CharField(null=True, blank=True, max_length=100)
    due = models.DateField(null=True, blank=True)
    terms = models.CharField(choices=paymentTerms, default='Cash', max_length=100)
    status = models.CharField(choices=invoiceStatus, default='Current', max_length=100)
    currency = models.CharField(choices=Currency, default='$', max_length=100)
    comments=models.CharField(blank=True,null=True,default='invoice',max_length=250)
    posted=models.BooleanField(blank=True, null=True,default=False)
    created=models.DateField(blank=True,null=True,auto_now_add=True)
   
    def __str__(self):
        return self.number
    
class AllifInvoiceItemsModel(models.Model):
    description=models.ForeignKey(PhysicalStockModel,related_name="invstkrelname",on_delete=models.CASCADE,blank=False,null=False)
    quantity = models.IntegerField(null=True, blank=True,default=0)
    invitemcon = models.ForeignKey(AllifInvoicesModel, blank=True, null=True, on_delete=models.CASCADE,related_name='invitrelnme')
    def __str__(self):
        return str(self.description)
    
    @property
    def selling_price(self):
        selling_price=self.quantity * self.description.unitPrice
        return selling_price

class AllifPostedSalesInvoicesModel(models.Model):
   
    inv_no=models.CharField(max_length=50,blank=True,null=True)
    customer=models.CharField(max_length=50,blank=True,null=True)
    inv_total_value=models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return str(self.inv_no)


###############################################################################################################################
#################3333 upload the csv file and insert the data into django model below
class Csv(models.Model):
    file_name=models.FileField(upload_to='csv')#csv here is a folder name inside media
    uploaded=models.DateTimeField(auto_now_add=True)
    activated=models.BooleanField(default=False)
    def __str__(self) :
        return f"File id: {self.id}"

class Sale(models.Model):
    PRODUCT_CHOICES=[
        ("TV","tv"),
        ("IPAD","ipad"),
        ("PLAYSTATION","playstation"),
    ]
    product=models.CharField(max_length=200,blank=True,null=True)
    
    quantity=models.PositiveIntegerField(blank=True,null=True)
    
    def __str__(self) :
        return self.product


######################3 TESTING IF IT WILL WORK ######################
class Person(models.Model):
    name = models.CharField(max_length=30,null=True)
    email = models.EmailField(blank=True,null=True)
    #birth_date = models.DateField()
    location = models.CharField(max_length=100, blank=True,null=True)
    price=models.IntegerField(null=True,blank=True)

######################3  IF IT WILL WORK ######################
class FromStoreModel(models.Model):
    store=models.CharField(max_length=250,blank=True,null=True)
    def __str__(self) :
        return self.store

class ToStoreModel(models.Model):
    store=models.CharField(max_length=250,blank=True,null=True)
    def __str__(self) :
        return self.store

class TransferingStoreModel(models.Model):
   
    store=models.ForeignKey(FromStoreModel,max_length=250,null=True,blank=True,on_delete=models.CASCADE)
    description = models.CharField(max_length=30,null=True,blank=True)
    quantity=models.IntegerField(null=True,blank=True)
    comments= models.CharField(max_length=30,null=True,blank=True)
    def __str__(self) :
        return self.description

class ReceivingStoreModel(models.Model):
   
    store=models.ForeignKey(ToStoreModel,max_length=250,null=True,blank=True,on_delete=models.CASCADE)
    description = models.CharField(max_length=30,null=True,blank=True)
    quantity=models.IntegerField(null=True,blank=True)
    comments= models.CharField(max_length=30,null=True,blank=True)
    def __str__(self) :
        return self.description


class AllifExpensesModel(models.Model):
    description=models.CharField(max_length=250,blank=True,null=True)
    amount=models.FloatField(max_length=250,blank=True,null=True)
    comments=models.CharField(max_length=50,blank=True,null=True)
    def __str__(self):
        return str(self.description)

class AllifCustomerPaymentsModel(models.Model):
    customer= models.ForeignKey(AllifmaalCustomersModel, max_length=100,on_delete=models.CASCADE,related_name="payclientrelname")
    amount=models.DecimalField(decimal_places=2,blank=True,null=True,max_digits=12,default=0)
    comments=models.CharField(max_length=50,blank=True,null=True)
    paid = models.DateField(blank=True, null=True,auto_now_add=True)
    def __str__(self):
        return str(self.customer)
    @property
    def get_total(self):
        balance=0
        total=int(balance)+int(self.amount)
        return total

class AllifCustomersBalanceModel(models.Model):
    customer= models.ForeignKey(AllifmaalCustomersModel, max_length=100,on_delete=models.CASCADE,related_name="clibalrelnam")
    balance=models.DecimalField(decimal_places=2,blank=True,null=True,max_digits=12,default=0)
    
    def __str__(self):
        return str(self.customer)


    
    

