# coding:utf-8
"""
百度人脸识别API工具类
Baidu Face Recognition API Utility
"""
import requests
import base64
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)


class FaceUtil:
    """百度人脸识别API封装类"""
    
    # API配置
    API_KEY = "ql21uVftf13jXL0FGEkFCCzH"
    SECRET_KEY = "81L7L2FRTMcEkuMr3opuyx8cccXsEw20"
    GROUP_ID = "aabb"
    
    # API端点
    TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"
    REGISTER_URL = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"
    SEARCH_URL = "https://aip.baidubce.com/rest/2.0/face/v3/search"
    
    # 超时设置（秒）
    TIMEOUT = 10
    
    @staticmethod
    def get_access_token() -> str:
        """
        获取百度API访问令牌
        
        Returns:
            str: 访问令牌
            
        Raises:
            Exception: 当API调用失败时
        """
        try:
            params = {
                "grant_type": "client_credentials",
                "client_id": FaceUtil.API_KEY,
                "client_secret": FaceUtil.SECRET_KEY
            }
            
            response = requests.post(
                FaceUtil.TOKEN_URL,
                params=params,
                timeout=FaceUtil.TIMEOUT
            )
            response.raise_for_status()
            
            result = response.json()
            access_token = result.get("access_token")
            
            if not access_token:
                raise Exception("获取访问令牌失败：响应中没有access_token")
            
            logger.info("成功获取访问令牌")
            return access_token
            
        except requests.Timeout:
            logger.error("获取访问令牌超时")
            raise Exception("网络超时，请重试")
        except requests.RequestException as e:
            logger.error(f"获取访问令牌失败: {str(e)}")
            raise Exception("服务暂时不可用，请稍后重试")
        except Exception as e:
            logger.error(f"获取访问令牌异常: {str(e)}")
            raise

    
    @staticmethod
    def register_face(base64_image: str, user_id: str) -> Dict:
        """
        注册人脸到百度人脸库
        
        Args:
            base64_image: Base64编码的图片字符串
            user_id: 用户唯一标识
            
        Returns:
            dict: 百度API响应结果
            
        Raises:
            Exception: 当注册失败时
        """
        try:
            # 获取访问令牌
            access_token = FaceUtil.get_access_token()
            
            # 构建请求URL
            url = f"{FaceUtil.REGISTER_URL}?access_token={access_token}"
            
            # 构建请求体 - 字段顺序与Java参考代码一致
            payload = {
                "image_type": "BASE64",
                "image": base64_image,
                "group_id": FaceUtil.GROUP_ID,
                "user_id": str(user_id)
            }
            
            # 发送请求
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=FaceUtil.TIMEOUT
            )
            response.raise_for_status()
            
            result = response.json()
            
            # 检查API返回的错误码
            if result.get("error_code") != 0:
                error_msg = result.get("error_msg", "未知错误")
                logger.error(f"人脸注册失败: {error_msg}")
                raise Exception(f"人脸注册失败: {error_msg}")
            
            logger.info(f"成功注册人脸，用户ID: {user_id}")
            return result
            
        except requests.Timeout:
            logger.error("人脸注册超时")
            raise Exception("网络超时，请重试")
        except requests.RequestException as e:
            logger.error(f"人脸注册请求失败: {str(e)}")
            raise Exception("服务暂时不可用，请稍后重试")
        except Exception as e:
            logger.error(f"人脸注册异常: {str(e)}")
            raise
    
    @staticmethod
    def find_face(base64_image: str) -> Optional[str]:
        """
        在人脸库中搜索匹配的人脸
        
        Args:
            base64_image: Base64编码的图片字符串
            
        Returns:
            str: 匹配的用户ID，如果未找到则返回None
            
        Raises:
            Exception: 当搜索失败时
        """
        try:
            # 获取访问令牌
            access_token = FaceUtil.get_access_token()
            
            # 构建请求URL
            url = f"{FaceUtil.SEARCH_URL}?access_token={access_token}"
            
            # 构建请求体
            payload = {
                "image": base64_image,
                "image_type": "BASE64",
                "group_id_list": FaceUtil.GROUP_ID
            }
            
            # 发送请求
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=FaceUtil.TIMEOUT
            )
            response.raise_for_status()
            
            result = response.json()
            
            # 检查API返回的错误码
            error_code = result.get("error_code")
            if error_code == 222207:
                # 未找到匹配的人脸
                logger.info("未找到匹配的人脸")
                return None
            elif error_code != 0:
                error_msg = result.get("error_msg", "未知错误")
                logger.error(f"人脸搜索失败: {error_msg}")
                raise Exception(f"人脸搜索失败: {error_msg}")
            
            # 提取匹配的用户ID
            result_data = result.get("result")
            if result_data and "user_list" in result_data:
                user_list = result_data["user_list"]
                if user_list and len(user_list) > 0:
                    user_id = user_list[0].get("user_id")
                    score = user_list[0].get("score", 0)
                    logger.info(f"找到匹配人脸，用户ID: {user_id}, 相似度: {score}")
                    return user_id
            
            logger.info("未找到匹配的人脸")
            return None
            
        except requests.Timeout:
            logger.error("人脸搜索超时")
            raise Exception("网络超时，请重试")
        except requests.RequestException as e:
            logger.error(f"人脸搜索请求失败: {str(e)}")
            raise Exception("服务暂时不可用，请稍后重试")
        except Exception as e:
            logger.error(f"人脸搜索异常: {str(e)}")
            raise
