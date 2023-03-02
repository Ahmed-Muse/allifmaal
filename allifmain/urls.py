from django.contrib import admin
from django.urls import path, include
import django

#start of images 
from django.conf import settings#for uploading files
from django.conf.urls.static import static
#end of images

urlpatterns = [
    path('admin/', admin.site.urls),
   
    #path('', include('website.urls')),#this line does all the routing for the views
    path('loginpage', include('login.urls')),#point to login


    #since login is doing all the authentication, we need the two lines below
    path('login/', include('django.contrib.auth.urls')),#this ensures and allows that we use the already built in authentication system
    #path('login/', include('login.urls')),#point to login

     path('', include('allifmaalapp.urls')),
     path('logistics/', include('logistics.urls')),

     

     path('allifmaalapp/', include('allifmaalapp.urls')),
     path('stockmanagementapp/', include('stockmanagementapp.urls')),

    
    
    
    ]
    
if settings.DEBUG:#if debug which is in development stage only, then add the path below
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#this will enable 