#coding:utf-8
__author__ = "ila"
import copy
from django.http import JsonResponse
from django.apps import apps
from django.db.models.aggregates import Count,Sum
from .models import examrecord
from util.codes import *
from util.auth import Auth
import util.message as mes

def examrecord_register(request):
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {'code': normal_code, "msg": mes.normal_code}
        req_dict = request.session.get("req_dict")

        error = examrecord.createbyreq(examrecord, examrecord, req_dict)
        if error != None:
            msg['code'] = crud_error_code
            msg['msg'] = "用户已存在,请勿重复注册!"
        return JsonResponse(msg)

def examrecord_login(request):
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {'code': normal_code, "msg": mes.normal_code}
        req_dict = request.session.get("req_dict")

        datas = examrecord.getbyparams(examrecord, examrecord, req_dict)
        if not datas:
            msg['code'] = password_error_code
            msg['msg'] = mes.password_error_code
            return JsonResponse(msg)

        req_dict['id'] = datas[0].get('id')
        return Auth.authenticate(Auth, examrecord, req_dict)


def examrecord_logout(request):
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {
            "msg": "登出成功",
            "code": 0
        }

        return JsonResponse(msg)


def examrecord_resetPass(request):
    '''
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code}

        req_dict = request.session.get("req_dict")

        error = examrecord.updatebyparams(examrecord,examrecord, req_dict)

        if error != None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)



def examrecord_session(request):
    '''
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code,"msg": mes.normal_code, "data": {}}

        req_dict={"id":request.session.get('params').get("id")}
        msg['data']  = examrecord.getbyparams(examrecord, examrecord, req_dict)[0]

        return JsonResponse(msg)



def examrecord_page(request):
    '''
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")

        #获取全部列名
        columns=  examrecord.getallcolumn( examrecord, examrecord)

        #当前登录用户所在表
        tablename = request.session.get("tablename")
        #当列属性authTable有值(某个用户表)[该列的列名必须和该用户表的登陆字段名一致]，则对应的表有个隐藏属性authTable为”是”，那么该用户查看该表信息时，只能查看自己的
        try:
            __authTables__=examrecord.__authTables__
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
            __authSeparate__=examrecord.__authSeparate__
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
            __hasMessage__=examrecord.__hasMessage__
        except:
            __hasMessage__=None
        if  __hasMessage__=="是":
            tablename=request.session.get("tablename")
            if tablename!="users":
                req_dict["userid"]=request.session.get("params").get("id")



        # 判断当前表的表属性isAdmin,为真则是管理员表
        # 当表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
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
            if tablename!="users" and "userid" in examrecord.getallcolumn(examrecord,examrecord):
                req_dict["userid"] = request.session.get("params").get("id")


        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  =examrecord.page(examrecord, examrecord, req_dict)

        return JsonResponse(msg)

def examrecord_autoSort(request):
    '''
    ．智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
主要信息列表（如商品列表，新闻列表）中使用，显示最近点击的或最新添加的5条记录就行
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")
        if "clicknum"  in examrecord.getallcolumn(examrecord,examrecord):
            req_dict['sort']='clicknum'
        else:
            req_dict['sort']='clicktime'
        req_dict['order']='desc'
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = examrecord.page(examrecord,examrecord, req_dict)

        return JsonResponse(msg)


