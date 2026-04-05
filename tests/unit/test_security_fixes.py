# coding:utf-8
# author:ila
import bcrypt
import jwt
import datetime
from django.test import TestCase
from main.users_model import users
from django.conf import settings

class SecurityFixesTest(TestCase):
    def setUp(self):
        """测试前准备"""
        self.test_password = "test123456"
        self.test_username = "testuser"

        # 创建测试用户
        self.user = users()
        self.user.username = self.test_username
        self.user.set_password(self.test_password)
        self.user.save()

        # 生成JWT token
        payload = {
            'tablename': 'users',
            'params': {'username': self.test_username},
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        self.test_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    def test_password_hashing(self):
        """测试密码哈希存储"""
        # 验证密码哈希存储
        self.assertNotEqual(self.user.password, self.test_password)

        # 验证密码验证
        self.assertTrue(self.user.check_password(self.test_password))
        self.assertFalse(self.user.check_password("wrongpassword"))

    def test_jwt_token_generation(self):
        """测试JWT token生成"""
        # 验证token格式
        self.assertIsInstance(self.test_token, str)

        # 验证token解码
        decoded = jwt.decode(self.test_token, settings.SECRET_KEY, algorithms=['HS256'])
        self.assertEqual(decoded['tablename'], 'users')
        self.assertEqual(decoded['params']['username'], self.test_username)

    def test_api_key_config(self):
        """测试API密钥配置"""
        # 验证API密钥配置
        self.assertTrue(hasattr(settings, 'BAIDU_FACE_API_KEY'))
        self.assertTrue(hasattr(settings, 'BAIDU_FACE_SECRET_KEY'))
        self.assertTrue(hasattr(settings, 'BAIDU_FACE_GROUP_ID'))

if __name__ == '__main__':
    unittest.main()