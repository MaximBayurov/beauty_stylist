from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.PollView.as_view(), name='detail'),
    path('<int:poll_id>/<int:pk>/', views.QuestionView.as_view(), name='question_detail'),
    path('<int:poll_id>/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:poll_id>/<int:question_id>/vote/', views.vote, name='vote'),
]