def examrecord_list(request):
    '''
    前台分页
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")

        #获取全部列名
        columns=  examrecord.getallcolumn( examrecord, examrecord)
        #表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
        try:
            __foreEndList__=examrecord.__foreEndList__
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
            __foreEndListAuth__=examrecord.__foreEndListAuth__
        except:
            __foreEndListAuth__=None


        #authSeparate
        try:
            __authSeparate__=examrecord.__authSeparate__
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
        msg['data']['pageSize']  = examrecord.page(examrecord, examrecord, req_dict)

        return JsonResponse(msg)

def examrecord_save(request):
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
        columns=  examrecord.getallcolumn( examrecord, examrecord)
        if tablename!='users' and req_dict.get("userid")!=None and 'userid' in columns:
            params=request.session.get("params")
            req_dict['userid']=params.get('id')


        error= examrecord.createbyreq(examrecord,examrecord, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def examrecord_add(request):
    '''
    前台新增
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")

        #获取全部列名
        columns=  examrecord.getallcolumn( examrecord, examrecord)

        try:
            __authSeparate__=examrecord.__authSeparate__
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
            __foreEndListAuth__=examrecord.__foreEndListAuth__
        except:
            __foreEndListAuth__=None

        if __foreEndListAuth__ and __foreEndListAuth__!="否":
            tablename=request.session.get("tablename")
            if tablename!="users":
                req_dict['userid']=request.session.get("params").get("id")

        error= examrecord.createbyreq(examrecord,examrecord, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)

