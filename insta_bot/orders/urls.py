from django.urls import path
from .views import book_view, instagram_webhook, panel_view, approve_order, cancel_order

urlpatterns = [
    path('book/', book_view, name='book'),
    path('panel/', panel_view, name='panel'),
    path('approve/<int:order_id>/', approve_order, name='approve_order'),
    path('cancel/<int:order_id>/', cancel_order, name='cancel_order'),

    path('webhook/', instagram_webhook, name='instagram_webhook'),
]







