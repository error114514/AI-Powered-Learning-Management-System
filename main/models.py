#coding:utf-8
__author__ = "ila"
from django.db import models

from .model import BaseModel

from datetime import datetime



class jiaoshi(BaseModel):
    __doc__ = u'''jiaoshi'''
    __tablename__ = 'jiaoshi'

    __loginUser__='gonghao'


    __authTables__={}
    __authPeople__='是'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __loginUserColumn__='gonghao'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    gonghao=models.CharField ( max_length=255,null=False,unique=True,verbose_name='工号' )
    mima=models.CharField ( max_length=255,null=False, unique=False,verbose_name='密码' )
    xingming=models.CharField ( max_length=255,null=False, unique=False,verbose_name='姓名' )
    xingbie=models.CharField ( max_length=255, null=True, unique=False,verbose_name='性别' )
    banji=models.CharField ( max_length=255, null=True, unique=False,verbose_name='班级' )
    shouji=models.CharField ( max_length=255, null=True, unique=False,verbose_name='手机' )
    youxiang=models.CharField ( max_length=255, null=True, unique=False,verbose_name='邮箱' )
    zhaopian=models.CharField ( max_length=255, null=True, unique=False,verbose_name='照片' )
    money=models.FloatField   (  null=True, unique=False,verbose_name='余额' )
    '''
    gonghao=VARCHAR
    mima=VARCHAR
    xingming=VARCHAR
    xingbie=VARCHAR
    banji=VARCHAR
    shouji=VARCHAR
    youxiang=VARCHAR
    zhaopian=VARCHAR
    money=Float
    '''
    class Meta:
        db_table = 'jiaoshi'
        verbose_name = verbose_name_plural = '教师'
class xuesheng(BaseModel):
    __doc__ = u'''xuesheng'''
    __tablename__ = 'xuesheng'

    __loginUser__='xuehao'


    __authTables__={}
    __authPeople__='是'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __loginUserColumn__='xuehao'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    xuehao=models.CharField ( max_length=255,null=False,unique=True,verbose_name='学号' )
    mima=models.CharField ( max_length=255,null=False, unique=False,verbose_name='密码' )
    xingming=models.CharField ( max_length=255,null=False, unique=False,verbose_name='姓名' )
    xingbie=models.CharField ( max_length=255, null=True, unique=False,verbose_name='性别' )
    banji=models.CharField ( max_length=255, null=True, unique=False,verbose_name='班级' )
    shouji=models.CharField ( max_length=255, null=True, unique=False,verbose_name='手机' )
    youxiang=models.CharField ( max_length=255, null=True, unique=False,verbose_name='邮箱' )
    zhaopian=models.CharField ( max_length=255, null=True, unique=False,verbose_name='照片' )
    money=models.FloatField   (  null=True, unique=False,verbose_name='余额' )
    '''
    xuehao=VARCHAR
    mima=VARCHAR
    xingming=VARCHAR
    xingbie=VARCHAR
    banji=VARCHAR
    shouji=VARCHAR
    youxiang=VARCHAR
    zhaopian=VARCHAR
    money=Float
    '''
    class Meta:
        db_table = 'xuesheng'
        verbose_name = verbose_name_plural = '学生'
class xuexitiandi(BaseModel):
    __doc__ = u'''xuexitiandi'''
    __tablename__ = 'xuexitiandi'



    __authTables__={}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='是'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='是'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    biaoti=models.CharField ( max_length=255, null=True, unique=False,verbose_name='标题' )
    fengmian=models.CharField ( max_length=255, null=True, unique=False,verbose_name='封面' )
    zhishiyaodian=models.CharField ( max_length=255, null=True, unique=False,verbose_name='知识要点' )
    xuexishipin=models.CharField ( max_length=255, null=True, unique=False,verbose_name='学习视频' )
    thumbsupnum=models.IntegerField  (  null=True, unique=False,verbose_name='赞' )
    crazilynum=models.IntegerField  (  null=True, unique=False,verbose_name='踩' )
    '''
    biaoti=VARCHAR
    fengmian=VARCHAR
    zhishiyaodian=VARCHAR
    xuexishipin=VARCHAR
    thumbsupnum=Integer
    crazilynum=Integer
    '''
    class Meta:
        db_table = 'xuexitiandi'
        verbose_name = verbose_name_plural = '课程管理'
