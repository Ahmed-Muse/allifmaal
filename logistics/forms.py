from django import forms

from .models import *

#from .allifwidget1 import DatePickerInput, TimePickerInput, DateTimePickerInput

############################# start of datepicker customization ##############################
class DatePickerInput(forms.DateInput):#use this class whereever you have a date and it will give you the calender
    input_type = 'date'#
class TimePickerInput(forms.TimeInput):#use this wherever you have time input
    input_type = 'time'
class DateTimePickerInput(forms.DateTimeInput):#use this wherever you have datetime input
    input_type = 'datetime'
    ################################# end of datepicker customization ################################

class AddVehicleDetailsForm(forms.ModelForm): #the forms here is the one imported up there.
    class Meta:
        model = AlwenVehiclesModel
        #fields = ['vehicle_image','vehicle_name', 'vehicle_make', 'vehicle_model',
                       #'year','license','vin','starting_odometer','primary_meter','vehicle_type','vehicle_status']
        fields = ['vehicle_image','vehicle_name','vehicle_make','vehicle_model', 'year','vehicle_type','vehicle_status','primary_meter','starting_odometer','mydocument','oil_type','oil_capacity','operator','comments']
        widgets={
            'vehicle_name':forms.TextInput(attrs={'class':'form-control'}),
            'vehicle_make':forms.TextInput(attrs={'class':'form-control'}),
            'vehicle_model':forms.TextInput(attrs={'class':'form-control'}),
            
            'starting_odometer':forms.TextInput(attrs={'class':'form-control'}),
            'year':forms.TextInput(attrs={'class':'form-control'}),

            
            'oil_capacity':forms.TextInput(attrs={'class':'form-control'}),
            'operator':forms.Select(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control'}),

            'oil_type':forms.Select(attrs={'class':'form-control'}),
            'vehicle_status':forms.Select(attrs={'class':'form-control'}),
            'vehicle_type':forms.Select(attrs={'class':'form-control'}),
            'primary_meter':forms.Select(attrs={'class':'form-control'}),
            'vehicle_image':forms.FileInput(attrs={'class':'form-control'}),
            'mydocument':forms.FileInput(attrs={'class':'form-control'}),
           
            #form-control here is the css class that we are passing
        }

        #fields='__all__'# this was used because of an error when running and the error said " .

class AddVehicleDailyMileageForm(forms.ModelForm): #the forms here is the one imported up there.
    class Meta:
        model = AlwenDailyMileageModel
        fields = ['vehicle','starting_odometer','ending_odometer','operator','notes']
        widgets={
            'starting_odometer':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'ending_odometer':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'operator':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'notes':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'vehicle':forms.Select(attrs={'class':'form-control','placeholder':''}),
        }

class AddFillUpsForm(forms.ModelForm): #the forms here is the one imported up there.
    class Meta:
        model = AlwenFillUpsModel
        fields = ['vehicle','card','quantity','unit_price','odometer','oil_type','station','operator','payment','receipt','notes','fuel_brand']

        widgets={
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            'unit_price':forms.TextInput(attrs={'class':'form-control'}),
            'odometer':forms.TextInput(attrs={'class':'form-control'}),
            'station':forms.TextInput(attrs={'class':'form-control'}),
            'operator':forms.Select(attrs={'class':'form-control'}),
            'fuel_brand':forms.TextInput(attrs={'class':'form-control'}),
            'notes':forms.TextInput(attrs={'class':'form-control'}),

            'vehicle':forms.Select(attrs={'class':'form-control'}),
            'card':forms.Select(attrs={'class':'form-control'}),
            'oil_type':forms.Select(attrs={'class':'form-control'}),
            'receipt':forms.FileInput(attrs={'class':'form-control','placeholder':''}),
            'payment':forms.Select(attrs={'class':'form-control'}),
        }

class AddServiceDetailsForm(forms.ModelForm):
    class Meta:
        model = AlwenServiceDetailsModel
        fields = ['vehicle','odometer','service_center','receipt','serviced_by','notes']
        widgets={
            'vehicle':forms.Select(attrs={'class':'form-control'}),
            'odometer':forms.TextInput(attrs={'class':'form-control'}),
            'service_center':forms.TextInput(attrs={'class':'form-control'}),
            
            'receipt':forms.FileInput(attrs={'class':'form-control'}),
            'serviced_by':forms.TextInput(attrs={'class':'form-control'}),
            'notes':forms.TextInput(attrs={'class':'form-control'}),

            }

class AddServiceTasksForm(forms.ModelForm):
    class Meta:
        model = ServiceTasksModel
        fields = ['task','spares_cost','labor_cost']
        widgets={
            'task':forms.TextInput(attrs={'class':'form-control'}),
            'spares_cost':forms.TextInput(attrs={'class':'form-control'}),
            'labor_cost':forms.TextInput(attrs={'class':'form-control'}),
            
            
        }


class VehicleDetailsUpdateForm(forms.ModelForm):
    class Meta:
        model = AlwenVehiclesModel
        #fields = ['vehicle_image','vehicle_name', 'vehicle_make', 'vehicle_model',
                       #'year','license','vin','starting_odometer','primary_meter','vehicle_type','vehicle_status']
        fields = ['vehicle_image','vehicle_name','vehicle_make','vehicle_model', 'year','vehicle_type','vehicle_status','primary_meter','starting_odometer','mydocument',
        'oil_type','oil_capacity','comments','operator']
        widgets={
            'vehicle_name':forms.TextInput(attrs={'class':'form-control'}),
            'vehicle_make':forms.TextInput(attrs={'class':'form-control'}),
            'vehicle_model':forms.TextInput(attrs={'class':'form-control'}),
            
            'starting_odometer':forms.TextInput(attrs={'class':'form-control'}),
            'year':forms.TextInput(attrs={'class':'form-control'}),
            'oil_capacity':forms.TextInput(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control'}),
            'operator':forms.Select(attrs={'class':'form-control'}),

            'oil_type':forms.Select(attrs={'class':'form-control'}),
            'vehicle_status':forms.Select(attrs={'class':'form-control'}),
            'vehicle_type':forms.Select(attrs={'class':'form-control'}),
            'primary_meter':forms.Select(attrs={'class':'form-control'}),
            
           
            #form-control here is the css class that we are passing
        }


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = CustomersModel
        fields = ['name','phone','email','country', 'city','address','contact']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),

            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'city':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'contact':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'country':forms.Select(attrs={'class':'form-control'}),
        
        }

