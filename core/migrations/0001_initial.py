# Generated by Django 3.1.7 on 2021-08-07 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('trisolace', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.CharField(max_length=200, null=True)),
                ('amount', models.PositiveIntegerField(default='0')),
                ('email', models.EmailField(default=' ', max_length=254)),
                ('ref', models.CharField(max_length=200)),
                ('verified', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trisolace.customer')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trisolace.product')),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
    ]
