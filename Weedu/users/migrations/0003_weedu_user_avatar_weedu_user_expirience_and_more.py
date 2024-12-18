# Generated by Django 5.1.3 on 2024-11-11 18:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0001_initial'),
        ('users', '0002_weedu_user_is_authenticated'),
    ]

    operations = [
        migrations.AddField(
            model_name='weedu_user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='users_avatar/'),
        ),
        migrations.AddField(
            model_name='weedu_user',
            name='expirience',
            field=models.SmallIntegerField(blank=True, default=0, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='weedu_user',
            name='level',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='weedu_user',
            name='praise',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='weedu_user',
            name='purchased_products',
            field=models.ManyToManyField(through='publish.Purchase', to='publish.shop'),
        ),
        migrations.AddField(
            model_name='weedu_user',
            name='registered_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
