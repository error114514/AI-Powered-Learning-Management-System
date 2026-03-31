from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import connection
import json
from .models import attendance_records, xuexitiandi, xuesheng

@csrf_exempt
@require_http_methods(["POST"])
def add_attendance(request):
    """新增考勤记录"""
    try:
        data = json.loads(request.body)
        course_id = data.get('course_id')
        user_id = data.get('user_id')
        attendance_time = data.get('attendance_time')

        if not all([course_id, user_id, attendance_time]):
            return JsonResponse({'code': 400, 'msg': '缺少必要参数'})

        # 检查课程是否存在
        if not xuexitiandi.objects.filter(id=course_id).exists():
            return JsonResponse({'code': 404, 'msg': '课程不存在'})

        # 检查用户是否存在
        if not xuesheng.objects.filter(id=user_id).exists():
            return JsonResponse({'code': 404, 'msg': '用户不存在'})

        # 创建考勤记录
        attendance = attendance_records.objects.create(
            course_id=course_id,
            user_id=user_id,
            attendance_time=attendance_time
        )

        return JsonResponse({'code': 200, 'msg': '考勤记录创建成功', 'data': {'id': attendance.id}})
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': f'服务器错误: {str(e)}'})

@csrf_exempt
@require_http_methods(["GET"])
def get_course_attendance(request, course_id):
    """获取指定课程考勤列表"""
    try:
        # 检查课程是否存在
        if not xuexitiandi.objects.filter(id=course_id).exists():
            return JsonResponse({'code': 404, 'msg': '课程不存在'})

        # 查询考勤记录
        attendance_list = attendance_records.objects.filter(
            course_id=course_id
        ).select_related('course', 'user').order_by('-attendance_time')

        # 格式化数据
        data = []
        for record in attendance_list:
            data.append({
                'id': record.id,
                'course_name': record.course.biaoti if record.course else '',  # 假设课程表有biaoti字段
                'user_name': record.user.xingming if record.user else '',  # 假设用户表有xingming字段
                'attendance_time': record.attendance_time.strftime('%Y-%m-%d %H:%M:%S')
            })

        return JsonResponse({'code': 200, 'msg': '获取成功', 'data': data})
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': f'服务器错误: {str(e)}'})
