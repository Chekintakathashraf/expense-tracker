from django.urls  import path
from .views import *
urlpatterns = [
    path('',index,name='index'),
    path('registration/',registration,name='registration'),
    path('login/',login_page,name='login'),
    path('logout/',logout_page,name='logout'),
    path('delete/<uuid>/',deleteTransaction,name='delete')
]
