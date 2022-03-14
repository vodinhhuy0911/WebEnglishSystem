from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import viewsets, generics, status, permissions
from rest_framework.views import APIView

from .models import Category,User, Answers, MultipleChoice
from .serializers import CategorySerializers,UserSerializers, MultipleChoiceSerializers, AnswerSeralizers
from django.conf import settings

# Create your views here.

class CategoryViewSet(viewsets.ViewSet,generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

class UserViewsSet(viewsets.ViewSet,generics.CreateAPIView):
    queryset = User.objects.filter(is_active = True)
    serializer_class = UserSerializers
    # parser_classes = [MultiPartParser,]

    def get_permissions(self):
        if self.action =='get_current_user':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False,url_path="current-user")
    def get_current_user(self,request):
        return Response(self.serializer_class(request.user).data,status=status.HTTP_200_OK)


class AuthInfo(APIView):
    def get(self,request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)

class MultipleChoiceViewSet(viewsets.ModelViewSet):
    queryset = MultipleChoice.objects.all()
    serializer_class = MultipleChoiceSerializers

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answers.objects.all()
    serializer_class = AnswerSeralizers