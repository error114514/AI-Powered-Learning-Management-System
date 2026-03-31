# coding:utf-8
__author__ = "ila"
import os,sys
from django.http import JsonResponse, HttpResponse
from django.apps import apps


def index(request):
    if request.method in ["GET", "POST"]:
        msg = {"code": 200, "msg": "success", "data": []}
        print("=================>index")
        # allModels = apps.get_app_config('main').get_models()
        # for m in allModels:
        #     print(m.__tablename__)
        #     print(dir(m))
        #     # for col in m._meta.fields:
        #     #     print("col name============>",col.name)
        #     #     print("col type============>",col.get_internal_type())
        # print(allModels)

        return JsonResponse(msg)


def test(request, p1):
    if request.method in ["GET", "POST"]:
        msg = {"code": 200, "msg": "success", "data": []}
        print("=================>index  ", p1)
        return JsonResponse(msg)

def null(request,):
    if request.method in ["GET", "POST"]:
        msg = {"code": 200, "msg": "success", "data": []}
        return JsonResponse(msg)

def check_suffix(filelName,path1):
    try:
        image_data = open(path1, "rb").read()
    except:
        image_data = "no file"
    if '.js' in filelName:
        return HttpResponse(image_data, content_type="application/javascript")
    elif '.jpg' in filelName or '.jpeg' in filelName or '.png' in filelName or '.gif' in filelName:
        return HttpResponse(image_data, content_type="image/png")
    elif '.css' in filelName:
        return HttpResponse(image_data, content_type="text/css")
    elif '.ttf' in filelName or '.woff' in filelName:
        return HttpResponse(image_data, content_type="application/octet-stream")
    elif '.mp4' in filelName:
        return HttpResponse(image_data, content_type="video/mp4")
    elif '.mp3' in filelName:
        return HttpResponse(image_data, content_type="audio/mp3")
    elif '.csv' in filelName:
        return HttpResponse(image_data, content_type="application/CSV")
    elif '.doc' in filelName:
        return HttpResponse(image_data, content_type="application/msword")
    elif '.docx' in filelName:
        return HttpResponse(image_data, content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    elif '.xls' in filelName:
        return HttpResponse(image_data, content_type="application/vnd.ms-excel")
    elif '.xlsx' in filelName:
        return HttpResponse(image_data, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    elif '.ppt' in filelName:
        return HttpResponse(image_data, content_type="application/vnd.ms-powerpoint")
    elif '.pptx' in filelName:
        return HttpResponse(image_data, content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation")
    else:
        return HttpResponse(image_data, content_type="text/html")

def admin_lib2(request, p1, p2):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/admin/lib/", p1, p2)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)
        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p2:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p2 or '.jpeg' in p2 or '.png' in p2 or '.gif' in p2:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p2:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p2 or '.woff' in p2:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p2:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p2:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def admin_lib3(request, p1, p2, p3):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/admin/lib/", p1, p2, p3)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)
        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p3:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p3 or '.jpeg' in p3 or '.png' in p3 or '.gif' in p3:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p3:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p3 or '.woff' in p3:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p3:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p3:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def admin_lib4(request, p1, p2, p3, p4):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/admin/lib/", p1, p2, p3, p4)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)
        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p4:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p4 or '.jpeg' in p4 or '.png' in p4 or '.gif' in p4:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p4:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p4 or '.woff' in p4:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p4:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p4:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def admin_page(request, p1):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/admin/page/", p1)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)
        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p1:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p1 or '.jpeg' in p1 or '.png' in p1 or '.gif' in p1:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p1:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p1 or '.woff' in p1:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p1:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p1:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def admin_page2(request, p1, p2):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/admin/page/", p1, p2)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)
        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p2:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p2 or '.jpeg' in p2 or '.png' in p2 or '.gif' in p2:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p2:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p2 or '.woff' in p2:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p2:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p2:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def admin_pages(request, p1):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/admin/pages/", p1)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)
        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p1:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p1 or '.jpeg' in p1 or '.png' in p1 or '.gif' in p1:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p1:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p1 or '.woff' in p1:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p1:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p1:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def admin_pages2(request, p1, p2):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/admin/pages/", p1, p2)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)

        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p2:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p2 or '.jpeg' in p2 or '.png' in p2 or '.gif' in p2:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p2:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p2 or '.woff' in p2:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p2:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p2:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def admin_file1(request, p1):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/admin/", p1)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)

        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p1:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p1 or '.jpeg' in p1 or '.png' in p1 or '.gif' in p1:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p1:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p1 or '.woff' in p1:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p1:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p1:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def admin_file2(request, p1, p2):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/admin/", p1, p2)
        if not  os.path.isfile(path1):
            path1 = os.path.join(os.getcwd(), "templates/front/admin/dist/", p1, p2)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)
        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p2:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p2 or '.jpeg' in p2 or '.png' in p2 or '.gif' in p2:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p2:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p2 or '.woff' in p2:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p2:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p2:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def admin_file3(request, p1, p2, p3):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/admin/", p1, p2, p3)

        if not  os.path.isfile(path1):
            path1 = os.path.join(os.getcwd(), "templates/front/admin/dist/", p1, p2,p3)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)
        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p3:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p3 or '.jpeg' in p3 or '.png' in p3 or '.gif' in p3:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p3:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p3 or '.woff' in p3:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p3:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p3:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def admin_file4(request, p1, p2, p3, p4):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/admin/", p1, p2, p3, p4)
        if not  os.path.isfile(path1):
            path1 = os.path.join(os.getcwd(), "templates/front/admin/dist/", p1, p2,p3,p4)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)
        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p4:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p4 or '.jpeg' in p4 or '.png' in p4 or '.gif' in p4:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p4:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p4 or '.woff' in p4:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p4:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p4:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")

