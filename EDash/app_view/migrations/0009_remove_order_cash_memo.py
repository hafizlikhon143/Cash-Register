# Generated by Django 4.0.3 on 2022-05-16 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_view', '0008_order_cash_memo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cash_memo',
        ),
    ]