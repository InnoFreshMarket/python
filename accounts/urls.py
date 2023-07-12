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
    path('get_chat/<int:user_id>', GetChatView.as_view(), name='get_chat'),
    path('chat/<int:chat_id>', MessagesView.as_view(), name='chat'),
    path('chat/<int:chat_id>/post_message', PostMessageView.as_view(), name='post_message'),
    path('chats/', ChatsView.as_view(), name='get_chats'),
    path('items/', ItemsView.as_view(), name='get_items'),
    path('farmer/', ItemsView2.as_view(), name='get_items_farmer'),
    path('to_order/<item_id>/<amount>', AddToOrder.as_view(), name='add_to_order'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('last_order/', LastOrderView.as_view(), name='last_order'),
    path('change_balance/', ChangeBalance.as_view(), name='change_balance'),
    path('pay_for_order/', PayForOrder.as_view(), name='pay_for_order'),
    path('change_inventory/', ChangeFarmerInventory.as_view(), name='change_inventory'),
    path('change_order/', ChangeOrder.as_view(), name='change_inventory'),
    path('clear_order/', ClearOrder.as_view(), name='clear_order'),
    path('delete_item/', DeleteItem.as_view(), name='delete_item'),
    path("", include(router.urls)),
]