from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

# Create your views here.

class CreateUserView(FormView):
    form_class = UserCreationForm
    template_name = "registration/create-user.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f"Logged in as {user.username}!")
        return super().form_valid(form)
