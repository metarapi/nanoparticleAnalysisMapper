# Generated by Django 4.2.6 on 2023-10-27 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_remove_experiment_csv_files_csvfile_experiment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
