from django import forms
from .models import *
from django.forms import (formset_factory, modelformset_factory)
#below is for EMS

class AddPhysicalProductForm(forms.ModelForm): #the forms here is the one imported up there.
    class Meta:
        model = PhysicalStockModel
        fields = ["partNumber",'description','quantity','unitcost','unitPrice','comments','weight','length',
        'width','color',"expiryDate",'reorderLevel',"vendor"]

        widgets={
            'partNumber':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'quantity':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'unitcost':forms.TextInput(attrs={'class':'form-control','placeholder':''}),

            'unitPrice':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'weight':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'length':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'width':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'color':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'expiryDate':forms.DateInput(attrs={'class':'form-control','placeholder':''}),
            'reorderLevel':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'vendor':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        }


class IssuePhysicalItemsForm(forms.ModelForm):
    	class Meta:
            model = PhysicalStockModel
            fields = ['description','issuedQuantity', 'issuedTo']
            widgets={
            'issuedQuantity':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'issuedTo':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            
        }
class ReceivePhysicalItemsForm(forms.ModelForm):
    	class Meta:
            model = PhysicalStockModel
            fields = ['description','receivedQuantity']
            widgets={
            'receivedQuantity':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           }
class PhysicalItemsReorderLevelForm(forms.ModelForm):
    	class Meta:
            model = PhysicalStockModel
            fields = ['reorderLevel']

class AboutPhysicalItemsForm(forms.ModelForm):
    	class Meta:
            model = PhysicalStockModel
            fields = ['weight','length']

class SearchPhysicalItemsForm(forms.ModelForm):
    	class Meta:
            model = PhysicalStockModel
            fields = ['partNumber','description']
            widgets={
            'partNumber':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           }

class addPODetailForm(forms.ModelForm):
    	class Meta:
            model = PurchaseOrdersModel
            fields = ['shipping','uplift','comments']
            widgets={
            'shipping':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'uplift':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           }

class addPOItemsForm(forms.ModelForm):
    	class Meta:
            model = PurchaseOrderItemsModel
            fields = ['supplier','items','quantity','unitcost','notes']
            widgets={
            'supplier':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'items':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'quantity':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'unitcost':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'notes':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           }


class AddAllifInvoiceForm(forms.ModelForm):
    class Meta:
        model = AllifInvoicesModel
        fields = ['customer','terms', 'due','status','currency','comments','posted']
        #posted=forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-control'}))
        posted=forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-control'}))
        widgets={
            'customer':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'terms':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'due':forms.DateInput(attrs={'class':'form-control','placeholder':''}),
            'status':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'currency':forms.Select(attrs={'class':'form-control','placeholder':''}),
            #'posted':forms.BooleanField(attrs={'class':'form-control'}),
            
            
            
           }

class AddAllifInvoiceItemsForm(forms.ModelForm):
    class Meta:
        model = AllifInvoiceItemsModel
        fields = ['description','quantity']
        widgets={
            'description':forms.Select(attrs={'class':'form-control','placeholder':''}),
           
            'quantity':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            
           }


############################################################3333 zamzam section###########################


######################################33 uploading excel files
class AddCSVFileForm(forms.ModelForm):
    	class Meta:
            model = Csv
            fields = ['file_name']


#################################3 transfer orders#########################3
class AddStoreForm(forms.ModelForm):
    	class Meta:
            model = StoresModel
            fields = ['name','comments']
            widgets={
            
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            
           }
            
class AddItemsToStoreForm(forms.ModelForm):
    	class Meta:
            model = StoreItemsModel
            fields = ['description','quantity','comments']
            widgets={
            
            'description':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'quantity':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            
           }


class AddTransferOderDetailsForm(forms.ModelForm):
    	class Meta:
            model = TransferOrdersModel
            fields = ['from_store','to_store','comments']
            widgets={
            
            'from_store':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'to_store':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            
           }

class AddItemsToTransferOrderForm(forms.ModelForm):
    	class Meta:
            model = TransferOderItemsModel
            fields = ['item','quantity','comments']
            widgets={
            
            'item':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'quantity':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            
           }

class PersonData(forms.Form):
	class meta:
		model = Person
		fields = '__all__'


class Physicalstockformsuploadexcel(forms.Form):
	class meta:
		model = PhysicalStockModel
		fields = '__all__'


class AllifAddExpensesForm(forms.ModelForm):
    class Meta:
        model = AllifExpensesModel
        fields = ['description', 'amount','comments']
        widgets={
            
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            
           }


class AllifAddCustomerPaymentsForm(forms.ModelForm):
    class Meta:
        model = AllifCustomerPaymentsModel
        fields = ['customer', 'amount','comments']
        widgets={
            
            'customer':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
           }


class AllifAddCustomerBalanceForm(forms.ModelForm):
    class Meta:
        model = AllifCustomersBalanceModel
        fields = ['customer', 'balance']
        widgets={
            
            'customer':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'balance':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            
           }