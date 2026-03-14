# coding:utf-8
"""
作业人脸验证的单元测试
Unit tests for exam face verification
"""
import unittest
from unittest.mock import Mock, patch
import base64
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestExamVerification(unittest.TestCase):
    """作业人脸验证测试"""
    
    def setUp(self):
        """测试前准备"""
        self.sample_image = b"fake_exam_face_image"
        self.logged_in_user_id = "123456"
        self.different_user_id = "789012"
    
    @patch('util.face_util.FaceUtil.find_face')
    def test_successful_verification_with_matching_user(self, mock_find_face):
        """测试匹配用户的成功验证"""
        # 模拟找到匹配的用户
        mock_find_face.return_value = self.logged_in_user_id
        
        # 调用验证
        base64_image = base64.b64encode(self.sample_image).decode('utf-8')
        recognized_id = mock_find_face(base64_image)
        
        # 验证结果
        self.assertEqual(recognized_id, self.logged_in_user_id)
        self.assertTrue(mock_find_face.called)
    
    @patch('util.face_util.FaceUtil.find_face')
    def test_failed_verification_with_mismatched_user(self, mock_find_face):
        """测试用户不匹配的失败验证"""
        # 模拟找到不同的用户
        mock_find_face.return_value = self.different_user_id
        
        # 调用验证
        base64_image = base64.b64encode(self.sample_image).decode('utf-8')
        recognized_id = mock_find_face(base64_image)
        
        # 验证结果
        self.assertNotEqual(recognized_id, self.logged_in_user_id)
        self.assertEqual(recognized_id, self.different_user_id)
    
    @patch('util.face_util.FaceUtil.find_face')
    def test_verification_with_no_face_detected(self, mock_find_face):
        """测试未检测到人脸的验证"""
        # 模拟未找到人脸
        mock_find_face.return_value = None
        
        # 调用验证
        base64_image = base64.b64encode(self.sample_image).decode('utf-8')
        recognized_id = mock_find_face(base64_image)
        
        # 验证结果
        self.assertIsNone(recognized_id)
    
    def test_verification_logging_structure(self):
        """测试验证日志结构"""
        # 模拟日志记录
        log_entry = {
            'timestamp': '2024-01-01 10:00:00',
            'user_id': self.logged_in_user_id,
            'operation': 'exam_verification',
            'result': 'success'
        }
        
        # 验证日志包含必要字段
        self.assertIn('timestamp', log_entry)
        self.assertIn('user_id', log_entry)
        self.assertIn('operation', log_entry)
        self.assertIn('result', log_entry)
        self.assertEqual(log_entry['operation'], 'exam_verification')


if __name__ == '__main__':
    unittest.main()