def front_pages(request, p1):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/pages/", p1)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)
        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p1:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p1 or '.jpeg' in p1 or '.png' in p1 or '.gif' in p1:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p1:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p1 or '.woff' in p1:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p1:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p1:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def front_pages2(request, p1, p2):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/pages/", p1, p2)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)

        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p2:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p2 or '.jpeg' in p2 or '.png' in p2 or '.gif' in p2:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p2:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p2 or '.woff' in p2:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p2:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p2:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def layui1(request, p1):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/layui/", p1)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)
        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p1:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p1 or '.jpeg' in p1 or '.png' in p1 or '.gif' in p1:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p1:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p1 or '.woff' in p1:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p1:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p1:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def layui2(request, p1, p2):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/layui/", p1, p2)
        print("layui2 path1========================>",path1)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)
        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p2:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p2 or '.jpeg' in p2 or '.png' in p2 or '.gif' in p2:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p2:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p2 or '.woff' in p2:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p2:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p2:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def layui3(request, p1, p2, p3):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/layui/", p1, p2, p3)
        print("layui3 path1========================>",path1)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)
        #
        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p3:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p3 or '.jpeg' in p3 or '.png' in p3 or '.gif' in p3:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p3:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p3 or '.woff' in p3:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p3:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p3:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def layui4(request, p1, p2, p3, p4):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/layui/", p1, p2, p3, p4)
        print("layui4 path1========================>",path1)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)
        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p4:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p4 or '.jpeg' in p4 or '.png' in p4 or '.gif' in p4:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p4:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p4 or '.woff' in p4:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p4:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p4:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def pages1(request, p1):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/pages/", p1)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)

        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p1:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p1 or '.jpeg' in p1 or '.png' in p1 or '.gif' in p1:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p1:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p1 or '.woff' in p1:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p1:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p1:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def pages2(request, p1, p2):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/pages/", p1, p2)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)

        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p2:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p2 or '.jpeg' in p2 or '.png' in p2 or '.gif' in p2:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p2:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p2 or '.woff' in p2:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p2:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p2:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def front_file1(request, p1):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/", p1)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)

        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p1:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p1 or '.jpeg' in p1 or '.png' in p1 or '.gif' in p1:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p1:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p1 or '.woff' in p1:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p1:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p1:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def front_file2(request, p1, p2):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/", p1, p2)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)

        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p2:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p2 or '.jpeg' in p2 or '.png' in p2 or '.gif' in p2:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p2:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p2 or '.woff' in p2:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p2:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p2:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")

