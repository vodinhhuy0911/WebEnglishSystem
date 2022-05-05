from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static
context = views.context_data()

urlpatterns = [
    path('', views.home, name="home-page"),
    path('login',auth_views.LoginView.as_view(template_name="login.html",redirect_authenticated_user = True,extra_context = context),name='login-page'),
    path('logout',views.logoutuser,name='logout'),
    path('userlogin', views.login_user, name="login-user"),
    path('profile', views.profile, name="profile-page"),
    path('update_profile', views.update_profile, name="update-profile"),
    path('update_password', views.update_password, name="update-password"),
    path('new_post', views.manage_post, name="new-post"),
    path('edit_post/<int:pk>', views.manage_post, name="edit-post"),
    path('save_post', views.save_post, name="save-post"),
    path('post/<int:pk>', views.view_post, name="view-post"),
    path('save_comment', views.save_comment, name="save-comment"),
    path('posts', views.list_posts, name="all-posts"),
    path('category/<int:pk>', views.category_posts, name="category-post"),
    path('delete_post/<int:pk>', views.delete_post, name="delete-post"),
    path('delete_comment/<int:pk>', views.delete_comment, name="delete-comment"),


    #QUIZ
    path('quiz',views.quiz,name="quiz"),
    path('user-home', views.user_home, name='user_home'),
    path('play/', views.play, name='play'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('submission-result/<int:pk>/', views.submission_result, name='submission_result'),
    path('register/', views.register, name='register'),
    path('test/',views.test,name="test"),
    path('test-reading-comprehension',views.test_reading_comprehension,name='test-reading-comprehension'),
    path('test-incomplete-text',views.test_incomplete_text,name='test-incomplete-text'),
    path('result/',views.test,name="result"),
    #QUIZ

    path('/automation/incomplete-sentences',views.post_incomplete_sentences,name="incomplete-sentences"),
    # path('/automation/incomplete-text',views.auto_incomplete_text,name="incomplete-text"),

    path('/automation/reading-comprehension',views.auto_incomplete_sentences,name="reading-comprehension"),
    path('/automation/result-reading-comprehension',views.result_reading_comprehension,name="result-reading-comprehension"),
    path('/automation/result_incomplete_sentences',views.result_incomplete_senteces,name="result_incomplete_sentences"),
    # path('/automation/result-incomplete-text',views.result_incomplete_text,name="result-incomplete-text")


]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)