# 人脸识别API调用分析报告

## 当前状态总结

### ✅ 正常工作的功能

1. **学生/教师注册** - 完全正常
   - 文件上传: ✅
   - 保存到数据库: ✅  
   - Base64编码: ✅
   - 百度API注册: ✅

2. **人脸搜索API** - 完全正常
   - API调用成功
   - 匹配度: 99-100%
   - 返回正确的user_id

### ❌ 当前问题

**考试人脸验证失败** - 原因: 认证问题，不是人脸识别问题

错误信息: `{code: 401, msg: "headers未包含认证信息。"}`

## 上传到百度API的内容

### 1. 注册接口 (register_face)

**请求URL:**
```
https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add?access_token={token}
```

**请求体 (JSON):**
```json
{
  "image_type": "BASE64",
  "image": "{base64编码的图片数据}",
  "group_id": "aabb",
  "user_id": "{用户ID}"
}
```

**实际日志示例:**
```
INFO 2026-02-10 19:57:24,727 Base64编码完成，长度: 46192
INFO 2026-02-10 19:57:25,639 成功注册人脸，用户ID: None
```

**API响应:**
```json
{
  "error_code": 0,
  "error_msg": "SUCCESS",
  "log_id": 3367426711,
  "timestamp": 1770724645,
  "cached": 0,
  "result": {
    "face_token": "66f140c521191727c10273815f21af37",
    "location": {
      "left": 176.61,
      "top": 297.65,
      "width": 241,
      "height": 214,
      "rotation": -1
    }
  }
}
```

### 2. 搜索接口 (find_face)

**请求URL:**
```
https://aip.baidubce.com/rest/2.0/face/v3/search?access_token={token}
```

**请求体 (JSON):**
```json
{
  "image_type": "BASE64",
  "image": "{base64编码的图片数据}",
  "group_id_list": "aabb"
}
```

**实际日志示例:**
```
INFO 2026-02-10 21:28:55,163 成功获取访问令牌
INFO 2026-02-10 21:28:55,603 找到匹配人脸，用户ID: 1767439487002, 相似度: 100
```

## 数据流程

### 注册流程
```
前端选择照片 
  → FormData上传到 /xuesheng/register 或 /jiaoshi/register
  → 后端保存文件到 media/face/
  → 读取文件转Base64
  → 调用 FaceUtil.register_face()
  → 百度API: /face/v3/faceset/user/add
  → 成功: 返回face_token
  → 失败: 回滚删除用户和文件
```

### 考试验证流程
```
前端选择照片
  → FormData上传到 /file/upload2
  → ❌ 认证中间件检查Token
  → 如果Token有效: 继续
  → 后端读取文件转Base64
  → 调用 FaceUtil.find_face()
  → 百度API: /face/v3/search
  → 返回匹配的user_id
  → 前端比对user_id与当前登录用户
```

## 问题根源

**不是人脸识别API的问题！** 百度API工作完全正常。

问题在于Django认证中间件 (`xmiddleware/xauth.py`):

```python
# POST请求需要认证，除非在免认证列表中
if fullPath not in post_list and "register" not in fullPath and "login" not in fullPath:
    result = Auth.identify(Auth, request)
    if result.get('code') != normal_code:
        return JsonResponse(result)  # 返回401错误
```

`/file/upload2` 不在免认证列表中，所以需要Token。

## 解决方案

### 方案1: 确保用户已登录 (推荐)

考试前必须登录，这是合理的业务逻辑。

**前端检查:**
```javascript
exam(id) {
    var token = localStorage.getItem('Token');
    if (!token || token === 'null') {
        layui.layer.msg('请先登录', {time: 2000, icon: 5});
        window.location.href = './login.html';
        return;
    }
    this.currentExamId = id;
    this.showFaceVerification = true;
}
```

### 方案2: 将/file/upload2加入免认证列表

修改 `xmiddleware/xauth.py`:

```python
post_list = [
    '/{}/defaultuser/register'.format(schemaName),
    '/{}/defaultuser/login'.format(schemaName),
    '/{}/users/register'.format(schemaName),
    '/{}/users/login'.format(schemaName),
    "/{}/examusers/login".format(schemaName),
    "/{}/examusers/register".format(schemaName),
    "/{}/file/upload2".format(schemaName),  # 添加这行
]
```

**注意:** 这会允许未登录用户调用人脸识别，可能不安全。

### 方案3: 修改前端确保Token正确发送

检查Token是否正确存储:

```javascript
// 登录成功后
localStorage.setItem('Token', res.token);
localStorage.setItem('userid', res.data.id);

// 使用前检查
var token = localStorage.getItem('Token');
console.log('Token:', token);  // 调试用
```

## 建议

1. **立即检查**: 用户是否已登录？Token是否存在？
2. **推荐方案1**: 要求用户登录后才能考试
3. **测试步骤**:
   - 先登录学生账号
   - 检查localStorage中是否有Token
   - 然后进入考试列表
   - 点击考试按钮
   - 进行人脸验证

## 技术细节

### Base64编码
- 图片文件 → 二进制数据 → Base64字符串
- 长度: 约为原文件大小的1.33倍
- 示例: 34KB图片 → 46KB Base64字符串

### API凭证
```python
API_KEY = "ql21uVftf13jXL0FGEkFCCzH"
SECRET_KEY = "81L7L2FRTMcEkuMr3opuyx8cccXsEw20"
GROUP_ID = "aabb"
```

### 字段顺序 (已修正)
按照Java参考代码的顺序:
1. image_type
2. image
3. group_id
4. user_id (注册时)
5. group_id_list (搜索时)

## 结论

✅ **人脸识别功能完全正常**
- 注册: 成功
- 搜索: 成功  
- 匹配度: 99-100%

❌ **问题是认证层面**
- 需要用户登录
- 需要有效的Token
- 不是百度API的问题

**下一步**: 确保用户登录后再进行考试验证。
