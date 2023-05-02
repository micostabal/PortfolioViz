from django.urls import path
from portfolioviz import views  

urlpatterns = [
    path('ping/', views.pong),
    path('portfolios/', views.get_portfolios),
    path('assets/', views.get_assets),
    path('portfolio/<str:portfolio_id>/value', views.get_portfolio_value),
    path('portfolio/<str:portfolio_id>/weights', views.get_weights),
]