def schema_front1(request, p1):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/", p1)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)
        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p1:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p1 or '.jpeg' in p1 or '.png' in p1 or '.gif' in p1:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p1:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p1 or '.woff' in p1:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p1:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p1:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def schema_front2(request, p1, p2):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/", p1, p2)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)

        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p2:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p2 or '.jpeg' in p2 or '.png' in p2 or '.gif' in p2:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p2:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p2 or '.woff' in p2:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p2:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p2:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def schema_front3(request, p1, p2, p3):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/", p1, p2, p3)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)
        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p3:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p3 or '.jpeg' in p3 or '.png' in p3 or '.gif' in p3:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p3:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p3 or '.woff' in p3:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p3:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p3:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def schema_front4(request, p1, p2, p3, p4):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/", p1, p2, p3, p4)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)

        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p4:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p4 or '.jpeg' in p4 or '.png' in p4 or '.gif' in p4:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p4:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p4 or '.woff' in p4:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p4:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p4:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")

def assets1(request, p1):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/assets/", p1)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)

        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p1:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p1 or '.jpeg' in p1 or '.png' in p1 or '.gif' in p1:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p1:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p1 or '.woff' in p1:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p1:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p1:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # elif '.map' in p1:
        #     return JsonResponse({})
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def assets2(request, p1, p2):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/assets/", p1, p2)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)
        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p2:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p2 or '.jpeg' in p2 or '.png' in p2 or '.gif' in p2:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p2:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p2 or '.woff' in p2:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p2:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p2:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # elif '.map' in p2:
        #     return JsonResponse({})
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def assets3(request, p1, p2, p3):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/assets/", p1, p2, p3)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)
        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p3:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p3 or '.jpeg' in p3 or '.png' in p3 or '.gif' in p3:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p3:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p3 or '.woff' in p3:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p3:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p3:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # elif '.map' in p3:
        #     return JsonResponse({})
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def assets4(request, p1, p2, p3, p4):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/assets/", p1, p2, p3, p4)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)
        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p4:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p4 or '.jpeg' in p4 or '.png' in p4 or '.gif' in p4:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p4:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p4 or '.woff' in p4:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p4:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p4:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # elif '.map' in p4:
        #     return JsonResponse({})
        # else:
        #     return HttpResponse(image_data, content_type="text/html")

def css1(request, p1):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/css/", p1)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)

        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p1:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p1 or '.jpeg' in p1 or '.png' in p1 or '.gif' in p1:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p1:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p1 or '.woff' in p1:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p1:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p1:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")

def js1(request, p1):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/js/", p1)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]),path1)

        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p1:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p1 or '.jpeg' in p1 or '.png' in p1 or '.gif' in p1:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p1:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p1 or '.woff' in p1:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p1:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p1:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")

def img1(request, p1):
    if request.method in ["GET", "POST"]:
        fullPath = request.get_full_path()
        print("{}=============>".format(sys._getframe().f_code.co_name), fullPath)
        path1 = os.path.join(os.getcwd(), "templates/front/img/", p1)

        return check_suffix(eval(eval(sys._getframe().f_code.co_name).__code__.co_varnames[-3]), path1)

        # try:
        #     image_data = open(path1, "rb").read()
        # except:
        #     image_data="no file"
        # if '.js' in p1:
        #     return HttpResponse(image_data, content_type="application/javascript")
        # elif '.jpg' in p1 or '.jpeg' in p1 or '.png' in p1 or '.gif' in p1:
        #     return HttpResponse(image_data, content_type="image/png")
        # elif '.css' in p1:
        #     return HttpResponse(image_data, content_type="text/css")
        # elif '.ttf' in p1 or '.woff' in p1:
        #     return HttpResponse(image_data, content_type="application/octet-stream")
        # elif '.mp4' in p1:
        #     return HttpResponse(image_data, content_type="video/mp4")
        # elif '.mp3' in p1:
        #     return HttpResponse(image_data, content_type="audio/mp3")
        # else:
        #     return HttpResponse(image_data, content_type="text/html")


