from django import forms
from .models import *


############################# start of datepicker customization ##############################
class DatePickerInput(forms.DateInput):#use this class whereever you have a date and it will give you the calender
    input_type = 'date'#
class TimePickerInput(forms.TimeInput):#use this wherever you have time input
    input_type = 'time'
class DateTimePickerInput(forms.DateTimeInput):#use this wherever you have datetime input
    input_type = 'datetime'
    ################################# end of datepicker customization ################################



class AddAllifmaalDetailsForm(forms.ModelForm):
    class Meta:
        model = AllifmaalDetailsModel
        fields = ['name','phone1','email','website', 'logo','address','phone2','pobox','city','country']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),

            'phone1':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'city':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'country':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'pobox':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'phone2':forms.TextInput(attrs={'class':'form-control'}),
            'website':forms.TextInput(attrs={'class':'form-control'}),
            #'logo':forms.ImageField(attrs={'class':'form-control'}),
        
        }

class AddAllifmaalScopeForm(forms.ModelForm):
    class Meta:
        model = AllifmaalScopeModel
        fields = ['name' ]

        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            
        }

class AddAllifmaalSupplierForm(forms.ModelForm):
    class Meta:
        model = AllifmaalSuppliersModel
        fields = ['name','phone','email','country', 'city','address','contact','balance','turnover']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),

            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'city':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'contact':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'country':forms.Select(attrs={'class':'form-control'}),
            'balance':forms.TextInput(attrs={'class':'form-control'}),
            'turnover':forms.TextInput(attrs={'class':'form-control'}),
        
        }


class AddAllifmaalCustomerForm(forms.ModelForm):
    class Meta:
        model = AllifmaalCustomersModel
        fields = ['name','phone','email','country', 'city','address','contact','balance','turnover']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),

            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'city':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'contact':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'country':forms.Select(attrs={'class':'form-control'}),
            'balance':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'turnover':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        
        }

##################### quotes ################
class AddAllifmaalQuoteDetailsForm(forms.ModelForm):
    class Meta:
        model = AllifmaalQuotesModel
        fields = ['customer','terms','prospect','currency','comments']

        widgets={
            'comments':forms.TextInput(attrs={'class':'form-control'}),
            
            'customer':forms.Select(attrs={'class':'form-control'}),
            'terms':forms.Select(attrs={'class':'form-control'}),
            'prospect':forms.Select(attrs={'class':'form-control'}),
            'currency':forms.Select(attrs={'class':'form-control'}),
           
            
            #form-control here is the css class that we are passing
        }

