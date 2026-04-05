# coding:utf-8
# author:ila
import jwt
import datetime
import copy
from django.http import JsonResponse
from django.apps import apps
from django.conf import settings

from util.codes import *
from util import message as mes


class Auth(object):
    def authenticate(self, model, req_dict):
        """
        用户登录，登录成功返回token；登录失败返回失败原因
        :param username:账号
        :param password:密码
        :return: json
        """
        msg = {'code': normal_code, 'msg': mes.normal_code, 'data': {}}
        tablename = model.__tablename__
        encode_dict = {"tablename": tablename, "params": req_dict}

        # 生成JWT token
        payload = {
            'tablename': tablename,
            'params': req_dict,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # 24小时过期
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        msg['data']["id"] = req_dict.get("id")
        msg["id"] = req_dict.get("id")
        msg['token'] = token
        return JsonResponse(msg)

    def identify(self, request):
        """
        用户鉴权
        :param request:本次请求对象
        :return: list
        """

        msg = {'code': normal_code, 'msg': mes.normal_code, 'data': {}}
        # django的header被处理过了
        token = request.META.get('HTTP_TOKEN')

        if token  and token !="null":

            auth_token = copy.deepcopy(token)

            try:
                # 解码JWT token
                decode_dict = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception) as e:
                msg['code'] = 401
                msg['msg'] = 'token验证失败，请重新登录'
                return msg

            tablename2 = decode_dict.get("tablename")

            params2 = decode_dict.get("params",{})

            datas=None
            allModels = apps.get_app_config('main').get_models()
            for model in allModels:
                if model.__tablename__ == tablename2:
                    datas = model.getbyparams(model, model, params2)

            if not datas:
                msg['code'] = username_error_code
                msg['msg'] = '找不到该用户信息'
                result = msg
            else:
                request.session['tablename'] = tablename2
                request.session['params'] = params2
                msg['msg'] = '身份验证通过。'
                result = msg
        else:
            msg['code'] = 401
            msg['msg'] = 'headers未包含认证信息。'
            result = msg
        return result
