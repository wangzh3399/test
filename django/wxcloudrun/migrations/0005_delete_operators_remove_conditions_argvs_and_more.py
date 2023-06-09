# Generated by Django 4.2 on 2023-07-10 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxcloudrun', '0004_noticeconfig_desc_noticeconfig_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='operators',
        ),
        migrations.RemoveField(
            model_name='conditions',
            name='argvs',
        ),
        migrations.RemoveField(
            model_name='conditions',
            name='operatorid',
        ),
        migrations.AddField(
            model_name='conditions',
            name='argvsdesc',
            field=models.CharField(blank=True, max_length=256, verbose_name='参数描述'),
        ),
        migrations.AddField(
            model_name='conditions',
            name='argvsnum',
            field=models.IntegerField(blank=True, null=True, verbose_name='参数个数'),
        ),
        migrations.AddField(
            model_name='conditions',
            name='funcname',
            field=models.CharField(blank=True, max_length=256, verbose_name='条件函数名'),
        ),
        migrations.AddField(
            model_name='conditions',
            name='retvaldesc',
            field=models.CharField(blank=True, max_length=256, verbose_name='参数描述'),
        ),
        migrations.AddField(
            model_name='conditions',
            name='retvalnum',
            field=models.IntegerField(blank=True, null=True, verbose_name='返回值个数'),
        ),
        migrations.AlterField(
            model_name='conditions',
            name='condtype',
            field=models.CharField(blank=True, max_length=16, verbose_name='类型'),
        ),
        migrations.AlterField(
            model_name='conditions',
            name='creatorid',
            field=models.CharField(blank=True, max_length=32, verbose_name='用户id'),
        ),
        migrations.AlterField(
            model_name='conditions',
            name='desc',
            field=models.CharField(blank=True, max_length=256, verbose_name='条件描述'),
        ),
        migrations.AlterField(
            model_name='conditions',
            name='name',
            field=models.CharField(blank=True, max_length=256, verbose_name='条件名'),
        ),
    ]
