from django.contrib import admin
from .models import Category, Post, Comment, Choice, Question, QuizProfile, AttemptedQuestion, Paragraph
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


from .forms import QuestionForm, ChoiceForm, ChoiceInlineFormset
# Register your models here.
# Register your models here.

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

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     if obj is not None and obj.pk is not None and obj.is_published is True:
    #         return False
    #     return True


admin.site.register(Question, QuestionAdmin)


#

# admin.site.register(Choice)
# admin.site.register(QuizProfile)
admin.site.register(AttemptedQuestion)

admin.site.register(Choice)
admin.site.register(QuizProfile)
# admin.site.register(AttemptedQuestion)
admin.site.register(Paragraph)
admin.site.register(Category)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment)