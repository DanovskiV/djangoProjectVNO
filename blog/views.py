from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView


class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'blog/post/list.html'

    def get_queryset(self):

        query = self.request.GET.get('q')
        if query == None:
            if self.request.GET.get("sort_by_letters"):
                return Post.objects.all().order_by("title")
            else:
                print("all")
                return Post.objects.all()
        else:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(title__contains=query) |
                Q(title__in=query) |
                Q(body__icontains=query) |
                Q(body__in=query) |
                Q(body__contains=query) |
                Q(comments__body__icontains=query)
            )


def post_list(request):
    # object_list = Post.objects.all()
    object_list = PostListView.queryset

    paginator = Paginator(object_list, 10)  # 10 posts in each page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    # print(posts)
    # if request.GET.get("sort_by_date"):
    #     posts = sort_by_date(request)
    #     print(posts)
    #
    # if request.GET.get("sort_by_letter"):
    #     posts = sort_by_letter(request)
    #     print(posts)

    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # if request.user.is_authenticated:
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.name = request.user.username
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                 {'post': post,
                  'comments': comments,
                  'comment_form': comment_form})


def sort_by_date(request):
    return Post.objects.all().order_by("publish")


def sort_by_letter(request):
    return Post.objects.all().order_by("title")