from django.urls import path
from .views import UserRegistration, UserLogin
from .views import ContentItemCreateView, ContentItemList,ContentItemDeleteView,AdminContentItemList
# , ContentItemUpdateView, ContentItemDeleteView

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-register'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('content/create/', ContentItemCreateView.as_view(), name='content-create'),
    path('content/list/', ContentItemList.as_view(), name='content-list'),
    path('content/<int:item_id>/delete/', ContentItemDeleteView.as_view(), name='content-delete'),
    path('admincontent/list/', AdminContentItemList.as_view(), name='admin-content-list'),


#     path('content/<int:content_id>/update/', ContentItemUpdateView.as_view(), name='content-update'),
]

