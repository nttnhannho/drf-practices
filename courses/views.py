from rest_framework import (
    viewsets,
    generics,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from courses.models import (
    Category,
    Course,
)
from courses.paginator import BasePagination
from courses.serializers import (
    CategorySerializer,
    CourseSerializer,
    LessonSerializer,
)


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
