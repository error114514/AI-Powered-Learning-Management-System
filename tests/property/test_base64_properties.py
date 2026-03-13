# coding:utf-8
"""
Base64编码的属性测试
Property-based tests for Base64 encoding
Feature: facial-recognition-integration, Property 4: Base64 Image Encoding
"""
import unittest
import base64
import sys
import os
from hypothesis import given, settings, strategies as st

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestBase64Properties(unittest.TestCase):
    """Base64编码属性测试"""
    
    @settings(max_examples=100)
    @given(image_data=st.binary(min_size=100, max_size=10000))
    def test_base64_encoding_decoding_roundtrip(self, image_data):
        """
        属性4: Base64图片编码
        对于任何图片文件数据，系统应该成功将其转换为有效的Base64编码字符串，
        并且解码后应该得到原始数据
        
        Feature: facial-recognition-integration, Property 4: Base64 Image Encoding
        Validates: Requirements 1.5, 2.2, 4.1
        """
        # 编码为Base64
        base64_encoded = base64.b64encode(image_data).decode('utf-8')
        
        # 验证编码结果是非空字符串
        self.assertIsInstance(base64_encoded, str)
        self.assertGreater(len(base64_encoded), 0)
        
        # 验证可以解码回原始数据
        decoded_data = base64.b64decode(base64_encoded)
        self.assertEqual(decoded_data, image_data)
    
    @settings(max_examples=100)
    @given(image_data=st.binary(min_size=1, max_size=50000))
    def test_base64_encoding_produces_valid_string(self, image_data):
        """
        测试Base64编码总是产生有效的字符串
        对于任何二进制数据，Base64编码应该产生只包含有效Base64字符的字符串
        
        Feature: facial-recognition-integration, Property 4: Base64 Image Encoding
        Validates: Requirements 1.5, 2.2, 4.1
        """
        # 编码为Base64
        base64_encoded = base64.b64encode(image_data).decode('utf-8')
        
        # 验证只包含有效的Base64字符 (A-Z, a-z, 0-9, +, /, =)
        valid_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')
        for char in base64_encoded:
            self.assertIn(char, valid_chars, 
                         f"Invalid Base64 character found: {char}")
    
    @settings(max_examples=100)
    @given(image_data=st.binary(min_size=100, max_size=10000))
    def test_base64_encoding_is_deterministic(self, image_data):
        """
        测试Base64编码是确定性的
        对于相同的输入，多次编码应该产生相同的结果
        
        Feature: facial-recognition-integration, Property 4: Base64 Image Encoding
        Validates: Requirements 1.5, 2.2, 4.1
        """
        # 多次编码相同数据
        encoded1 = base64.b64encode(image_data).decode('utf-8')
        encoded2 = base64.b64encode(image_data).decode('utf-8')
        encoded3 = base64.b64encode(image_data).decode('utf-8')
        
        # 验证结果相同
        self.assertEqual(encoded1, encoded2)
        self.assertEqual(encoded2, encoded3)


if __name__ == '__main__':
    unittest.main()
