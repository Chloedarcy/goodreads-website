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
            try:
                # Run the fetch command to get the books
                call_command('fetch_goodreads_data', email=email, password=password)

                # Fetch the newly added books
                books = Book.objects.all()
         
                # Store the list of books in the session
                request.session['books_list'] = [{'title': book.title, 'author': book.author} for book in books]

                print("HERE!")
                
                # Redirect to the index page
                return redirect('index')

            except CommandError as e:
                form.add_error(None, str(e))  # Add error to form
        return render(request, 'crm/goodreads_login.html', {'form': form})
    
def index(request):
    # Retrieve books from the session
    books_list = request.session.pop('books_list', None)

    # If there are no books in the session, fetch from the database
    if not books_list:
        books = Book.objects.all()
        books_list = [{'title': book.title, 'author': book.author} for book in books]

    for book in books:
        print(book.Title)

    return render(request, 'index.html', {'books': books_list})
