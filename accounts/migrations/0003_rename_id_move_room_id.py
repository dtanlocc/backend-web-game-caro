# Generated by Django 4.2 on 2023-04-16 02:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_useraccount_id_room_move'),
    ]

    operations = [
        migrations.RenameField(
            model_name='move',
            old_name='id',
            new_name='room_id',
        ),
    ]
