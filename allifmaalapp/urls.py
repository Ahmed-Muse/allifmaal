from django.urls import path
from . import views
app_name='allifmaalapp'
urlpatterns = [
 

path('', views.allifmaalmaindashboard, name="allifmaalmaindashboard"),
path('Allifmaal-Engineering-Ltd-Details/', views.allifmaal_settings_details, name="allifmaal_settings_details"),
path('Allifmaal-Update-Details/<int:pk>/', views.update_allifmaal_company_details, name="update_allifmaal_company_details"),
path('delete-Allifmaal-company-detail/<int:pk>/', views.delete_allifmaal_company_detail, name="delete_allifmaal_company_detail"),

path('Add-Allifmaal-Scope-Detail/', views.allifmaal_scope_details, name="allifmaal_scope_details"),
path('Update-Allifmaal-Scope-detail/<int:pk>/', views.update_allifmaal_scope_details, name="update_allifmaal_scope_details"),
path('delete-Allifmaal-scope-detail/<int:pk>/', views.delete_allifmaal_scope_detail, name="delete_allifmaal_scope_detail"),

################################3 suppliers ##################3
path('Allifmaal-Suppliers/', views.allifmaal_suppliers, name="allifmaal_suppliers"),
path('Allifmaal-Supplier-Details/<int:pk>/', views.show_allifmaal_supplier_details, name="show_allifmaal_supplier_details"),
path('Delete-The-Supplier/<int:pk>/', views.delete_allifmaal_supplier, name="delete_allifmaal_supplier"),
path('Update-Supplier-Details/<int:pk>/', views.update_allifmaal_supplier, name="update_allifmaal_supplier"),


path('Allifmaal-Customers/', views.allifmaalcustomers, name="allifmaalcustomers"),
path('Allifmaal-Customer-Details/<int:pk>/', views.show_allifmaal_customer_details, name="show_allifmaal_customer_details"),
path('delete_customer/<str:pk>/', views.delete_allifmaal_customer, name="delete_allifmaal_customer"),
path('Update-Customer-Details/<str:pk>/', views.update_allifmaal_customer, name="update_allifmaal_customer"),


path('Customer-Payments/', views.AllifmaalCustomerPayments, name="AllifmaalCustomerPayments"),
path('customer-top-up/<str:pk>/', views.AllifmaaltopUpCustomerAccount, name="AllifmaaltopUpCustomerAccount"),
path('Delete-Customer-Payment/<str:pk>/', views.DeleteAllifmaalCustomerPayment, name="DeleteAllifmaalCustomerPayment"),
path('Payment-Details/<str:pk>/', views.AllifmaalCustomerPaymentDetails, name="AllifmaalCustomerPaymentDetails"),


############## QUOTATIONS ########################3
path('Allifmaal-Quotes/', views.allifmaal_quotes, name="allifmaal_quotes"),
path('Create-New-Quote/', views.create_allifmaal_quote, name="create_allifmaal_quote"),
path('Delete-Quote/<int:pk>/', views.delete_allifmaal_quote, name="delete_allifmaal_quote"),
path('Add-Quote-Details/<int:pk>/', views.add_allifmaal_Quote_details, name="add_allifmaal_Quote_details"),
path('Add-Quote-Items/<int:pk>/', views.add_allifmaal_quote_items, name="add_allifmaal_quote_items"),
path('Delete-Quote-Item/<int:pk>/', views.delete_allifmaal_quote_item, name="delete_allifmaal_quote_item"),
path('Convert-Quote-To-Pdf/<int:pk>/', views.allifmaal_quote_to_pdf, name="allifmaal_quote_to_pdf"),


############ invoices #################
path('Allifmaal-Invoices/', views.allifmaal_invoices, name="allifmaal_invoices"),
path('Create-New-Invoice/', views.create_allifmaal_invoice, name="create_allifmaal_invoice"),
path('Delete-This-Invoice!/<str:pk>/', views.delete_allifmaal_invoice, name="delete_allifmaal_invoice"),
path('Delete-This-Posted-Invoice!/<str:pk>/', views.delete_allifmaal_posted_invoice, name="delete_allifmaal_posted_invoice"),
path('Add-Invoice-Details/<str:pk>/', views.add_allifmaal_invoice_details, name="add_allifmaal_invoice_details"),
path('Add-Invoice-Items/<str:pk>/', views.add_allifmaal_invoice_items, name="add_allifmaal_invoice_items"),
path('Delete-Item-From-This-Invoice/<str:pk>/', views.delete_allifmaal_invoice_item, name="delete_allifmaal_invoice_item"),
path('Post-Invoice/<str:pk>/', views.post_allifmaal_invoice, name="post_allifmaal_invoice"),
path('Convert-Invoice-To-Pdf/<str:pk>/', views.allifmaal_invoice_to_pdf, name="allifmaal_invoice_to_pdf"),
path('Posted-Invoices/', views.allifpostedinvoices, name="allifpostedinvoices"),

##########################3333 expenses #####################
path('Allifmaal-Expenses/', views.allifmaalExpenses, name="allifmaalExpenses"),
path('Delete-Expense/<str:pk>/', views.deleteAllifmaalExpense, name="deleteAllifmaalExpense"),

####################### TASKS #################3
path('Allifmaal-Tasks/', views.allifmaal_Tasks, name="allifmaal_Tasks"),
path('Mark-This-Task-Complete/<str:pk>/', views.markAllifmaalTaskComplete, name="markAllifmaalTaskComplete"),
path('Completed-Tasks/', views.allifmaalCompletedTasksList, name="allifmaalCompletedTasksList"),
path('Delete-This-Task/<str:pk>/', views.delete_allifmaal_task, name="delete_allifmaal_task"),
path('Update-This-Task/<str:pk>/', views.update_allifmaal_tasks, name="update_allifmaal_tasks"),

########################### accounting #####################3
path('Allifmaal-general-ledgers/', views.allifmaalGeneralLedgers, name="allifmaalGeneralLedgers"),
path('View-General-Ledger-Details/<str:pk>/', views.AllifmaalGeneralLedgerDetails, name="AllifmaalGeneralLedgerDetails"),

path('Update-General-Ledger-Account/<str:pk>/', views.updateAllifmaalGeneralLedger, name="updateAllifmaalGeneralLedger"),
path('Delete-General-Ledger-Account/<str:pk>/', views.deleteAllifmaalGeneralLedgerAccount, name="deleteAllifmaalGeneralLedgerAccount"),
 
path('Allifmaal-Chart-Of-Accounts/', views.allifmaal_add_show_chart_of_account, name="allifmaal_add_show_chart_of_account"),
path('Allifmaal-Delete-Chart-Of-Account/<str:pk>/', views.allifmaal_delete_chart_of_account, name="allifmaal_delete_chart_of_account"),
path('Allifmaal-Edit-Chart-Of-Account/<str:pk>/', views.edit_chart_of_account, name="edit_chart_of_account"),
path('View-Account-Details/<str:pk>/', views.show_account_of_account_details, name="show_account_of_account_details"),

path('Synchronize-Account/', views.synchacc, name="synchacc"),
########################################3 INVENTORY ######################################
path('Allifmaal-Inventory-Categories/', views.allifmaal_inventory_category, name="allifmaal_inventory_category"),
path('Update-Inventory-Category/<str:pk>/', views.allifmaalUpdateStockCategoryDetails, name="allifmaalUpdateStockCategoryDetails"),
path('Delete-Category/<str:pk>/', views.deleteStockCategory, name="deleteStockCategory"),
path('Category-Details/<str:pk>/', views.allifmaalStockCategoryDetails, name="allifmaalStockCategoryDetails"),

path('Allifmaal-Inventory/', views.allifmaal_inventory, name="allifmaal_inventory"),
path('View-Product-Details/<str:pk>/', views.allifmaalProductFullDetails, name="allifmaalProductFullDetails"),
path('Delete-Stock-Item/<str:pk>/', views.deleteStockItem, name="deleteStockItem"),
path('Update-Item-Details/<str:pk>/', views.allifmaalUpdateStockDetails, name="allifmaalUpdateStockDetails"),

path('Physical-Inventory/', views.physicalInventory, name="physicalInventory"),


# Purchase orders
path('Allifmaal-Purchase-Orders/', views.AllifmaalPurchaseOrders, name="AllifmaalPurchaseOrders"),
path('Create-New-Purchase-Order/', views.Allifmaal_create_new_purchase_order, name="Allifmaal_create_new_purchase_order"),
path('Delete-This-Purchase-Order/<int:pk>/', views.AllifmaalDeletePO, name="AllifmaalDeletePO"),
path('Add-PO-Details/<int:pk>/', views.Allifmaal_Add_PO_Details, name="Allifmaal_Add_PO_Details"),
path('Add-Allifmaal-PO-Items/<int:pk>/', views.Allifmaal_Add_PO_items, name="Allifmaal_Add_PO_items"),
path('Delete-PO-Item/<int:pk>/', views.delete_allifmaal_po_item, name="delete_allifmaal_po_item"),

path('Add-Misc-Cost-To-This-PO/<int:pk>/', views.Allifmaal_Add_PO_Misc_Cost, name="Allifmaal_Add_PO_Misc_Cost"),
path('Delete-PO-Misc-Cost-Item/<int:pk>/', views.delete_allifmaal_po_misc_cost, name="delete_allifmaal_po_misc_cost"),
path('Post-This-Purchase-Order/<int:pk>/', views.AllifmaalPOPosting, name="AllifmaalPOPosting"),


##################### HRM ##########################
path('human-resource', views.hrm, name="human-resource"),#this is the home page
path('delete-staff/<str:pk>/', views.deleteStaff, name="delete-staff"),
path('update-staff/<str:pk>/', views.updateStaffDetails, name="update-staff"),
path('Staff-Details/<str:pk>/', views.staff_Details, name="staff_Details"),

########### ASSETS ###################
path('Allifmaal-Assets/', views.AllifmaalAssets, name="AllifmaalAssets"),
path('Delete-This-Asset/<str:pk>/', views.DeleteAllifmaalAsset, name="DeleteAllifmaalAsset"),

####################### BANKS SECTION ####################
path('Allifmaal-Banks', views.AllifmaalBanks, name="AllifmaalBanks"),#this is the home page
path('View-Bank-Details/<str:pk>/', views.ShowBankDetails, name="ShowBankDetails"),
path('Update-Bank-Details/<str:pk>/', views.updateBankDetails, name="updateBankDetails"),
path('Delete-This-Bank/<str:pk>/', views.deleteBank, name="deleteBank"),

path('Allifmaal-Bank-Deposits', views.AllifmaalBankDeposits, name="AllifmaalBankDeposits"),
path('Delete-This-Bank-Deposit/<str:pk>/', views.deleteBankDeposit, name="deleteBankDeposit"),
path('Edit-This-Deposit/<str:pk>/', views.updateBankDepositDetails, name="updateBankDepositDetails"),
path('Show-Deposit-Details/<str:pk>/', views.ShowBankDepositDetails, name="ShowBankDepositDetails"),


path('Allifmaal-Bank-Withdrawals', views.AllifmaalBankWithdrawls, name="AllifmaalBankWithdrawls"),
path('Delete-This-Bank-Withdrawal/<str:pk>/', views.deleteBankWithdrawal, name="deleteBankWithdrawal"),
path('Edit-Withdrawal-Details/<str:pk>/', views.updateBankWithdrawalDetails, name="updateBankWithdrawalDetails"),
path('Withdrawal-Details/<str:pk>/', views.ShowBankWithdrawalDetails, name="ShowBankWithdrawalDetails"),

########################## profit and loss ###############
path('Profit-And-Loss', views.profitAndLoss, name="profitAndLoss"),

############## money withdrawal from the business ###############
path('Cash-Withdrawings', views.moneyWithdrawalFromCompany, name="moneyWithdrawalFromCompany"),
path('Update-Cash-Withdrawings/<str:pk>/', views.updateMoneyWithdrawalDetails, name="updateMoneyWithdrawalDetails"),
path('Delete-Cash-Withrawal/<str:pk>/', views.deleteMoneyWithdrawal, name="deleteMoneyWithdrawal"),
  
  ########### for learning only ############3
  path('forlearningonly', views.forlearningonly, name="forlearningonly"),
  path('Auto-Fill-Form-Field-On-Selection', views.autofill_form_field_when_dropdown_selected, name="autofill_form_field_when_dropdown_selected"),
  path('edit_autofill_form_field_when_dropdown/<str:pk>/', views.edit_autofill_form_field_when_dropdown, name="edit_autofill_form_field_when_dropdown"),
  path('delete_autofill_form_field_when_dropdown/<str:pk>/', views.delete_autofill_form_field_when_dropdown, name="delete_autofill_form_field_when_dropdown"),
 
  
]   