def add_attendance(request):
    '''
    添加考勤记录接口
    Add attendance record endpoint
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})

    if request.method == "POST":
        import json
        from datetime import datetime
        from main.models import attendance_records, xuexitiandi, xuesheng

        msg = {"code": 200, "msg": "success", "data": []}

        try:
            # 获取请求数据
            data = json.loads(request.body)
            user_id = data.get('user_id')
            course_id = data.get('course_id')
            attendance_time = data.get('attendance_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            if not user_id or not course_id:
                msg['code'] = 400
                msg['msg'] = "缺少必要参数：user_id 或 course_id"
                return JsonResponse(msg)

            # 检查课程是否存在
            if not xuexitiandi.objects.filter(id=course_id).exists():
                msg['code'] = 404
                msg['msg'] = "课程不存在"
                return JsonResponse(msg)

            # 检查用户是否存在
            if not xuesheng.objects.filter(id=user_id).exists():
                msg['code'] = 404
                msg['msg'] = "用户不存在"
                return JsonResponse(msg)

            # 创建考勤记录（使用 attendance_records 表）
            attendance = attendance_records.objects.create(
                course_id=course_id,
                user_id=user_id,
                attendance_time=datetime.now()
            )

            msg['msg'] = "考勤记录成功"
            msg['data'] = {'id': attendance.id}

        except Exception as e:
            msg['code'] = 500
            msg['msg'] = f"添加失败：{str(e)}"

        return JsonResponse(msg)


def get_course_attendance(request, course_id):
    '''
    获取课程考勤记录接口
    Get course attendance records endpoint
    '''
    if request.method == "OPTIONS":
        return JsonResponse({})

    if request.method == "GET":
        from main.models import attendance_records, xuexitiandi, xuesheng
        import json
        import logging

        msg = {"code": 200, "msg": "success", "data": []}

        logging.info(f"======>>>> 开始查询考勤记录，course_id: {course_id}")

        try:
            # 检查课程是否存在
            course_exists = xuexitiandi.objects.filter(id=course_id).exists()
            logging.info(f"======>>>> 课程是否存在：{course_exists}")

            if not course_exists:
                msg['code'] = 404
                msg['msg'] = "课程不存在"
                logging.warning(f"======>>>> 课程不存在：{course_id}")
                return JsonResponse(msg)

            # 查询考勤记录（从 attendance_records 表）- 移除 select_related
            attendance_list = attendance_records.objects.filter(
                course_id=course_id
            ).order_by('-attendance_time')

            logging.info(f"======>>>> 查询到的考勤记录数量：{len(attendance_list)}")

            data = []
            for record in attendance_list:
                # 获取用户名 - 手动查询 xuesheng 表
                user_name = ''
                if record.user_id:
                    student = xuesheng.objects.filter(id=record.user_id).first()
                    if student:
                        user_name = getattr(student, 'xingming', '')
                    logging.info(f"======>>>> 用户 ID: {record.user_id}, 用户名：{user_name}")

                # 获取课程名称 - 手动查询 xuexitiandi 表
                course = xuexitiandi.objects.filter(id=record.course_id).first()
                course_name = course.biaoti if course else ''

                logging.info(
                    f"======>>>> 考勤记录：ID={record.id}, course={course_name}, user={user_name}, time={record.attendance_time}")

                attendance_record = {
                    'id': record.id,
                    'course_name': course_name,
                    'user_name': user_name,
                    'attendance_time': record.attendance_time.strftime(
                        '%Y-%m-%d %H:%M:%S') if record.attendance_time else ''
                }

                data.append(attendance_record)

            msg['data'] = data
            logging.info(f"======>>>> 返回数据：{data}")

        except Exception as e:
            logging.error(f"======>>>> 查询异常：{str(e)}")
            msg['code'] = 500
            msg['msg'] = f"查询失败：{str(e)}"

        return JsonResponse(msg)