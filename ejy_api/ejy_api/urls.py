
from django.contrib import admin
from django.urls import path,include
# from blog_api.views import all_blogs



urlpatterns = [
    path('admin/', admin.site.urls),

    path('blog/',include('blog_api.urls')),
    path('user/',include('user_api.urls')),
    path('comment/',include('comments_api.urls'))

    
        

    

]
