# Generated by Django 4.1.4 on 2023-05-10 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uni', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='selected_exam',
            unique_together={('t_a', 'e_x')},
        ),
    ]
