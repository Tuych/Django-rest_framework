# Generated by Django 5.0.4 on 2024-04-25 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('desc', models.TextField()),
                ('rating', models.IntegerField()),
                ('uzb_gross', models.IntegerField()),
                ('world_gross', models.IntegerField()),
                ('phone_number', models.CharField(max_length=13)),
            ],
        ),
    ]
