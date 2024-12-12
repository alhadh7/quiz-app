from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Question, UserAnswer, User
from .serializers import QuestionSerializer, UserSerializer
import random

class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = serializer.get_tokens(user)
            return Response(tokens, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUser(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = get_object_or_404(User, username=username)
        if user.check_password(password):
            serializer = UserSerializer()
            tokens = serializer.get_tokens(user)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class GetQuestion(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_questions = Question.objects.all()
        answered_questions = UserAnswer.objects.filter(
            user=request.user
        ).values_list('question_id', flat=True)
        available_questions = all_questions.exclude(id__in=answered_questions)
        if not available_questions.exists():
            return Response(
                {"message": "You have completed all available questions!"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        question = random.choice(list(available_questions))
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SubmitAnswer(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        question_id = request.data.get('question_id')
        selected_option = request.data.get('selected_option')
        print(selected_option)
        question = get_object_or_404(Question, id=question_id)
        is_correct = question.correct_option == selected_option
        print(is_correct)
        UserAnswer.objects.create(
            user=request.user,
            question=question,
            selected_option=selected_option,
            is_correct=is_correct
            
        )

        response_data = {
            "is_correct": is_correct,
            "correct_option": question.correct_option if not is_correct else None
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    
class GetSessionDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_answers = request.user.answers.all()
        total_questions = user_answers.count()
        correct_answers = user_answers.filter(is_correct=True).count()
        incorrect_answers = total_questions - correct_answers

        return Response({
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "incorrect_answers": incorrect_answers,
        }, status=status.HTTP_200_OK)