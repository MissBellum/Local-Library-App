from django.shortcuts import render

# Create your views here.
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin


@login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)



class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 5


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book

"""class AuthorListView(LoginRequiredMixin, generic.DetailView):
    model = Author"""

@login_required
def authorlist(request):
    author_list = Author.objects.all()
    
    context = {
    'author_list' : author_list,
    }
    
    return render(request, 'author_list.html', context=context)

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )    


class BorrowedListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/staff_page.html'
   # paginate_by = 5
    permission_required = 'catalog.can_mark_returned'
    
    def get_queryset(self):
        all_borrows = BookInstance.objects.filter(status__exact='o').order_by('due_back')
        print(all_borrows)
        return (all_borrows)
        
           
