#coding:utf-8
__author__ = "ila"
import copy
import os
import base64
import logging
from django.http import JsonResponse
from django.apps import apps
from django.db.models.aggregates import Count,Sum
from .models import xuesheng
from util.codes import *
from util.auth import Auth
import util.message as mes
from util.face_util import FaceUtil

logger = logging.getLogger(__name__)

def xuesheng_register(request):
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {'code': normal_code, "msg": mes.normal_code}
        req_dict = request.session.get("req_dict")
        
        # 处理人脸照片上传
        face_photo_file = request.FILES.get('facePhoto')
        if not face_photo_file:
            logger.warning("注册失败: 未上传人脸照片")
            msg['code'] = crud_error_code
            msg['msg'] = "请上传人脸照片"
            return JsonResponse(msg)
        
        logger.info(f"收到人脸照片上传: {face_photo_file.name}, 大小: {face_photo_file.size} bytes")
        
        # 检查文件类型
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png']
        if face_photo_file.content_type not in allowed_types:
            logger.warning(f"注册失败: 不支持的文件类型 {face_photo_file.content_type}")
            msg['code'] = crud_error_code
            msg['msg'] = "只支持JPG和PNG格式的图片"
            return JsonResponse(msg)
        
        # 检查文件大小 (最大10MB)
        if face_photo_file.size > 10 * 1024 * 1024:
            logger.warning(f"注册失败: 文件过大 {face_photo_file.size} bytes")
            msg['code'] = crud_error_code
            msg['msg'] = "图片文件不能超过10MB"
            return JsonResponse(msg)
        
        # 保存上传的文件
        import time
        import hashlib
        file_ext = os.path.splitext(face_photo_file.name)[1]
        timestamp = str(int(time.time() * 1000))
        file_hash = hashlib.md5((timestamp + face_photo_file.name).encode()).hexdigest()
        filename = f"{file_hash}{file_ext}"
        
        # 确保media/face目录存在
        face_dir = os.path.join(os.getcwd(), "media", "face")
        os.makedirs(face_dir, exist_ok=True)
        
        file_path = os.path.join(face_dir, filename)
        
        # 保存文件
        try:
            with open(file_path, 'wb+') as destination:
                for chunk in face_photo_file.chunks():
                    destination.write(chunk)
            logger.info(f"人脸照片已保存: {file_path}")
        except Exception as e:
            logger.error(f"保存人脸照片失败: {str(e)}")
            msg['code'] = crud_error_code
            msg['msg'] = "保存人脸照片失败"
            return JsonResponse(msg)
        
        # 将文件路径添加到req_dict (保存到zhaopian字段)
        req_dict['zhaopian'] = f"upload/{filename}"

        # 默认设置性别为男性
        if 'xingbie' not in req_dict or not req_dict.get('xingbie'):
            req_dict['xingbie'] = '男'

        # 创建用户记录
        error = xuesheng.createbyreq(xuesheng, xuesheng, req_dict)
        if error != None:
            # 删除已上传的文件
            try:
                os.remove(file_path)
                logger.info(f"已删除文件: {file_path}")
            except:
                pass
            logger.warning(f"创建用户失败: {error}")
            msg['code'] = crud_error_code
            msg['msg'] = "用户已存在,请勿重复注册!"
            return JsonResponse(msg)
        
        user_id = str(req_dict.get('id'))
        logger.info(f"用户创建成功，ID: {user_id}")
        
        # 人脸注册
        try:
            # 读取文件并转换为Base64
            with open(file_path, 'rb') as f:
                image_data = f.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
            
            logger.info(f"Base64编码完成，长度: {len(base64_image)}")
            
            # 调用百度API注册人脸
            result = FaceUtil.register_face(base64_image, user_id)
            logger.info(f"学生人脸注册成功，用户ID: {user_id}, 结果: {result}")
            
        except Exception as e:
            # 人脸注册失败，回滚用户创建
            error_msg = str(e)
            logger.error(f"学生人脸注册失败: {error_msg}")
            
            try:
                # 删除刚创建的用户记录
                if user_id:
                    xuesheng.deletes(xuesheng, xuesheng, [user_id])
                    logger.info(f"已回滚删除用户: {user_id}")
                # 删除已上传的文件
                os.remove(file_path)
                logger.info(f"已删除文件: {file_path}")
            except Exception as rollback_error:
                logger.error(f"回滚失败: {str(rollback_error)}")
            
            msg['code'] = crud_error_code
            msg['msg'] = f"人脸注册失败: {error_msg}"
            return JsonResponse(msg)
        
        return JsonResponse(msg)

