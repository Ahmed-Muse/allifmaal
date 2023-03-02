from django.urls import path
app_name='login'
from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('loginpage', views.loginpage, name="loginpage"),#this is the home page
    path('register', views.registerpage, name="registerpage"),#this is the home page
    path('logout', views.logoutpage, name="logout"),#this is the home page
    path('user-profile', views.systemUserProfile, name="user-profile"),#this is the home page
    path('edit-profile', views.editProfile, name="edit-profile"),
	#path('store/', views.store, name="store"),
	
]