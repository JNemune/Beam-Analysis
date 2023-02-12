# Generated by Django 4.1.6 on 2023-02-04 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('len', models.FloatField()),
                ('unit_1', models.CharField(max_length=10)),
                ('f', models.FloatField()),
                ('ft', models.FloatField()),
                ('w', models.FloatField()),
                ('wt', models.FloatField()),
                ('unit_2', models.CharField(max_length=10)),
            ],
        ),
    ]
