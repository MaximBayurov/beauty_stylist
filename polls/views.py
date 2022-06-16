from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice, Poll


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'polls_list'

    def get_queryset(self):
        return Poll.objects.filter(
            active=True
        ).order_by('-id')


class QuestionView(generic.DetailView):
    model = Question
    template_name = 'polls/question.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def render_to_response(self, context, **response_kwargs):
        context['poll_id'] = self.kwargs['poll_id']

        return super().render_to_response(context, **response_kwargs)


class PollView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'
    context_object_name = 'poll'

    def get_queryset(self):
        return Poll.objects.filter(active=True)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get(self, request, *args, **kwargs):

        return super().get(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        context['poll_id'] = self.kwargs['poll_id']

        return super().render_to_response(context, **response_kwargs)


def vote(request, poll_id, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/question.html', {
            'question': question,
            'poll_id': poll_id,
            'error_message': "Не выбран вариант ответа!",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(poll_id, question.id)))