class xuexiziliao(BaseModel):
    __doc__ = u'''xuexiziliao'''
    __tablename__ = 'xuexiziliao'



    __authTables__={}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='是'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='是'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    ziliaomingcheng=models.CharField ( max_length=255, null=True, unique=False,verbose_name='资料名称' )
    fengmian=models.CharField ( max_length=255, null=True, unique=False,verbose_name='封面' )
    xiangqing=models.TextField   (  null=True, unique=False,verbose_name='详情' )
    thumbsupnum=models.IntegerField  (  null=True, unique=False,verbose_name='赞' )
    crazilynum=models.IntegerField  (  null=True, unique=False,verbose_name='踩' )
    wenjian=models.CharField ( max_length=255, null=True, unique=False,verbose_name='文件' )
    '''
    ziliaomingcheng=VARCHAR
    fengmian=VARCHAR
    xiangqing=Text
    thumbsupnum=Integer
    crazilynum=Integer
    wenjian=VARCHAR
    '''
    class Meta:
        db_table = 'xuexiziliao'
        verbose_name = verbose_name_plural = '学习资料'
class shishengjiaoliu(BaseModel):
    __doc__ = u'''shishengjiaoliu'''
    __tablename__ = 'shishengjiaoliu'



    __authTables__={'xuehao':'xuesheng',}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='是'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    xuehao=models.CharField ( max_length=255, null=True, unique=False,verbose_name='学号' )
    xingming=models.CharField ( max_length=255, null=True, unique=False,verbose_name='姓名' )
    tiwen=models.TextField   (  null=True, unique=False,verbose_name='提问' )
    shijian=models.DateTimeField  (  null=True, unique=False,verbose_name='时间' )
    sfsh=models.CharField ( max_length=255, null=True, unique=False,verbose_name='是否审核' )
    shhf=models.TextField   (  null=True, unique=False,verbose_name='审核回复' )
    '''
    xuehao=VARCHAR
    xingming=VARCHAR
    tiwen=Text
    shijian=DateTime
    sfsh=VARCHAR
    shhf=Text
    '''
    class Meta:
        db_table = 'shishengjiaoliu'
        verbose_name = verbose_name_plural = '师生交流'
class forum(BaseModel):
    __doc__ = u'''forum'''
    __tablename__ = 'forum'



    __authTables__={}
    __foreEndListAuth__='是'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    title=models.CharField ( max_length=255, null=True, unique=False,verbose_name='帖子标题' )
    content=models.TextField   ( null=False, unique=False,verbose_name='帖子内容' )
    parentid=models.BigIntegerField  (  null=True, unique=False,verbose_name='父节点id' )
    userid=models.BigIntegerField  ( null=False, unique=False,verbose_name='用户id' )
    username=models.CharField ( max_length=255, null=True, unique=False,verbose_name='用户名' )
    isdone=models.CharField ( max_length=255, null=True, unique=False,verbose_name='状态' )
    '''
    title=VARCHAR
    content=Text
    parentid=BigInteger
    userid=BigInteger
    username=VARCHAR
    isdone=VARCHAR
    '''
    class Meta:
        db_table = 'forum'
        verbose_name = verbose_name_plural = '互动交流'
class cart(BaseModel):
    __doc__ = u'''cart'''
    __tablename__ = 'cart'



    __authTables__={}
    __authSeparate__='是'#后台列表权限
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    tablename=models.CharField ( max_length=255, null=True, unique=False,verbose_name='商品表名' )
    userid=models.BigIntegerField  ( null=False, unique=False,verbose_name='用户id' )
    goodid=models.BigIntegerField  ( null=False, unique=False,verbose_name='商品id' )
    goodname=models.CharField ( max_length=255, null=True, unique=False,verbose_name='商品名称' )
    picture=models.CharField ( max_length=255, null=True, unique=False,verbose_name='图片' )
    buynumber=models.IntegerField  ( null=False, unique=False,verbose_name='购买数量' )
    price=models.FloatField   (  null=True, unique=False,verbose_name='单价' )
    discountprice=models.FloatField   (  null=True, unique=False,verbose_name='会员价' )
    '''
    tablename=VARCHAR
    userid=BigInteger
    goodid=BigInteger
    goodname=VARCHAR
    picture=VARCHAR
    buynumber=Integer
    price=Float
    discountprice=Float
    '''
    class Meta:
        db_table = 'cart'
        verbose_name = verbose_name_plural = '购物车表'
class orders(BaseModel):
    __doc__ = u'''orders'''
    __tablename__ = 'orders'



    __authTables__={}
    __authSeparate__='是'#后台列表权限
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    orderid=models.CharField ( max_length=255,null=False,unique=True,verbose_name='订单编号' )
    tablename=models.CharField ( max_length=255, null=True, unique=False,verbose_name='商品表名' )
    userid=models.BigIntegerField  ( null=False, unique=False,verbose_name='用户id' )
    goodid=models.BigIntegerField  ( null=False, unique=False,verbose_name='商品id' )
    goodname=models.CharField ( max_length=255, null=True, unique=False,verbose_name='商品名称' )
    picture=models.CharField ( max_length=255, null=True, unique=False,verbose_name='商品图片' )
    buynumber=models.IntegerField  ( null=False, unique=False,verbose_name='购买数量' )
    price=models.FloatField   ( null=False, unique=False,verbose_name='价格/积分' )
    discountprice=models.FloatField   (  null=True, unique=False,verbose_name='折扣价格' )
    total=models.FloatField   ( null=False, unique=False,verbose_name='总价格/总积分' )
    discounttotal=models.FloatField   (  null=True, unique=False,verbose_name='折扣总价格' )
    type=models.IntegerField  (  null=True, unique=False,verbose_name='支付类型' )
    status=models.CharField ( max_length=255, null=True, unique=False,verbose_name='状态' )
    address=models.CharField ( max_length=255, null=True, unique=False,verbose_name='地址' )
    '''
    orderid=VARCHAR
    tablename=VARCHAR
    userid=BigInteger
    goodid=BigInteger
    goodname=VARCHAR
    picture=VARCHAR
    buynumber=Integer
    price=Float
    discountprice=Float
    total=Float
    discounttotal=Float
    type=Integer
    status=VARCHAR
    address=VARCHAR
    '''
    class Meta:
        db_table = 'orders'
        verbose_name = verbose_name_plural = '订单'
class address(BaseModel):
    __doc__ = u'''address'''
    __tablename__ = 'address'



    __authTables__={}
    __authSeparate__='是'#后台列表权限
    __foreEndListAuth__='是'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    userid=models.BigIntegerField  ( null=False, unique=False,verbose_name='用户id' )
    address=models.CharField ( max_length=255,null=False, unique=False,verbose_name='地址' )
    name=models.CharField ( max_length=255,null=False, unique=False,verbose_name='收货人' )
    phone=models.CharField ( max_length=255,null=False, unique=False,verbose_name='电话' )
    isdefault=models.CharField ( max_length=255,null=False, unique=False,verbose_name='是否默认地址[是/否]' )
    '''
    userid=BigInteger
    address=VARCHAR
    name=VARCHAR
    phone=VARCHAR
    isdefault=VARCHAR
    '''
    class Meta:
        db_table = 'address'
        verbose_name = verbose_name_plural = '地址'
class exampaper(BaseModel):
    __doc__ = u'''exampaper'''
    __tablename__ = 'exampaper'



    __authTables__={}
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    name=models.CharField ( max_length=255,null=False, unique=False,verbose_name='试卷名称' )
    time=models.IntegerField  ( null=False, unique=False,verbose_name='考试时长(分钟)' )
    status=models.IntegerField  ( null=False, unique=False,verbose_name='试卷状态' )
    '''
    name=VARCHAR
    time=Integer
    status=Integer
    '''
    class Meta:
        db_table = 'exampaper'
        verbose_name = verbose_name_plural = '试卷表'
class examquestion(BaseModel):
    __doc__ = u'''examquestion'''
    __tablename__ = 'examquestion'



    __authTables__={}
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    paperid=models.BigIntegerField  ( null=False, unique=False,verbose_name='所属试卷id（外键）' )
    papername=models.CharField ( max_length=255,null=False, unique=False,verbose_name='试卷名称' )
    questionname=models.CharField ( max_length=255,null=False, unique=False,verbose_name='试题名称' )
    options=models.TextField   (  null=True, unique=False,verbose_name='选项，json字符串' )
    score=models.BigIntegerField  (  null=True, unique=False,verbose_name='分值' )
    answer=models.CharField ( max_length=255, null=True, unique=False,verbose_name='正确答案' )
    analysis=models.TextField   (  null=True, unique=False,verbose_name='答案解析' )
    type=models.BigIntegerField  (  null=True, unique=False,verbose_name='试题类型，0：单选题 1：多选题 2：判断题 3：填空题（暂不考虑多项填空）' )
    sequence=models.BigIntegerField  (  null=True, unique=False,verbose_name='试题排序，值越大排越前面' )
    '''
    paperid=BigInteger
    papername=VARCHAR
    questionname=VARCHAR
    options=Text
    score=BigInteger
    answer=VARCHAR
    analysis=Text
    type=BigInteger
    sequence=BigInteger
    '''
    class Meta:
        db_table = 'examquestion'
        verbose_name = verbose_name_plural = '试题表'
