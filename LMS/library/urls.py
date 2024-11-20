from django.urls import path,include
from . import views

from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
    path('home/',views.home,name='home'),
    path('books/',views.Books,name='books'),
    path('mybag/',views.myBag,name='myBag'),
    path('add_to_bag/',views.add_to_bag,name='add_to_bag'),
    path('remove/',views.remove_book,name='remove'),
    path('checkout/',views.checkout,name='checkout'),
    path('returns/',views.returns,name='returns'),
    path('rental/',views.rental,name='rental'),
    path('search_books/',views.search_books,name='search_books'),
    path('login/',LoginView.as_view(template_name='registration/login.html'),name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.custom_logout,name='logout'),
    path('readers/',views.readers,name='readers'),
    path('fine/',views.fine,name='fine'),
]
