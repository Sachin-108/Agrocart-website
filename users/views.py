from django.shortcuts import render,redirect,get_object_or_404
from .models import NewUser,Category,Product,Cart, CartItem,Checkout,onlinepayment,ProductForm,Farmer
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from datetime import date
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib import messages
import json, razorpay


# Create your views here.

@login_required
def admindashboard(request):
    # Check if the user accessing this view is of user_type 'admin'.
    if request.user.user_type != 'admin':
        # If the user is not an admin, return a '403 Forbidden' response.
        return HttpResponseForbidden()
    # If the user is an admin, render the 'admindashboard.html' template.
    return render(request, 'admindashboard.html')


def about(request):
    # Render the 'about.html' template when the 'about' view is accessed.
    return render(request, 'about.html')

def cancellation(request):
    # Render the 'about.html' template when the 'cancellation' view is accessed.
    return render(request, 'cancellation.html')

def policy(request):
    # Render the 'contact.html' template when the 'about' view is accessed.
    return render(request,'policy.html')

def Terms_and_conditions(request):
    # Render the 'about.html' template when the 'cancellation' view is accessed.
    return render(request, 'Terms_and_conditions.html')


def Dharwad(request):
    products = ProductForm.objects.all()
    return render(request, 'Dharwad.html', {'products': products})

def Bengaluru(request):
    products = ProductForm.objects.all()
    return render(request, 'Bengaluru.html', {'products': products})

def Raichur(request):
    products = ProductForm.objects.all()
    return render(request, 'Raichur.html', {'products': products})

def Koppal(request):
    products = ProductForm.objects.all()
    return render(request, 'Koppal.html', {'products': products})



def shipping(request):
    # Render the 'about.html' template when the 'cancellation' view is accessed.
    return render(request, 'shipping.html')

def contact(request):
    # Render the 'contact.html' template when the 'about' view is accessed.
    return render(request,'contact.html')

def orders(request):
    # Render the 'contact.html' template when the 'about' view is accessed.
    return render(request,'orders.html')

def checkout_list(request):
    checkouts = Checkout.objects.all()
    total_orders = checkouts.count()  # Count the total number of orders
    return render(request, 'checkout_list.html', {'checkouts': checkouts, 'total_orders': total_orders})


def index(request):
    # Retrieve all categories from the Category model and store their values.
    # category_values = Category.objects.all().values()
    # Retrieve all products, including their associated categories, from the Product model.
    product_data = ProductForm.objects.all()
    # Initialize variables for the user's shopping cart, cart items, and checkout message.
    cart = None
    cart_items = None
    checkout_message = ""

    # Check if the user is authenticated (logged in).
    if request.user.is_authenticated:
        # Ensure the authenticated user is of user_type 'customer'; otherwise, return a '403 Forbidden' response.
        if request.user.user_type != 'customer':
            return HttpResponseForbidden()
        
        # Try to retrieve the user's shopping cart, including its associated cart items and products.
        try:
            cart = Cart.objects.prefetch_related('cartitem_set__product').get(user=request.user)
            cart_items = cart.cartitem_set.all()
        except Cart.DoesNotExist:
            # If the user has no cart, set cart and cart_items to None.
            cart = None
            cart_items = None

        # Check if the user has items in the cart to display a checkout message.
        if cart_items:
            checkout_message = "You have items in your cart. Proceed to checkout."
    
    # Define the template for rendering the 'index' view.
    template = 'index.html'

    # Create a context dictionary to pass data to the template.
    context = {
        # 'category_values': category_values,
        'product_data': product_data,
        'cart': cart,
        'cart_items': cart_items,
        'checkout_message': checkout_message,
    }

    # Render the 'index.html' template with the provided context data.
    return render(request, template, context)



# login_view
def login_view(request):
    try:
        # Check if the user is already authenticated (logged in).
        if request.user.is_authenticated:
            # If the user is an admin, redirect to the 'admindashboard' view.
            if request.user.user_type == 'admin':
                return redirect('admindashboard')
            # If the user is a customer, redirect to the 'index' view.
            elif request.user.user_type == 'customer':
                return redirect('index')

        # Check if the HTTP request method is POST (typically used for form submissions).
        if request.method == 'POST':
            # Retrieve the username and password from the POST data.
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Try to authenticate the user using the provided username and password.
            user = authenticate(request, username=username, password=password)

            # If a user is authenticated and is of user_type 'customer', log them in and redirect to 'index'.
            if user and user.user_type == 'customer':
                login(request, user)
                return redirect('index')

            # If a user is authenticated and is of user_type 'admin', log them in and redirect to 'admindashboard'.
            if user and user.user_type == 'admin':
                login(request, user)
                print("User ID:", user.id)  # Print the user's ID (for debugging or logging purposes).
                return redirect('admindashboard')

            # If the user authentication fails, display an error message and render the 'login' template.
            else:
                error_message = 'Invalid login credentials'
                return render(request, 'customer_register.html', {'error_message': error_message})

        # If the HTTP request method is not POST (e.g., GET), render the 'login' template.
        else:
            return render(request, 'login.html')

    except Exception as e:
        # Handle any exceptions that may occur and print them for debugging purposes.
        print(e)




def logout_view(request):
    # Log the user out by calling the 'logout' function from Django's authentication system.
    logout(request)
    
    # Display a success message to the user indicating a successful logout.
    messages.info(request, "Logged out successfully!")

    # Redirect the user to the 'login' view after logging out.
    return redirect('login')



def delete_category(request, category_id):
    # Use get_object_or_404 to retrieve the category or return a 404 response if it doesn't exist.
    category = get_object_or_404(Category, id=category_id)
    
    # Retrieve the category name for displaying in the success message.
    category_name = category.title
    
    # Delete the category from the database.
    category.delete()
    
    # Display a success message to indicate that the category was deleted successfully.
    messages.success(request, f"Category '{category_name}' deleted successfully!")
    
    # Redirect the user to the 'category_details' view after the category is deleted.
    return redirect('category_details')
    

def delete_product(request, product_id):
    # Use get_object_or_404 to retrieve the category or return a 404 response if it doesn't exist.
    product = get_object_or_404(Product, id=product_id)
    
    # Retrieve the category name for displaying in the success message.
    product_name = Product.title
    
    # Delete the category from the database.
    product.delete()
    
    # Display a success message to indicate that the category was deleted successfully.
    messages.success(request, f"Product '{product_name}' deleted successfully!")
    
    # Redirect the user to the 'category_details' view after the category is deleted.
    return redirect('product_data')



def save_customer(request):
    # Get the current date.
    current_date = date.today()
    
    # Initialize a data variable (not used in this code snippet).
    data = "hello"

    # Check if the HTTP request method is POST (typically used for form submissions).
    if request.method == 'POST':
        # Retrieve form data submitted in the POST request.
        form_data = request.POST
        
        # Retrieve the profile picture file from the POST data.
        profile_picture = request.FILES.get('profile_picture')

        # Generate a hashed password based on the user's contact information.
        password = make_password(form_data['contact'])

        # Create a NewUser object with the provided user data and profile picture.
        user_profile = NewUser(
            first_name=form_data['name'],
            username=form_data['email'],
            last_name=form_data['pincode'],
            email=form_data['email'],
            user_type='customer',
            city=form_data['city'],
            state=form_data['state'],
            country=form_data['state'],  # This may be an issue, check if it should be 'country'
            date_joined=current_date,
            password=password,
            is_staff=0,
            profile_photo=profile_picture,
            date_of_birth=form_data['date_of_birth'],
            address=form_data['address'],
            contact=form_data['contact']
        )

        # Save the user profile to the database.
        user_profile.save()
        messages.success(request, 'Registration successful! Your contact number is your password. Happy Shopping!!!')


        # Redirect the user to the 'login' view after successfully saving the profile.
        return redirect('login')

    else:
        # If the request method is not POST, render the 'customer_register.html' template.
        context = {
            'data': data,
        }
        template = loader.get_template('customer_register.html')
        return HttpResponse(template.render(context, request))




def add_category(request):
    # Check if the HTTP request method is POST (typically used for form submissions).
    if request.method == 'POST':
        # Retrieve the 'title' parameter from the POST data.
        title = request.POST.get('title')

        # Create a new category with the provided title and save it to the database.
        category_create = Category.objects.create(title=title)

        # Redirect the user to the 'category_details' view after creating the category.
        return redirect('category_details')

    # If the request method is not POST, render the 'add_category.html' template.
    return render(request, 'add_category.html')

# views.py
from django.shortcuts import render
from .models import NewUser

def registered_users_count_view(request):
    registered_users_count = NewUser.objects.count()
    return render(request, 'registered_users_count.html', {'registered_users_count': registered_users_count})



