from django.db import models


class AllifmaalDetailsModel(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)
    address=models.CharField(max_length=50,blank=True,null=True)
    pobox=models.CharField(max_length=50,blank=True,null=True)
    email=models.EmailField(max_length=50,blank=True,null=True)
    website=models.CharField(max_length=50,blank=True,null=True)
    phone1=models.CharField(max_length=50,blank=True,null=True)
    city=models.CharField(max_length=50,blank=True,null=True)
    country=models.CharField(max_length=50,blank=True,null=True)
    phone2=models.CharField(max_length=50,blank=True,null=True)
    logo=models.ImageField(blank=True,null=True)

    def __str__(self):
        return self.name
class AllifmaalScopeModel(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return '{}'.format(self.name)

#################3 suppliers ################
class AllifmaalSuppliersModel(models.Model):
    Country = [
    ('Somalia', 'Somalia'),
     ('Somaliland', 'Somaliland'),
    ('Kenya', 'Kenya'),
     ('Other', 'Other'),
    ]
    name = models.CharField(null=True, blank=True, max_length=20)
    phone = models.CharField(null=True, blank=True, max_length=30)
    email= models.CharField(null=True, blank=True, max_length=100)
    country = models.CharField(choices=Country, blank=True, max_length=30)
    city= models.CharField(null=True, blank=True, max_length=30)
    address = models.CharField(null=True, blank=True, max_length=30)
    balance=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    turnover=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
   
    contact = models.CharField(null=True, blank=True, max_length=30)

    def __str__(self):
        return '{}'.format(self.name)

class AllifmaalCustomersModel(models.Model):
    Country = [
    ('Somalia', 'Somalia'),
     ('Somaliland', 'Somaliland'),
    ('Kenya', 'Kenya'),
     ('Other', 'Other'),
    ]
    name = models.CharField(null=True, blank=True, max_length=20)
    phone = models.CharField(null=True, blank=True, max_length=30)
    email= models.CharField(null=True, blank=True, max_length=100)
    country = models.CharField(choices=Country, blank=True, max_length=30)
    city= models.CharField(null=True, blank=True, max_length=30)
    address = models.CharField(null=True, blank=True, max_length=30)
    sales=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    balance=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    turnover=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    contact = models.CharField(null=True, blank=True, max_length=30)

    def __str__(self):
        return '{}'.format(self.name)
class AllifmaalCustomerPaymentsModel(models.Model):
    payment_method=[
        ("Cash","Cash"),
        ("Cheque","Cheque"),
        ("Credit Card","Credit Card"),
    ]
   
    
    customer= models.ForeignKey(AllifmaalCustomersModel,related_name="allifcustpaymentreltedname",on_delete=models.SET_NULL,blank=True,null=True)
    amount= models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    date=models.DateField(auto_now=True)
    comments=models.CharField(max_length=15,blank=True,null=True, default='comment')
    account= models.ForeignKey('AllifmaalChartOfAccountsModel',related_name="allifcustpymaccrelnm",on_delete=models.SET_NULL,blank=True,null=True)
    mode=models.CharField(choices=payment_method,max_length=20,blank=True,null=True,default="Cash")
    
    
    def __str__(self):
        return '{}'.format(self.customer)

################################3 QUOTES ###########################3
class AllifmaalQuotesModel(models.Model):
    paymentTerms = [
    ('Cash', 'Cash'),
    ('Deposit', 'Deposit'),
    ('15 days', '15 days'),
    ('30 days', '30 days'),
    ('Other', 'Other'),
   
    ]
    Currency = [
    ('KES','KES'),
    ('$', 'USD'),
    ('£', 'EURO'),
    ]
    prospects = [
    ('Default', 'Default'),
    ('Likely', 'Likely'),
    ('Confirmed', 'Confirmed'),
    ('Closed', 'Closed'),
    ('Lost', 'Lost'),
   
    ]
    number = models.CharField(null=True, blank=True, max_length=20)
    customer= models.ForeignKey(AllifmaalCustomersModel,related_name="allifrelatcustquote",on_delete=models.SET_NULL,blank=True,null=True)
    terms = models.CharField(choices=paymentTerms, default='Cash', max_length=20)
    prospect = models.CharField(choices=prospects, default='Default', max_length=20)
    currency = models.CharField(choices=Currency, default='$', max_length=20)
    comments=models.CharField(blank=True,null=True,default='Quote',max_length=20)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    total=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)

    def __str__(self):
        return '{}'.format(self.number)

