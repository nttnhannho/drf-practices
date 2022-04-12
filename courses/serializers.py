from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from courses.models import (
    Category,
    Course,
    Lesson,
)


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    image = SerializerMethodField()

    def get_image(self, course):
        request = self.context['request']
        name = course.image.name
        if name.startswith('static/'):
            path = f'/{name}'
        else:
            path = f'/static/{name}'

        return request.build_absolute_uri(path)

    class Meta:
        model = Course
        fields = ('id', 'subject', 'image', 'created_at', 'category')


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'subject', 'image', 'created_at', 'updated_at', 'course')
