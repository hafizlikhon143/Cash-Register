# Generated by Django 4.0.3 on 2022-05-16 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_view', '0009_remove_order_cash_memo'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashmemo',
            name='name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]