import json
import requests
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import re
from django.contrib.auth import get_user_model
from .models import xuesheng, examrecord, xuexitiandi, xuexiziliao, discussxuexitiandi, discussxuexiziliao

# DeepSeek API 配置
DEEPSEEK_API_KEY = 'sk-110104bc985447b0b511543ae724a430'
DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'


def get_current_user(request):
    """从请求头中获取当前用户"""
    token = request.headers.get('Token')
    print("token", token)
    if not token:
        return None

    try:
        # 尝试使用学号（xuehao）查找用户
        user = xuesheng.objects.get(xuehao=token)
        return user
    except (ValueError, xuesheng.DoesNotExist):
        try:
            # 如果学号找不到，尝试使用ID查找
            user = xuesheng.objects.get(id=token)
            return user
        except (ValueError, xuesheng.DoesNotExist):
            return None


def get_user_learning_data(userId):
    """获取用户的学习数据（主要基于作业记录）"""
    if not userId:
        return None

    try:
        # 先获取用户对象
        user = xuesheng.objects.get(id=userId)

        # 获取用户的作业记录
        exam_records = examrecord.objects.filter(userid=userId).order_by('-addtime')

        # 计算作业统计数据
        total_exams = exam_records.count()
        total_score = sum(record.myscore for record in exam_records if record.myscore is not None)
        avg_score = total_score / total_exams if total_exams > 0 else 0

        # 分析作业表现趋势
        recent_exams = exam_records[:5]
        recent_scores = [record.myscore for record in recent_exams if record.myscore is not None]
        recent_avg = sum(recent_scores) / len(recent_scores) if recent_scores else 0

        # 分析作业类型分布
        exam_types = {}
        for record in exam_records:
            paper_name = record.papername
            if paper_name not in exam_types:
                exam_types[paper_name] = {'count': 0, 'total_score': 0}
            exam_types[paper_name]['count'] += 1
            if record.myscore is not None:
                exam_types[paper_name]['total_score'] += record.myscore

        # 获取最佳和最差表现的作业
        best_exam = max(exam_records, key=lambda x: x.myscore if x.myscore is not None else 0) if exam_records else None
        worst_exam = min(exam_records,
                         key=lambda x: x.myscore if x.myscore is not None else 100) if exam_records else None

        return {
            'user': user,  # 添加用户对象
            'exam_records': exam_records,
            'total_exams': total_exams,
            'avg_score': avg_score,
            'recent_avg': recent_avg,
            'exam_types': exam_types,
            'best_exam': best_exam,
            'worst_exam': worst_exam,
            'recent_scores': recent_scores
        }
    except xuesheng.DoesNotExist:
        print(f"用户ID {userId} 不存在")
        return None
    except Exception as e:
        print(f"获取学习数据时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def generate_comprehensive_evaluation(learning_data):
    """生成基于作业记录的综合评价"""
    if not learning_data:
        return "暂无足够的作业记录数据来生成综合评价。"

    user = learning_data['user']
    exam_records = learning_data['exam_records']
    total_exams = learning_data['total_exams']
    avg_score = learning_data['avg_score']
    recent_avg = learning_data['recent_avg']
    best_exam = learning_data['best_exam']
    worst_exam = learning_data['worst_exam']

    # 生成评价
    evaluation = f"📊 作业综合评价\n\n"
    evaluation += f"👤 用户：{user.xingming}\n"
    evaluation += f"📝 总作业次数：{total_exams}次\n"
    evaluation += f"🎯 平均成绩：{avg_score:.1f}分\n"
    evaluation += f"📈 最近5次平均：{recent_avg:.1f}分\n\n"

    # 分析作业表现
    if total_exams == 0:
        evaluation += "暂无作业记录，建议多参与作业练习。"
    else:
        # 成绩分析
        if avg_score >= 90:
            evaluation += "🌟 成绩优秀！\n"
            evaluation += "  - 表现非常出色，继续保持良好的学习状态\n"
            evaluation += "  - 可以尝试更高难度的作业内容\n"
            evaluation += "  - 考虑帮助其他同学，分享学习经验\n\n"
        elif avg_score >= 80:
            evaluation += "👍 成绩良好！\n"
            evaluation += "  - 表现不错，继续保持\n"
            evaluation += "  - 可以适当挑战一些进阶作业\n"
            evaluation += "  - 加强薄弱知识点的练习\n\n"
        elif avg_score >= 70:
            evaluation += "📈 成绩一般\n"
            evaluation += "  - 需要更加努力\n"
            evaluation += "  - 建议加强基础知识的巩固\n"
            evaluation += "  - 多参与基础练习，提高解题能力\n\n"
        else:
            evaluation += "📚 需要提升\n"
            evaluation += "  - 建议加强学习，多参与作业练习\n"
            evaluation += "  - 寻求老师和同学的帮助\n"
            evaluation += "  - 制定明确的学习计划\n\n"

        # 趋势分析
        if recent_avg > avg_score:
            evaluation += "📈 进步趋势：\n"
            evaluation += "  - 最近表现有进步，继续保持！\n"
            evaluation += "  - 可以尝试更复杂的题目\n\n"
        elif recent_avg < avg_score:
            evaluation += "📉 下降趋势：\n"
            evaluation += "  - 最近表现有所下降，需要注意\n"
            evaluation += "  - 建议回顾基础知识，加强练习\n\n"
        else:
            evaluation += "📊 稳定表现：\n"
            evaluation += "  - 成绩保持稳定，可以尝试突破\n\n"

        # 最佳和最差表现
        if best_exam:
            evaluation += f"🏆 最佳表现：{best_exam.papername} - {best_exam.myscore}分\n"
            evaluation += f"  - 在这个作业中表现出色，可以总结成功经验\n\n"

        if worst_exam:
            evaluation += f"📉 需要改进：{worst_exam.papername} - {worst_exam.myscore}分\n"
            evaluation += "  - 这个作业表现有待提高，建议加强相关知识点学习\n\n"

    return evaluation


def generate_personal_recommendations(learning_data):
    """生成基于作业记录的个性化成长推荐"""
    if not learning_data:
        return "暂无足够的作业记录数据来生成个性化推荐。"

    user = learning_data['user']
    exam_records = learning_data['exam_records']
    total_exams = learning_data['total_exams']
    avg_score = learning_data['avg_score']
    recent_avg = learning_data['recent_avg']
    exam_types = learning_data['exam_types']
    best_exam = learning_data['best_exam']
    worst_exam = learning_data['worst_exam']

    recommendations = f"🎯 个性化成长推荐\n\n"
    recommendations += f"👤 用户：{user.xingming}\n"
    recommendations += f"📝 总作业次数：{total_exams}次\n"
    recommendations += f"🎯 平均成绩：{avg_score:.1f}分\n\n"

    # 基于成绩的推荐
    if total_exams == 0:
        recommendations += "📚 建议开始参与作业练习，积累学习数据\n"
        recommendations += "  - 从基础作业开始，逐步提高难度\n"
        recommendations += "  - 定期完成作业，建立学习习惯\n\n"
    else:
        # 成绩分析推荐
        if avg_score >= 90:
            recommendations += "🏆 成绩优秀推荐：\n"
            recommendations += "  - 可以尝试更高难度的作业\n"
            recommendations += "  - 参与竞赛类作业，挑战自我\n"
            recommendations += "  - 考虑担任学习小组的指导角色\n"
            recommendations += "  - 深入研究感兴趣的学科领域\n\n"
        elif avg_score >= 80:
            recommendations += "📈 成绩良好推荐：\n"
            recommendations += "  - 保持当前学习节奏\n"
            recommendations += "  - 可以尝试一些进阶作业\n"
            recommendations += "  - 加强薄弱知识点的学习\n"
            recommendations += "  - 参与小组讨论，分享学习经验\n\n"
        elif avg_score >= 70:
            recommendations += "📈 成绩一般推荐：\n"
            recommendations += "  - 加强基础知识学习\n"
            recommendations += "  - 多参与基础练习，提高解题能力\n"
            recommendations += "  - 寻求老师和同学的帮助\n"
            recommendations += "  - 制定明确的学习计划\n\n"
        else:
            recommendations += "📚 需要提升推荐：\n"
            recommendations += "  - 建议加强学习，多参与作业练习\n"
            recommendations += "  - 从基础作业开始，逐步提高\n"
            recommendations += "  - 寻求老师和同学的帮助\n"
            recommendations += "  - 制定明确的学习目标和计划\n\n"

        # 趋势分析推荐
        if recent_avg > avg_score:
            recommendations += "📈 进步趋势推荐：\n"
            recommendations += "  - 继续保持良好的学习状态\n"
            recommendations += "  - 可以尝试更复杂的题目\n"
            recommendations += "  - 总结成功经验，应用到其他学科\n\n"
        elif recent_avg < avg_score:
            recommendations += "📉 下降趋势推荐：\n"
            recommendations += "  - 最近表现有所下降，需要注意\n"
            recommendations += "  - 建议回顾基础知识，加强练习\n"
            recommendations += "  - 寻找学习中的问题，及时调整\n\n"
        else:
            recommendations += "📊 稳定表现推荐：\n"
            recommendations += "  - 成绩保持稳定，可以尝试突破\n"
            recommendations += "  - 寻找新的学习方法和策略\n"
            recommendations += "  - 拓展学习领域，全面发展\n\n"

        # 基于作业类型的推荐
        if exam_types:
            recommendations += "📚 作业类型推荐：\n"
            # 找出用户参与最多的作业类型
            top_type = max(exam_types.items(), key=lambda x: x[1]['count'])[0]
            recommendations += f"  - 你最常参与的作业类型：{top_type}\n"
            recommendations += "  - 可以深入钻研这个领域的知识\n"
            recommendations += "  - 尝试不同类型的作业，全面发展\n\n"

        # 基于最佳和最差表现的推荐
        if best_exam:
            recommendations += f"🏆 最佳表现领域：{best_exam.papername}\n"
            recommendations += "  - 在这个领域表现出色，可以继续深入\n"
            recommendations += "  - 总结成功经验，应用到其他学科\n\n"

        if worst_exam:
            recommendations += f"📉 需要改进领域：{worst_exam.papername}\n"
            recommendations += "  - 这个领域表现有待提高\n"
            recommendations += "  - 建议加强相关知识点学习\n"
            recommendations += "  - 寻求老师和同学的帮助\n\n"

    # 通用学习建议
    recommendations += "💡 通用学习建议：\n"
    recommendations += "  - 制定明确的学习目标\n"
    recommendations += "  - 保持规律的学习习惯\n"
    recommendations += "  - 积极参与作业练习\n"
    recommendations += "  - 定期复习和总结\n"
    recommendations += "  - 寻求反馈，不断改进\n"

    return recommendations


def parse_messages(request):
    """解析请求中的messages数据"""
    messages = []

    if request.method == 'POST':
        # 检查是否是JSON格式
        content_type = request.META.get('CONTENT_TYPE', '')
        if 'application/json' in content_type:
            try:
                data = json.loads(request.body)
                messages = data.get('messages', [])
            except json.JSONDecodeError:
                pass

        # 如果不是JSON格式或解析失败，尝试从POST参数获取
        if not messages:
            post_data = request.POST
            message_dict = {}

            for key, value in post_data.items():
                if key.startswith('messages['):
                    match = re.match(r'messages\[(\d+)\]\[(\w+)\]', key)
                    if match:
                        index = int(match.group(1))
                        field = match.group(2)
                        if index not in message_dict:
                            message_dict[index] = {}
                        message_dict[index][field] = value

            if message_dict:
                max_index = max(message_dict.keys())
                for i in range(max_index + 1):
                    if i in message_dict:
                        messages.append(message_dict[i])

    return messages


@csrf_exempt
@require_http_methods(["POST"])
def ai_chat(request):
    """
    AI聊天接口，代理调用DeepSeek API（非流式）
    """
    try:
        messages = parse_messages(request)

        if not messages:
            return JsonResponse({
                'code': 1,
                'msg': '消息不能为空'
            })

        # 从请求头或POST数据中获取用户ID
        if hasattr(request.session, 'get'):
            params = request.session.get('params', {})
            user_id = params.get('id')

        print(f"从Session获取到的用户ID: {user_id}")

        if not user_id:
            return JsonResponse({'code': 1, 'msg': '缺少用户ID'})

        # 获取最后一条消息内容
        last_message = messages[-1]['content'] if messages else ''

        # 检查是否是特殊指令
        if '@综合评价' in last_message:
            # 处理综合评价指令
            learning_data = get_user_learning_data(user_id)
            ai_response = generate_comprehensive_evaluation(learning_data)
            return JsonResponse({
                'code': 0,
                'msg': 'success',
                'data': {
                    'response': ai_response
                }
            })
        elif '@个性化成长推荐' in last_message:
            # 处理个性化成长推荐指令
            learning_data = get_user_learning_data(user_id)
            ai_response = generate_personal_recommendations(learning_data)
            return JsonResponse({
                'code': 0,
                'msg': 'success',
                'data': {
                    'response': ai_response
                }
            })

        # 如果不是特殊指令，继续调用DeepSeek API
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}'
        }

        payload = {
            'model': 'deepseek-chat',
            'messages': messages,
            'temperature': 0.7,
            'max_tokens': 1024
        }

        try:
            response = requests.post(
                DEEPSEEK_API_URL,
                headers=headers,
                json=payload,
                timeout=60
            )
        except requests.exceptions.Timeout:
            return JsonResponse({
                'code': 1,
                'msg': 'API请求超时，请稍后再试'
            })
        except requests.exceptions.RequestException as e:
            return JsonResponse({
                'code': 1,
                'msg': f'API请求失败: {str(e)}'
            })

        if response.status_code != 200:
            return JsonResponse({
                'code': 1,
                'msg': f'API调用失败，状态码: {response.status_code}, 响应: {response.text[:200]}'
            })

        try:
            result = response.json()
        except json.JSONDecodeError as e:
            return JsonResponse({
                'code': 1,
                'msg': f'API返回数据格式错误: {str(e)}, 原始响应: {response.text[:200]}'
            })

        if 'choices' not in result or not result['choices']:
            return JsonResponse({
                'code': 1,
                'msg': f'API返回数据格式异常: {json.dumps(result)[:200]}'
            })

        ai_response = result['choices'][0]['message']['content']
        return JsonResponse({
            'code': 0,
            'msg': 'success',
            'data': {
                'response': ai_response
            }
        })

    except Exception as e:
        return JsonResponse({
            'code': 1,
            'msg': f'服务器错误: {str(e)}'
        })


