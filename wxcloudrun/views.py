import json
from basicfunc import *

from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.replies import TextReply
from wechatpy import parse_message


logger = getlogger('djangoserver.log')


def index(request, _):
    """
    获取主页

     `` request `` 请求对象
    """

    return render(request, 'index.html')
def default(request):
    method = request.method
    logger.debug('request method:'+method)
    url = request.path
    logger.debug('request url:'+url)
    header = {}
    for i in request.META:
        if i.startswith('HTTP'):
            header[i] = request.META[i]
    logger.debug('request header:\r\n'+str(header))
    body = request.body
    logger.debug('request header:\r\n'+str(body))
    return HttpResponse('nothing')

def wxapi(request, _):
    token = "test"
    if request.method == 'GET':
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        try:
            res = check_signature(token, signature, timestamp, nonce)
            logger.info(res)
        except InvalidSignatureException:
        # 处理异常情况或忽略
            logger.error(InvalidSignatureException)
        #echostr = request.GET.get('echostr')
        return HttpResponse(request.GET.get('echostr'))
    else:
        reqbody = request.body
        msg = parse_message(reqbody)
        logger.info(msg)
        reply = TextReply(content='text reply', message=msg)
        xml = reply.render()
        logger.info(msg)
        return HttpResponse(xml)

def counter(request, _):
    """
    获取当前计数

     `` request `` 请求对象
    """

    rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'GET' or request.method == 'get':
        rsp = get_count()
    elif request.method == 'POST' or request.method == 'post':
        rsp = update_count(request)
    else:
        rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
                            json_dumps_params={'ensure_ascii': False})
    logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
    return rsp


def get_count():
    """
    获取当前计数
    """

    try:
        data = Counters.objects.get(id=1)
    except Counters.DoesNotExist:
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'code': 0, 'data': data.count},
                        json_dumps_params={'ensure_ascii': False})


def update_count(request):
    """
    更新计数，自增或者清零

    `` request `` 请求对象
    """

    logger.info('update_count req: {}'.format(request.body))

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if 'action' not in body:
        return JsonResponse({'code': -1, 'errorMsg': '缺少action参数'},
                            json_dumps_params={'ensure_ascii': False})

    if body['action'] == 'inc':
        try:
            data = Counters.objects.get(id=1)
        except Counters.DoesNotExist:
            data = Counters()
        data.id = 1
        data.count += 1
        data.save()
        return JsonResponse({'code': 0, "data": data.count},
                    json_dumps_params={'ensure_ascii': False})
    elif body['action'] == 'clear':
        try:
            data = Counters.objects.get(id=1)
            data.delete()
        except Counters.DoesNotExist:
            logger.info('record not exist')
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'code': -1, 'errorMsg': 'action参数错误'},
                    json_dumps_params={'ensure_ascii': False})
