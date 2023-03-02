from django.urls import path


from . import views
app_name='stockmanagementapp'

urlpatterns = [
    path('stock-dashboard', views.stock_dashboard, name="stock-dashboard"),
    path('error-page-landing', views.error_page, name="error_page"),
    path('stock', views.stock, name="stock"),#this is the home page
    path('delete-stock-item/<str:pk>/', views.deletePhysicalStockItem, name="delete-stock-item"),
    path('update-stock-item/<str:pk>/', views.updatePhysicalStock, name="update-stock-item"),
    path('item-details/<str:pk>/', views.productFullDetails, name="item-details"),
    path('issue-stock/<str:pk>/', views.issuePhysicalStockItems, name="issue-stock"),
    path('receive-stock/<str:pk>/', views.receivePhysicalStockItems, name="receive-stock"),
    
    path('receive-or-issue-stock/<str:pk>/', views.issueOrReceiveItems, name="receive-or-issue-stock"),
    path('issued-stock-history', views.issuedPhysicalStockHistory, name="issued-stock-history"),#this is the home page
    path('delete-stock-history/<str:pk>/', views.deletePhysicalStockHistory, name="delete-stock-history"),
    path('purchase-orders', views.purchase_orders_list, name="purchase-orders"),#this is the home page
    path('create_new_po', views.create_new_po, name="create_new_po"),
    path('delete-purchase-order/<str:pk>/', views.delete_po, name="delete-purchase-order"),
    path('add_po_details/<str:pk>/', views.add_po_details, name="add_po_details"),
    path('add_po_items_allif/<str:pk>/', views.add_po_items_allif, name="add_po_items_allif"),
    path('delete_po_item/<str:pk>/', views.delete_po_item, name="delete_po_item"),
    path('post-purchase-order/<str:pk>/', views.posting_po, name="posting_po"),

    #####################################3 interstore transfers section #####################################3
    path('stores', views.stores, name="stores"),#this is the home page
    path('update-store/<int:pk>', views.update_store, name="update-store"),
    path('delete-store/<int:pk>', views.delete_store, name="delete-store"),
    path('add-stock-to-store/<int:pk>', views.add_stock_to_store, name="add-stock-to-store"),
    path('delete-item/<int:pk>', views.delete_store_item, name="delete_store_item"),
    path('transfer-orders', views.transfer_orders_list, name="transfer-orders"),#this is the home page
    path('create-new-transfer-order', views.create_new_transfer_order, name="create-new-transfer-order"),#this is the home page
    path('delete-transfer-order/<int:pk>', views.delete_transfer_order, name="delete-transfer-order"),
    path('add-details-to-transfer-order/<int:pk>', views.add_transfer_order_details, name="add-details-to-transfer-order"),
    path('add-items-to-transfer-order/<int:pk>', views.add_items_to_transfer_order, name="add-items-to-transfer-order"),
    path('delete_transfer_order_item/<int:pk>', views.delete_transfer_order_item, name="delete_transfer_order_item"),
    path('post-transfer-order/<int:pk>', views.post_transfer_order, name="post-transfer-order"),
    path('allifmaal_purchase_order_pdf/<int:pk>', views.allifmaal_purchase_order_pdf, name="allifmaal_purchase_order_pdf"),


    

    #######################3 upload file section ####################
    path('upload-file', views.upload_file_view, name="upload-file"),#this is the home page
    ##################3 tsting @#################3
    path('export-simple-data', views.export_stock, name="export-simple-data"),#this is the home page
    path('simple-upload', views.simple_reference_upload, name="simple-upload"),#this is the home page
    path('upload_stock', views.upload_stock, name="upload_stock"),#this is the home page

    ################################3 sales ############################
    
    path('enterprise_resource_management', views.enterprise_resource_management, name="enterprise_resource_management"),
    path('Allif-invoices-list', views.allif_invoices_list, name="allif_invoices_list"),
    path('create-new-allif-invoice', views.AllifNewInvoice, name="AllifNewInvoice"),
    path('delete-allif-invoice-instance/<int:pk>', views.AllifDeleteInvoice, name="AllifDeleteInvoice"),
    path('allif-add-invoice-details/<int:pk>', views.AllifInvDetails, name="AllifInvDetails"),
    path('allif-add-invoice-items/<int:pk>', views.AllifAddItemsInvoice, name="AllifAddItemsInvoice"),
    path('delete_invoice_item/<int:pk>', views.delete_invoice_item, name="delete_invoice_item"),
    
    path('convert-allif-invoice-to-pdf-doc/<int:pk>', views.AllifInvpdf, name="AllifInvpdf"),
    path('allif-invoice-posting-action/<int:pk>', views.allif_invoice_posting_view, name="allif_invoice_posting_view"),
    path('allif-posted-invoices', views.allif_posted_invoices_list, name="allif_posted_invoices_list"),
    path('Allif_delete_posted_invoice/<int:pk>', views.Allif_delete_posted_invoice, name="Allif_delete_posted_invoice"),

    path('allif_add_show_expenses', views.allif_add_show_expenses, name="allif_add_show_expenses"),
    path('delete-expense/<int:pk>', views.deleteAllifExpenses, name="deleteAllifExpenses"),
    path('allif_customerPayments', views.allif_customerPayments, name="allif_customerPayments"),
    path('deleteAllifPayment/<int:pk>', views.deleteAllifPayment, name="deleteAllifPayment"),
    




    ##################################


    

    
   
  
]