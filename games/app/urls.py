from django.urls import path
from . import views
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)


urlpatterns=[
        path('',views.game_login,name='game_login'),
        path('home/',views.home,name='home'),
        path('game_logout',views.game_logout,name='game_logout'),
        path('add_game',views.add_game,name='add_game'),
        path('edit/<gid>',views.edit,name='edit'),
        path('delete_game/<gid>',views.delete_game,name='delete_game'),
        path('adminbookings/', views.admin_bookings, name='admin_bookings'),
        path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
        path('verify_otp_reg',views.verify_otp_reg, name='verify_otp_reg'),



        path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
        path('password_reset_done/', CustomPasswordResetDoneView.as_view(), name='pass_reset_done'),
        path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
        path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='pass_reset_complete'),




        path('register/', views.register, name='register'),
        path('user_home', views.user_home, name='user_home'),
        path('game/<int:game_id>/', views.view_game, name='view_game'),
        path('book-slot/<int:game_id>/', views.book_slot, name='book_slot'),
        path('booking-confirmation/<int:game_id>/', views.booking_confirmation, name='booking_confirmation'),
        path('my-bookings/', views.my_bookings, name='my_bookings'),
        path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
        


]