def xuesheng_login(request):
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {'code': normal_code, "msg": mes.normal_code}
        req_dict = request.session.get("req_dict")

        datas = xuesheng.getbyparams(xuesheng, xuesheng, req_dict)
        if not datas:
            msg['code'] = password_error_code
            msg['msg'] = mes.password_error_code
            return JsonResponse(msg)

        req_dict['id'] = datas[0].get('id')
        return Auth.authenticate(Auth, xuesheng, req_dict)


def xuesheng_logout(request):
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {
            "msg": "登出成功",
            "code": 0
        }

        return JsonResponse(msg)


def xuesheng_resetPass(request):
    '''
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code}

        req_dict = request.session.get("req_dict")

        error = xuesheng.updatebyparams(xuesheng,xuesheng, req_dict)

        if error != None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)



def xuesheng_session(request):
    ''''
    获取session中的用户信息
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code,"msg": mes.normal_code, "data": {}}

        req_dict={"id":request.session.get('params').get("id")}
        data = xuesheng.getbyparams(xuesheng, xuesheng, req_dict)

        if len(data) > 0:
            msg['data'] = data[0]

            # 检查照片文件是否存在，如果不存在则尝试从 media/face 目录查找
            photo_filename = msg['data'].get('zhaopian')
            if photo_filename:
                # 检查 templates/front 目录下是否存在
                front_path = os.path.join(os.getcwd(), "templates", "front", photo_filename)
                if not os.path.exists(front_path):
                    # 尝试从 media/face 目录查找
                    media_face_path = os.path.join(os.getcwd(), "media", "face", photo_filename)
                    if os.path.exists(media_face_path):
                        logger.info(f"照片文件在 media/face 目录找到: {photo_filename}")
                        # 复制文件到 templates/front 目录
                        import shutil
                        try:
                            shutil.copy2(media_face_path, front_path)
                            logger.info(f"已复制照片到 templates/front: {photo_filename}")
                        except Exception as e:
                            logger.warning(f"复制照片失败: {str(e)}")
                    else:
                        logger.warning(f"照片文件不存在: {photo_filename}")

        return JsonResponse(msg)



def xuesheng_page(request):
    '''
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")

        #获取全部列名
        columns=  xuesheng.getallcolumn( xuesheng, xuesheng)

        #当前登录用户所在表
        tablename = request.session.get("tablename")
        #当列属性authTable有值(某个用户表)[该列的列名必须和该用户表的登陆字段名一致]，则对应的表有个隐藏属性authTable为”是”，那么该用户查看该表信息时，只能查看自己的
        try:
            __authTables__=xuesheng.__authTables__
        except:
            __authTables__=None

        if __authTables__!=None and  __authTables__!={}:

            for authColumn,authTable in __authTables__.items():
                if authTable==tablename:
                    params = request.session.get("params")
                    req_dict[authColumn]=params.get(authColumn)
                    break

            #authColumn=list(__authTables__.keys())[0]
            #authTable=__authTables__.get(authColumn)

            # if authTable==tablename:
                #params = request.session.get("params")
                #req_dict[authColumn]=params.get(authColumn)

        '''__authSeparate__此属性为真，params添加userid，后台只查询个人数据'''
        try:
            __authSeparate__=xuesheng.__authSeparate__
        except:
            __authSeparate__=None

        if __authSeparate__=="是":
            tablename=request.session.get("tablename")
            if tablename!="users" and 'userid' in columns:
                try:
                    req_dict['userid']=request.session.get("params").get("id")
                except:
                    pass

        #当项目属性hasMessage为”是”，生成系统自动生成留言板的表messages，同时该表的表属性hasMessage也被设置为”是”,字段包括userid（用户id），username(用户名)，content（留言内容），reply（回复）
        #接口page需要区分权限，普通用户查看自己的留言和回复记录，管理员查看所有的留言和回复记录
        try:
            __hasMessage__=xuesheng.__hasMessage__
        except:
            __hasMessage__=None
        if  __hasMessage__=="是":
            tablename=request.session.get("tablename")
            if tablename!="users":
                req_dict["userid"]=request.session.get("params").get("id")



        # 判断当前表的表属性isAdmin,为真则是管理员表
        # 当表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的作业记录(同时应用于其他表)
        __isAdmin__ = None

        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__==tablename:

                try:
                    __isAdmin__ = m.__isAdmin__
                except:
                    __isAdmin__ = None
                break

        # 当前表也是有管理员权限的表
        if  __isAdmin__ == "是" and req_dict.get("userid"):
            del req_dict["userid"]
        else:
            #非管理员权限的表,判断当前表字段名是否有userid
            if tablename!="users" and "userid" in xuesheng.getallcolumn(xuesheng,xuesheng):
                req_dict["userid"] = request.session.get("params").get("id")


        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  =xuesheng.page(xuesheng, xuesheng, req_dict)

        return JsonResponse(msg)

def xuesheng_autoSort(request):
    '''
    ．智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
