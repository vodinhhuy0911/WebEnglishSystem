from django.contrib import admin
from .models import Category,MultipleChoice,ReadingComprehension,Answers
# Register your models here.

admin.site.register(Category)
admin.site.register(MultipleChoice)
admin.site.register(ReadingComprehension)
admin.site.register(Answers)
