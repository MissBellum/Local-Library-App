from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/authors', views.authorlist, name="authors"),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('staff/', views.BorrowedListView.as_view(), name='staff'),
    #path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    
]

"""
This approach can be useful if you want to use the same view for multiple resources,
and pass data to configure its behavior in each case.

path('myurl/<fish>', views.my_view, {'my_template_name': 'some_path'}, name='aurl'),
"""
