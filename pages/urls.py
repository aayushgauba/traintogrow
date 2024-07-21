"""
URL configuration for traintogrow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('class', views.classType, name='classType'),
    path('contact', views.contact, name='contact'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('courses', views.courses, name='courses'),
    path('activation/sucess', views.account_activation_sent, name='account_activation_sent'),
    path('reset-password', views.PasswordResetView, name='password_reset'),
    path('logout/', views.logout, name='logout'),
    path('buy-course/<int:course_id>/', views.buy_course, name='buy_course'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('profile', views.profile, name='profile'),
    path('invoices', views.invoices, name='invoices'),
    path('invoices/<int:invoice_id>', views.invoiceDetail, name='invoiceDetail'),
    path('coursework/<int:course_id>/', views.coursework, name='coursework'),
    path('file/<int:file_id>/', views.fileView, name='fileView'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
