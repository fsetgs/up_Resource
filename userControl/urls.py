
from django.urls import path,include
from userControl import views
app_name='userControl'
urlpatterns = [
    path('login/',views.login),
    path('register/',views.register),
    path('update/<int:id>/',views.update),
    path('usershow/',views.usershow),
    path('insertUser/',views.insertUser),
    path('search_user/',views.search_user),
    path('uppassword/<int:id>/',views.uppassword),

    path('dingdingEnter/',views.dingdingEnter), #钉钉pc端进入后台
    path('verifyIdentity/',views.verifyIdentity), #钉钉pc端校验
]