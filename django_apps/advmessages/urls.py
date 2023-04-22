from django.urls import include, path
from .views import MessageRequestView

urlpatterns = [
    path(
        '',
        MessageRequestView.as_view(),
        name='message_request_view'
    )
]