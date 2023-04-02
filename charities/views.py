from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from accounts.permissions import IsCharityOwner, IsBenefactor
from charities.models import Task, Benefactor, Charity
from charities.serializers import (
    TaskSerializer, CharitySerializer, BenefactorSerializer
)


class BenefactorRegistration(APIView):
    def post(self, request):
        # experience = request.data.get('experience')
        # free_time_per_week = request.data.get('free_time_per_week')
        # Benefactor.objects.create(user=user, experience=experience, free_time_per_week=free_time_per_week)
        serializer = BenefactorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CharityRegistration(APIView):
    def post(self, request):
        # name = request.data.get('name')
        # reg_number = request.data.get('reg_number')
        # Charity.objects.create(user=user, name=name, reg_number=reg_number)
        serializer = CharitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class Tasks(generics.ListCreateAPIView):
    class Tasks(generics.ListCreateAPIView):
        serializer_class = TaskSerializer

        def get_queryset(self):
            return Task.objects.all_related_tasks_to_user(self.request.user)

        def post(self, request, *args, **kwargs):
            data = {
                **request.data,
                "charity_id": request.user.charity.id
            }
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        def get_permissions(self):
            if self.request.method in SAFE_METHODS:
                self.permission_classes = [IsAuthenticated, ]
            else:
                self.permission_classes = [IsCharityOwner, ]

            return [permission() for permission in self.permission_classes]

        def filter_queryset(self, queryset):
            filter_lookups = {}
            for name, value in Task.filtering_lookups:
                param = self.request.GET.get(value)
                if param:
                    filter_lookups[name] = param
            exclude_lookups = {}
            for name, value in Task.excluding_lookups:
                param = self.request.GET.get(value)
                if param:
                    exclude_lookups[name] = param

            return queryset.filter(**filter_lookups).exclude(**exclude_lookups)


class TaskRequest(APIView):
    permission_classes = (IsAuthenticated, IsBenefactor)

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        if task.state != 'P':
            data = {'detail': 'This task is not pending.'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        task.state = 'W'
        benefactor = Benefactor.objects.get(user=request.user)
        task.assigned_benefactor = benefactor
        task.save()
        data = {'detail': 'Request sent.'}
        return Response(data, status=status.HTTP_200_OK)


class TaskResponse(APIView):
    permission_classes = (IsAuthenticated, IsCharityOwner)

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        response = request.data.get('response')
        if task.state != 'W':
            data = {'detail': 'This task is not waiting.'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        if response == 'A':
            task.state = 'A'
            task.save()
            data = {'detail': 'Response sent.'}
            return Response(data, status=status.HTTP_200_OK)
        elif response == 'R':
            task.state = 'P'
            task.assigned_benefactor = None
            task.save()
            data = {'detail': 'Response sent.'}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'detail': 'Required field ("A" for accepted / "R" for rejected)'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class DoneTask(APIView):
    permission_classes = (IsAuthenticated, IsCharityOwner)

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, charity=request.user.charity)

        if task.state != 'A':
            data = {'detail': 'Task is not assigned yet.'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        task.state = 'D'
        task.save()
        data = {'detail': 'Task has been done successfully.'}
        return Response(data, status=status.HTTP_200_OK)