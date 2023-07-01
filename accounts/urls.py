from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import *

router = DefaultRouter()
router.register(r"", UserViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('info/<int:user_id>', InfoView.as_view(), name='info'),
    path('comments/<int:id>', CommentView.as_view(), name='comments'),
    path('getId/', MyIdSet.as_view(), name='myid'),
    path('to_order/<item_id>/<amount>', AddToOrder.as_view(), name='add_to_order'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('last_order/', LastOrderView.as_view(), name='last_order'),
    path("", include(router.urls)),
]