from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import Courses, Invoice
from django.contrib.auth.hashers import make_password, check_password
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

stripe.api_key = settings.STRIPE_SECRET_KEY

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def classType(request):
    return render(request, "classType.html")

def contact(request):
    return render(request, "contact.html")

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('courses')
            else:
                messages.error(request, 'Your account is inactive.')
        else:
            messages.error(request, 'Invalid username or password.')
        
    return render(request, 'login.html')

@login_required
def courses(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        if title and description and price:
            Courses.objects.create(Title = title, Description = description, Price = price)
    courses = Courses.objects.all()
    return render(request, "courses.html", {"user":request.user, "courses":courses})

@login_required
@require_POST
def buy_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    token = request.POST.get('stripeToken')
    try:
        charge = stripe.Charge.create(
            amount=int(float(course.Price)/100),
            currency='usd',
            description=course.Title,
            source=token,
        )
        invoice = Invoice.objects.get(Course_id = course_id, profile_id = request.user.id)
        invoice.Paid = True
        invoice.save()
        return render(request, 'payment_success.html')
    except stripe.error.StripeError:
        return render(request, 'payment_error.html')

@login_required
def course_detail(request, course_id):
    course = Courses.objects.get(id=course_id)
    invoice = Invoice.objects.create(Course_id = course.id, profile_id = request.user.id, Paid = False)
    context = {
        'course': course,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'buyCourse.html', context)

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')

def account_activation_sent(request):
    return render(request, "activationSucess.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if username and email and password1 == password2:
            user = User.objects.create(username=username, email=email, password=make_password(password1))
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('email/verify.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http',
            })
            send_mail(subject, '', 'train2grow24@outlook.com', [user.email],  html_message=message)
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'signup.html')

def invoices(request):
    invoices = Invoice.objects.filter(profile_id = request.user.id)
    print(invoices)
    return render(request,'invoices.html', {"invoices":invoices})

def PasswordResetView(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.get(email = email):
            user = User.objects.get(email=email)
            current_site = get_current_site(request)
            subject = 'Reset Your Password'
            message = render_to_string('email/passwordReset.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http',
            })
            send_mail(subject, '', 'train2grow24@outlook.com', [user.email],  html_message=message)
            return redirect('login')
    return render(request, 'passwordResetInitial.html')

def reset(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 == password2:
                user.password = make_password(password1)
                user.save()
                return redirect('login')
        return render(request, 'passwordReset.html')
    else:
        return render(request, 'email/verify.html',{'user':User.objects.get(pk=uid)})


def profile(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user = User.objects.get(id = request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        redirect("profile")
    return render(request, "profile.html")

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('account_activation_sent')
    else:
        return render(request, 'email/verify.html',{'user':User.objects.get(pk=uid)})