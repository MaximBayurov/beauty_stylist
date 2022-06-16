from django.contrib import admin

# Register your models here.

from .models import Question, Choice, Poll


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Информация о времени', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'active', 'question']}),
    ]
    list_display = ('name', 'active')
    list_filter = ['active']
    search_fields = ['name']


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
