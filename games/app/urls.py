from django.urls import path
from . import views


urlpatterns=[
        path('',views.game_login,name='game_login'),
        path('home/',views.home,name='home'),
        path('game_logout',views.game_logout,name='game_logout'),
        path('add_game',views.add_game,name='add_game'),
        path('edit/<gid>',views.edit,name='edit'),
        path('delete_game/<gid>',views.delete_game,name='delete_game'),
        path('adminbookings/', views.admin_bookings, name='admin_bookings'),



        path('register/', views.register, name='register'),
        path('user_home', views.user_home, name='user_home'),
        path('game/<int:game_id>/', views.view_game, name='view_game'),
        path('game/<int:game_id>/book/', views.book_slot, name='book_slot'),
        path('user/bookings/', views.user_bookings, name='user_bookings'),
        path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
        path('game/<int:game_id>/book/confirmation/', views.booking_confirmation, name='booking_confirmation'),
        path('game/<int:game_id>/booking-success/', views.booking_success, name='booking_success'), 


]