@csrf_exempt
@require_http_methods(["POST"])
def ai_chat_stream(request):
    """
    AI聊天接口，流式响应（SSE格式）
    """
    try:
        messages = parse_messages(request)

        if not messages:
            def error_stream():
                yield 'data: {"error": "消息不能为空"}\n\n'
            return StreamingHttpResponse(error_stream(), content_type='text/event-stream')

        # 从请求头或POST数据中获取用户ID
        if hasattr(request.session, 'get'):
            params = request.session.get('params', {})
            user_id = params.get('id')

        print(f"从Session获取到的用户ID: {user_id}")

        # 获取最后一条消息内容
        last_message = messages[-1]['content'] if messages else ''

        # 检查是否是特殊指令
        if '@综合评价' in last_message:
            # 处理综合评价指令

            learning_data = get_user_learning_data(user_id)
            ai_response = generate_comprehensive_evaluation(learning_data)

            def generate():
                # 流式输出综合评价
                yield f'data: {{"content": {json.dumps(ai_response)}}}\n\n'
                yield 'data: [DONE]\n\n'

            return StreamingHttpResponse(generate(), content_type='text/event-stream')
        elif '@个性化成长推荐' in last_message:
            # 处理个性化成长推荐指令
            token = request.headers.get('Token')
            learning_data = get_user_learning_data(user_id)
            ai_response = generate_personal_recommendations(learning_data)

            def generate():
                # 流式输出个性化推荐
                yield f'data: {{"content": {json.dumps(ai_response)}}}\n\n'
                yield 'data: [DONE]\n\n'

            return StreamingHttpResponse(generate(), content_type='text/event-stream')

        # 如果不是特殊指令，继续调用DeepSeek API
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}'
        }

        payload = {
            'model': 'deepseek-chat',
            'messages': messages,
            'temperature': 0.7,
            'max_tokens': 1024,
            'stream': True
        }

        def generate():
            try:
                response = requests.post(
                    DEEPSEEK_API_URL,
                    headers=headers,
                    json=payload,
                    timeout=60,
                    stream=True
                )

                if response.status_code != 200:
                    yield f'data: {{"error": "API调用失败: {response.status_code}"}}\n\n'
                    return

                for line in response.iter_lines():
                    if line:
                        line_str = line.decode('utf-8')
                        if line_str.startswith('data: '):
                            data_str = line_str[6:]  # 去掉 'data: ' 前缀
                            if data_str == '[DONE]':
                                yield 'data: [DONE]\n\n'
                                break
                            try:
                                data = json.loads(data_str)
                                if 'choices' in data and len(data['choices']) > 0:
                                    delta = data['choices'][0].get('delta', {})
                                    if 'content' in delta:
                                        content = delta['content']
                                        yield f'data: {{"content": {json.dumps(content)}}}\n\n'
                            except json.JSONDecodeError:
                                continue

            except requests.exceptions.Timeout:
                yield 'data: {"error": "请求超时"}\n\n'
            except Exception as e:
                yield f'data: {{"error": "{str(e)}"}}\n\n'

        return StreamingHttpResponse(generate(), content_type='text/event-stream')

    except Exception as e:
        def error_stream():
            yield f'data: {{"error": "服务器错误: {str(e)}"}}\n\n'
        return StreamingHttpResponse(error_stream(), content_type='text/event-stream')
