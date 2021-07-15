from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from django.views.generic import ListView
from .models import Question, Answer, QuestionForm, AnswerForm
from django.db.models import Q


class QuestionsListView(ListView):
    queryset = Question.objects.all()
    # queryset = Question.objects.filter(Q(ans))
    context_object_name = 'questions'
    paginate_by = 10
    template_name = 'questions/questions_list.html'

    def get_queryset(self):

        query = self.request.GET.get('q')
        if query == None:
            return Question.objects.all()
        else:
            return Question.objects.filter(
                Q(body__icontains=query) or
                Q(body__contains=query) or
                Q(body__in=query) or
                Q(name__icontains=query) or
                Q(name__contains=query) or
                Q(name__in=query) or
                Q(answers__body__icontains=query)
            )


def questions_list(request):
    # object_list = Question.objects.all()
    object_list = QuestionsListView.queryset

    paginator = Paginator(object_list, 10)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    return render(request,
                  'questions/questions_list.html',
                  {'page': page,
                   'questions': questions})


def question_detail(request, year, month, day, question):
    question = get_object_or_404(Question, slug=question,
                                 status='open',
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day)
    # List of active comments for this post
    answers = question.answers.filter(active=True)
    print(answers)
    if request.method == 'POST':

        answer_form = AnswerForm(data=request.POST)
        if answer_form.is_valid():
            if request.user.is_authenticated:
                new_answer = answer_form.save(commit=False)
                new_answer.name = request.user.username
                new_answer.answer = question
                new_answer.save()
    else:
        answer_form = AnswerForm()
    return render(request,
                  'questions/question_detail.html',
                  {'question': question,
                   'answers': answers,
                   'answer_form': answer_form})


def ask_question(request):
    object_list = Question.objects.all()

    if request.method == 'POST':
        question_form = QuestionForm(data=request.POST)
        if question_form.is_valid():

            if request.user.is_authenticated:
                new_question = question_form.save(commit=False)
                new_question.author = request.user
                # # new_question.slag = new_question.title
                # new_question.slag = slugify(new_question.title)
                # print(new_question.slag, new_question.title)
                new_question.save()
            else:
                question_form = QuestionForm()
                return render(request, 'questions/question_ask.html', {
                    'question_form': question_form,
                })

            return render(request, 'questions/question_ask.html', {
                      'question_form': question_form,
                  })
    else:
        question_form = QuestionForm()

    return render(request,
                  'questions/question_ask.html',
                  {
                      'question_form': question_form,
                  }
                  )
