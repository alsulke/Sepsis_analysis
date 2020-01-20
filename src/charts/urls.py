"""charts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from .views import home,predict
from charts.views import HomeView,ChartData
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',home,name="home"),
    path('predict/',predict,name="predict"),
    # path('model/',model_form_upload,name="model"),
    # path('upload/',simple_upload,name="upload"),
    # path('charts/',get_data,name="charts"),
    url(r'^charts/$', HomeView.as_view(), name='charts'),
    # url(r'^api/data/$', get_data, name='api-data'),
    url(r'^api/chart/data/$', ChartData.as_view()),
    url(r'^admin/', admin.site.urls),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)#settings.MEDIA_URL,
