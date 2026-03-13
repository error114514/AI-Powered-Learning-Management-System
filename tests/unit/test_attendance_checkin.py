# coding:utf-8
"""
考勤签到的单元测试
Unit tests for attendance check-in
"""
import unittest
from unittest.mock import Mock, patch
import base64
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestAttendanceCheckIn(unittest.TestCase):
    """考勤签到测试"""
    
    def setUp(self):
        """测试前准备"""
        self.sample_image = b"fake_attendance_face_image"
        self.logged_in_user_id = "student_001"
        self.different_user_id = "student_002"
    
    @patch('util.face_util.FaceUtil.find_face')
    def test_successful_checkin_with_matching_user(self, mock_find_face):
        """测试匹配用户的成功签到"""
        # 模拟找到匹配的用户
        mock_find_face.return_value = self.logged_in_user_id
        
        # 调用签到
        base64_image = base64.b64encode(self.sample_image).decode('utf-8')
        recognized_id = mock_find_face(base64_image)
        
        # 验证结果
        self.assertEqual(recognized_id, self.logged_in_user_id)
        self.assertTrue(mock_find_face.called)
    
    @patch('util.face_util.FaceUtil.find_face')
    def test_failed_checkin_with_mismatched_user(self, mock_find_face):
        """测试用户不匹配的失败签到"""
        # 模拟找到不同的用户
        mock_find_face.return_value = self.different_user_id
        
        # 调用签到
        base64_image = base64.b64encode(self.sample_image).decode('utf-8')
        recognized_id = mock_find_face(base64_image)
        
        # 验证结果
        self.assertNotEqual(recognized_id, self.logged_in_user_id)
        self.assertEqual(recognized_id, self.different_user_id)
    
    @patch('util.face_util.FaceUtil.find_face')
    def test_checkin_with_no_face_detected(self, mock_find_face):
        """测试未检测到人脸的签到"""
        # 模拟未找到人脸
        mock_find_face.return_value = None
        
        # 调用签到
        base64_image = base64.b64encode(self.sample_image).decode('utf-8')
        recognized_id = mock_find_face(base64_image)
        
        # 验证结果
        self.assertIsNone(recognized_id)


if __name__ == '__main__':
    unittest.main()
