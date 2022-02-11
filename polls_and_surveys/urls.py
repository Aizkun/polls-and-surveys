from django.contrib import admin
from django.urls import path

from Poll import views as pollViews
from Poll.views import LoginFormView, RegisterFormView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginFormView.as_view(), name='login'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', pollViews.home, name='accueil'),
    path('create/', pollViews.create, name='creer'),
    path('vote/<poll_id>/', pollViews.vote, name='vote'),
    path('results/<poll_id>/', pollViews.results, name='resultats'),
]