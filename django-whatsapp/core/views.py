from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import GroupCreationForm
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from .forms import GroupCreationForm
from django.utils import timezone


openai_api_key = 'Your Key'
openai.api_key = openai_api_key

def ask_openai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-4",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
    )

    answer = 'The Bot uses GPT4 model which is paid service hence the service is unavailable currently!!! Sorry for inconviencence'
    return answer

def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})



@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.admin = request.user  # Set the current user as the admin
            group.save()
            form.save_m2m()  # Save the many-to-many members relationship
            return redirect('group_chat', group_id=group.id)
    else:
        form = GroupCreationForm()
    return render(request, 'create_group.html', {'form': form})


class GroupChatView(TemplateView):
    template_name = 'core/group_chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group_id'] = self.kwargs['group_id']
        return context