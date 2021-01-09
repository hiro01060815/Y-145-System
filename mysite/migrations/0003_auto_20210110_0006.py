# Generated by Django 3.1 on 2021-01-09 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mysite', '0002_d31info_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='d31info',
            name='form',
            field=models.CharField(default='', max_length=10000, verbose_name='フォーム内容'),
        ),
        migrations.CreateModel(
            name='UserStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userstatus', models.IntegerField(default=0, verbose_name='モデルステータス')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1', to=settings.AUTH_USER_MODEL, verbose_name='ユーザ')),
            ],
        ),
    ]