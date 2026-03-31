import json
import requests
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import re
from django.contrib.auth import get_user_model
from .models import xuesheng, examrecord, xuexitiandi, xuexiziliao, discussxuexitiandi, discussxuexiziliao, exampaper, examquestion
import random

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
    AI 聊天接口，代理调用 DeepSeek API（非流式）
    """
    try:
        messages = parse_messages(request)

        if not messages:
            return JsonResponse({
                'code': 1,
                'msg': '消息不能为空'
            })

        # 从请求头或 POST 数据中获取用户 ID
        if hasattr(request.session, 'get'):
            params = request.session.get('params', {})
            user_id = params.get('id')

        print(f"从 Session 获取到的用户 ID: {user_id}")

        if not user_id:
            return JsonResponse({'code': 1, 'msg': '缺少用户 ID'})

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

        elif '@作业知识点分析' in last_message or '@GM' in last_message:
            # 处理作业知识点分析指令
            learning_data = get_user_learning_data(user_id)

            # 检查是否指定了具体作业 ID
            match = re.search(r'(\d+)', last_message)
            exam_id = int(match.group(1)) if match else None

            ai_response = generate_knowledge_analysis(learning_data, exam_id)
            return JsonResponse({
                'code': 0,
                'msg': 'success',
                'data': {
                    'response': ai_response
                }
            })

        elif '@薄弱知识点巩固' in last_message:
            # 处理薄弱知识点巩固指令
            learning_data = get_user_learning_data(user_id)

            # 先分析知识点
            analysis_text = generate_knowledge_analysis(learning_data)

            # 提取薄弱知识点
            weak_points = []
            if '需要加强的知识点' in analysis_text:
                lines = analysis_text.split('\n')
                for line in lines:
                    if '•' in line and '需要加强的知识点' not in line:
                        kp_name = line.split('•')[1].split('(')[0].strip()
                        if kp_name:
                            weak_points.append(kp_name)

            ai_response = generate_remediation_plan(learning_data, weak_points)
            return JsonResponse({
                'code': 0,
                'msg': 'success',
                'data': {
                    'response': ai_response
                }
            })

        # 如果不是特殊指令，调用 DeepSeek API (非流式)
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
                'msg': 'API 请求超时，请稍后再试'
            })
        except requests.exceptions.RequestException as e:
            return JsonResponse({
                'code': 1,
                'msg': f'API 请求失败：{str(e)}'
            })

        if response.status_code != 200:
            return JsonResponse({
                'code': 1,
                'msg': f'API 调用失败，状态码：{response.status_code}, 响应：{response.text[:200]}'
            })

        try:
            result = response.json()
        except json.JSONDecodeError as e:
            return JsonResponse({
                'code': 1,
                'msg': f'API 返回数据格式错误：{str(e)}, 原始响应：{response.text[:200]}'
            })

        if 'choices' not in result or not result['choices']:
            return JsonResponse({
                'code': 1,
                'msg': f'API 返回数据格式异常：{json.dumps(result)[:200]}'
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
            'msg': f'服务器错误：{str(e)}'
        })


@csrf_exempt
@require_http_methods(["POST"])
def ai_chat_stream(request):
    """
    AI 聊天接口，流式响应（SSE 格式）
    """
    try:
        messages = parse_messages(request)

        if not messages:
            def error_stream():
                yield 'data: {"error": "消息不能为空"}\n\n'

            return StreamingHttpResponse(error_stream(), content_type='text/event-stream')

        # 从请求头或 POST 数据中获取用户 ID
        if hasattr(request.session, 'get'):
            params = request.session.get('params', {})
            user_id = params.get('id')

        print(f"从 Session 获取到的用户 ID: {user_id}")

        # 获取最后一条消息内容
        last_message = messages[-1]['content'] if messages else ''

        # 检查是否是特殊指令
        if '@综合评价' in last_message:
            # 处理综合评价指令
            learning_data = get_user_learning_data(user_id)
            ai_response = generate_comprehensive_evaluation(learning_data)

            def generate_ce():
                # 流式输出综合评价
                yield f'data: {{"content": {json.dumps(ai_response)}}}\n\n'
                yield 'data: [DONE]\n\n'

            return StreamingHttpResponse(generate_ce(), content_type='text/event-stream')

        elif '@个性化成长推荐' in last_message:
            # 处理个性化成长推荐指令
            learning_data = get_user_learning_data(user_id)
            ai_response = generate_personal_recommendations(learning_data)

            def generate_pr():
                # 流式输出个性化推荐
                yield f'data: {{"content": {json.dumps(ai_response)}}}\n\n'
                yield 'data: [DONE]\n\n'

            return StreamingHttpResponse(generate_pr(), content_type='text/event-stream')

        elif '@作业知识点分析' in last_message or '@GM' in last_message:
            # 处理作业知识点分析指令
            learning_data = get_user_learning_data(user_id)

            # 检查是否指定了具体作业 ID
            match = re.search(r'(\d+)', last_message)
            exam_id = int(match.group(1)) if match else None

            ai_response = generate_knowledge_analysis(learning_data, exam_id)

            def generate_ka():
                yield f'data: {{"content": {json.dumps(ai_response)}}}\n\n'
                yield 'data: [DONE]\n\n'

            return StreamingHttpResponse(generate_ka(), content_type='text/event-stream')

        elif '@薄弱知识点巩固' in last_message:
            # 处理薄弱知识点巩固指令
            learning_data = get_user_learning_data(user_id)

            # 先分析知识点
            analysis_text = generate_knowledge_analysis(learning_data)

            # 提取薄弱知识点
            weak_points = []
            if '需要加强的知识点' in analysis_text:
                lines = analysis_text.split('\n')
                for line in lines:
                    if '•' in line and '需要加强的知识点' not in line:
                        kp_name = line.split('•')[1].split('(')[0].strip()
                        if kp_name:
                            weak_points.append(kp_name)

            ai_response = generate_remediation_plan(learning_data, weak_points)

            def generate_rp():
                yield f'data: {{"content": {json.dumps(ai_response)}}}\n\n'
                yield 'data: [DONE]\n\n'

            return StreamingHttpResponse(generate_rp(), content_type='text/event-stream')

        # 如果不是特殊指令，调用 DeepSeek API (流式模式)
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

        def generate_ds():
            try:
                response = requests.post(
                    DEEPSEEK_API_URL,
                    headers=headers,
                    json=payload,
                    timeout=60,
                    stream=True
                )

                if response.status_code != 200:
                    yield f'data: {{"error": "API 调用失败：{response.status_code}"}}\n\n'
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

        return StreamingHttpResponse(generate_ds(), content_type='text/event-stream')

    except Exception as e:
        def error_stream():
            yield f'data: {{"error": "服务器错误：{str(e)}"}}\n\n'

        return StreamingHttpResponse(error_stream(), content_type='text/event-stream')


#region 2026、3、31 新增GM指令

def analyze_exam_knowledge_points(exam_record):
    """分析单次作业的知识点"""
    if not exam_record or not exam_record.papername:
        return []

    # 获取试卷信息
    try:
        paper = exampaper.objects.filter(name=exam_record.papername).first()
        if not paper:
            return []

        # 获取该试卷的所有题目
        questions = examquestion.objects.filter(paperid=paper.id)
        knowledge_points = []

        for question in questions:
            if question.knowledge_point:  # 假设有 knowledge_point 字段
                knowledge_points.append({
                    'name': question.knowledge_point,
                    'question_type': question.questiontype,
                    'score': question.score,
                    'user_answer': exam_record.answer if hasattr(exam_record, 'answer') else None,
                    'correct_answer': question.answer
                })

        return knowledge_points
    except Exception as e:
        print(f"分析知识点失败：{str(e)}")
        return []


def generate_knowledge_analysis(learning_data, specific_exam_id=None):
    """生成作业知识点分析"""
    if not learning_data:
        return "暂无学习数据，无法进行分析。"

    user = learning_data['user']
    exam_records = learning_data['exam_records']

    if not exam_records.exists():
        return "暂无作业记录，请先完成至少一次作业。"

    # 如果指定了具体作业 ID，只分析该作业
    if specific_exam_id:
        target_exam = exam_records.filter(id=specific_exam_id).first()
        if not target_exam:
            return "未找到指定的作业记录。"

        analysis = f"📚 作业知识点分析报告\n\n"
        analysis += f"👤 用户：{user.xingming}\n"
        analysis += f"📝 作业名称：{target_exam.papername}\n"
        analysis += f"🎯 得分：{target_exam.myscore}分\n"
        analysis += f"⏰ 完成时间：{target_exam.addtime.strftime('%Y-%m-%d %H:%M')}\n\n"

        # 分析该作业的知识点
        knowledge_points = analyze_exam_knowledge_points(target_exam)

        if not knowledge_points:
            analysis += "📌 该作业暂未收录详细知识点信息。\n"
            analysis += "💡 建议：联系老师完善作业题库的知识点标注。\n"
        else:
            analysis += f"📊 涉及知识点数量：{len(knowledge_points)}个\n\n"

            mastered = []
            weak = []

            for kp in knowledge_points:
                # 简单判断：如果题目做对了，认为是掌握的
                if kp.get('user_answer') == kp.get('correct_answer'):
                    mastered.append(kp['name'])
                else:
                    weak.append(kp['name'])

            if mastered:
                analysis += "✅ 已掌握知识点:\n"
                for name in set(mastered):
                    analysis += f"   • {name}\n"
                analysis += "\n"

            if weak:
                analysis += "⚠️ 待加强知识点:\n"
                for name in set(weak):
                    analysis += f"   • {name}\n"
                analysis += "\n"

                analysis += "💡 巩固建议:\n"
                analysis += "   1. 针对上述薄弱知识点，重新学习相关课程内容\n"
                analysis += "   2. 查找对应的学习资料进行专项练习\n"
                analysis += "   3. 向老师或同学请教不懂的问题\n"
                analysis += "   4. 完成同类知识点的其他作业进行巩固\n"

        return analysis

    # 分析所有作业的整体情况
    analysis = f"📚 综合知识点分析报告\n\n"
    analysis += f"👤 用户：{user.xingming}\n"
    analysis += f"📝 总作业次数：{exam_records.count()}次\n"
    analysis += f"🎯 平均成绩：{learning_data['avg_score']:.1f}分\n\n"

    all_knowledge_points = {}

    # 统计所有作业的知识点掌握情况
    for record in exam_records:
        kps = analyze_exam_knowledge_points(record)
        for kp in kps:
            kp_name = kp['name']
            if kp_name not in all_knowledge_points:
                all_knowledge_points[kp_name] = {'mastered': 0, 'total': 0}

            all_knowledge_points[kp_name]['total'] += 1
            if kp.get('user_answer') == kp.get('correct_answer'):
                all_knowledge_points[kp_name]['mastered'] += 1

    if not all_knowledge_points:
        analysis += "📌 当前作业库暂未收录详细的知识点信息。\n"
        analysis += "💡 建议：完善题库建设，为每道题目标注所属知识点。\n"
        return analysis

    analysis += f"📊 涉及知识点总数：{len(all_knowledge_points)}个\n\n"

    # 按掌握程度分类
    strong_points = []
    weak_points = []

    for kp_name, stats in all_knowledge_points.items():
        mastery_rate = stats['mastered'] / stats['total'] if stats['total'] > 0 else 0
        if mastery_rate >= 0.8:
            strong_points.append((kp_name, mastery_rate))
        elif mastery_rate < 0.6:
            weak_points.append((kp_name, mastery_rate))

    # 排序
    strong_points.sort(key=lambda x: x[1], reverse=True)
    weak_points.sort(key=lambda x: x[1])

    if strong_points:
        analysis += "✅ 掌握较好的知识点 (正确率≥80%):\n"
        for name, rate in strong_points[:10]:  # 只显示前 10 个
            analysis += f"   • {name} ({rate * 100:.0f}%)\n"
        analysis += "\n"

    if weak_points:
        analysis += "⚠️ 需要加强的知识点 (正确率<60%):\n"
        for name, rate in weak_points:
            analysis += f"   • {name} ({rate * 100:.0f}%)\n"
        analysis += "\n"

        analysis += "💡 针对性巩固建议:\n"
        analysis += "   1. 优先复习排名靠前的薄弱知识点\n"
        analysis += "   2. 查看课程资料中对应的章节内容\n"
        analysis += "   3. 完成专项练习题进行强化\n"
        analysis += "   4. 标记错题，定期回顾\n"
        analysis += "   5. 组建学习小组，互相讨论\n\n"

    # 推荐学习资源
    analysis += "📖 推荐学习路径:\n"
    if weak_points:
        analysis += f"   第一步：重点攻克 {weak_points[0][0]}\n"
        if len(weak_points) > 1:
            analysis += f"   第二步：学习 {weak_points[1][0]}\n"
        if len(weak_points) > 2:
            analysis += f"   第三步：巩固 {weak_points[2][0]}\n"
    else:
        analysis += "   继续保持当前学习状态，可以尝试更高难度的作业！\n"

    return analysis


def generate_remediation_plan(learning_data, weak_knowledge_points=None):
    """生成薄弱知识点巩固计划"""
    if not learning_data:
        return "暂无学习数据，无法生成巩固计划。"

    user = learning_data['user']

    if not weak_knowledge_points:
        return "未识别到明显的薄弱知识点，请继续使用 @作业知识点分析 指令进行分析。"

    plan = f"🎯 个性化巩固学习计划\n\n"
    plan += f"👤 用户：{user.xingming}\n"
    plan += f"📚 薄弱知识点数量：{len(weak_knowledge_points)}个\n\n"

    plan += "📋 第一阶段 (第 1-2 周):\n"
    plan += "   重点突破最薄弱的 3 个知识点:\n"
    for i, kp in enumerate(weak_knowledge_points[:3], 1):
        plan += f"   {i}. {kp}\n"
        plan += f"      - 观看相关教学视频\n"
        plan += f"      - 阅读课程资料对应章节\n"
        plan += f"      - 完成 5-10 道基础练习题\n"
    plan += "\n"

    plan += "📋 第二阶段 (第 3-4 周):\n"
    plan += "   巩固提升阶段:\n"
    for i, kp in enumerate(weak_knowledge_points[3:6], 4):
        plan += f"   {i}. {kp}\n"
        plan += f"      - 系统复习相关知识体系\n"
        plan += f"      - 完成中等难度练习题\n"
        plan += f"      - 整理错题笔记\n"
    plan += "\n"

    plan += "📋 第三阶段 (第 5-6 周):\n"
    plan += "   综合提升与检测:\n"
    plan += "   - 完成综合性作业测试\n"
    plan += "   - 参加模拟考试\n"
    plan += "   - 查漏补缺，重点复习易错点\n"
    plan += "\n"

    plan += "💡 学习方法建议:\n"
    plan += "   1. 番茄工作法：专注学习 25 分钟，休息 5 分钟\n"
    plan += "   2. 费曼学习法：尝试向他人讲解知识点\n"
    plan += "   3. 间隔重复：定期回顾已学内容\n"
    plan += "   4. 主动回忆：合上书本，回忆关键概念\n"
    plan += "   5. 交叉学习：不同科目交替学习，避免疲劳\n"
    plan += "\n"

    plan += "🏆 预期目标:\n"
    plan += f"   - 薄弱知识点正确率提升至 70% 以上\n"
    plan += f"   - 整体作业平均分提高 10-15 分\n"
    plan += f"   - 建立完整的知识体系框架\n"

    return plan

#endregion