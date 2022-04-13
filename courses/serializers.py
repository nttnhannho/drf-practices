from rest_framework.fields import SerializerMethodField
from rest_framework import serializers

from courses.models import (
    Category,
    Course,
    Lesson,
    Tag,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'image', 'created_at', 'updated_at', 'course']


class LessonDetailSerializer(LessonSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['content', 'tags']
