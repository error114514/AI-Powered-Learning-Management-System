# coding:utf-8
__author__ = "ila"
import bcrypt

from django.db import models

from .model import BaseModel


class users(BaseModel):
    # id=models.BigIntegerField(verbose_name="自增id")
    username = models.CharField(max_length=100, verbose_name=u'账号')
    password = models.CharField(max_length=255, verbose_name=u'密码')  # 增加长度以存储哈希值
    role = models.CharField(max_length=100, verbose_name=u'角色')
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    __tablename__ = 'users'

    class Meta:
        db_table = 'users'
        verbose_name = verbose_name_plural = u'管理员表'

    def set_password(self, raw_password):
        """设置密码，自动进行哈希"""
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, raw_password):
        """验证密码"""
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

    # def __str__(self):
    #     return self.username
