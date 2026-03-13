# coding:utf-8
"""
FaceUtil类的单元测试
Unit tests for FaceUtil class
"""
import unittest
from unittest.mock import patch, Mock
import base64
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from util.face_util import FaceUtil


class TestFaceUtil(unittest.TestCase):
    """FaceUtil工具类测试"""
    
    def setUp(self):
        """测试前准备"""
        self.sample_image = base64.b64encode(b"fake_image_data").decode('utf-8')
        self.sample_user_id = "test_user_123"
    
    @patch('util.face_util.requests.post')
    def test_get_access_token_success(self, mock_post):
        """测试成功获取访问令牌"""
        # 模拟成功响应
        mock_response = Mock()
        mock_response.json.return_value = {"access_token": "test_token_abc123"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        # 调用方法
        token = FaceUtil.get_access_token()
        
        # 验证结果
        self.assertEqual(token, "test_token_abc123")
        self.assertTrue(mock_post.called)
        
    @patch('util.face_util.requests.post')
    def test_get_access_token_no_token_in_response(self, mock_post):
        """测试响应中没有访问令牌"""
        # 模拟响应中没有access_token
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        # 验证抛出异常
        with self.assertRaises(Exception) as context:
            FaceUtil.get_access_token()
        
        self.assertIn("access_token", str(context.exception))
    
    @patch('util.face_util.requests.post')
    def test_get_access_token_timeout(self, mock_post):
        """测试获取令牌超时"""
        # 模拟超时
        mock_post.side_effect = Exception("网络超时，请重试")
        
        # 验证抛出异常
        with self.assertRaises(Exception) as context:
            FaceUtil.get_access_token()
        
        self.assertIn("超时", str(context.exception))

    
    @patch('util.face_util.FaceUtil.get_access_token')
    @patch('util.face_util.requests.post')
    def test_register_face_success(self, mock_post, mock_get_token):
        """测试成功注册人脸"""
        # 模拟获取令牌
        mock_get_token.return_value = "test_token"
        
        # 模拟成功响应
        mock_response = Mock()
        mock_response.json.return_value = {
            "error_code": 0,
            "error_msg": "SUCCESS"
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        # 调用方法
        result = FaceUtil.register_face(self.sample_image, self.sample_user_id)
        
        # 验证结果
        self.assertEqual(result["error_code"], 0)
        self.assertTrue(mock_post.called)
        
        # 验证请求参数
        call_args = mock_post.call_args
        json_data = call_args[1]['json']
        self.assertEqual(json_data['user_id'], self.sample_user_id)
        self.assertEqual(json_data['group_id'], FaceUtil.GROUP_ID)
        self.assertEqual(json_data['image_type'], "BASE64")
    
    @patch('util.face_util.FaceUtil.get_access_token')
    @patch('util.face_util.requests.post')
    def test_register_face_api_error(self, mock_post, mock_get_token):
        """测试人脸注册API返回错误"""
        # 模拟获取令牌
        mock_get_token.return_value = "test_token"
        
        # 模拟错误响应
        mock_response = Mock()
        mock_response.json.return_value = {
            "error_code": 222202,
            "error_msg": "pic not has face"
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        # 验证抛出异常
        with self.assertRaises(Exception) as context:
            FaceUtil.register_face(self.sample_image, self.sample_user_id)
        
        self.assertIn("人脸注册失败", str(context.exception))
    
    @patch('util.face_util.FaceUtil.get_access_token')
    @patch('util.face_util.requests.post')
    def test_find_face_success(self, mock_post, mock_get_token):
        """测试成功搜索人脸"""
        # 模拟获取令牌
        mock_get_token.return_value = "test_token"
        
        # 模拟成功响应
        mock_response = Mock()
        mock_response.json.return_value = {
            "error_code": 0,
            "error_msg": "SUCCESS",
            "result": {
                "user_list": [
                    {
                        "user_id": self.sample_user_id,
                        "score": 95.5
                    }
                ]
            }
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        # 调用方法
        user_id = FaceUtil.find_face(self.sample_image)
        
        # 验证结果
        self.assertEqual(user_id, self.sample_user_id)
        self.assertTrue(mock_post.called)
    
    @patch('util.face_util.FaceUtil.get_access_token')
    @patch('util.face_util.requests.post')
    def test_find_face_not_found(self, mock_post, mock_get_token):
        """测试未找到匹配人脸"""
        # 模拟获取令牌
        mock_get_token.return_value = "test_token"
        
        # 模拟未找到响应
        mock_response = Mock()
        mock_response.json.return_value = {
            "error_code": 222207,
            "error_msg": "user not found"
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        # 调用方法
        user_id = FaceUtil.find_face(self.sample_image)
        
        # 验证结果
        self.assertIsNone(user_id)
    
    @patch('util.face_util.FaceUtil.get_access_token')
    @patch('util.face_util.requests.post')
    def test_find_face_api_error(self, mock_post, mock_get_token):
        """测试人脸搜索API返回错误"""
        # 模拟获取令牌
        mock_get_token.return_value = "test_token"
        
        # 模拟错误响应
        mock_response = Mock()
        mock_response.json.return_value = {
            "error_code": 222202,
            "error_msg": "pic not has face"
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        # 验证抛出异常
        with self.assertRaises(Exception) as context:
            FaceUtil.find_face(self.sample_image)
        
        self.assertIn("人脸搜索失败", str(context.exception))


if __name__ == '__main__':
    unittest.main()
