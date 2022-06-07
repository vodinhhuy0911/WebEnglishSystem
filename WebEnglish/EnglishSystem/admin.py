from django.contrib import admin
from .models import Category, Post, Comment, Choice, Question, Paragraph
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


from .forms import QuestionForm, ChoiceForm, ChoiceInlineFormset



class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostForm


class ChoiceInline(admin.TabularInline):
    model = Choice
    can_delete = False
    max_num = Choice.MAX_CHOICES_COUNT
    min_num = Choice.MAX_CHOICES_COUNT
    form = ChoiceForm
    formset = ChoiceInlineFormset


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = (ChoiceInline, )
    list_display = ['html', 'is_published']
    list_filter = ['is_published']
    search_fields = ['html', 'choices__html']
    actions = None
    form = QuestionForm




admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Paragraph)
admin.site.register(Category)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment)