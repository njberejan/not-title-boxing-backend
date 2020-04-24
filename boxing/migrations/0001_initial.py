# Generated by Django 3.0.5 on 2020-04-24 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseExercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('audio_file', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='WorkOut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('length', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WarmUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.IntegerField()),
                ('workout', models.ManyToManyField(related_name='warm_up', to='boxing.WorkOut')),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.IntegerField()),
                ('workout', models.ManyToManyField(related_name='rounds', to='boxing.WorkOut')),
            ],
        ),
        migrations.CreateModel(
            name='CorePeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.IntegerField()),
                ('workout', models.ManyToManyField(related_name='core_period', to='boxing.WorkOut')),
            ],
        ),
        migrations.CreateModel(
            name='Combo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.ManyToManyField(related_name='combo', to='boxing.Round')),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('baseexercise_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='boxing.BaseExercise')),
                ('combo', models.ManyToManyField(related_name='moves', to='boxing.Combo')),
            ],
            bases=('boxing.baseexercise',),
        ),
        migrations.CreateModel(
            name='CoreExercise',
            fields=[
                ('baseexercise_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='boxing.BaseExercise')),
                ('core_period', models.ManyToManyField(related_name='core_exercises', to='boxing.CorePeriod')),
            ],
            bases=('boxing.baseexercise',),
        ),
        migrations.CreateModel(
            name='CardioExercise',
            fields=[
                ('baseexercise_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='boxing.BaseExercise')),
                ('warm_up', models.ManyToManyField(null=True, related_name='cardio_exercises', to='boxing.WarmUp')),
            ],
            bases=('boxing.baseexercise',),
        ),
        migrations.CreateModel(
            name='BurnOut',
            fields=[
                ('baseexercise_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='boxing.BaseExercise')),
                ('round', models.ManyToManyField(related_name='burnout', to='boxing.Round')),
            ],
            bases=('boxing.baseexercise',),
        ),
    ]
