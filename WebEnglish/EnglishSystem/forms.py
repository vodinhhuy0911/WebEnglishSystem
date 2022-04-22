from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _
from .models import Question, Choice

class UpdateProfile(UserChangeForm):
    username = forms.CharField(max_length=250, help_text="The Username field is required.")
    email = forms.EmailField(max_length=250, help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250, help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250, help_text="The Last Name field is required.")
    current_password = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')

    def clean_current_password(self):
        if not self.instance.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError(f"Password is Incorrect")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")


class UpdatePasswords(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm rounded-0'}), label="Old Password")
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm rounded-0'}), label="New Password")
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm rounded-0'}),
        label="Confirm New Password")

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class savePost(forms.ModelForm):
    user = forms.CharField(max_length=30, label="Author")
    category = forms.CharField(max_length=30, label="Category")
    title = forms.CharField(max_length=250, label="Title")
    short_description = forms.Textarea()
    content = forms.Textarea()
    meta_keywords = forms.Textarea()
    banner_path = forms.ImageField(label="Banner Image")
    status = forms.CharField(max_length=2)

    class Meta():
        model = models.Post
        fields = (
        'user', 'category', 'title', 'short_description', 'content', 'meta_keywords', 'banner_path', 'status',)

    def clean_category(self):
        catID = self.cleaned_data['category']
        try:
            category = models.Category.objects.get(id=catID)
            return category
        except:
            raise forms.ValidationError('Selected Category is invalid')

    def clean_user(self):
        userID = self.cleaned_data['user']
        try:
            user = models.User.objects.get(id=userID)
            return user
        except:
            raise forms.ValidationError('Selected User is invalid')


class saveComment(forms.ModelForm):
    post = forms.CharField(max_length=30, label="Post")
    name = forms.CharField(max_length=250, label="Name")
    email = forms.CharField(max_length=250, label="Email")
    subject = forms.CharField(max_length=250, label="Subject")
    message = forms.Textarea()

    class Meta():
        model = models.Comment
        fields = ('post', 'name', 'email', 'subject', 'message',)

    def clean_post(self):
        postID = self.cleaned_data['post']
        try:
            post = models.Post.objects.get(id=postID)
            return post
        except:
            raise forms.ValidationError('Post ID is invalid')


#QUIZ



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['html', 'is_published']
        widgets = {
            'html': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
        }


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['html', 'is_correct']
        widgets = {
            'html': forms.Textarea(attrs={'rows': 2, 'cols': 80}),
        }


class ChoiceInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        super(ChoiceInlineFormset, self).clean()

        correct_choices_count = 0
        for form in self.forms:
            if not form.is_valid():
                return

            if form.cleaned_data and form.cleaned_data.get('is_correct') is True:
                correct_choices_count += 1

        try:
            assert correct_choices_count == Question.ALLOWED_NUMBER_OF_CORRECT_CHOICES
        except AssertionError:
            raise forms.ValidationError(_('Exactly one correct choice is allowed.'))


User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exists")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("This user is not active")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
