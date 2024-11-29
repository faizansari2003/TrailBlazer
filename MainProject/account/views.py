from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm, CustomerRegistrationForm, AddressForm, ForgetPasswordForm, OTPForm, ResetPasswordForm
from django.contrib.auth.models import User
from .models import Customer
import random
from cart.views import add_to_cart

# views.py
def login_view(request):
    next_page = request.GET.get('next', '')  # Capture the 'next' parameter, which is the page the user was trying to access
    print(next_page,'here is next')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print("login done")
                # Redirect to the next page if it's available, else default to 'home'
                if next_page:
                    print(request.META.get('HTTP_REFERER'),'back')
                    # return redirect('http://127.0.0.1:8000/product/all-products/')
                    id =int(str(next_page).split('/')[-2])
                    add_to_cart(request,id)
                    print(id,type(id))
                    return redirect('product',id )
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
        else:
            messages.error(request, 'Invalid form submission')
            return redirect('login')

    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})






# Registration view
# Registration view
def register_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        customer_form = CustomerRegistrationForm(request.POST)

        if user_form.is_valid() and customer_form.is_valid():
            # Create user and related objects...
            user = user_form.save()
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()

            messages.success(request, 'Registration successful! Please log in to continue.')
            return redirect('login')  # Redirect to login page after success
        else:
            print("Form errors:", user_form.errors, customer_form.errors)
            messages.error(request, 'There were errors in the form. Please check and try again.')
    else:
        user_form = UserRegistrationForm()
        customer_form = CustomerRegistrationForm()

    return render(request, 'account/register.html', {
        'user_form': user_form,
        'customer_form': customer_form,
    })




# Logout view
def logout_view(request):
    logout(request)
    return redirect('index')  # Redirect to index.html after logout





# Forgot Password view with OTP functionality
class ForgotPassword(View):
    def get(self, request):
        context = {
            'form': ForgetPasswordForm()
        }
        return render(request, 'account/form.html', context)

    def post(self, request):
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            try:
                user = User.objects.get(username=username, email=email)
                
                # Generate a random OTP
                otp = random.randint(1000, 9999)

                # Send OTP to email
                send_otp_to_email(user, otp)

                # Store OTP and username in the session
                request.session['otp'] = otp
                request.session['username'] = username

                messages.success(request, 'An OTP has been sent to your registered email ID.')
                
                context = {
                    'form': OTPForm(),
                    'form_action': '/account/verify-otp/',
                    'otp': 'verify-otp'
                }
                return render(request, 'account/form.html', context)

            except User.DoesNotExist:
                messages.error(request, 'Enter an email registered with the username.')
                return redirect('forgot_password')

        else:
            messages.error(request, 'Invalid form submission.')
            return redirect('forgot_password')
        



def send_otp_to_email(user, otp):
    """
    Helper function to send OTP to the user's email.
    """
    send_mail(
        subject="OTP for Reset Password",
        message=f'{otp} is your OTP for the password reset request.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False  # Set to True in production to suppress errors
    )
    # Print OTP in the console for debugging (remove in production)
    print(f'\n\n\n\n\n{otp}\n\n\n\n')

def verifyOTP(request):
    if request.method == "POST":
        otp = request.session.get('otp')
        username = request.session.get('username')

        # Check if the user requested to resend the OTP
        if request.POST.get('resend_otp') == 'true':
            new_otp = random.randint(1000, 9999)
            request.session['otp'] = new_otp

            # Get the user to resend the OTP
            user = get_object_or_404(User, username=username)
            send_otp_to_email(user, new_otp)

            messages.success(request, 'A new OTP has been sent to your email.')

            context = {
                'form': OTPForm(),
                'form_action': '/account/verify-otp/',
                'otp': 'verify-otp'
            }
            return render(request, 'account/form.html', context)

        form_data = request.POST.get('otp')  # Get the user-entered OTP

        if form_data is None:
            messages.error(request, 'OTP is missing. Please enter the OTP sent to your email.')
            context = {
                'form': OTPForm(),
                'form_action': '/account/verify-otp/',
                'otp': 'verify-otp'
            }
            return render(request, 'account/form.html', context)

        try:
            form_data = int(form_data)  # Convert user-entered OTP to integer
        except ValueError:
            messages.error(request, 'Invalid OTP format. Please enter a numeric OTP.')
            context = {
                'form': OTPForm(),
                'form_action': '/account/verify-otp/',
                'otp': 'verify-otp'
            }
            return render(request, 'account/form.html', context)

        if otp and int(otp) == form_data:
            context = {
                'form': ResetPasswordForm(),
                'form_name': f'Enter new password for {username}',
                'form_action': '/account/reset-password/',
            }
            return render(request, 'account/form.html', context)
        else:
            messages.error(request, 'Invalid OTP. Please try again or request a new one.')
            context = {
                'form': OTPForm(),
                'form_action': '/account/verify-otp/',
                'otp': 'verify-otp'
            }
            return render(request, 'account/form.html', context)
    else:
        return redirect('home')


# Password Reset view
def resetPassword(request):
    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        username = request.session.get('username')
        if password == confirm_password:
            user = get_object_or_404(User, username=username)
            user.set_password(password)
            user.save()

            send_mail(
                subject="Password Reset Complete",
                message='Your password has been successfully reset. You can now login with your new password',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=True
            )

            return redirect('login')
        else:
            context = {
                'form': ResetPasswordForm(data=request.POST),
                'form_name': f'Password and Confirm Password did not match for {username}',
                'form_action': '/account/reset-password/',
            }
            messages.error(request, 'Both the passwords do not match.')
            return render(request, 'account/form.html', context)
    else:
        return redirect('home')
    













# view for sending email when the user log in
# from django.shortcuts import render, redirect, get_object_or_404
# from django.views import View
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib import messages
# from django.core.mail import send_mail
# from django.conf import settings

# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
                
#                 # Send email to the user upon successful login
#                 subject = "Welcome Back!"
#                 message = f"Hello {username},\n\nYou have successfully logged into your account. We're happy to see you back!"
#                 recipient = user.email
#                 sender = settings.EMAIL_HOST_USER

#                 try:
#                     send_mail(subject, message, sender, [recipient])
#                     messages.success(request, f'Welcome back, {username}! A confirmation email has been sent to your registered email.')
#                 except Exception as e:
#                     messages.error(request, f'Login successful, but failed to send email: {e}')

#                 return redirect('index')  # Redirect to index.html after successful login
#             else:
#                 messages.error(request, 'Invalid username or password')
#         else:
#             messages.error(request, 'Invalid form submission')
#     else:
#         form = AuthenticationForm()

#     return render(request, 'account/login.html', {'form': form})