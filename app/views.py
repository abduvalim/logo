from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import ListView, TemplateView

from app.form import ContactForm, LoginForm, RegisterForm, send_email
from app.models import Product, User
# from token import account_activation_token


def index(request):
    return render(request, 'app/index.html')



def about(request):
    return render(request,'app/about.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            email_subject = f'New contact {form.cleaned_data["email"]}: {form.cleaned_data["subject"]}'
            email_message = form.cleaned_data['message']
            send_mail(email_subject, email_message, settings.CONTACT_EMAIL, settings.ADMIN_EMAIL)
            return render(request, 'app/succes.html')
    form = ContactForm()
    context = {'form': form}
    return render(request, 'app/contact.html', context)


def single_post(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    context = {
        'product': product
    }
    return render(request, 'app/single-post.html', context)

def blog(request):
    products = Product.objects.order_by('-id')
    context = {
        'products':products
    }
    return render(request, 'app/blog.html', context)






def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('index')

    return render(request, 'app/login.html', {'form':form})

#

def logout_view(request):
    logout(request)
    return render(request, 'app/logout.html')


class blogPage(ListView):
    template_name = 'app/blog.html'
    model = Product
    queryset = Product.objects.all()
    context_object_name = 'products'


def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            send_email(form.data.get('email'), request, 'register')
            messages.add_message(
                request,
                level=messages.INFO,
                message='Xabar yuborildi, emailingizni tekshiring'
            )
            return redirect('register')
    return render(request, 'app/register.html', {'form': form})


class ActivateEmailView(TemplateView):
    template_name = 'app/confrim.html'

    def get(self, request, *args, **kwargs):
        uid = kwargs.get('uid')
        token = kwargs.get('token')

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except Exception as e:
            print(e)
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.add_message(
                request=request,
                level=messages.SUCCESS,
                message="Your account successfully activated!"
            )
            return redirect('index')
        else:
            return HttpResponse('Activation link is invalid!')
class BlogSearchView(ListView):
    model = Product
    template_name = 'app/blog.html'
    context_object_name = 'posts'


    def get_queryset(self):
        query =self.request.GET.get('q')
        return Product.objects.filter(text__icontains=query).order_by('text')
