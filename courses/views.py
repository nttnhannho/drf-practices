from django.http import Http404
from rest_framework import (
    viewsets,
    generics,
    status,
    permissions,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import views

from courses.models import (
    Category,
    Course,
    Lesson,
    Tag,
    User,
)
from courses.paginator import BasePagination
from courses.serializers import (
    CategorySerializer,
    CourseSerializer,
    LessonSerializer,
    LessonDetailSerializer,
    UserSerializer,
)
from django.conf import settings


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = CourseSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        courses = Course.objects.filter(active=True)

        q = self.request.query_params.get('q')
        if q is not None:
            courses = courses.filter(subject__contains=q)

        category_id = self.request.query_params.get('category_id')
        if category_id is not None:
            courses = courses.filter(category_id=category_id)

        return courses

    @action(methods=['GET'], detail=True, url_path='lessons')
    def get_lessons(self, request, pk):
        course = Course.objects.get(pk=pk)
        lessons = course.lessons.filter(active=True)

        q = request.query_params.get('q')
        if q is not None:
            lessons = lessons.filter(subject__contains=q)

        return Response(LessonSerializer(lessons, many=True).data, status=status.HTTP_200_OK)


class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.filter(active=True)
    serializer_class = LessonDetailSerializer

    @action(methods=['POST'], detail=True, url_path='tags')
    def add_tag(self, request, pk):
        try:
            lesson = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            tags = request.data.get('tags')
            if tags is not None:
                for tag in tags:
                    t, _ = Tag.objects.get_or_create(name=tag)
                    lesson.tags.add(t)
                lesson.save()

                return Response(self.serializer_class(lesson).data, status=status.HTTP_201_CREATED)

            return Response(status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'get_current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['GET'], detail=False, url_path='current-user')
    def get_current_user(self, request):
        return Response(self.serializer_class(request.user).data, status=status.HTTP_200_OK)


class AuthInfo(views.APIView):
    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)
