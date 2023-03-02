from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(StoresModel)

admin.site.register(Csv)
admin.site.register(Sale)
admin.site.register(Person)
admin.site.register(PhysicalStockModel)

admin.site.register(FromStoreModel)
admin.site.register(ToStoreModel)
admin.site.register(TransferingStoreModel)
admin.site.register(ReceivingStoreModel)
admin.site.register(TransferOrdersModel)
admin.site.register(TransferOderItemsModel)
admin.site.register(AllifInvoiceItemsModel)



    