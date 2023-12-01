from django.urls import path,include
from .  import views
from.views import SearchResultsView

urlpatterns = [
    path('home',views.home,name='home'),
    path('newuser',views.createUser),
    path('',views.login_form),
    path('logout',views.logout_form),
    path('changepassword',views.changepassword),
    path('cars',views.getcars,name='cars'),
     path('moredetails/<int:car_id>/', views.more_details_view, name='moredetails'),
    path('verify/',views.verifyUser,name="verify"),
    path('success/',views.success,name="success"),
    path('invoice', views.info, name='invoice'),
    path('search',SearchResultsView.as_view(),name='search'),
]