import random

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
import json
from . import models, forms
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from .models import QuizProfile, Question, AttemptedQuestion
from .forms import UserLoginForm, RegistrationForm


from .models import QuizProfile, AttemptedQuestion, Choice
from .forms import RegistrationForm
from .source import main


def context_data():
    context = {
        'site_name': 'Learning English',
        'page': 'home',
        'page_title': 'News Portal',
        'categories': models.Category.objects.filter(status=1).all(),
    }
    return context


# Create your views here.
def home(request):
    context = context_data()
    posts = models.Post.objects.filter(status=1).order_by('-date_created').all()
    context['page'] = 'home'
    context['page_title'] = 'Home'
    context['latest_top'] = posts[:2]
    context['latest_bottom'] = posts[2:12]
    print(posts)
    return render(request, 'home.html', context)


# login
def login_user(request):
    logout(request)
    resp = {"status": 'failed', 'msg': ''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status'] = 'success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp), content_type='application/json')


# Logout
def logoutuser(request):
    logout(request)
    return redirect('/')


@login_required
def update_profile(request):
    context = context_data()
    context['page_title'] = 'Update Profile'
    user = User.objects.get(id=request.user.id)
    if not request.method == 'POST':
        form = forms.UpdateProfile(instance=user)
        context['form'] = form
        print(form)
    else:
        form = forms.UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile-page")
        else:
            context['form'] = form

    return render(request, 'update_profile.html', context)