def category_details(request):
    # Retrieve information about all categories from the Category model and store their values.
    category_info = Category.objects.all().values()
    
    # Print the category information (for debugging or logging purposes).
    print("Category Info:", category_info)

    # Get the template for rendering the 'category_details' view.
    template = loader.get_template('category_details.html')

    # Create a context dictionary to pass the category information to the template.
    context = {
        'category_info': category_info,
    }

    # Render the 'category_details.html' template with the provided context data.
    return HttpResponse(template.render(context, request))



# def delete_product(request, product_id):
#     # Use get_object_or_404 to retrieve the product by its ID, or return a 404 response if it doesn't exist.
#     product = get_object_or_404(Product, id=product_id)
    
#     # Check if the HTTP request method is POST (typically used for form submissions).
#     if request.method == 'POST':
#         # If it's a POST request, delete the product from the database.
#         product.delete()
        
#         # Display a success message to indicate that the product was deleted successfully.
#         messages.success(request, f"Product '{product.title}' deleted successfully!")
        
#         # Redirect to a page showing a list of products or another appropriate page (e.g., 'product_list').
#         return redirect('product_list')

#     # If the request method is not POST, render the 'product_data.html' template and pass the product data to it.
#     return render(request, 'product_data.html', {'product': product})




def add_product(request):
    # Retrieve a list of all categories, including their IDs and titles.
    data = Category.objects.all().values('id', 'title')
    
    # Print the category data (for debugging or logging purposes).
    print("Data:", data)

    # Check if the HTTP request method is POST (typically used for form submissions).
    if request.method == 'POST':
        # Retrieve form data submitted in the POST request.
        form_data = request.POST
        
        # Retrieve the product picture file from the POST data.
        product_picture = request.FILES.get('product_picture')

        # Create a new Product object with the provided product data and product picture.
        add_product = Product(
            title=form_data['title'],
            description=form_data['description'],
            price=form_data['price'],
            category_id_id=form_data['category'],  # Assign the selected category's ID
            sku=form_data['sku'],
            weight=form_data['weight'],
            dimensions=form_data['dimensions'],
            product_image=product_picture
        )

        # Save the new product to the database.
        add_product.save()

        # Redirect the user to the 'product_data' view after successfully adding the product.
        return redirect('product_data')

    # If the request method is not POST, render the 'add_product.html' template.
    else:
        context = {
            'data': data,
        }
        template = loader.get_template('add_product.html')
        return HttpResponse(template.render(context, request))




@login_required
# def product_data(request):
#     # Check if the authenticated user is of user_type 'admin'; otherwise, return a '403 Forbidden' response.
#     if request.user.user_type != 'admin':
#         return HttpResponseForbidden()
    
#     # Retrieve information about all products, including their associated categories.
#     product_info = Product.objects.select_related('category_id').all()
    
#     # Print the product information (for debugging or logging purposes).
#     print("Product Info:", product_info)

#     # Get the template for rendering the 'product_data' view.
#     template = loader.get_template('product_data.html')

#     # Create a context dictionary to pass the product information to the template.
#     context = {
#         'product_info': product_info,
#     }

#     # Render the 'product_data.html' template with the provided context data.
#     return HttpResponse(template.render(context, request))


def product_data(request):
    # Check if the authenticated user is of user_type 'admin'; otherwise, return a '403 Forbidden' response.
    if request.user.user_type != 'admin':
        return HttpResponseForbidden()
    
    # Retrieve information about all products, including their associated categories.
    product_info =ProductForm.objects.all()
    
    # Print the product information (for debugging or logging purposes).
    print("Product Info:", product_info)

    # Create a context dictionary to pass the product information to the template.
    context = {
        'products': product_info,  # Change 'product_info' to 'products' to match template variable name
    }

    # Render the 'product_data.html' template with the provided context data.
    return render(request, 'product_data.html', context)




from django.shortcuts import redirect, get_object_or_404
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    # Retrieve the product by its primary key, or return a 404 response if it doesn't exist.
    product = get_object_or_404(ProductForm, pk=product_id)
    
    # Get the authenticated user.
    user = request.user
    
    # Print the user's ID (for debugging or logging purposes).
    print("User ID:", user.id)
        
    # Get or create a shopping cart associated with the user.
    cart, created = Cart.objects.get_or_create(user=user)
        
    # Get or create a cart item for the selected product.
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product, user=user)
        
    # If the cart item was not created (i.e., already exists), increment its quantity.
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        
    # Redirect the user to the 'index' view after adding the product to the cart.
    return redirect('index')



