# Generated by Django 4.0.4 on 2022-04-14 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_lessonview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonview',
            name='lesson',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='courses.lesson'),
        ),
    ]