@login_required
def update_password(request):
    context = context_data()
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = forms.UpdatePasswords(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile-page")
        else:
            context['form'] = form
    else:
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form
    return render(request, 'update_password.html', context)


@login_required
def profile(request):
    context = context_data()
    context['page'] = 'profile'
    context['page_title'] = "Profile"
    return render(request, 'profile.html', context)


@login_required
def manage_post(request, pk=None):
    context = context_data()
    if not pk is None:
        context['page'] = 'edit_post'
        context['page_title'] = 'Edit Post'
        context['post'] = models.Post.objects.get(id=pk)
    else:
        context['page'] = 'new_post'
        context['page_title'] = 'New Post'
        context['post'] = {}

    return render(request, 'manage_post.html', context)


@login_required
def save_post(request):
    resp = {'status': 'failed', 'msg': '', 'id': None}
    if request.method == 'POST':
        if request.POST['id'] == '':
            form = forms.savePost(request.POST, request.FILES)
        else:
            post = models.Post.objects.get(id=request.POST['id'])
            form = forms.savePost(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            if request.POST['id'] == '':
                postID = models.Post.objects.all().last().id
            else:
                postID = request.POST['id']
            resp['id'] = postID
            resp['status'] = 'success'
            messages.success(request, "Post has been saved successfully.")
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br />')
                    resp['msg'] += str(f"[{field.label}] {error}")

    else:
        resp['msg'] = "Request has no data sent."
    return HttpResponse(json.dumps(resp), content_type="application/json")


def view_post(request, pk=None):
    context = context_data()
    post = models.Post.objects.get(id=pk)
    context['page'] = 'post'
    context['page_title'] = post.title
    context['post'] = post
    context['latest'] = models.Post.objects.exclude(id=pk).filter(status=1).order_by('-date_created').all()[:10]
    context['comments'] = models.Comment.objects.filter(post=post).all()
    context['actions'] = False
    if request.user.is_superuser or request.user.id == post.user.id:
        context['actions'] = True
    return render(request, 'single_post.html', context)


def save_comment(request):
    resp = {'status': 'failed', 'msg': '', 'id': None}
    if request.method == 'POST':
        if request.POST['id'] == '':
            form = forms.saveComment(request.POST)
        else:
            comment = models.Comment.objects.get(id=request.POST['id'])
            form = forms.saveComment(request.POST, instance=comment)

        if form.is_valid():
            form.save()
            if request.POST['id'] == '':
                commentID = models.Post.objects.all().last().id
            else:
                commentID = request.POST['id']
            resp['id'] = commentID
            resp['status'] = 'success'
            messages.success(request, "Comment has been saved successfully.")
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br />')
                    resp['msg'] += str(f"[{field.label}] {error}")

    else:
        resp['msg'] = "Request has no data sent."
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def list_posts(request):
    context = context_data()
    context['page'] = 'all_post'
    context['page_title'] = 'All Posts'
    if request.user.is_superuser:
        context['posts'] = models.Post.objects.order_by('-date_created').all()
    else:
        context['posts'] = models.Post.objects.filter(user=request.user).all()

    context['latest'] = models.Post.objects.filter(status=1).order_by('-date_created').all()[:10]

    return render(request, 'posts.html', context)


def category_posts(request, pk=None):
    context = context_data()
    if pk is None:
        messages.error(request, "File not Found")
        return redirect('home-page')
    try:
        category = models.Category.objects.get(id=pk)
    except:
        messages.error(request, "File not Found")
        return redirect('home-page')

    context['category'] = category
    context['page'] = 'category_post'
    context['page_title'] = f'{category.name} Posts'
    context['posts'] = models.Post.objects.filter(status=1, category=category).all()

    context['latest'] = models.Post.objects.filter(status=1).order_by('-date_created').all()[:10]

    return render(request, 'category.html', context)


@login_required
def delete_post(request, pk=None):
    resp = {'status': 'failed', 'msg': ''}
    if pk is None:
        resp['msg'] = 'Post ID is Invalid'
        return HttpResponse(json.dumps(resp), content_type="application/json")
    try:
        post = models.Post.objects.get(id=pk)
        post.delete()
        messages.success(request, "Post has been deleted successfully.")
        resp['status'] = 'success'
    except:
        resp['msg'] = 'Post ID is Invalid'

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_comment(request, pk=None):
    resp = {'status': 'failed', 'msg': ''}
    if pk is None:
        resp['msg'] = 'Comment ID is Invalid'
        return HttpResponse(json.dumps(resp), content_type="application/json")
    try:
        comment = models.Comment.objects.get(id=pk)
        comment.delete()
        messages.success(request, "Comment has been deleted successfully.")
        resp['status'] = 'success'
    except:
        resp['msg'] = 'Comment ID is Invalid'

    return HttpResponse(json.dumps(resp), content_type="application/json")

#QUIZ
def quiz(request):
    context = {}
    return render(request, 'quiz/quiz.html', context=context)


@login_required()
def user_home(request):
    context = {}
    return render(request, 'quiz/user_home.html', context=context)


def leaderboard(request):

    top_quiz_profiles = QuizProfile.objects.order_by('-total_score')[:500]
    total_count = top_quiz_profiles.count()
    context = {
        'top_quiz_profiles': top_quiz_profiles,
        'total_count': total_count,
    }
    return render(request, 'quiz/leaderboard.html', context=context)


@login_required()
def play(request):
    quiz_profile, created = QuizProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        question_pk = request.POST.get('question_pk')
        # print(question_pk)
        attempted_question = quiz_profile.attempts.select_related('question').get(question__pk=question_pk)

        choice_pk = request.POST.get('choice_pk')

        try:
            selected_choice = attempted_question.question.choices.get(pk=choice_pk)
        except ObjectDoesNotExist:
            raise Http404

        quiz_profile.evaluate_attempt(attempted_question, selected_choice)

        return redirect(attempted_question)

    else:
        question = quiz_profile.get_new_question()
        if question is not None:
            quiz_profile.create_attempt(question)

        context = {
            'question': question,
        }

        return render(request, 'quiz/play.html', context=context)


@login_required()
def submission_result(request, pk=None):
    attempted_question = get_object_or_404(AttemptedQuestion, pk=pk)
    context = {
        'attempted_question': attempted_question,
    }

    return render(request, 'quiz/submission_result.html', context=context)


#
# def login_view(request):
#     title = "Login"
#     form = UserLoginForm(request.POST or None)
#     if form.is_valid():
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         user = authenticate(username=username, password=password)
#         login(request, user)
#         return redirect('/user-home')
#     return render(request, 'quiz/login.html', {"form": form, "title": title})



def register(request):
    title = "Create account"
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = RegistrationForm()

    context = {'form': form, 'title': title}
    return render(request, 'quiz/registration.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('/')


def error_404(request):
    data = {}
    return render(request, 'quiz/error_404.html', data)


def error_500(request):
    data = {}
    return render(request, 'quiz/error_500.html', data)



#AUTOMATION
def post_incomplete_sentences(request):

    data ={}
    return render(request,'automation/incomplete-sentences.html',data)

    context = {}
    context['page_title'] = 'Incomplete Senteces'
    return render(request,'automation/incomplete-sentences.html',context)

def result_incomplete_senteces(request):
    context = {}
    context['page_title'] = 'Incomplete Senteces'
    if request.method == 'POST':
        question = request.POST.get('question')
        answerA = request.POST.get('answer_a')
        answerB = request.POST.get('answer_b')
        answerC = request.POST.get('answer_c')
        answerD = request.POST.get('answer_d')
        print(answerA,answerB,answerC,answerD)
        inputQuestion = str(question) + "___" + str(answerA) + "___" + str(answerB) + "___" + str(answerC) + "___" + str(answerD)
        arr = inputQuestion.split('___')
        arr[4] = arr[4].replace(' \n', '')
        arr[4] = arr[4].replace('\n', '')
        context['result'] = main.bigram_MaskedLanguageModel(inputQuestion)

    return render(request, 'automation/result.html', context)


@login_required()
def test(request):
    if request.method == 'POST':
        question_pk = request.POST.getlist('question_pk')
        result = 0.0
        for pk in question_pk:
            choice_pk = request.POST.get('choice_pk-'+str(pk))
            is_answer = Choice.objects.get(pk=choice_pk)
            if is_answer.is_correct == True:
                mask = Question.objects.get(pk=pk)
                result += float(mask.maximum_marks)
        context = {
            'question_pk':question_pk,
            'result':result
        }
        return render(request,'quiz/result.html',context)
    else:
        list_question = list(Question.objects.all())
        random.shuffle(list_question)
        result = []
        for question in list_question[:1]:
            c = list(Choice.objects.filter(question = question))
            input = question.html+ "___" + c[0].html+ "___" + c[1].html+ "___"+ c[2].html+ "___"+ c[3].html
            # result.append("a")
            result.append(main.bigram_MaskedLanguageModel(input))
            # list_percent =
        context = {
            'list_question': zip(list_question[:1],result)
            # 'input':listInput
        }
        # print(context["input"][0])
        return render(request, 'quiz/test.html', context=context)

