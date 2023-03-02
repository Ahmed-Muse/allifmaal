from django.urls import path


#start of images 
from django.conf import settings#for uploading files
from django.conf.urls.static import static
from django.contrib import admin
#end of images

from . import views
app_name='logistics'

urlpatterns = [
        #Leave as empty string for base url
        #path('admin/',admin.site.urls,name='myadminpage'),
        
    path('Alwen-logistics-website', views.alwen_website, name="alwen_website"),
    path('logistics-dashboard', views.logistics_dashboard, name="logistics-dashboard"),
    #path('admin', admin.site.urls),
	path('logistics', views.logistics, name="logistics"),#this is the home page
    path('vehicles', views.vehicles, name="vehicles"),#this is the home page
    path('Alwen-vehicle-details/<str:pk>/', views.alwen_vehicle_details, name="alwen_vehicle_details"),
    path('Delete-vehicle/<str:pk>/', views.delete_alwen_car, name="delete_alwen_car"),
    
    path('update_vehicle_details/<str:pk>/', views.update_vehicle_details, name="update_vehicle_details"),
    path('delete_vehicle/<str:pk>/', views.delete_vehicle, name="delete_vehicle"),
    path('daily-mileages', views.dailyMileage, name="dailyMileage"),#this is the home page
    path('delete_milleage/<str:pk>/', views.delete_milleage, name="delete_milleage"),
    
    path('Alwen-fill-ups', views.fill_ups, name="fill_ups"),
    path('fill-ups-details/<str:pk>/', views.alwen_fillups_details, name="alwen_fillups_details"),
    path('update_fillup/<str:pk>/', views.update_fillup, name="update_fillup"),
    path('delete_alwen_fillup/<str:pk>/', views.delete_alwen_fillup, name="delete_alwen_fillup"),

    
    path('services', views.services, name="services"),
    path('create-new-service', views.create_service, name="create_service"),
    path('delete_service/<str:pk>/', views.delete_service, name="delete_service"),
    
    path('add-service-details/<str:pk>/', views.add_service_details, name="add_service_details"),
    path('add_show_service_tasks/<str:pk>/', views.add_show_service_tasks, name="add_show_service_tasks"),
    path('delete_service_task/<str:pk>/', views.delete_service_task, name="delete_service_task"),

    
 
 
    #########################3 customer section#############################3
    path('customers', views.add_show_customers, name="logistics-customers"),#this is the home page
    path('customer-details/<str:pk>/', views.allifmaalcustomerdetails, name="see-customer-details"),
    path('update-customer-details/<str:pk>/', views.update_customer, name="update-log-customer-details"),
    path('delete-customer/<str:pk>/', views.delete_customer, name="delete-log-customer"),
    path('top-up-customer-account/<str:pk>/', views.topUpCustomerAccount, name="topUpCustomerAccount"),


    #########################3 carrier section#############################3
    path('carriers', views.add_show_carriers, name="logistics-carriers"),#this is the home page
    path('update-carrier-details/<str:pk>/', views.update_carrier, name="update-log-carrier-details"),
    path('delete-carrier/<str:pk>/', views.delete_carrier, name="delete-log-carrier"),

    ################################# shipments section ################3
    path('shipments', views.shipments_list, name="logistics-shipments-list"),#this is the home page
    path('create-shipment', views.create_blank_shipment, name="create-logistics-new-shipments"),
    path('delete-shipment/<int:pk>', views.delete_shipment, name="delete-log-shipment"),

    path('shipment_summary/<int:pk>', views.shipment_summary, name="shipment_summary"),

    path('add-shipment-details/<int:pk>', views.add_shipment_details, name="logistics-add-shipment-details"),
    path('add-items-to-shipment/<int:pk>', views.add_show_shipment_items, name="add-items-to-shipment"),
    path('delete-shipment-item/<int:pk>', views.delete_shipment_item, name="delete-shipment-item"),
    path('update-shipment-item/<int:pk>', views.update_shipment_item, name="update-shipment-item"),
    path('parcel_details/<int:pk>', views.parcel_details, name="parcel_details"),


    ########################3 invoices ########################
    path('Alwen-invoices', views.alwen_invoices, name="alwen_invoices"),
    path('create-new-invoice', views.create_alwen_invoice, name="create_alwen_invoice"),
    path('create_alwen_invoice_job/<int:pk>/', views.create_alwen_invoice_job, name="create_alwen_invoice_job"),
    
    path('add-invoice-details/<int:pk>/', views.add_invoice_details, name="add_invoice_details"),
    path('delete_invoice/<int:pk>', views.delete_invoice, name="delete_invoice"),
    path('add-items-to-invoice/<int:pk>/', views.add_invoice_items_alwen, name="add_invoice_items_alwen"),
    path('post-logistics-invoice/<int:pk>/', views.post_logistics_invoice, name="post_logistics_invoice"),
    
    path('delete_invoice_items/<int:pk>/', views.delete_invoice_items, name="delete_invoice_items"),
    path('posted-invoices', views.allifpostedinvoices, name="allifpostedinvoices"),

    path('alwen-invoice-pdf/<int:pk>', views.alwen_invoice_pdf, name="alwen_invoice_pdf"),

    ###################3 assets ############################### now ok
    path('Alwen-assets', views.AlwenAssets, name="AlwenAssets"),
    path('delete_asset/<int:pk>', views.delete_asset, name="delete_asset"),
    path('AlwenExpenses', views.AlwenExpenses, name="AlwenExpenses"),
    path('alwenDeleteExpense/<int:pk>', views.alwenDeleteExpense, name="alwenDeleteExpense"),

    ################3 jobs #############
    path('alwen_jobs_list', views.alwen_jobs_list, name="alwen_jobs_list"),
    path('create-new-job', views.AllifNewJobs, name="AllifNewJobs"),
    path('delete-job/<int:pk>', views.delete_job, name="delete_job"),

    path('add-job-details/<int:pk>', views.add_job_details, name="add_job_details"),
    path('add-items-to-job/<int:pk>', views.add_job_items, name="add_job_items"),
    path('delete_job_items/<int:pk>', views.delete_job_items, name="delete_job_items"),
    path('alwen_job_invoice_pdf/<int:pk>', views.alwen_job_invoice_pdf, name="alwen_job_invoice_pdf"),

    path('allif_invoice_job/<int:pk>', views.allif_invoice_job, name="allif_invoice_job"),
    path('allif_job_transaction_report_pdf/<int:pk>', views.allif_job_transaction_report_pdf, name="allif_job_transaction_report_pdf"),

    

    ############################################## chart of accounts #####################
    path('add_show_chart_of_accounts', views.add_show_chart_of_account, name="add_show_chart_of_account"),
    path('delete_chart_of_account/<int:pk>', views.delete_chart_of_account, name="delete_chart_of_account"),
    

    #################3 drivers ###############
    path('add_show_drivers', views.add_show_drivers, name="add_show_drivers"),
    path('delete_driver/<int:pk>', views.delete_driver, name="delete_driver"),
    path('update_driver/<int:pk>', views.update_driver, name="update_driver"),

    ####################333 CARDS ################################
    path('cards', views.cards, name="cards"),
    path('update-card/<int:pk>', views.update_card, name="update_card"),
    path('delete-card/<int:pk>', views.deleteCard, name="deleteCard"),
    path('top-up-card/<int:pk>', views.topUpCard, name="topUpCard"),
    path('delete_top_up/<int:pk>', views.delete_top_up, name="delete_top_up"),
    

    
    
	
]
if settings.DEBUG:#if debug which is in development stage only, then add the path below
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#this will enable 