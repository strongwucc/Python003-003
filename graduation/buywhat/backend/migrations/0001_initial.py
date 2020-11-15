# Generated by Django 2.2.16 on 2020-11-15 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mobile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('worth_n', models.IntegerField(default=0)),
                ('not_worth_n', models.IntegerField(default=0)),
                ('comment_n', models.IntegerField(default=0)),
                ('source', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='', max_length=1000)),
                ('sentiment', models.DecimalField(decimal_places=10, max_digits=11)),
                ('comment_t', models.DateTimeField()),
                ('create_t', models.DateTimeField()),
                ('mobile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Mobile')),
            ],
        ),
    ]
