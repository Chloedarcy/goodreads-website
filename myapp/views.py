from django.shortcuts import render, redirect

from django.views import View
from .forms import GoodreadsLoginForm
from django.core.management import call_command
from django.core.management import call_command
from django.core.management.base import CommandError

from .models import Book

def index(request):
    books = Book.objects.all()
    return render(request, 'index.html', {'books': books})


class GoodreadsLoginView(View):
    def get(self, request):
        form = GoodreadsLoginForm()
        return render(request, 'crm/goodreads_login.html', {'form': form})

    def post(self, request):
        form = GoodreadsLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                call_command('fetch_goodreads_data', email=email, password=password)
                return redirect('index')  # Redirect to the index page
            except CommandError as e:
                form.add_error(None, str(e))  # Add error to form
        return render(request, 'crm/goodreads_login.html', {'form': form})