def view_cart(request, product_id):
    # Retrieve the product by its primary key, or return a 404 response if it doesn't exist.
    product = get_object_or_404(ProductForm, pk=product_id)
    
    # Get the authenticated user, if available.
    user = request.user
    
    # Check if the user is authenticated (logged in).
    if request.user.is_authenticated:
        # Print the user's ID (for debugging or logging purposes).
        print("User ID:", user.id)
        
        # Get or create a shopping cart associated with the user.
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Get or create a cart item for the selected product.
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product, user=user)
        
        # If the cart item was not created (i.e., already exists), increment its quantity.
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
        
        # Redirect the user to the 'checkout' view after adding the product to the cart.
        return redirect('checkout')
    else:
        # Handle the case when the user is not authenticated (anonymous user).
        # You can store the product IDs in the session or use cookies.
        return redirect('login')





def remove_from_cart(request, cart_item_id):
    try:
        # Try to retrieve the cart item by its ID and verify that it belongs to the authenticated user.
        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        
        # Delete the cart item from the user's cart.
        cart_item.delete()
        
        # Redirect to the 'checkout' view after successfully removing the item from the cart.
        return redirect('index')
    except CartItem.DoesNotExist:
        # Handle the case when the cart item is not found, raising a 404 error.
        raise Http404("Cart item not found")




def view_cart(request):
    # Get the user's ID (not typically needed for retrieving cart items).
    user = request.user.id
    
    # Retrieve all cart items associated with the authenticated user.
    cart_items = CartItem.objects.filter(user=request.user)
    
    # Create a context dictionary with cart_items to pass to the template.
    context = {'cart_items': cart_items}
    
    # Render the 'checkout' template with the provided context data.
    return render(request, 'checkout', context)




def clear_cart(request):
    # Get the authenticated user.
    user = request.user
    
    try:
        # Try to retrieve the user's active cart.
        user_cart = Cart.objects.get(user=user, status='active')
        
        # Delete all cart items associated with the user's active cart.
        CartItem.objects.filter(cart=user_cart).delete()
        
        # Redirect to the 'index' page or another desired page after clearing the cart.
        return redirect('index')
    
    except Cart.DoesNotExist:
        # Handle the case when the user's active cart is not found.
        # Redirect to the 'index' page or another desired page.
        return redirect('index')





# def checkout(request):
#     # Check if the authenticated user is of user_type 'customer'; otherwise, return a '403 Forbidden' response.
#     if request.user.user_type != 'customer':
#         return HttpResponseForbidden()
    
#     # Get the authenticated user.
#     user = request.user
    
#     # Retrieve cart items associated with the user's cart.
#     cart_items = CartItem.objects.filter(cart__user=user)
    
#     # Initialize an empty list and total price to zero.
#     ls = []
#     total_price = 0

#     # Loop through each cart item to calculate subtotals and the total price.
#     for x in cart_items:
#         sub_total = x.product.price * x.quantity
#         sub_total = int(sub_total)
#         total_price += sub_total
#         ls.append(sub_total)

#     # Check if the HTTP request method is POST (typically used for form submissions).
#     if request.method == 'POST':
#         # Retrieve customer information and selected payment option from the POST data.
#         firstname = request.POST.get('firstname')
#         lastname = request.POST.get('lastname')
#         email = request.POST.get('email')
#         city = request.POST.get('city')
#         phone_no = request.POST.get('phone_no')
#         address = request.POST.get('address')
#         payment_option = request.POST.get('payment_option')
        
#         # Get the user's cart.
#         cart = Cart.objects.get(user=user)
        
#         # Create a Checkout object to represent the order.
#         order = Checkout.objects.create(
#             user=user,
#             firstname=firstname,
#             lastname=lastname,
#             email=email,
#             cart=cart,
#             address=address,
#             city=city,
#             phone_no=phone_no,
#             payment_option=payment_option,
#             total_price=total_price
#         )
        
#         # Render the 'checkout.html' template and display a success message.
#         template = loader.get_template('checkout.html')
#         messages.success(request, "Your order has been placed successfully!")
        
#         # If the payment option is 'online_payment', redirect to a specific page (e.g., 'blog').
#         if payment_option == 'online_payment':
#             return redirect('blog')
        
#         # Clear the user's cart items after placing the order.
#         cart_items.delete()
        
#         # Return the 'checkout.html' template with the context.
#         return render(request, 'checkout.html', context)
    
