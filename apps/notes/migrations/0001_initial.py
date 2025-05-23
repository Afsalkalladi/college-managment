# Generated by Django 4.2.7 on 2025-05-23 16:34

import apps.notes.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('academics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignmentSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='submissions/')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('marks', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('feedback', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('file', models.FileField(upload_to=apps.notes.models.student_note_upload_path)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('verification_status', models.CharField(default='pending', max_length=20)),
                ('scheme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.scheme')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.studentprofile')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.subject')),
            ],
        ),
        migrations.CreateModel(
            name='NoteVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verification_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=20)),
                ('feedback', models.TextField(blank=True)),
                ('note', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='notes.studentnote')),
                ('verified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.teacherprofile')),
            ],
        ),
    ]