class AddCustomerPaymentForm(forms.ModelForm):
    class Meta:
        model =CustomerPaymentsModel
        fields = ['customer','amount','comments']
        widgets={
            'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'customer':forms.Select(attrs={'class':'form-control'}),
        
        }



class AddCarrierForm(forms.ModelForm):
    class Meta:
        model = CarriersModel
        fields = ['carrier','capacity','unit', 'owner','phone','email','address']

class AddShippmentForm(forms.ModelForm):
    class Meta:
        model = ShipmentsModel
        fields = ['carrier','date','expected', 'status','origin','destination','via','comments']
        widgets={
            'origin':forms.TextInput(attrs={'class':'form-control'}),
            'destination':forms.TextInput(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control'}),
            'carrier':forms.Select(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'via':forms.Select(attrs={'class':'form-control'}),
            'date':forms.DateInput(attrs={'class':'form-control'}),
            'date' : DatePickerInput(attrs={'class':'form-control'}),
            #'expected':widgets.DateInput(attrs={'type': 'date'}),
            'expected' : DatePickerInput(attrs={'class':'form-control'}),
            #'expected': forms.DateInput(attrs={'class': 'datepicker', 'id': 'data_input'})
           
            #form-control here is the css class that we are passing
        }
        

        #widgets = {
            #'order_date': widgets.DateInput(attrs={'type': 'date'})
        #}
        #fields='__all__'# this was used because of an error when running and the error said " .


class AddShippmentItemsForm(forms.ModelForm):
    class Meta:
        model = ShipmentItemsModel
        fields = ['consigner','consignee', 'details','address','weight','units',
        'lenth','width','height','dimension_units','received','value','rate','payer','payment','status','destination','comments']

        widgets={
            'consigner':forms.Select(attrs={'class':'form-control'}),
            'consignee':forms.Select(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'payer':forms.Select(attrs={'class':'form-control'}),
            'payment':forms.Select(attrs={'class':'form-control'}),
            
            'units':forms.Select(attrs={'class':'form-control'}),
            'dimension_units':forms.Select(attrs={'class':'form-control'}),
            
            'rate':forms.TextInput(attrs={'class':'form-control'}),
            
            'details':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control'}),
            'weight':forms.TextInput(attrs={'class':'form-control'}),
            'lenth':forms.TextInput(attrs={'class':'form-control'}),
            'height':forms.TextInput(attrs={'class':'form-control'}),
            'width':forms.TextInput(attrs={'class':'form-control'}),
            'destination':forms.TextInput(attrs={'class':'form-control'}),
            'value':forms.TextInput(attrs={'class':'form-control'}),
            
            #'received':forms.DateInput(attrs={'class':'form-control'}),
            'received' : DatePickerInput(attrs={'class':'form-control'}),
           
            #form-control here is the css class that we are passing
        }
        #fields='__all__'# this was used because of an error when running and the error said " .


class AddAlwenInvoiceDetailsForm(forms.ModelForm):
    class Meta:
        model = AlwenInvoicesModel
        fields = ['customer','invoice_terms', 'invoice_due_Date','invoice_status','invoice_currency','invoice_comments','job','posting_inv_status']

        widgets={
            'invoice_comments':forms.TextInput(attrs={'class':'form-control'}),
            
            'customer':forms.Select(attrs={'class':'form-control'}),
            'invoice_terms':forms.Select(attrs={'class':'form-control'}),
            'invoice_status':forms.Select(attrs={'class':'form-control'}),
            'invoice_currency':forms.Select(attrs={'class':'form-control'}),
            'job':forms.Select(attrs={'class':'form-control'}),
            'posting_inv_status':forms.Select(attrs={'class':'form-control'}),

            #'invoice_due_Date':forms.DateInput(attrs={'class':'form-control'}),
            'invoice_due_Date' : DatePickerInput(attrs={'class':'form-control'}),
            
           
            #form-control here is the css class that we are passing
        }
        #fields='__all__'# this was used because of an error when running and the error said " .

class AddAlwenInvoiceItemsForm(forms.ModelForm):
    class Meta:
        model = AlwenInvoiceItemsModel
        fields = ['description','quantity','unit_price' ]

        widgets={
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            'unit_price':forms.TextInput(attrs={'class':'form-control'}),
            
        }
        

class AddAlwenAssetsForm(forms.ModelForm):
    class Meta:
        model = AlwenAssetsModel
        fields = ['description', 'value','lifespan','acquired']
        widgets={
           
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'value':forms.TextInput(attrs={'class':'form-control'}),
            'lifespan':forms.TextInput(attrs={'class':'form-control'}),
            #'acquired':forms.DateInput(attrs={'class':'form-control'}),
            'acquired' : DatePickerInput(attrs={'class':'form-control'}),
           

            }


class AddAlwenExpensesForm(forms.ModelForm):
    class Meta:
        model = AlwenExpensesModel
        fields = ['description', 'amount','comments']
        widgets={
           
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'amount':forms.TextInput(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control'}),
           

            }

class AddAlwenJobDetailsForm(forms.ModelForm):
    class Meta:
        model = AlwenJobsModel
        fields = ['customer','description', 'vehicle','driver','ending_date','starting_odometer',
        'ending_odometer','status','comments','uplift','refernce','delivery']

        widgets={
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'delivery':forms.TextInput(attrs={'class':'form-control'}),
            'starting_odometer':forms.TextInput(attrs={'class':'form-control'}),
            'ending_odometer':forms.TextInput(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control'}),
            'uplift':forms.TextInput(attrs={'class':'form-control'}),
            'refernce':forms.TextInput(attrs={'class':'form-control'}),
            'customer':forms.Select(attrs={'class':'form-control'}),
            'vehicle':forms.Select(attrs={'class':'form-control'}),
            'driver':forms.Select(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            
            #'ending_date':forms.DateInput(attrs={'class':'form-control'}),
            'ending_date' : DatePickerInput(attrs={'class':'form-control'}),
            
            
           
            #form-control here is the css class that we are passing
        }




class AddAlwenJobItemsForm(forms.ModelForm):
    class Meta:
        model = AlwenJobItemsModel
        fields = ['description', 'quantity','unit_cost','comments']

        widgets={
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            'unit_cost':forms.TextInput(attrs={'class':'form-control'}),
            
            'comments':forms.TextInput(attrs={'class':'form-control'}),
           

            'description':forms.Select(attrs={'class':'form-control'}),
            
            
           
            #form-control here is the css class that we are passing
        }



############################# chart of accounts ##################3
class AddAllifChartOfAccountForm(forms.ModelForm):
    class Meta:
        model = AllifChartOfAccountsModel
        fields = ['code','description', 'statement','category','nature','type','balance']
        widgets={
            'code':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'balance':forms.TextInput(attrs={'class':'form-control'}),
            
            'statement':forms.Select(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'nature':forms.Select(attrs={'class':'form-control'}),
            'type':forms.Select(attrs={'class':'form-control'}),
           
            
           
            #form-control here is the css class that we are passing
        }

class AdddriversForm(forms.ModelForm):
    class Meta:
        model=AlwenDriversModel
        fields=['name','photo','driver_license','driver_id']

        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'photo':forms.FileInput(attrs={'class':'form-control'}),
            'driver_license':forms.FileInput(attrs={'class':'form-control'}),
            'driver_id':forms.FileInput(attrs={'class':'form-control'}),
            
           
            #form-control here is the css class that we are passing
        }

#################################3 CARDS ###############################3

class AddCardsForm(forms.ModelForm):
    class Meta:
        model=CardsModel
        fields=['name','number','balance','comment','currency']

        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'number':forms.TextInput(attrs={'class':'form-control'}),
            'balance':forms.TextInput(attrs={'class':'form-control'}),
            'comment':forms.TextInput(attrs={'class':'form-control'}),
            'currency':forms.Select(attrs={'class':'form-control'}),
          
        }

class AddCardTopUpsForm(forms.ModelForm):
    class Meta:
        model=CardsTopUpsModel
        fields=['card','amount','comments']

        widgets={
            'card':forms.Select(attrs={'class':'form-control'}),
            'amount':forms.TextInput(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control'}),
          
        }