主要信息列表（如商品列表，新闻列表）中使用，显示最近点击的或最新添加的5条记录就行
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")
        if "clicknum"  in xuesheng.getallcolumn(xuesheng,xuesheng):
            req_dict['sort']='clicknum'
        else:
            req_dict['sort']='clicktime'
        req_dict['order']='desc'
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = xuesheng.page(xuesheng,xuesheng, req_dict)

        return JsonResponse(msg)


def xuesheng_list(request):
    '''
    前台分页
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")

        #获取全部列名
        columns=  xuesheng.getallcolumn( xuesheng, xuesheng)
        #表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
        try:
            __foreEndList__=xuesheng.__foreEndList__
        except:
            __foreEndList__=None

        if __foreEndList__=="是":
            tablename=request.session.get("tablename")
            if tablename!="users" and 'userid' in columns:
                try:
                    req_dict['userid']=request.session.get("params").get("id")
                except:
                    pass
        #forrEndListAuth
        try:
            __foreEndListAuth__=xuesheng.__foreEndListAuth__
        except:
            __foreEndListAuth__=None


        #authSeparate
        try:
            __authSeparate__=xuesheng.__authSeparate__
        except:
            __authSeparate__=None

        if __foreEndListAuth__ =="是" and __authSeparate__=="是":
            tablename=request.session.get("tablename")
            if tablename!="users":
                req_dict['userid']=request.session.get("params",{"id":0}).get("id")

        tablename = request.session.get("tablename")
        if tablename == "users" and req_dict.get("userid") != None:#判断是否存在userid列名
            del req_dict["userid"]
        else:
            __isAdmin__ = None

            allModels = apps.get_app_config('main').get_models()
            for m in allModels:
                if m.__tablename__==tablename:

                    try:
                        __isAdmin__ = m.__isAdmin__
                    except:
                        __isAdmin__ = None
                    break

            if __isAdmin__ == "是" and req_dict.get("userid"):
                del req_dict["userid"]
            else:
                #非管理员权限的表,判断当前表字段名是否有userid
                if "userid" in columns:
                    try:
                        # 本接口可以匿名访问,所以try判断是否为匿名
                        req_dict['userid']=request.session.get("params").get("id")
                    except:
                            pass

        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = xuesheng.page(xuesheng, xuesheng, req_dict)

        return JsonResponse(msg)

def xuesheng_save(request):
    '''
    后台新增
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        tablename=request.session.get("tablename")
        #获取全部列名
        columns=  xuesheng.getallcolumn( xuesheng, xuesheng)
        if tablename!='users' and req_dict.get("userid")!=None and 'userid' in columns:
            params=request.session.get("params")
            req_dict['userid']=params.get('id')


        error= xuesheng.createbyreq(xuesheng,xuesheng, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def xuesheng_add(request):
    '''
    前台新增
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")

        #获取全部列名
        columns=  xuesheng.getallcolumn( xuesheng, xuesheng)

        try:
            __authSeparate__=xuesheng.__authSeparate__
        except:
            __authSeparate__=None

        if __authSeparate__=="是":
            tablename=request.session.get("tablename")
            if tablename!="users" and 'userid' in columns:
                try:
                    req_dict['userid']=request.session.get("params").get("id")
                except:
                    pass

        try:
            __foreEndListAuth__=xuesheng.__foreEndListAuth__
        except:
            __foreEndListAuth__=None

        if __foreEndListAuth__ and __foreEndListAuth__!="否":
            tablename=request.session.get("tablename")
            if tablename!="users":
                req_dict['userid']=request.session.get("params").get("id")

        error= xuesheng.createbyreq(xuesheng,xuesheng, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)

def xuesheng_thumbsup(request,id_):
    '''
     点赞：表属性thumbsUp[是/否]，刷表新增thumbsupnum赞和crazilynum踩字段，
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        id_=int(id_)
        type_=int(req_dict.get("type",0))
        rets=xuesheng.getbyid(xuesheng,xuesheng,id_)

        update_dict={
        "id":id_,
        }
        if type_==1:#赞
            update_dict["thumbsupnum"]=int(rets[0].get('thumbsupnum'))+1
        elif type_==2:#踩
            update_dict["crazilynum"]=int(rets[0].get('crazilynum'))+1
        error = xuesheng.updatebyparams(xuesheng,xuesheng, update_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def xuesheng_info(request,id_):
    '''
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        data = xuesheng.getbyid(xuesheng,xuesheng, int(id_))
        if len(data)>0:
            msg['data']=data[0]
        #浏览点击次数
        try:
            __browseClick__= xuesheng.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__=="是"  and  "clicknum"  in xuesheng.getallcolumn(xuesheng,xuesheng):
            try:
                clicknum=int(data[0].get("clicknum",0))+1
            except:
                clicknum=0+1
            click_dict={"id":int(id_),"clicknum":clicknum}
            ret=xuesheng.updatebyparams(xuesheng,xuesheng,click_dict)
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return JsonResponse(msg)

def xuesheng_detail(request,id_):
    '''
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        data =xuesheng.getbyid(xuesheng,xuesheng, int(id_))
        if len(data)>0:
            msg['data']=data[0]

        #浏览点击次数
        try:
            __browseClick__= xuesheng.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__=="是"   and  "clicknum"  in xuesheng.getallcolumn(xuesheng,xuesheng):
            try:
                clicknum=int(data[0].get("clicknum",0))+1
            except:
                clicknum=0+1
            click_dict={"id":int(id_),"clicknum":clicknum}

            ret=xuesheng.updatebyparams(xuesheng,xuesheng,click_dict)
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return JsonResponse(msg)


def xuesheng_update(request):
    '''
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        if req_dict.get("mima") and req_dict.get("password"):
            if "mima" not  in xuesheng.getallcolumn(xuesheng,xuesheng) :
                del req_dict["mima"]
            if  "password" not  in xuesheng.getallcolumn(xuesheng,xuesheng) :
                del req_dict["password"]
        try:
            del req_dict["clicknum"]
        except:
            pass
        error = xuesheng.updatebyparams(xuesheng, xuesheng, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def xuesheng_delete(request):
    '''
    批量删除
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")

        error=xuesheng.deletes(xuesheng,
            xuesheng,
             req_dict.get("ids")
        )
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def xuesheng_vote(request,id_):
    '''
    浏览点击次数（表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1）
统计商品或新闻的点击次数；提供新闻的投票功能
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code}


        data= xuesheng.getbyid(xuesheng, xuesheng, int(id_))
        for i in data:
            votenum=i.get('votenum')
            if votenum!=None:
                params={"id":int(id_),"votenum":votenum+1}
                error=xuesheng.updatebyparams(xuesheng,xuesheng,params)
                if error!=None:
                    msg['code'] = crud_error_code
                    msg['msg'] = error
        return JsonResponse(msg)


