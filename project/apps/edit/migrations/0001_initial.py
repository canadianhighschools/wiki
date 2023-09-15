# Generated by Django 4.2.5 on 2023-09-15 13:35

import apps.core.data.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edited', models.BooleanField(auto_created=True, default=False, editable=False, verbose_name='Edited')),
                ('section', models.CharField(max_length=255, verbose_name='Edited Section')),
                ('status', models.SmallIntegerField(default=0, verbose_name='Status')),
                ('approver', models.OneToOneField(auto_created=True, blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='approver', to=settings.AUTH_USER_MODEL, verbose_name='Approver')),
                ('content', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='data.textcontent')),
                ('contributor', models.OneToOneField(auto_created=True, editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='contributor', to=settings.AUTH_USER_MODEL, verbose_name='Contributor')),
                ('revision', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='data.revision')),
            ],
            options={
                'verbose_name': 'Commit',
                'verbose_name_plural': 'Commits',
                'db_table': 'Commit',
            },
            bases=(models.Model, apps.core.data.models.AbstractDatedModel),
        ),
    ]