def examrecord_thumbsup(request,id_):
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
        rets=examrecord.getbyid(examrecord,examrecord,id_)

        update_dict={
        "id":id_,
        }
        if type_==1:#赞
            update_dict["thumbsupnum"]=int(rets[0].get('thumbsupnum'))+1
        elif type_==2:#踩
            update_dict["crazilynum"]=int(rets[0].get('crazilynum'))+1
        error = examrecord.updatebyparams(examrecord,examrecord, update_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def examrecord_info(request,id_):
    '''
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        data = examrecord.getbyid(examrecord,examrecord, int(id_))
        if len(data)>0:
            msg['data']=data[0]
        #浏览点击次数
        try:
            __browseClick__= examrecord.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__=="是"  and  "clicknum"  in examrecord.getallcolumn(examrecord,examrecord):
            try:
                clicknum=int(data[0].get("clicknum",0))+1
            except:
                clicknum=0+1
            click_dict={"id":int(id_),"clicknum":clicknum}
            ret=examrecord.updatebyparams(examrecord,examrecord,click_dict)
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return JsonResponse(msg)

def examrecord_detail(request,id_):
    '''
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        data =examrecord.getbyid(examrecord,examrecord, int(id_))
        if len(data)>0:
            msg['data']=data[0]

        #浏览点击次数
        try:
            __browseClick__= examrecord.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__=="是"   and  "clicknum"  in examrecord.getallcolumn(examrecord,examrecord):
            try:
                clicknum=int(data[0].get("clicknum",0))+1
            except:
                clicknum=0+1
            click_dict={"id":int(id_),"clicknum":clicknum}

            ret=examrecord.updatebyparams(examrecord,examrecord,click_dict)
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = retfo
        return JsonResponse(msg)


def examrecord_update(request):
    '''
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        if req_dict.get("mima") and req_dict.get("password"):
            if "mima" not  in examrecord.getallcolumn(examrecord,examrecord) :
                del req_dict["mima"]
            if  "password" not  in examrecord.getallcolumn(examrecord,examrecord) :
                del req_dict["password"]
        try:
            del req_dict["clicknum"]
        except:
            pass
        error = examrecord.updatebyparams(examrecord, examrecord, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def examrecord_delete(request):
    '''
    批量删除
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")

        error=examrecord.deletes(examrecord,
            examrecord,
             req_dict.get("ids")
        )
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def examrecord_vote(request,id_):
    '''
    浏览点击次数（表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1）
统计商品或新闻的点击次数；提供新闻的投票功能
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code}


        data= examrecord.getbyid(examrecord, examrecord, int(id_))
        for i in data:
            votenum=i.get('votenum')
            if votenum!=None:
                params={"id":int(id_),"votenum":votenum+1}
                error=examrecord.updatebyparams(examrecord,examrecord,params)
                if error!=None:
                    msg['code'] = crud_error_code
                    msg['msg'] = error
        return JsonResponse(msg)


def examrecord_groupby(request):
    '''
    管理员用户：当表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")

        #处理参数
        try:
            page1 = int(req_dict.get("page"))
        except:
            page1 = 1
        try:
            limit1 = int(req_dict.get("limit"))
        except:
            limit1 = 10

        #值为"是"仅能查看自己的记录和add接口后台赋值userid的值
        try:
            __authSeparate__ = examrecord.__authSeparate__
        except:
            __authSeparate__ = None

        # print(examrecord.getallcolumn(examrecord,examrecord))
        if __authSeparate__=="是":
            #print("req_dict==============>",req_dict)
            #如果当前表有userid字段,且通过身份认证
            if "userid"  in examrecord.getallcolumn(examrecord,examrecord) and request.session.get("params")!=None:
                #参数增加userid
                req_dict["userid"]=request.session.get("params").get("id")
        #如果当前表没有userid字段,且参数里有userid键值对
        if  "userid" not  in examrecord.getallcolumn(examrecord,examrecord) and "userid" in list(req_dict.keys()):
            #删除参数userid
            del req_dict["userid"]
        try:
            del req_dict["page"]
            del req_dict["limit"]
        except:
            pass
        tablename=request.session.get("tablename")
        if tablename=="users" and req_dict.get("userid")!=None:
            del req_dict["userid"]
        else:
            #判断当前登陆表是否具有管理员权限
            __isAdmin__ = None

            allModels = apps.get_app_config('main').get_models()
            for m in allModels:
                if m.__tablename__==tablename:

                    try:
                        __isAdmin__ = m.__isAdmin__
                    except:
                        __isAdmin__ = None
                    break

            #是,则删除userid参数
            if __isAdmin__=="是":
                del req_dict["userid"]
            else:
                #否,则赋值userid参数
                req_dict["userid"]=request.session.get("params").get("id")
        print("req_dict===========>",req_dict)
        #20200928 去掉总记录数查询.因为只有一条记录,所以总记录数从查询所的记录获取
        #本次查询所有,求总记录数
        # alldata = examrecord.objects.filter(**req_dict). \
        #     annotate(userids=Count('userid'),paperids=Count('paperid'),papernames=Count('papername')). \
        #         values("userid", "paperid", "papername","myscore","userids"). \
        #         all()
        # print("alldata=============>",alldata)
        # print("alldata=============>",alldata.  aggregate(myscore=Sum('myscore')))

        #本次分页查询
        start=limit1 * (page1 - 1)
        end=limit1 * (page1 - 1)+limit1+1
        datas = examrecord.objects.filter(**req_dict).\
                    annotate(userids=Count('userid'),paperids=Count('paperid'),papernames=Count('papername')). \
                values("userid", "paperid", "papername","myscore"). \
                    all()[start:end]
        print("datas=============>", datas)
        print("datas=============>", datas.aggregate(myscore=Sum('myscore')))

        #处理分页查询所得数据
        try:
            data = [model_to_dict(i) for i in datas]
        except:
            data = datas
        dataDict = {}
        for i in data:
            keyName1="{}#{}#{}".format(i.get("userid"),i.get("paperid"),i.get("papername"))
            if dataDict.get(keyName1)==None:
                dataDict[keyName1]={"userid":i.get("userid"),"paperid":i.get("paperid"),"papername":i.get("papername"),"myscore":i.get("myscore")}
            else:
                dataDict[keyName1]["myscore"]=dataDict.get(keyName1).get("myscore")+i.get("myscore")

        #赋值分页查询所得数据
        dataList =list(dataDict.values())

        # 处理所有查询,计算总页数
        total = len(dataList)
        try:
            div = divmod(total, limit1)
            if div[1] > 0:
                totalPage = div[0] + 1
            else:
                totalPage = div[0]
        except:
            totalPage = 1

        # 赋值分页参数
        msg["data"] = {"pageSize": limit1,
                       "total": total,
                       "totalPage": totalPage,
                       "currPage": page1,
                       "list":dataList
                       }

        return JsonResponse(msg)



def examrecord_deleterecords(request):
    '''
    按键值对参数添加删除记录
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code}
        req_dict = request.session.get("req_dict")
        error=examrecord.deletebyparams(examrecord,examrecord,req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)
