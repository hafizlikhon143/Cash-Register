# Generated by Django 4.0.3 on 2022-05-16 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_view', '0004_alter_cart_phone_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashMemo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('order_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_view.order')),
            ],
        ),
    ]
