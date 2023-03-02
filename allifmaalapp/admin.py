from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(AllifmaalDetailsModel)
admin.site.register(AllifmaalInvoiceItemsModel)

admin.site.register(ForLearningOnlyModel)
admin.site.register(AllifmaalChartOfAccountsModel)
admin.site.register(AllifmaalHumanResourcesModel)