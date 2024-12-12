from django.urls import path
from .views import LoginUser, RegisterUser, GetQuestion, SubmitAnswer, GetSessionDetails

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register_user'),
    path('login/', LoginUser.as_view(), name='login_user'),
    path('question/', GetQuestion.as_view(), name='get_question'),
    path('submit/', SubmitAnswer.as_view(), name='submit_answer'),
    path('session/', GetSessionDetails.as_view(), name='get_session_details'),
]