class AllifmaalQuoteItemsModel(models.Model):
  
    
    description= models.ForeignKey('AllifmaalStocksModel',related_name="allifquoteitemdescrelatednm",on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
   
    allifquoteitemconnector= models.ForeignKey(AllifmaalQuotesModel, blank=True, null=True, on_delete=models.CASCADE,related_name='allifquoteitemrelated')
    
    def __str__(self):
        return '{}'.format(self.description)
    #below calculates the total selling price for the model
    @property
    def quote_selling_price(self):
        selling_price=self.quantity * self.description.unitPrice
        return selling_price



########################### INVOICES #################################
class AllifmaalInvoicesModel(models.Model):
    paymentTerms = [
    ('Cash', 'Cash'),
    ('Deposit', 'Deposit'),
    ('15 days', '15 days'),
    ('30 days', '30 days'),
   
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
    customer= models.ForeignKey(AllifmaalCustomersModel,related_name="allifrelatcustinvoice",on_delete=models.SET_NULL,blank=False,null=True)
    invoice_number = models.CharField(null=True, blank=True, max_length=20)
    invoice_due_Date = models.DateField(null=True, blank=True)
    invoice_terms = models.CharField(choices=paymentTerms, default='Cash', max_length=20)
    invoice_status = models.CharField(choices=invoiceStatus, default='Current', max_length=20)
    invoice_currency = models.CharField(choices=Currency, default='$', max_length=20)
    invoice_comments=models.CharField(blank=True,null=True,default='invoice',max_length=20)
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    invoice_total=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    posting_inv_status=models.CharField(choices=posting_status, default='waiting', max_length=100,blank=True,null=True)
    invoice_items_total_cost=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    
    

    def __str__(self):
        return '{}'.format(self.invoice_number)

   
class AllifmaalInvoiceItemsModel(models.Model):
  
   
    description= models.ForeignKey('AllifmaalStocksModel',related_name="allidescrelatednm",on_delete=models.SET_NULL,blank=True,null=True)
    
   
    quantity=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    unit_price=models.DecimalField(max_digits=10,blank=True,null=True,decimal_places=1,default=0)
   
    allifinvitemconnector= models.ForeignKey(AllifmaalInvoicesModel, blank=True, null=True, on_delete=models.CASCADE,related_name='allifinvitemrelated')
    
    def __str__(self):
        return '{}'.format(self.description)
    #below calculates the total selling price for the model
    @property
    def selling_price(self):
        selling_price=self.quantity * self.description.unitPrice
        return selling_price


class AllifmaalTasksModel(models.Model):
   
    task_status = [
    ('complete', 'complete'),
    ('incomplete', 'incomplete'),
    
    ]
    day = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
    
    ]
    
    task = models.CharField(max_length=20,blank=False)
    status = models.CharField(max_length=10,choices=task_status,default='incomplete')
   
    createDate=models.DateTimeField(auto_now_add=True)
    dueDate=models.DateTimeField(auto_now_add=False,auto_now=False,blank=True,null=True)
    taskDay = models.CharField(max_length=10,choices=day,default='Monday')
    assignedto=models.ForeignKey('AllifmaalHumanResourcesModel',on_delete=models.SET_NULL,blank=True,null=True,related_name="taskassignrelname")
    
    
    def __str__(self):
    		return self.task

##################################### general ledger ########################

class AllifmaalGeneralLedgersModel(models.Model):
    
    date=models.DateField(blank=True,null=True,auto_now_add=True)

    description=models.CharField(max_length=30,blank=True,null=True,unique=True)
    
    balance=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    
    def __str__(self):
        return str(self.description)

############################# CHART OF ACCOUNTS #########################

class AllifmaalChartOfAccountsModel(models.Model):

    mydefaultvalue=AllifmaalGeneralLedgersModel.objects.first()
    myitemid=mydefaultvalue.id
    Financial_Statement= [
    ('Income Statement','Income Statement'),
    ('Balance Sheet', 'Balance Sheet'),
    
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
    generalPosting=[
        ("sale","sale"),
        ("purchase","purchase"),
    ]
  
    code=models.CharField(max_length=20,blank=True,null=True,unique=True)
    description=models.CharField(max_length=30,blank=True,null=True,unique=True)
    balance=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    statement=models.CharField(choices=Financial_Statement,max_length=20,blank=True,null=True)
    category=models.ForeignKey(AllifmaalGeneralLedgersModel, blank=True, null=True, on_delete=models.SET_NULL,related_name='coaglrelname',default=myitemid)
    nature=models.CharField(choices=Account_nature,max_length=20,blank=True,null=True)
    type=models.CharField(choices=Account_Type,max_length=20,blank=True,null=True)
    posting=models.CharField(choices=generalPosting,max_length=20,blank=True,null=True)
   
    def __str__(self):
        return str(self.description)

        #return str(self.code)+ "||" +str(self.category)+"||" +str(self.description)
        
class AllifmaalExpensesModel(models.Model):
    payment_method=[
        ("Cash","Cash"),
        ("Cheque","Cheque"),
        ("Credit Card","Credit Card"),
    ]
    pay_from=models.ForeignKey(AllifmaalChartOfAccountsModel, blank=False,null=True,on_delete=models.SET_NULL,related_name='coaexprelnanemcon')
    pay_to=models.ForeignKey(AllifmaalChartOfAccountsModel, blank=False, null=True, on_delete=models.SET_NULL,related_name='coaexprelnamepayto')
    supplier=models.ForeignKey(AllifmaalSuppliersModel, blank=False, null=True, on_delete=models.SET_NULL,related_name='expsupprelanmecon')
    mode=models.CharField(choices=payment_method,max_length=20,blank=False,null=True,default="Cash")
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    description=models.CharField(max_length=25,blank=False,null=True)
    amount=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    comments=models.CharField(max_length=20,blank=True,null=True)
    def __str__(self):
        return str(self.description)
    #def save(self, *args, **kwargs):
        #if self.pay_from is None:
        #self.pay_from== AllifmaalChartOfAccountsModel.objects.filter(description="Cash")
       
       
        #super(AllifmaalExpensesModel, self).save(*args, **kwargs)


#########################################3 STOCK ##############################################
class AllifmaalStockCategoriesModel(models.Model):
    
    description = models.CharField(max_length=15, blank=False, null=True,unique=True)
   
    def __str__(self):
    		return str(self.description) # this will show up in the admin area

class AllifmaalStocksModel(models.Model):
    #store=models.ForeignKey(StoresModel, blank=True, null=True, on_delete=models.CASCADE,related_name='storerelatedname'
    #coa_less_than_queryset=AllifmaalChartOfAccountsModel.objects.filter(code__lte=19999)
    category=models.ForeignKey(AllifmaalStockCategoriesModel, blank=True, null=True,on_delete=models.SET_NULL,related_name='catinvtconrlnm')

    partNumber = models.CharField(max_length=20, blank=True, null=True,unique=True)# unique prevents data duplication
    description = models.CharField(max_length=30, blank=True, null=True)
   
    quantity=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    buyingPrice=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    unitcost=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    standardUnitCost=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    unitPrice=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)

    inventory_account=models.ForeignKey(AllifmaalChartOfAccountsModel, blank=False, null=True,on_delete=models.SET_NULL,related_name='coainvrelnm')
    income_account=models.ForeignKey(AllifmaalChartOfAccountsModel, blank=False, null=True,on_delete=models.SET_NULL,related_name='coaincomerelnm')
    expense_account=models.ForeignKey(AllifmaalChartOfAccountsModel, blank=False, null=True,on_delete=models.SET_NULL,related_name='coaexprelnm')
    
    def __str__(self):
    		return str(self.description) # this will show up in the admin area

##################################

class AllifmaalPurchaseOrdersModel(models.Model):
    payment_method=[
        ("Cash","Cash"),
        ("Credit","Credit"),
    ]
    posting_status = [
    ('waiting','waiting'),
    ('posted', 'posted'),
        
    ]
    po_number = models.CharField(null=True, blank=True, max_length=100)
    shipping=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    uplift=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=2)
    comments = models.CharField(null=True, blank=True, max_length=100)
    supplier= models.ForeignKey(AllifmaalSuppliersModel,related_name="suplporelnme",on_delete=models.SET_NULL,blank=False,null=True)
    payment_terms = models.CharField(choices=payment_method, default='Cash', max_length=20)
    
    total=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
   
    posting_po_status=models.CharField(choices=posting_status, default='waiting', max_length=100,blank=True,null=True)
   
    
    def __str__(self):
        return str(self.po_number)

