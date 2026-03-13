import json
import requests
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import re

# DeepSeek API 配置
DEEPSEEK_API_KEY = 'sk-110104bc985447b0b511543ae724a430'
DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'


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