class AddAllifmaalQuoteItemsForm(forms.ModelForm):
    class Meta:
        model = AllifmaalQuoteItemsModel
        fields = ['description','quantity' ]

        widgets={
            'description':forms.Select(attrs={'class':'form-control'}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            
            
        }


class AddAllifmaalInvoiceDetailsForm(forms.ModelForm):
    class Meta:
        model = AllifmaalInvoicesModel
        fields = ['customer','invoice_terms', 'invoice_due_Date','invoice_status','invoice_currency','invoice_comments','posting_inv_status']

        widgets={
            'invoice_comments':forms.TextInput(attrs={'class':'form-control'}),
            
            'customer':forms.Select(attrs={'class':'form-control'}),
            'invoice_terms':forms.Select(attrs={'class':'form-control'}),
            'invoice_status':forms.Select(attrs={'class':'form-control'}),
            'invoice_currency':forms.Select(attrs={'class':'form-control'}),
           
            'posting_inv_status':forms.Select(attrs={'class':'form-control'}),

            #'invoice_due_Date':forms.DateInput(attrs={'class':'form-control'}),
            'invoice_due_Date' : DatePickerInput(attrs={'class':'form-control'}),
            
            #form-control here is the css class that we are passing
        }
        #fields='__all__'# this was used because of an error when running and the error said " .

class AddAllifmaalInvoiceItemsForm(forms.ModelForm):
    class Meta:
        model = AllifmaalInvoiceItemsModel
        fields = ['description','quantity','unit_price' ]

        widgets={
            'description':forms.Select(attrs={'class':'form-control'}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            'unit_price':forms.TextInput(attrs={'class':'form-control'}),
            
        }

class AddAllifmaalCustomerPaymentForm(forms.ModelForm):
    class Meta:
        model =AllifmaalCustomerPaymentsModel
        fields = ['customer','amount','comments','account','mode']
        widgets={
            'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'customer':forms.Select(attrs={'class':'form-control'}),
            'account':forms.Select(attrs={'class':'form-control'}),
             'mode':forms.Select(attrs={'class':'form-control'}),
        
        }
    def __init__(self,*args,**kwargs):
        assets_queryset=AllifmaalChartOfAccountsModel.objects.filter(code__lte=19999)

        super().__init__(*args, **kwargs)
        
        self.fields['account'].queryset=assets_queryset

class AddAllifmaalExpensesForm(forms.ModelForm):
    
    class Meta:
        model = AllifmaalExpensesModel
        fields = ['description', 'amount','comments','pay_from','supplier','pay_to','mode']
        widgets={
        
        'description':forms.TextInput(attrs={'class':'form-control'}),
        'amount':forms.TextInput(attrs={'class':'form-control'}),
        'comments':forms.TextInput(attrs={'class':'form-control'}),
        'pay_from':forms.Select(attrs={'class':'form-control'}),
        'supplier':forms.Select(attrs={'class':'form-control'}),
        'pay_to':forms.Select(attrs={'class':'form-control'}),
        'mode':forms.Select(attrs={'class':'form-control'}),
        
        }

    def __init__(self,*args,**kwargs):
        
        Assets=AllifmaalGeneralLedgersModel.objects.all().filter(description="Assets").first()
        assets_queryset_two=AllifmaalChartOfAccountsModel.objects.filter(category=Assets)
        assets_queryset=AllifmaalChartOfAccountsModel.objects.filter(code__lte=19999)
        expenses=AllifmaalChartOfAccountsModel.objects.filter(code__gte=49999)
       
        super().__init__(*args, **kwargs)
       
        self.fields['pay_from'].queryset=assets_queryset
        self.fields['pay_to'].queryset=expenses
        
        #self.fields['sizes'].choices = sizes
         #result2=AllifmaalHumanResourcesModel.objects.all()
        #results=list(chain(result2, article_list,assets_queryset))
    

class AddAllifmaalTasksForm(forms.ModelForm): #the forms here is the one imported up there.
    class Meta:
        model = AllifmaalTasksModel
        fields = ['task','status','dueDate','taskDay','assignedto']
        widgets={
            
            'task':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            
            'dueDate':DatePickerInput(attrs={'class':'form-control','placeholder':'Task due date'}),
            'taskDay':forms.Select(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            
             'assignedto':forms.Select(attrs={'class':'form-control'}),
            
            #form-control here is the css class that we are passing
        } 

class AddAllifmaalStockCategoryForm(forms.ModelForm):
    class Meta:
        model =AllifmaalStockCategoriesModel
        fields = ['description']
        widgets={
            
            'description':forms.TextInput(attrs={'class':'form-control'}),
          
           
            
        }

#####################3 geneal ledgers ########
class AddAllifmaalGeneralLedgerAccountForm(forms.ModelForm):
    class Meta:
        model =AllifmaalGeneralLedgersModel
        fields = ['description', 'balance']
        widgets={
            
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'balance':forms.TextInput(attrs={'class':'form-control'}),
           
            
        }

############################# chart of accounts ##################3
class AddAllifmaalChartOfAccountForm(forms.ModelForm):
    class Meta:
        model = AllifmaalChartOfAccountsModel
        fields = ['code','description', 'statement','category','nature','type','balance','posting']
        widgets={
            'code':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'balance':forms.TextInput(attrs={'class':'form-control'}),
            
            'statement':forms.Select(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'nature':forms.Select(attrs={'class':'form-control'}),
            'type':forms.Select(attrs={'class':'form-control'}),
            'posting':forms.Select(attrs={'class':'form-control'}),
           
            
           
            #form-control here is the css class that we are passing
        }


################################ STOCK MANAGEMENT ##############################
class AddAllifmaalStockForm(forms.ModelForm):
    class Meta:
        model = AllifmaalStocksModel
        fields = ['category','partNumber','description','buyingPrice', 'quantity','unitcost','unitPrice','inventory_account','income_account','expense_account','standardUnitCost']
        widgets={
            'partNumber':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            'unitcost':forms.TextInput(attrs={'class':'form-control'}),
            'unitPrice':forms.TextInput(attrs={'class':'form-control'}),
            'standardUnitCost':forms.TextInput(attrs={'class':'form-control'}),
            'buyingPrice':forms.TextInput(attrs={'class':'form-control'}),
            
            'inventory_account':forms.Select(attrs={'class':'form-control'}),
            'income_account':forms.Select(attrs={'class':'form-control'}),
            'expense_account':forms.Select(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
          # the css class that we are passing
        }
    def __init__(self,*args,**kwargs):
        
        assets_queryset=AllifmaalChartOfAccountsModel.objects.filter(code__lte=19999)
        revenue=AllifmaalChartOfAccountsModel.objects.filter(code__gte=39999,code__lte=49999)
       
        super().__init__(*args, **kwargs)
       
        self.fields['inventory_account'].queryset=assets_queryset
        self.fields['income_account'].queryset=revenue
        self.fields['expense_account'].queryset=assets_queryset

class AddAllifmaalPurchaseOrderDetailsForm(forms.ModelForm):
    class Meta:
        model = AllifmaalPurchaseOrdersModel
        fields = ['shipping','uplift', 'comments','supplier','payment_terms','posting_po_status']
        widgets={
            'shipping':forms.TextInput(attrs={'class':'form-control'}),
            'uplift':forms.TextInput(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control'}),
        
            
            'supplier':forms.Select(attrs={'class':'form-control'}),
            'payment_terms':forms.Select(attrs={'class':'form-control'}),
            'posting_po_status':forms.Select(attrs={'class':'form-control'}),
            
            
        }


class AddAllifmaalPurchaseOrderItemsForm(forms.ModelForm):
    class Meta:
        model = AllifmaalPurchaseOrderItemsModel
        fields = ['items','quantity', 'unitcost']
        widgets={
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            'unitcost':forms.TextInput(attrs={'class':'form-control'}),
           
            'items':forms.Select(attrs={'class':'form-control'}),
           
            
        }

class AddAllifmaalPurchaseOrderMiscCostForm(forms.ModelForm):
    class Meta:
        model = AllifmaalPurchaseOrderMiscCostsModel
        fields = ['supplier','description','amount']
        widgets={
            'description':forms.TextInput(attrs={'class':'form-control'}),
            
            'amount':forms.TextInput(attrs={'class':'form-control'}),
        
            'supplier':forms.Select(attrs={'class':'form-control'}),
            
            
        }



###########################3 HRM ###################
class AddStaffForm(forms.ModelForm): #the forms here is the one imported up there.
    class Meta:
        model = AllifmaalHumanResourcesModel
        fields = ["staffNo",'firstName','lastName','middleName','comment','staffImage','staffGender',
        'department',"title",'education','salary']
        widgets={
            'staffNo':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'firstName':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'lastName':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'middleName':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'staffGender':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'comment':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'department':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'education':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'salary':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           

            'staffImage':forms.FileInput(attrs={'class':'form-control','placeholder':''}),
            
        }

################# asset
class AddAllifmaalAssetsForm(forms.ModelForm):
    class Meta:
        model = AllifmaalAssetsModel
        fields = ['description', 'value','lifespan','acquired','asset_account','payment_terms','quantity','cost_account','supplier']
        widgets={
           
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            'value':forms.TextInput(attrs={'class':'form-control'}),
            'lifespan':forms.TextInput(attrs={'class':'form-control'}),
            #'acquired':forms.DateInput(attrs={'class':'form-control'}),
            'acquired' : DatePickerInput(attrs={'class':'form-control'}),
            'cost_account':forms.Select(attrs={'class':'form-control'}),
            'asset_account':forms.Select(attrs={'class':'form-control'}),
            'payment_terms':forms.Select(attrs={'class':'form-control'}),
            'supplier':forms.Select(attrs={'class':'form-control'}),
           

            }
    
    def __init__(self,*args,**kwargs):

        assets_queryset=AllifmaalChartOfAccountsModel.objects.filter(code__lte=19999)
       
        super().__init__(*args, **kwargs)
       
        self.fields['cost_account'].queryset=assets_queryset
        self.fields['asset_account'].queryset=assets_queryset

###################### banks ###################
class AddAllifmaalBankForm(forms.ModelForm):
    class Meta:
        model = AllifmaalBanksModel
        fields = ['name','balance','account','comments']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'balance':forms.TextInput(attrs={'class':'form-control'}),
            'account':forms.TextInput(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control'}),
           
            
        }

class AddAllifmaalBankDepositForm(forms.ModelForm):
    class Meta:
        model = AllifmaalBankDepositsModel
        fields = ['description','amount','bank','comments']
        widgets={
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'amount':forms.TextInput(attrs={'class':'form-control'}),
            'bank':forms.Select(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control'}),
           
            
        }


class AddAllifmaalBankWithdrawalForm(forms.ModelForm):
    class Meta:
        model = AllifmaalBankWithdrawalsModel
        fields = ['description','amount','bank','comments']
        widgets={
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'amount':forms.TextInput(attrs={'class':'form-control'}),
            'bank':forms.Select(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control'}),
           
            
        }

class AddMoneyDrawingForm(forms.ModelForm): #the forms here is the one imported up there.
    class Meta:
        model = MoneyDrawingModel
        fields = ['description','account','amount','fromacc']
        widgets={
           
            'description':forms.TextInput(attrs={'class':'form-control','id':'DescriptionID'}),
            'account':forms.Select(attrs={'class':'form-control','id':'QuantityID'}),
            'fromacc':forms.Select(attrs={'class':'form-control','id':'QuantityID'}),
            'amount':forms.TextInput(attrs={'class':'form-control','id':'AmountID'}),
        }
    def __init__(self,*args,**kwargs):

        account=AllifmaalChartOfAccountsModel.objects.filter(code__lte=69999,code__gte=60000)
        asset=AllifmaalChartOfAccountsModel.objects.filter(code__lte=19999)
       
        super().__init__(*args, **kwargs)
       
        self.fields['account'].queryset=account
        self.fields['fromacc'].queryset=asset
        
###########33 for learing only #3

class AddItemLearningForm(forms.ModelForm): #the forms here is the one imported up there.
    class Meta:
        model = ForLearningOnlyModel
        fields = ["items",'description','quantity','rate','amount']
        widgets={
            'items':forms.Select(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control','id':'DescriptionID'}),
            'quantity':forms.TextInput(attrs={'class':'form-control','id':'QuantityID'}),
            'rate':forms.TextInput(attrs={'class':'form-control','id':'RateID'}),
            'amount':forms.TextInput(attrs={'class':'form-control','id':'AmountID'}),
        }

