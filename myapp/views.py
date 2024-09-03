from django.shortcuts import render, redirect

from django.views import View
from .forms import GoodreadsLoginForm
from django.core.management import call_command
from django.core.management import call_command
from django.core.management.base import CommandError

from .models import Book

from django.shortcuts import render, redirect
from .models import Book

class GoodreadsLoginView(View):
    def get(self, request):
        form = GoodreadsLoginForm()
        return render(request, 'crm/goodreads_login.html', {'form': form})

    def post(self, request):
        form = GoodreadsLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Run the fetch command to get the books
            call_command('fetch_goodreads_data', email=email, password=password)

            # Fetch the newly added books
            books = Book.objects.all()

            # Store the list of books in the session
            request.session['books_list'] = [{'title': book.title, 'author': book.author} for book in books]
                
            #Change below
            books_list = request.session.pop('books_list', None)

            # If there are no books in the session, fetch from the database
            if not books_list:
                books = Book.objects.all()
                books_list = [{'title': book.title, 'author': book.author} for book in books]

            render(request, 'crm/index.html', {'books': books_list})
            
        return render(request, 'crm/goodreads_login.html', {'form': form})
    
