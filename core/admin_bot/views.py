from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from admin_bot.models import Telegram_user, UserState
from admin_bot.serializers import UserSerializer, UserStateSerializer


class UserAPI(APIView):

    def get(self, request):
        tel_user = Telegram_user.objects.all()
        serializer = UserSerializer(tel_user, many=True).data
        return Response(serializer)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPI(APIView):

    queryset = Telegram_user.objects.all()
    serializer_class = UserSerializer

    def get(self, request, user_id):
        user = get_object_or_404(Telegram_user, id=user_id)
        serializer = UserSerializer(user).data
        return Response(serializer)


    def put(self, request, user_id):
        user = get_object_or_404(Telegram_user, id=user_id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserStateAPI(APIView):
    queryset = UserState.objects.all()
    serializer_class = UserStateSerializer

    def get(self, request):
        user_state = UserState.objects.all()
        serializer = UserStateSerializer(user_state, many=True).data
        return Response(serializer)

    def post(self, request):
        serializer = UserStateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserStateDetailAPI(APIView):
    queryset = UserState.objects.all()
    serializer_class = UserStateSerializer

    def get(self, request, user_id):
        user = get_object_or_404(Telegram_user, user_id=user_id)
        user_state = get_object_or_404(UserState, user=user.id)
        serializer = UserStateSerializer(user_state).data
        return Response(serializer)


    def put(self, request, user_id):
        user = get_object_or_404(Telegram_user, user_id=user_id)
        user_state = get_object_or_404(UserState, user=user.id)
        serializer = UserStateSerializer(user_state, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)