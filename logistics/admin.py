from django.contrib import admin

from .models import *
admin.site.site_header="Alwen ERP"
admin.site.site_title="Alwen Transport - Admin Site"
admin.site.index_title="Alwen Admin Site"

# Register your models here.
admin.site.register(AlwenVehiclesModel)
admin.site.register(ShipmentsModel)
admin.site.register(ShipmentItemsModel)
admin.site.register(CustomersModel)
admin.site.register(CarriersModel)
admin.site.register(AlwenExpensesModel)
admin.site.register(AlwenAssetsModel)
admin.site.register(AlwenJobsModel)
admin.site.register(AlwenJobItemsModel)
admin.site.register(AlwenJobItemsSellingModel)
admin.site.register(AlwenInvoicesModel)
admin.site.register(AlwenDriversModel)
#admin.site.register(CardsModel)
admin.site.register(AlwenFillUpsModel)
admin.site.register(AlwenServiceDetailsModel)

@admin.register(CardsModel)
class CardsModeladmin(admin.ModelAdmin):
    list_display=('name','number','balance','currency')
    ordering=('name',)# since this is a topple, u need to add the comma and if u leave u will get an error... this sets the ordering
    fields=(('name','number'),'comment','balance','currency')

    #u can also add search box/field if you need
    search_fields=('name','number')
    list_filter=('name','balance')

    