class AllifmaalPurchaseOrderItemsModel(models.Model):

    items= models.ForeignKey(AllifmaalStocksModel,related_name="poitemrallirelnm",on_delete=models.CASCADE)
    quantity=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    unitcost=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    po_item_con= models.ForeignKey(AllifmaalPurchaseOrdersModel, blank=True, null=True, on_delete=models.CASCADE,related_name='poitrelname')
   
    def __str__(self):
        return '{}'.format(self.items)

class AllifmaalPurchaseOrderMiscCostsModel(models.Model):
    supplier=models.ForeignKey(AllifmaalSuppliersModel, blank=True, null=True, on_delete=models.SET_NULL,related_name='suppmiscrlnme')
    description = models.CharField(max_length=30, blank=True, null=True)
    amount=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    po_misc_cost_con= models.ForeignKey(AllifmaalPurchaseOrdersModel, blank=True, null=True, on_delete=models.CASCADE,related_name='pomiscrlnm')
   
    def __str__(self):
        return '{}'.format(self.description)

##############################3 hrm #########################
gender = (
		('Male', 'Male'),
		('Female', 'Female'),
	)

class AllifmaalHumanResourcesModel(models.Model):
    staffNo = models.IntegerField(default='0',blank=True,null=True,unique=True)
    firstName = models.CharField(max_length=50,blank=False,null=True)
    lastName = models.CharField(max_length=50,blank=True,null=True)
    middleName = models.CharField(max_length=50,blank=True,null=True)
    staffImage=models.ImageField(upload_to='hrmapp/images/staff/%Y/',null=True, blank=True)#save according to year
    staffGender = models.CharField(max_length=255, blank=True, null=True,choices=gender)
    department = models.CharField(max_length=50,blank=True,null=True)
    title = models.CharField(max_length=50,blank=True,null=True)
    education = models.CharField(max_length=50,blank=True,null=True)
    comment = models.CharField(max_length=250,blank=True,null=True)
    dateJoined =  models.DateTimeField(auto_now_add=True,blank=True,null=True)
    #timestamp = models.DateTimeField(auto_now_add=True, auto_now=False,default=0)
    salary=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)

    def __str__(self):
    	return self.firstName


