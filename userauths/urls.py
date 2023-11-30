from django.urls import path
from userauths import views


app_name = "userauths"

urlpatterns = [
    path('sign-up/',views.register_view, name="sign-up"),
    path('log-in/',views.login_view, name="log-in"),
    path('log-out/',views.logout_view, name="log-out"),

]