#     # Create a context dictionary with relevant data to pass to the 'checkout.html' template.
#     context = {
#         'ls': ls,
#         'cart_items': cart_items,
#         'total_price': total_price,
#         'id': user.id
#     }
    
#     return render(request, 'checkout.html', context)


def checkout(request):
    # Check if the authenticated user is of user_type 'customer'; otherwise, return a '403 Forbidden' response.
    if request.user.user_type != 'customer':
        return HttpResponseForbidden()
    
    # Get the authenticated user.
    user = request.user
    
    # Retrieve cart items associated with the user's cart.
    cart_items = CartItem.objects.filter(cart__user=user)
    
    # Initialize an empty list and total price to zero.
    ls = []
    total_price = 0

    # Loop through each cart item to calculate subtotals and the total price.
    for x in cart_items:
        sub_total =float( x.product.price) * x.quantity
        sub_total = int(sub_total)
        total_price += sub_total
        ls.append(sub_total)

    # Check if the HTTP request method is POST (typically used for form submissions).
    if request.method == 'POST':
        try:
            # Retrieve customer information and selected payment option from the POST data.
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            city = request.POST.get('city')
            phone_no = request.POST.get('phone_no')
            address = request.POST.get('address')
            payment_option = request.POST.get('payment_option')
            
            # Get the user's cart.
            cart = Cart.objects.get(user=user)
            
            # Create a Checkout object to represent the order.
            order = Checkout.objects.create(
                user=user,
                firstname=firstname,
                lastname=lastname,
                email=email,
                cart=cart,
                address=address,
                city=city,
                phone_no=phone_no,
                payment_option=payment_option,
                total_price=total_price
            )
            
            # Display a success message.
            messages.success(request, "Your order has been placed successfully!")
            
            # If the payment option is 'online_payment', redirect to a specific page (e.g., 'blog').
            if payment_option == 'online_payment':
                return redirect('blog')
            
            # Clear the user's cart items after placing the order.
            cart_items.delete()
            
            # Return the 'checkout.html' template with the context.
            context = {
                'ls': ls,
                'cart_items': cart_items,
                'total_price': total_price,
                'id': user.id
            }
            return render(request, 'checkout.html', context)
        
        except Exception as e:
            # Handle exceptions
            context = {
                'ls': ls,
                'cart_items': cart_items,
                'total_price': total_price,
                'id': user.id,
                'error_message': str(e)
            }
            return render(request, 'checkout.html', context)
    
    # Create a context dictionary with relevant data to pass to the 'checkout.html' template.
    context = {
        'ls': ls,
        'cart_items': cart_items,
        'total_price': total_price,
        'id': user.id
    }
    
    return render(request, 'checkout.html', context)



def update_quantity(request, item_id, action):
    try:
        # Try to retrieve the cart item by its ID.
        item = CartItem.objects.get(id=item_id)
    except CartItem.DoesNotExist:
        # If the item is not found, return a JSON response with an error message and a 404 status code.
        return JsonResponse({'error': 'Item not found'}, status=404)

    # Check the action requested, and update the quantity accordingly.
    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease':
        item.quantity -= 1

    # Save the updated item with the new quantity.
    item.save()

    # Return a JSON response with the new quantity after the update.
    return JsonResponse({'new_quantity': item.quantity})




def blog(request):
    # Get the authenticated user's ID and print it (for debugging or logging purposes).
    i = request.user.id
    print("User ID:", i)

    # Retrieve the latest checkout data associated with the user's ID.
    data = Checkout.objects.filter(user_id=i).latest('user_id')
    print("Latest Checkout Data:", data)

    # Extract the user's first name from the checkout data.
    first_name = data.firstname

    # Retrieve cart items associated with the user's cart.
    cart_items = CartItem.objects.filter(cart__user=i)

    # Initialize the total price to zero and calculate it based on cart items.
    total_price = 0
    for x in cart_items:
        total_price += float(x.product.price) * x.quantity
        print("Total price:", total_price)

    # Retrieve the first name and registration number from the latest checkout data.
    reg_no = data.firstname

    # Get the total price and create a template for rendering.
    print("Total Price", total_price)
    template = loader.get_template('blog.html')

    # Create a context dictionary with data to pass to the 'blog.html' template.
    context = {
        'i': i,
        'data': data,
        'reg_no': reg_no,
        'first_name': first_name,
        'total_price': total_price,
        'cart_items': cart_items
    }

    if request.method == 'POST':
        # Retrieve the payment amount from the POST data and convert it to the appropriate format.
        amount = float(request.POST.get("amount")) * 100
        print("Amount:", amount)

        # Create a Razorpay client and generate a payment order.
        client = razorpay.Client(auth=("rzp_test_ri97joaWOlajJM", "ZnlnYhOmDeiM3nn5nuTMyPOL"))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        print("Payment:", payment)

        # Create a record of the online payment.
        Fees = onlinepayment(user_id_id=i, amount=amount / 100, payment_id=payment['id'])
        Fees.save()

        # Delete cart items after the payment is processed.
        cart_items.delete()

        # Render the 'blog.html' template with the payment information.
        return render(request, 'blog.html', {'payment': payment})

    # Return the rendered template with the context data.
    return HttpResponse(template.render(context, request))




