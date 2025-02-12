from django.urls import path
from . import views


urlpatterns=[
        path('',views.game_login,name='game_login'),
        path('home/',views.home,name='home'),
        path('game_logout',views.game_logout,name='game_logout'),
        path('add_game',views.add_game,name='add_game'),
        path('edit/<gid>',views.edit,name='edit'),
        path('delete_game/<gid>',views.delete_game,name='delete_game'),
]