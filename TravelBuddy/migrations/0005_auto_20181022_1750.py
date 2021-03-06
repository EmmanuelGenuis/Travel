# Generated by Django 2.1.2 on 2018-10-22 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TravelBuddy', '0004_auto_20181022_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='Join',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan', to='TravelBuddy.Plan')),
                ('added_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='TravelBuddy.User')),
            ],
        ),
        migrations.RemoveField(
            model_name='destination',
            name='added_by',
        ),
        migrations.RemoveField(
            model_name='destination',
            name='destination',
        ),
        migrations.DeleteModel(
            name='Destination',
        ),
    ]
