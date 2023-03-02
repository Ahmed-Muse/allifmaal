from import_export import resources
from .models import Person,PhysicalStockModel

class PersonResource(resources.ModelResource):
    class Meta:
        model = Person

class PhysicalStockResource(resources.ModelResource):
    class Meta:
        model = PhysicalStockModel