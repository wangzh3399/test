# Generated by Django 4.2 on 2023-07-08 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxcloudrun', '0003_noticeconfig_changetime_noticeconfig_createtime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conditons',
            old_name='ownderid',
            new_name='creatorid',
        ),
        migrations.RenameField(
            model_name='monitortask',
            old_name='userid',
            new_name='creatorid',
        ),
        migrations.RenameField(
            model_name='noticeconfig',
            old_name='userid',
            new_name='creatorid',
        ),
        migrations.RenameField(
            model_name='operators',
            old_name='ownderid',
            new_name='creatorid',
        ),
        migrations.RenameField(
            model_name='stockpool',
            old_name='userid',
            new_name='creatorid',
        ),
        migrations.AlterField(
            model_name='monitortask',
            name='lastrun',
            field=models.CharField(blank=True, max_length=20, verbose_name='最后运行时间'),
        ),
        migrations.AlterField(
            model_name='monitortask',
            name='runstatus',
            field=models.CharField(blank=True, max_length=16, verbose_name='运行状态'),
        ),
    ]