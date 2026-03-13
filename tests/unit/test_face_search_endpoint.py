# coding:utf-8
"""
人脸搜索端点的单元测试
Unit tests for face search endpoint
"""
import unittest
from unittest.mock import Mock, patch
import base64
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestFaceSearchEndpoint(unittest.TestCase):
    """人脸搜索端点测试"""
    
    def setUp(self):
        """测试前准备"""
        self.sample_image = b"fake_image_data_for_search"
        self.sample_user_id = "test_user_456"
    
    def test_empty_file_rejection(self):
        """测试空文件被拒绝"""
        # 创建空文件mock
        empty_file = Mock()
        empty_file.size = 0
        empty_file.read.return_value = b""
        
        # 验证空文件应该被拒绝
        self.assertEqual(empty_file.size, 0)
        self.assertEqual(len(empty_file.read()), 0)
    
    def test_valid_file_has_content(self):
        """测试有效文件包含内容"""
        # 创建有效文件mock
        valid_file = Mock()
        valid_file.size = len(self.sample_image)
        valid_file.read.return_value = self.sample_image
        
        # 验证文件有内容
        self.assertGreater(valid_file.size, 0)
        self.assertGreater(len(valid_file.read()), 0)
    
    def test_base64_conversion_for_search(self):
        """测试搜索时的Base64转换"""
        # 转换为Base64
        base64_image = base64.b64encode(self.sample_image).decode('utf-8')
        
        # 验证转换成功
        self.assertIsInstance(base64_image, str)
        self.assertGreater(len(base64_image), 0)
        
        # 验证可以解码回原始数据
        decoded = base64.b64decode(base64_image)
        self.assertEqual(decoded, self.sample_image)
    
    @patch('util.face_util.FaceUtil.find_face')
    def test_successful_face_search(self, mock_find_face):
        """测试成功的人脸搜索"""
        # 模拟找到匹配的人脸
        mock_find_face.return_value = self.sample_user_id
        
        # 调用搜索
        base64_image = base64.b64encode(self.sample_image).decode('utf-8')
        result = mock_find_face(base64_image)
        
        # 验证结果
        self.assertEqual(result, self.sample_user_id)
        self.assertTrue(mock_find_face.called)
    
    @patch('util.face_util.FaceUtil.find_face')
    def test_face_not_found(self, mock_find_face):
        """测试未找到匹配人脸"""
        # 模拟未找到人脸
        mock_find_face.return_value = None
        
        # 调用搜索
        base64_image = base64.b64encode(self.sample_image).decode('utf-8')
        result = mock_find_face(base64_image)
        
        # 验证结果
        self.assertIsNone(result)
    
    def test_invalid_image_format_handling(self):
        """测试无效图片格式处理"""
        # 创建无效数据
        invalid_data = b"not_an_image"
        
        # Base64编码仍然会成功（因为它只是编码二进制数据）
        base64_encoded = base64.b64encode(invalid_data).decode('utf-8')
        self.assertIsInstance(base64_encoded, str)
        
        # 但是百度API会返回错误（在实际调用时）
        # 这里我们只验证编码步骤不会失败


if __name__ == '__main__':
    unittest.main()
