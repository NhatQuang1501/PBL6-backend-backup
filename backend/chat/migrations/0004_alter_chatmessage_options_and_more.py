# Generated by Django 5.1.2 on 2024-10-23 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_chatmessage_receiver_alter_chatmessage_sender_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatmessage',
            options={'ordering': ['created_at'], 'verbose_name_plural': 'Message'},
        ),
        migrations.RenameField(
            model_name='chatmessage',
            old_name='timestamp',
            new_name='created_at',
        ),
    ]
