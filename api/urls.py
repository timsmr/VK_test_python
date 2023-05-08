from django.urls import path
from . import views
app_name = 'api'

urlpatterns = [
    path('create_user/', views.CustomUserCreate.as_view(), name="create_user"),
    path('<int:pk>/', views.CustomUser.as_view(), name="get_user"),
    path('<int:sender>/request/<int:receiver>/', views.CreateRequest.as_view(), name="create_request"),
    path('<int:sender>/request/<int:receiver>/accept/', views.HandleAcceptDecline.as_view(), name="accept_request"),
    path('<int:sender>/request/<int:receiver>/decline/', views.HandleAcceptDecline.as_view(), name="decline_request"),
    path('<int:user>/request/outgoing/', views.HandleOutgoingIncomingRequests.as_view(), name="get_outgoing_requests"),
    path('<int:user>/request/incoming/', views.HandleOutgoingIncomingRequests.as_view(), name="get_incoming_requests"),
    path('<int:pk>/friends/', views.GetFriends.as_view(), name="get_user_friends"),
    path('<int:sender>/friends/<int:receiver>/status/', views.StatusFriend.as_view(), name="get_friend_status"),
    path('<int:sender>/friends/<int:receiver>/delete/', views.DeleteFriend.as_view(), name="delete_friend"),
]
