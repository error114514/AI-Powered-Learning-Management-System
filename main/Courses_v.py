# coding:utf-8
__author__ = "ila"
import copy
import base64
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.apps import apps
from django.db.models import Q
from django.db import transaction
from .models import xuexitiandi, xuesheng
from util.codes import *
from util.auth import Auth
import util.message as mes
from util.face_util import FaceUtil
from util import message as mes
import datetime
from .model import Attendance

logger = logging.getLogger(__name__)

def teacher_face_sign_in(request, course_id):
    """
    教师端人脸识别签到API
    POST /api/courses/{course_id}/teacher_face_sign_in
    """
    if request.method == "OPTIONS":
        return JsonResponse({})

    if request.method != "POST":
        return JsonResponse({'code': system_error_code, 'msg': '只支持POST请求'})

    msg = {'code': normal_code, 'msg': '签到成功', 'data': {}}
    req_dict = request.session.get("req_dict")

    # 验证教师身份
    teacher_id = request.session.get("params", {}).get("id")
    if not teacher_id:
        msg['code'] = non_authorized_code
        msg['msg'] = '未登录或身份验证失败'
        return JsonResponse(msg)

    # 获取上传的文件
    file = request.FILES.get("file")
    if not file:
        msg['code'] = crud_error_code
        msg['msg'] = '未上传文件'
        return JsonResponse(msg)

    if file.size == 0:
        msg['code'] = crud_error_code
        msg['msg'] = '上传的文件为空'
        return JsonResponse(msg)

    try:
        # 读取文件并转换为 Base64
        file_bytes = file.read()
        base64_image = base64.b64encode(file_bytes).decode('utf-8')

        # 获取课程信息 - 使用 xuexitiandi 模型
        course = xuexitiandi.objects.filter(id=course_id).first()
        if not course:
            msg['code'] = crud_error_code
            msg['msg'] = '课程不存在'
            return JsonResponse(msg)

        # 获取所有学生列表
        enrolled_students = xuesheng.objects.all()

        # 如果没有学生，返回提示
        if not enrolled_students:
            msg['code'] = normal_code
            msg['msg'] = '未找到符合条件的学生'
            msg['data'] = {'matched_students': []}
            return JsonResponse(msg)

        # 提取人脸特征并进行比对
        matched_students = []
        unmatched_students = []

        for student in enrolled_students:
            # 获取学生的照片字段
            student_face_photo = student.zhaopian

            if not student_face_photo:
                unmatched_students.append({
                    'id': student.id,
                    'name': student.xingming,
                    'reason': '没有人脸照片'
                })
                continue

            try:
                # 调用 FaceUtil 进行人脸比对
                recognized_user_id = FaceUtil.find_face(base64_image)

                if recognized_user_id and str(recognized_user_id) == str(student.id):
                    matched_students.append({
                        'id': student.id,
                        'name': student.xingming
                    })
                else:
                    unmatched_students.append({
                        'id': student.id,
                        'name': student.xingming,
                        'reason': '人脸不匹配'
                    })
            except Exception as e:
                logger.error(f"人脸比对失败：{str(e)}")
                unmatched_students.append({
                    'id': student.id,
                    'name': student.xingming,
                    'reason': f'人脸识别错误：{str(e)}'
                })

        # 创建签到记录
        for student in matched_students:
            # 检查是否已经签到
            existing_record = Attendance.objects.filter(
                course_id=course_id,
                student_id=student['id'],
                timestamp__date=datetime.date.today()
            ).first()

            if not existing_record:
                # 创建新的签到记录
                attendance_data = {
                    'course_id': course_id,
                    'student_id': student['id'],
                    'timestamp': datetime.datetime.now(),
                    'method': 'teacher_face_sign_in',
                    'source_image_id': file.name,
                    'status': 'signed_in'
                }

                with transaction.atomic():
                    Attendance.objects.create(**attendance_data)

        # 构建响应
        if matched_students:
            msg['data'] = {
                'matched_students': matched_students,
                'unmatched_students': unmatched_students,
                'total_matched': len(matched_students),
                'total_unmatched': len(unmatched_students)
            }
            msg['msg'] = f'成功匹配 {len(matched_students)} 名学生'
        else:
            msg['code'] = normal_code
            msg['msg'] = '未找到符合条件的学生'
            msg['data'] = {
                'matched_students': [],
                'unmatched_students': unmatched_students,
                'total_matched': 0,
                'total_unmatched': len(unmatched_students)
            }

        return JsonResponse(msg)

    except Exception as e:
        logger.error(f"教师人脸识别签到失败：{str(e)}")
        msg['code'] = crud_error_code
        msg['msg'] = f'签到失败：{str(e)}'
        return JsonResponse(msg)

def xuexitiandi_attendance(request):
    """
    考勤页面 - 教师端人脸识别签到
    GET /xuexitiandi/attendance
    """
    if request.method == "OPTIONS":
        return JsonResponse({})

    # 验证教师身份
    teacher_id = request.session.get("params", {}).get("id")
    if not teacher_id:
        return JsonResponse({'code': non_authorized_code, 'msg': '未登录或身份验证失败'})

    # 获取课程ID（可以从请求参数或session中获取）
    course_id = request.GET.get('course_id') or 1  # 默认值1，需要根据实际情况调整

    # 渲染考勤页面
    return render(request, 'pages/xuexitiandi/attendance.html', {
        'course_id': course_id,
        'teacher_id': teacher_id
    })