################assets
class AllifmaalAssetsModel(models.Model):
    
    payment_method=[("Cash","Cash"), ("Credit","Credit"),]

    supplier= models.ForeignKey(AllifmaalSuppliersModel,related_name="suplporelnmeasset",on_delete=models.SET_NULL,blank=False,null=True)

    payment_terms = models.CharField(choices=payment_method, default='Cash', max_length=20,blank=False)

    asset_account=models.ForeignKey(AllifmaalChartOfAccountsModel, blank=False, null=True,on_delete=models.SET_NULL,related_name='assetcoareln')

    cost_account=models.ForeignKey(AllifmaalChartOfAccountsModel, blank=False, null=True,on_delete=models.SET_NULL,related_name='costcoareln')

    description=models.CharField(max_length=30,blank=False,null=True)
    quantity=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    value=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    lifespan=models.CharField(max_length=10,blank=True,null=True)
    acquired= models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.description)

########################## banks #########################
class AllifmaalBanksModel(models.Model):
    
    name=models.CharField(max_length=15,blank=False,null=True)
    account=models.CharField(max_length=15,blank=True,null=True)
    balance= models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    date=models.DateField(auto_now=True)
    comments=models.CharField(max_length=15,blank=True,null=True, default='comment')
    
    
    def __str__(self):
        return '{}'.format(self.name)

class AllifmaalBankDepositsModel(models.Model):
    description=models.CharField(max_length=15,blank=True,null=True)
    bank= models.ForeignKey(AllifmaalBanksModel,related_name="depositbankreln",on_delete=models.SET_NULL,blank=False,null=True)
    amount= models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    date=models.DateField(auto_now=True)
    comments=models.CharField(max_length=15,blank=True,null=True, default='Deposit')
    
    def __str__(self):
        return '{}'.format(self.description)

class AllifmaalBankWithdrawalsModel(models.Model):
    description=models.CharField(max_length=15,blank=True,null=True)
    bank= models.ForeignKey(AllifmaalBanksModel,related_name="withdrawbankreln",on_delete=models.SET_NULL,blank=False,null=True)
    amount= models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    date=models.DateField(auto_now=True)
    comments=models.CharField(max_length=15,blank=True,null=True, default='Withdrawal')
    
    def __str__(self):
        return '{}'.format(self.description)

class MoneyDrawingModel(models.Model):
    description=models.CharField(max_length=15,blank=True,null=True)
    account= models.ForeignKey(AllifmaalChartOfAccountsModel,related_name="drawcoareln",on_delete=models.SET_NULL,blank=False,null=True)
    amount= models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    date=models.DateField(auto_now=True)
    fromacc= models.ForeignKey(AllifmaalChartOfAccountsModel,related_name="drawcoarcash",on_delete=models.SET_NULL,blank=False,null=True)
   
    
    def __str__(self):
        return '{}'.format(self.description)
################### for learning purposes only ############333

class ForLearningOnlyModel(models.Model):
    #mydefault=AllifmaalStocksModel.objects.all().first
    items= models.ForeignKey(AllifmaalStocksModel,related_name="poitemrallirelnmtesting",
    on_delete=models.CASCADE)
    description = models.CharField(max_length=30, blank=True, null=True)

    quantity=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    rate=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    amount=models.DecimalField(max_digits=10,blank=False,null=True,decimal_places=1,default=0)
    def __str__(self):
        return '{}'.format(self.items)














