# Generated by Django 3.1.2 on 2021-04-17 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmn', '0002_note_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='image',
            field=models.ImageField(default=1, upload_to='user_images/'),
            preserve_default=False,
        ),
    ]
