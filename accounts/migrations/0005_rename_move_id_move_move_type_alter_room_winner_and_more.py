# Generated by Django 4.2 on 2023-04-16 02:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_room_id_move_room'),
    ]

    operations = [
        migrations.RenameField(
            model_name='move',
            old_name='move_id',
            new_name='move_type',
        ),
        migrations.AlterField(
            model_name='room',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('size', models.IntegerField(default=16)),
                ('cells', models.JSONField(default=dict)),
                ('room', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.room')),
            ],
        ),
    ]