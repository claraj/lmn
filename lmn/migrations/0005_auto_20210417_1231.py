# Generated by Django 3.1.2 on 2021-04-17 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmn', '0004_auto_20210417_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='image',
            field=models.ImageField(upload_to='user_images/'),
        ),
    ]