# Generated by Django 2.2.3 on 2019-12-07 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=10)),
                ('lastName', models.CharField(max_length=10)),
                ('empId', models.IntegerField()),
            ],
        ),
    ]
