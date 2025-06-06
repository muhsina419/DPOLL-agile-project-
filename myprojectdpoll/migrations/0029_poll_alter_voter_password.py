# Generated by Django 5.1.6 on 2025-05-29 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myprojectdpoll', '0028_userprofile_has_voted_alter_voter_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='voter',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$870000$jfTzAuE8JP6zRGXNUfoGC3$G5iXR5FZbqxBAjDpuSTgwPSYYATJEptjiIJArAOps10=', max_length=128),
        ),
    ]
