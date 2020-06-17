# Generated by Django 3.0.5 on 2020-06-17 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_remove_bird_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sighting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('habitat', models.CharField(choices=[('G', 'On the ground'), ('T', 'In trees or bushes'), ('P', 'Perched on a fence or wire'), ('N', 'In a nest'), ('F', 'Flying'), ('W', 'Wading or swimming')], default='G', max_length=1)),
                ('bird', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Bird')),
            ],
        ),
    ]
