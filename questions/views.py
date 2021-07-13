from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Question, Answer, QuestionForm, AnswerForm


class QuestionsListView(ListView):
    queryset = Question.objects.all()
    context_object_name = 'questions'
    paginate_by = 3
    template_name = 'questions/questions_list.html'


def questions_list(request):
    object_list = Question.objects.all()
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    # if request.method == 'POST':
    #     # A comment was posted
    #     question_form = AnswerForm(data=request.POST)
    #     if question_form.is_valid():
    #         # Create Comment object but don't save to database yet
    #         new_question = question_form.save(commit=False)
    #         # Assign the current post to the comment
    #         new_question.answer = object_list
    #         # Save the comment to the database
    #         new_question.save()
    # else:
    #     question_form = QuestionForm(data=request.POST)

    # return render(request,
    #               'questions/questions_list.html',
    #               {'page': page,
    #                'questions': questions,
    #                'questions_form': question_form})
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

    if request.method == 'POST':

        answer_form = AnswerForm(data=request.POST)
        if answer_form.is_valid():
            if request.user.is_authenticated:
                new_answer = answer_form.save(commit=False)
                new_answer.name = request.user.username
                new_answer.question = question
                new_answer.save()
                return render(request,
                              'questions/question_detail.html',
                              {'question': question,
                               'answers': answers,
                               'answer_form': answer_form})
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
