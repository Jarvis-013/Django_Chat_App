from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from core.api import MessageModelViewSet, UserModelViewSet
from . import views

router = DefaultRouter()
router.register(r'message', MessageModelViewSet, basename='message-api')
router.register(r'user', UserModelViewSet, basename='user-api')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('', login_required(
        TemplateView.as_view(template_name='core/whatsapp.html')), name='whatsapp'),
    path('simpleui/', login_required(
        TemplateView.as_view(template_name='core/chat.html')), name='simpleui'),
    # path('chatbot/', views.chatbot, name='chatbot'),
    path('chatbot/', login_required(
        TemplateView.as_view(template_name='core/chatbot.html')), name='chatbot'),
    path('create-group/', views.create_group, name='create_group'),
    path('group-chat/<int:group_id>/', GroupChatView.as_view(), name='group_chat'),
    # path('group-chat/<int:group_id>/', GroupChatView.as_view(), name='group_chat'),
]
