# Generated by Django 4.2.7 on 2025-05-23 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('notes', '0001_initial'),
        ('teachers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsubmission',
            name='assignment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teachers.assignment'),
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.studentprofile'),
        ),
    ]