class examrecord(BaseModel):
    __doc__ = u'''examrecord'''
    __tablename__ = 'examrecord'



    __authTables__={}
    __authSeparate__='是'#后台列表权限
    __foreEndListAuth__='是'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __examinationPaper__='是'#[examinationPaper:是/否]后台生成普通试卷功能
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    userid=models.BigIntegerField  ( null=False, unique=False,verbose_name='用户id' )
    username=models.CharField ( max_length=255, null=True, unique=False,verbose_name='用户名' )
    paperid=models.BigIntegerField  ( null=False, unique=False,verbose_name='试卷id（外键）' )
    papername=models.CharField ( max_length=255,null=False, unique=False,verbose_name='试卷名称' )
    questionid=models.BigIntegerField  ( null=False, unique=False,verbose_name='试题id（外键）' )
    questionname=models.CharField ( max_length=255,null=False, unique=False,verbose_name='试题名称' )
    options=models.TextField   (  null=True, unique=False,verbose_name='选项，json字符串' )
    score=models.BigIntegerField  (  null=True, unique=False,verbose_name='分值' )
    answer=models.CharField ( max_length=255, null=True, unique=False,verbose_name='正确答案' )
    analysis=models.TextField   (  null=True, unique=False,verbose_name='答案解析' )
    myscore=models.BigIntegerField  ( null=False, unique=False,verbose_name='试题得分' )
    myanswer=models.CharField ( max_length=255, null=True, unique=False,verbose_name='考生答案' )
    '''
    userid=BigInteger
    username=VARCHAR
    paperid=BigInteger
    papername=VARCHAR
    questionid=BigInteger
    questionname=VARCHAR
    options=Text
    score=BigInteger
    answer=VARCHAR
    analysis=Text
    myscore=BigInteger
    myanswer=VARCHAR
    '''
    class Meta:
        db_table = 'examrecord'
        verbose_name = verbose_name_plural = '考试记录表'
class storeup(BaseModel):
    __doc__ = u'''storeup'''
    __tablename__ = 'storeup'



    __authTables__={}
    __authSeparate__='是'#后台列表权限
    __foreEndListAuth__='是'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    userid=models.BigIntegerField  ( null=False, unique=False,verbose_name='用户id' )
    refid=models.BigIntegerField  (  null=True, unique=False,verbose_name='收藏id' )
    tablename=models.CharField ( max_length=255, null=True, unique=False,verbose_name='表名' )
    name=models.CharField ( max_length=255,null=False, unique=False,verbose_name='收藏名称' )
    picture=models.CharField ( max_length=255,null=False, unique=False,verbose_name='收藏图片' )
    '''
    userid=BigInteger
    refid=BigInteger
    tablename=VARCHAR
    name=VARCHAR
    picture=VARCHAR
    '''
    class Meta:
        db_table = 'storeup'
        verbose_name = verbose_name_plural = '收藏表'
class news(BaseModel):
    __doc__ = u'''news'''
    __tablename__ = 'news'



    __authTables__={}
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    title=models.CharField ( max_length=255,null=False, unique=False,verbose_name='标题' )
    introduction=models.TextField   (  null=True, unique=False,verbose_name='简介' )
    picture=models.CharField ( max_length=255,null=False, unique=False,verbose_name='图片' )
    content=models.TextField   ( null=False, unique=False,verbose_name='内容' )
    '''
    title=VARCHAR
    introduction=Text
    picture=VARCHAR
    content=Text
    '''
    class Meta:
        db_table = 'news'
        verbose_name = verbose_name_plural = '网站公告'
class discussxuexitiandi(BaseModel):
    __doc__ = u'''discussxuexitiandi'''
    __tablename__ = 'discussxuexitiandi'



    __authTables__={}
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    refid=models.BigIntegerField  ( null=False, unique=False,verbose_name='关联表id' )
    userid=models.BigIntegerField  ( null=False, unique=False,verbose_name='用户id' )
    content=models.TextField   ( null=False, unique=False,verbose_name='评论内容' )
    reply=models.TextField   (  null=True, unique=False,verbose_name='回复内容' )
    '''
    refid=BigInteger
    userid=BigInteger
    content=Text
    reply=Text
    '''
    class Meta:
        db_table = 'discussxuexitiandi'
        verbose_name = verbose_name_plural = '课程管理评论表'
class discussxuexiziliao(BaseModel):
    __doc__ = u'''discussxuexiziliao'''
    __tablename__ = 'discussxuexiziliao'



    __authTables__={}
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    refid=models.BigIntegerField  ( null=False, unique=False,verbose_name='关联表id' )
    userid=models.BigIntegerField  ( null=False, unique=False,verbose_name='用户id' )
    content=models.TextField   ( null=False, unique=False,verbose_name='评论内容' )
    reply=models.TextField   (  null=True, unique=False,verbose_name='回复内容' )
    '''
    refid=BigInteger
    userid=BigInteger
    content=Text
    reply=Text
    '''
    class Meta:
        db_table = 'discussxuexiziliao'
        verbose_name = verbose_name_plural = '学习资料评论表'
