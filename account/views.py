from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import LoginForm, UserRegistrationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Post


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'blog/post/list.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    object_list = Post.objects.all()
                    paginator = Paginator(object_list, 10)  # 10 posts in each page
                    page = request.GET.get('page')
                    try:
                        posts = paginator.page(page)
                    except PageNotAnInteger:
                        posts = paginator.page(1)
                    except EmptyPage:
                        posts = paginator.page(paginator.num_pages)

                    # return HttpResponse('Authenticated successfully')
                    # return render(request, 'blog/post/list.html',
                    #               {'page': page,
                    #                'posts': posts})
                    return redirect("/")
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})