def handle_payment_callback(payment_id, amount, user_id):
    # Print the payment ID, amount, and user ID (for debugging or logging purposes).
    print("Payment ID:", payment_id)
    print("Amount:", amount)
    print("User ID:", user_id)
    
    try:
        # Try to retrieve an onlinepayment record with the provided payment details.
        user = onlinepayment.objects.get(payment_id=payment_id, amount=amount, user_id=user_id)
        
        # Check if the payment has not been marked as paid.
        if not user.paid:
            # Mark the payment as paid and save the record.
            user.paid = True
            user.save()
        
        # Return a success message indicating that the payment was successfully processed.
        return "Payment successfully processed."
    
    except onlinepayment.DoesNotExist:
        # Handle the case when the payment details are invalid or not found.
        return "Payment not processed. Invalid payment details."




@csrf_exempt
def success(request):
    if request.method == 'POST':
        # Retrieve POST data from the request.
        a = request.POST

        # Initialize payment_id as an empty string.
        payment_id = ''

        # Loop through the POST data to find the 'razorpay_order_id'.
        for key, val in a.items():
            if key == 'razorpay_order_id':
                payment_id = val
                break

        # Retrieve the onlinepayment record based on the 'razorpay_order_id'.
        user = onlinepayment.objects.get(payment_id=payment_id)

        # Mark the payment as paid and save the record.
        user.paid = True
        user.save()

        # Extract amount, student ID, and payment ID from the onlinepayment record.
        amt = user.amount
        stu_id = user.user_id_id
        payment_id = user.payment_id

        # Print the extracted amount, student ID, and payment ID (for debugging or logging purposes).
        print("Amount - Student ID - Payment ID:", amt, stu_id, payment_id)

        # Call the handle_payment_callback function to process the payment.
        handle_payment_callback(payment_id, amt, stu_id)

    # Render the 'success.html' template.
    return render(request, 'success.html')

def cart(request):
    return render(request, "cart.html")

def dash(request):
    return render(request,"dash.html")



def dash(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        uname = request.POST.get('uname')  # Corrected here
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        district = request.POST.get('district')
        img = request.FILES.get('img')  # Assuming 'img' is the name of the file input field

        # Create a new Product object and save it to the database
        product = ProductForm(uname=uname, name=name, price=price, quantity=quantity, district=district,img=img)
        product.save()

    # Fetch all products from the database
    products = ProductForm.objects.all()
    template = loader.get_template('dash.html')
    context = {
        'products': products,
    }
    return HttpResponse(template.render(context, request))


def save_farmer(request):
    return render(request,"save_farmer.html")


def save_farmer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        uname = request.POST.get('uname')
        gender = request.POST.get('gender')
        district = request.POST.get('district')
        phone = request.POST.get('phone')
        if Farmer.objects.filter(uname=uname).exists():
            return HttpResponse("<h1 style='color:white; background-color: red; text-align:center;'>User Already Exists... Please Login.</h1>")
        else:
            new_farmer=Farmer(name=name,uname=uname,gender=gender,district=district,phone=phone)
            new_farmer.save()
            return redirect("farmer_login")
    else:
        return render(request,"save_farmer.html")
    
def farmer_login(request):
    return render(request,"farmer_login.html")






def farmer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Retrieve the Farmer object based on the provided username
        try:
            farmer = Farmer.objects.get(name=username)
        except Farmer.DoesNotExist:
            farmer = None

        # Check if the farmer exists and the password matches
        if farmer and farmer.phone == password:
            return render(request, 'dash.html')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'farmer_login.html', {'error_message': error_message})

    return render(request, 'farmer_login.html')







