# Generated by Django 5.0.7 on 2024-07-25 08:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0002_alter_leave_id_alter_leave_leavetype'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='defaultdays',
            field=models.IntegerField(default=30, verbose_name='Leave days per year counter'),
        ),
        migrations.AlterField(
            model_name='leave',
            name='enddate',
            field=models.DateField(blank=True, help_text='Coming back on ..', null=True, verbose_name='End Date'),
        ),
        migrations.AlterField(
            model_name='leave',
            name='leavetype',
            field=models.CharField(choices=[('sick', 'Sick Leave'), ('casual', 'Casual Leave'), ('emergency', 'Emergency Leave'), ('study', 'Study Leave'), ('maternity', 'Maternity Leave'), ('bereavement', 'Bereavement Leave'), ('quarantine', 'Self Quarantine'), ('compensatory', 'Compensatory Leave'), ('sabbatical', 'Sabbatical Leave')], default='sick', max_length=20),
        ),
        migrations.AlterField(
            model_name='leave',
            name='reason',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='Reason for Leave'),
        ),
        migrations.AlterField(
            model_name='leave',
            name='startdate',
            field=models.DateField(blank=True, help_text='Leave start date is on ..', null=True, verbose_name='Start Date'),
        ),
        migrations.AlterField(
            model_name='leave',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='leave',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
