from django.shortcuts import render,get_object_or_404,redirect
from .models import books,mybag,Checkout
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def home(request):
  return render(request,'main.html')


def Books(request):
  boks=books.objects.all()

  return render(request,'books.html',{'boks':boks})


@login_required
def add_to_bag(request):
    
    if request.method == "POST":
        print("GOT THE REQUEST")
        book_id = request.POST.get('book_id')  # Getting the book_id from the form submission
        user = request.user
        print(book_id)
        print(user)

        try:
            book = books.objects.get(id=book_id)  # Retrieving the book instance from the database
        except books.DoesNotExist:
            return HttpResponse("Book not found")

        # Creating the mybag item, linking the book to the user's cart
        item, created = mybag.objects.get_or_create(user=user, book=book)
        
        if created:
            messages.success(request,f"'{book.title}' was added.")

        else:
            messages.warning(request,f"'{book.title}' is already added.")
        # if created:
        #     print('Yes Created')
        #     # return redirect('myBag')  # Redirect to the user's "myBag" page if the book was added
        # else:
        #     return HttpResponse("This book is already in your bag")  # If the book is already in the bag, show a message

    return redirect("books")




# @login_required
def myBag(request):
    
    if request.user.is_authenticated:
        current_date_time=timezone.now()
        # Retrieve the user's mybag items
        mybag_items = mybag.objects.filter(user=request.user)

        return render(request, 'myBag.html', {'mybag_items': mybag_items,'current_date_time':current_date_time})
    else:
        return redirect('login')  # Redirect to login if the user is not authenticated



@login_required
def remove_book(request):
    if request.method=="POST":
        print("Got the signal from you about the getting of the status and it is all good")
        book_id=request.POST.get('book_id')
        print(book_id)
        mybag.objects.filter(user=request.user,book_id=book_id).delete()
        

    else:
        pass
    
    return redirect('myBag')




@login_required
def checkout(request):
    current_date_time = timezone.now()
    
    # Ensure that the user is authenticated
    if request.user.is_authenticated:
        mybag_items = mybag.objects.filter(user=request.user)

        # If the bag is empty, show a warning message and redirect
        if not mybag_items:
            messages.warning(request, "Nothing in the bag")
            return redirect('myBag')

        # Handle the POST request for checkout
        if request.method == "POST":
            start_date = current_date_time
            return_date_str = request.POST.get('return_date')

            try:
                # Parse and validate the return date
                return_date = datetime.strptime(return_date_str, "%Y-%m-%d").date()
                return_due_date = datetime.combine(return_date, start_date.time())
            except ValueError:
                messages.error(request, "Invalid return date format. Please enter a valid date.")
                return redirect('myBag')  # Redirect if invalid date format

            # Loop through the items in the user's bag and create a checkout record
            for item in mybag_items:
                checkoutt = Checkout.objects.create(
                    reader=request.user,  # Associate the checkout with the logged-in user
                    book=item.book,
                    checkout_date=start_date,
                    return_due_date=return_due_date
                )
                # Update the book status to unavailable
                item.book.status = False
                item.book.save()
                checkoutt.save()

            # After processing the checkout, delete items from the user's bag
            mybag_items.delete()

            messages.success(request, "Checkout Successful!")
            
    return redirect('myBag')




@login_required
def returns(request):
    rentals=Checkout.objects.filter(reader=request.user,returned=False)
    # print(rentals.book.title)

    # for rental in rentals:
    #   print(rentals.reader.username)
    

    return render(request,'returns.html',{'rentals':rentals})
   



@login_required
def rental(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            checkout_id = request.POST.get('checkout_id')
            if checkout_id:
                # Ensure the checkout entry is from the logged-in user
                checkout_instance = get_object_or_404(Checkout, id=checkout_id, reader=request.user)
                
                if not checkout_instance.returned:
                    checkout_instance.returned = True
                    checkout_instance.save()

                    # Update book status to available
                    checkout_instance.book.status = True
                    checkout_instance.book.save()

    return redirect('returns')




def search_books(request):
    query = request.GET.get('search_query', '').strip()  # Get the query from the URL parameters
    print("Search query:", query)  # Debugging the query

    if query:
        # Filter books based on the search query (case-insensitive)
        filtered_books = books.objects.filter(title__icontains=query)
    else:
        filtered_books = books.objects.none()  # Return an empty queryset if no query is given

    print("Filtered books:", filtered_books)  # Debugging the filtered books

    # Creating a list of dictionaries with the necessary book details
    results = [
        {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'status': book.status,
            'image_url': book.image.url if book.image else '/static/default_book_image.jpg',  # Fallback for missing images
        }
        for book in filtered_books
    ]
    
    return JsonResponse(results, safe=False)




def signup(request):
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
    else:
            form=UserCreationForm()
    return render(request,'signup.html',{'form':form})


def custom_logout(request):
    logout(request)
    return redirect('books')


def readers(request):
    reader_list=Checkout.objects.filter(returned=False)
    

    return render(request,'readers.html',{'reader_list':reader_list})
    




def fine(request):

    current_date=timezone.now().date()
    print(current_date)
    fine=Checkout.objects.filter(reader=request.user,return_due_date__lt=current_date)
    print(fine)
    
    fines=[]
    for finee in fine:
        overdue_days=(current_date-finee.return_due_date).days
        fine_amount=overdue_days*10

        fines.append({
            'book':finee.book.title,
            'checkout_date':finee.checkout_date,
            'Expected_return_date':finee.return_due_date,
            'overdue_days':overdue_days,
            'fine':fine_amount


        })


    return render(request,'fine.html',{'fines':fines})



        
        
      
        
    
    

