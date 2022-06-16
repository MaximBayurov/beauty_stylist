from django import forms
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from .forms import UserRegistrationForm


def index(request):
    return render(request, 'djangoProject/main.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    process_form(user_form)
    return render(request, 'registration/register.html', {'user_form': user_form})


class CustomLoginView(LoginView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        process_form(context['form'])

        return context


def process_form(form):
    if not isinstance(form, forms.BaseForm):
        return

    for field in form.fields:
        form.fields[field].widget.attrs['class'] = 'form-control'

    fields_order = list(form.fields)
    form.fields[fields_order[0]].widget.attrs['order'] = 'first'
    form.fields[fields_order[len(fields_order) - 1]].widget.attrs['order'] = 'last'
