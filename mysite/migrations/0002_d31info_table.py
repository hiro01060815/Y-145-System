# Generated by Django 3.1 on 2021-01-01 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='d31info',
            name='table',
            field=models.IntegerField(default=0, verbose_name='テーブル優先順位'),
        ),
    ]