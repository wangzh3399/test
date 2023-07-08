#!/usr/bin/python#!coding=utf-8

from __future__ import absolute_import

import os

from celery import Celery

from django.conf import settings

app = Celery('wxcloudrun')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wxcloudrun.settings')

app.config_from_object('django.conf:settings')

app.conf.beat_schedule = {
    'schedule_task': {  # 随便取名字
        'task': 'celerytest.task.schedule_task',  # 指定需要定时的任务
        #'schedule': crontab(minute=0, hour=0),  # 每天0：00 执行
    },
}


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

'''

autodiscover_tasks instructs celery to auto-discover all asynchronous tasks for all the applications listed under `INSTALLED_APPS`,

Celery will look for definitions of asynchronous tasks within a file named `tasks.py` file in each of the application directory.

'''

@app.task(bind=True)

def debug_task(self):

    print('Request: {0!r}'.format(self.request))
    

