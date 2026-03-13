/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80036
 Source Host           : localhost:3306
 Source Schema         : dj_intellrnmgmtsystem

 Target Server Type    : MySQL
 Target Server Version : 80036
 File Encoding         : 65001

 Date: 11/02/2026 09:53:03
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for address
-- ----------------------------
DROP TABLE IF EXISTS `address`;
CREATE TABLE `address`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `addtime` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `userid` bigint(0) NOT NULL COMMENT '用户id',
  `address` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '地址',8997
  `name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '收货人',
  `phone` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '电话',
  `isdefault` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '是否默认地址[是/否]',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1613791426242 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '地址' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of address
-- ----------------------------
INSERT INTO `address` VALUES (1, '2025-12-15 11:01:36', 1, '北京市海淀区中关村南大街5号（北京大学）', '李某', '13823888881', '是');
INSERT INTO `address` VALUES (2, '2025-12-15 11:01:36', 2, '上海市杨浦区邯郸路220号（复旦大学）', '张某', '13823888882', '是');
INSERT INTO `address` VALUES (3, '2025-12-15 11:01:36', 3, '广东省广州市天河区五山路381号（华南理工大学）', '王某', '13823888883', '是');
INSERT INTO `address` VALUES (4, '2025-12-15 11:01:36', 4, '江苏省南京市栖霞区仙林大道163号（南京大学）', '刘某', '13823888884', '是');
INSERT INTO `address` VALUES (5, '2025-12-15 11:01:36', 5, '浙江省杭州市西湖区余杭塘路866号（浙江大学）', '赵某', '13823888885', '是');
INSERT INTO `address` VALUES (6, '2025-12-15 11:01:36', 6, '湖北省武汉市洪山区珞喻路1037号（华中科技大学）', '陈某', '13823888886', '是');
INSERT INTO `address` VALUES (1613791426241, '2025-12-15 11:23:46', 1613791194016, '广东省广州市天河区中山大道西55号（华南师范大学）', '张三', '11100000000', '是');

-- ----------------------------
-- Table structure for cart
-- ----------------------------
DROP TABLE IF EXISTS `cart`;
CREATE TABLE `cart`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `addtime` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `tablename` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT 'xuexiziliao' COMMENT '商品表名',
  `userid` bigint(0) NOT NULL COMMENT '用户id',
  `goodid` bigint(0) NOT NULL COMMENT '商品id',
  `goodname` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '商品名称',
  `picture` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '图片',
  `buynumber` int(0) NOT NULL COMMENT '购买数量',
  `price` float NULL DEFAULT NULL COMMENT '单价',
  `discountprice` float NULL DEFAULT NULL COMMENT '会员价',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1613791522891 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '购物车表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of cart
-- ----------------------------

-- ----------------------------
-- Table structure for config
-- ----------------------------
DROP TABLE IF EXISTS `config`;
CREATE TABLE `config`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '配置参数名称',
  `value` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '配置参数值',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '配置文件' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of config
-- ----------------------------
INSERT INTO `config` VALUES (1, '智能化学习管理系统侧视图', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/picture1.jpg');
INSERT INTO `config` VALUES (2, '智能化学习管理系统轮播图2', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/picture2.jpg');
INSERT INTO `config` VALUES (3, '智能化学习管理系统轮播图3', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/picture3.jpg');
INSERT INTO `config` VALUES (6, '智能化学习管理系统首页配置', NULL);

-- ----------------------------
-- Table structure for discussxuexitiandi
-- ----------------------------
DROP TABLE IF EXISTS `discussxuexitiandi`;
CREATE TABLE `discussxuexitiandi`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `addtime` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `refid` bigint(0) NOT NULL COMMENT '关联表id',
  `userid` bigint(0) NOT NULL COMMENT '用户id',
  `content` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '评论内容',
  `reply` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '回复内容',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 158 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '学习天地评论表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of discussxuexitiandi
-- ----------------------------
INSERT INTO `discussxuexitiandi` VALUES (151, '2025-12-15 11:01:36', 1, 1, '关于高校课程《1》的学习疑问：1章节法条理解不清', '回复：高校课程《1》的该知识点核心是课程要点，需结合案例记忆');
INSERT INTO `discussxuexitiandi` VALUES (152, '2025-12-15 11:01:36', 2, 2, '关于高校课程《2》的学习疑问：2章节法条理解不清', '回复：高校课程《2》的该知识点核心是课程要点，需结合案例记忆');
INSERT INTO `discussxuexitiandi` VALUES (153, '2025-12-15 11:01:36', 3, 3, '关于高校课程《3》的学习疑问：3章节法条理解不清', '回复：高校课程《3》的该知识点核心是课程要点，需结合案例记忆');
INSERT INTO `discussxuexitiandi` VALUES (154, '2025-12-15 11:01:36', 4, 4, '关于高校课程《4》的学习疑问：4章节法条理解不清', '回复：高校课程《4》的该知识点核心是课程要点，需结合案例记忆');
INSERT INTO `discussxuexitiandi` VALUES (155, '2025-12-15 11:01:36', 5, 5, '关于高校课程《5》的学习疑问：5章节法条理解不清', '回复：高校课程《5》的该知识点核心是课程要点，需结合案例记忆');
INSERT INTO `discussxuexitiandi` VALUES (156, '2025-12-15 11:01:36', 6, 6, '关于高校课程《6》的学习疑问：6章节法条理解不清', '回复：高校课程《6》的该知识点核心是课程要点，需结合案例记忆');
INSERT INTO `discussxuexitiandi` VALUES (157, '2026-01-13 17:27:03', 31, 1613791194016, '关于高校课程《31》的学习疑问：31章节法条理解不清', NULL);

-- ----------------------------
-- Table structure for discussxuexiziliao
-- ----------------------------
DROP TABLE IF EXISTS `discussxuexiziliao`;
CREATE TABLE `discussxuexiziliao`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `addtime` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `refid` bigint(0) NOT NULL COMMENT '关联表id',
  `userid` bigint(0) NOT NULL COMMENT '用户id',
  `content` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '评论内容',
  `reply` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '回复内容',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1613791515081 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '学习资料评论表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of discussxuexiziliao
-- ----------------------------
INSERT INTO `discussxuexiziliao` VALUES (161, '2025-12-15 11:01:36', 1, 1, '高校课程学习资料《1》知识点解析详细，实用性强', '高校课程知识点需结合理论知识+实践案例双重复习');
INSERT INTO `discussxuexiziliao` VALUES (162, '2025-12-15 11:01:36', 2, 2, '高校课程学习资料《2》知识点解析详细，实用性强', '高校课程知识点需结合理论知识+实践案例双重复习');
INSERT INTO `discussxuexiziliao` VALUES (163, '2025-12-15 11:01:36', 3, 3, '高校课程学习资料《3》知识点解析详细，实用性强', '高校课程知识点需结合理论知识+实践案例双重复习');
INSERT INTO `discussxuexiziliao` VALUES (164, '2025-12-15 11:01:36', 4, 4, '高校课程学习资料《4》知识点解析详细，实用性强', '高校课程知识点需结合理论知识+实践案例双重复习');
INSERT INTO `discussxuexiziliao` VALUES (165, '2025-12-15 11:01:36', 5, 5, '高校课程学习资料《5》知识点解析详细，实用性强', '高校课程知识点需结合理论知识+实践案例双重复习');
INSERT INTO `discussxuexiziliao` VALUES (166, '2025-12-15 11:01:36', 6, 6, '高校课程学习资料《6》知识点解析详细，实用性强', '高校课程知识点需结合理论知识+实践案例双重复习');
INSERT INTO `discussxuexiziliao` VALUES (1613791515080, '2025-12-15 11:25:15', 1613790833254, 1613791194016, '高校课程学习资料《1613790833254》知识点解析详细，实用性强', NULL);

-- ----------------------------
-- Table structure for exampaper
-- ----------------------------
DROP TABLE IF EXISTS `exampaper`;
CREATE TABLE `exampaper`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `addtime` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '试卷名称',
  `time` int(0) NOT NULL COMMENT '考试时长(分钟)',
  `status` int(0) NOT NULL DEFAULT 0 COMMENT '试卷状态',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1613791037287 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '试卷表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of exampaper
-- ----------------------------
INSERT INTO `exampaper` VALUES (1613790668780, '2025-12-15 11:11:08', '高校课程（大学语文）模拟试卷', 60, 1);
INSERT INTO `exampaper` VALUES (1613791037286, '2025-12-15 11:17:17', '高校课程（高等数学）模拟试卷', 90, 1);

-- ----------------------------
-- Table structure for examquestion
-- ----------------------------
DROP TABLE IF EXISTS `examquestion`;
CREATE TABLE `examquestion`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `addtime` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `paperid` bigint(0) NOT NULL COMMENT '所属试卷id（外键）',
  `papername` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '试卷名称',
  `questionname` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '试题名称',
  `options` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '选项，json字符串',
  `score` bigint(0) NULL DEFAULT 0 COMMENT '分值',
  `answer` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '正确答案',
  `analysis` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '答案解析',
  `type` bigint(0) NULL DEFAULT 0 COMMENT '试题类型，0：单选题 1：多选题 2：判断题 3：填空题（暂不考虑多项填空）',
  `sequence` bigint(0) NULL DEFAULT 100 COMMENT '试题排序，值越大排越前面',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1613791151090 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '试题表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of examquestion
-- ----------------------------
INSERT INTO `examquestion` VALUES (1613791072668, '2025-12-20 03:17:22', 1613790668780, '测试试题1', '1+1=', '[{\"text\":\"A.1\",\"code\":\"A\"},{\"text\":\"B.2\",\"code\":\"B\"},{\"text\":\"C.3\",\"code\":\"C\"}]', 25, 'B', '1+1=2', 0, 1);
INSERT INTO `examquestion` VALUES (1613791112641, '2025-12-20 03:17:54', 1613790668780, '测试试题1', '1+1不等于', '[{\"text\":\"A.1\",\"code\":\"A\"},{\"text\":\"B.3\",\"code\":\"B\"},{\"text\":\"C.4\",\"code\":\"C\"},{\"text\":\"D.2\",\"code\":\"D\"}]', 25, 'A,B,C', '1+1=2', 1, 2);
INSERT INTO `examquestion` VALUES (1613791132567, '2025-12-20 03:18:35', 1613791037286, '测试试题2', '1+1=2', '[{\"text\":\"A.对\",\"code\":\"A\"},{\"text\":\"B.错\",\"code\":\"B\"}]', 25, 'A', '1+1=2', 2, 3);
INSERT INTO `examquestion` VALUES (1613791151089, '2025-12-20 03:18:55', 1613790668780, '测试试题1', '1+1=', '[]', 25, '2', '1+1=2', 3, 4);

-- ----------------------------
-- Table structure for examrecord
-- ----------------------------
DROP TABLE IF EXISTS `examrecord`;
CREATE TABLE `examrecord`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `addtime` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `userid` bigint(0) NOT NULL COMMENT '用户id',
  `username` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '用户名',
  `paperid` bigint(0) NOT NULL COMMENT '试卷id（外键）',
  `papername` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '试卷名称',
  `questionid` bigint(0) NOT NULL COMMENT '试题id（外键）',
  `questionname` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '试题名称',
  `options` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '选项，json字符串',
  `score` bigint(0) NULL DEFAULT 0 COMMENT '分值',
  `answer` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '正确答案',
  `analysis` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '答案解析',
  `myscore` bigint(0) NOT NULL DEFAULT 0 COMMENT '试题得分',
  `myanswer` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '考生答案',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1613791334318 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '考试记录表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of examrecord
-- ----------------------------

-- ----------------------------
-- Table structure for forum
-- ----------------------------
DROP TABLE IF EXISTS `forum`;
CREATE TABLE `forum`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `addtime` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `title` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '帖子标题',
  `content` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '帖子内容',
  `parentid` bigint(0) NULL DEFAULT NULL COMMENT '父节点id',
  `userid` bigint(0) NOT NULL COMMENT '用户id',
  `username` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '用户名',
  `isdone` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '状态',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1613791487452 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '学习论坛' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of forum
-- ----------------------------
INSERT INTO `forum` VALUES (62, '2025-12-15 11:01:36', '高校课程学习交流-高校课程学习交流', '【高校课程交流】【高校课程交流】帖子内容2', 2, 2, '用户名2', '开放');
INSERT INTO `forum` VALUES (63, '2025-12-15 11:01:36', '高校课程学习交流-高校课程学习交流', '【高校课程交流】【高校课程交流】帖子内容3', 3, 3, '用户名3', '开放');
INSERT INTO `forum` VALUES (64, '2025-12-15 11:01:36', '高校课程学习交流-高校课程学习交流', '【高校课程交流】【高校课程交流】帖子内容4', 4, 4, '用户名4', '开放');
INSERT INTO `forum` VALUES (65, '2025-12-15 11:01:36', '高校课程学习交流-高校课程学习交流', '【高校课程交流】【高校课程交流】帖子内容5', 5, 5, '用户名5', '开放');
INSERT INTO `forum` VALUES (66, '2025-12-15 11:01:36', '高校课程学习交流-高校课程学习交流', '【高校课程交流】【高校课程交流】帖子内容6', 6, 6, '用户名6', '开放');
INSERT INTO `forum` VALUES (1613791471491, '2025-12-15 11:24:31', '高校课程学习交流-高校课程学习交流', '【高校课程交流】<p>高校课程学习心得交流高校课程学习心得交流</p>', 0, 1613791194016, '\"01\"', '开放');
INSERT INTO `forum` VALUES (1613791487451, '2025-12-15 11:24:47', NULL, '【高校课程交流】高校课程学习心得交流', 1613791471491, 1613791194016, '\"01\"', NULL);

-- ----------------------------
-- Table structure for jiaoshi
-- ----------------------------
DROP TABLE IF EXISTS `jiaoshi`;
CREATE TABLE `jiaoshi`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `addtime` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `gonghao` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '工号',
  `mima` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '密码',
  `xingming` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '姓名',
  `xingbie` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '性别',
  `banji` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '班级',
  `shouji` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '手机',
  `youxiang` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `zhaopian` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '照片',
  `money` float NULL DEFAULT 0 COMMENT '余额',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `gonghao`(`gonghao`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1613790920069 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '教师' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of jiaoshi
-- ----------------------------
INSERT INTO `jiaoshi` VALUES (11, '2025-12-15 11:01:35', '教师1', '123456', '王大学讲师', '男', '班级1', '13823888881', 'gongan1@qq.com', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/jiaoshi_zhaopian1.jpg', 100);
INSERT INTO `jiaoshi` VALUES (12, '2025-12-15 11:01:35', '教师2', '123456', '李大学讲师', '男', '班级2', '13823888882', 'gongan2@qq.com', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/jiaoshi_zhaopian2.jpg', 100);
INSERT INTO `jiaoshi` VALUES (13, '2025-12-15 11:01:35', '教师3', '123456', '张大学讲师', '男', '班级3', '13823888883', 'gongan3@qq.com', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/jiaoshi_zhaopian3.jpg', 100);
INSERT INTO `jiaoshi` VALUES (14, '2025-12-15 11:01:35', '教师4', '123456', '刘大学讲师', '男', '班级4', '13823888884', 'gongan4@qq.com', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/jiaoshi_zhaopian4.jpg', 100);
INSERT INTO `jiaoshi` VALUES (15, '2025-12-15 11:01:35', '教师5', '123456', '赵大学讲师', '男', '班级5', '13823888885', 'gongan5@qq.com', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/jiaoshi_zhaopian5.jpg', 100);
INSERT INTO `jiaoshi` VALUES (16, '2025-12-15 11:01:36', '教师6', '123456', '陈大学讲师', '男', '班级6', '13823888886', 'gongan6@qq.com', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/jiaoshi_zhaopian6.jpg', 100);
INSERT INTO `jiaoshi` VALUES (1613790920068, '2025-12-15 11:15:20', '1', '1', '李大学课程讲师', '女', '班级2', '13800000000', 'ligongan@qq.com', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/1613790945198.jpg', 0);

-- ----------------------------
-- Table structure for news
-- ----------------------------
DROP TABLE IF EXISTS `news`;
CREATE TABLE `news`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `addtime` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `title` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '标题',
  `introduction` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '简介',
  `picture` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '图片',
  `content` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '内容',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 155 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '网站公告' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of news
-- ----------------------------
INSERT INTO `news` VALUES (141, '2025-12-15 11:01:36', '【新功能】高校学习平台笔记功能正式上线', '为提升高校课程学习效率，平台新增课程笔记功能，支持图文编辑、一键导出、同步云端！', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/1613790861967.jpg', '尊敬的用户：\r\n为进一步提升大家的高校课程学习体验，我们于2025年12月18日正式上线课程笔记功能。\r\n核心功能说明：\r\n1. 支持在高校课程课程播放页实时编辑图文笔记，自动关联对应课时；\r\n2. 笔记支持法条标注、案例补充、重点划线功能；\r\n3. 所有笔记自动同步至云端，多端登录均可查看；\r\n4. 支持一键导出为PDF格式，方便备考复习。\r\n使用路径：高校课程课程播放页 → 右侧工具栏 → 笔记。\r\n如有使用问题，可联系在线客服（9:00-22:00）。\r\n感谢您的支持！\r\n高校学习平台运营团队\r\n2025-12-18');
INSERT INTO `news` VALUES (142, '2025-12-15 11:01:36', '2026高校课程寒假集训特惠活动开启 最高立减300元', '寒假高校课程集训限时优惠来袭！全品类课程参与折扣，新用户额外赠送学习资料包！', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/news_picture2.jpg', '尊敬的用户：\r\n为回馈广大用户的支持，高校学习平台特推出2026寒假课程特惠活动：\r\n一、活动时间：2025年12月20日 - 2026年1月10日\r\n二、活动内容：\r\n1. 单课购买：满200减50，满500减150，满1000减300；\r\n2. 课程套餐：购买任意高校课程年卡/季卡套餐，赠送价值99元的《公安法条汇编》资料包；\r\n3. 新用户福利：首次注册用户可领取20元无门槛优惠券（有效期30天）。\r\n三、参与方式：\r\n登录高校学习平台APP/网页端，选购课程时自动抵扣优惠，无需手动领取。\r\n温馨提示：优惠不可叠加使用，活动最终解释权归平台所有。\r\n高校学习平台运营团队\r\n2025-12-17');
INSERT INTO `news` VALUES (143, '2025-12-15 11:01:36', '【系统维护】12月20日凌晨高校学习平台暂停服务2小时', '为优化系统性能，高校学习平台将于12月20日凌晨2:00-4:00进行维护，期间暂停所有服务！', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/news_picture3.jpg', '尊敬的用户：\r\n为给大家提供更稳定的高校课程学习环境，平台将进行系统升级维护，具体安排如下：\r\n1. 维护时间：2025年12月20日 02:00 - 04:00\r\n2. 影响范围：高校学习平台网页端、APP端所有功能（课程播放、资料下载、订单支付等）暂停服务；\r\n3. 注意事项：\r\n   - 维护前请及时保存高校课程学习进度和笔记；\r\n   - 维护期间已购买的高校课程课程有效期将顺延2小时；\r\n   - 如有紧急问题可拨打客服热线：400-XXXX-XXXX（7*24小时）。\r\n给您带来的不便，敬请谅解！\r\n高校学习平台技术部\r\n2025-12-16');
INSERT INTO `news` VALUES (144, '2025-12-15 11:01:36', '2025年度高校课程优秀学员名单公布 最高奖励全年免费课程', '表彰在2025年度高校课程学习表现突出的学员，颁发荣誉证书及课程奖励！', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/news_picture4.jpg', '尊敬的用户：\r\n经过综合评选（高校课程学习时长、课程完成率、作业质量、考试成绩），平台评选出2025年度优秀学员100名，现将相关事宜公告如下：\r\n一、奖励设置：\r\n1. 一等奖（10名）：全年任意高校课程课程免费学习权限 + 定制课程手册；\r\n2. 二等奖（30名）：半年高校课程课程免费学习权限 + 警用装备模型一套；\r\n3. 三等奖（60名）：3个月高校课程课程免费学习权限 + 平台周边礼品。\r\n二、名单查询：\r\n登录高校学习平台官网 → 个人中心 → 公告栏 → 2025年度优秀学员名单。\r\n三、领奖方式：\r\n获奖学员请于2025年12月25日前联系客服核实信息，奖励将在3个工作日内发放。\r\n恭喜所有获奖学员，也感谢全体用户的积极参与！\r\n高校学习平台运营团队\r\n2025-12-15');
INSERT INTO `news` VALUES (145, '2025-12-15 11:01:36', '【新课上线】2026年高校课程课程实践课重磅发布', '联合公安系统资深教官打造，全程执法实战教学，学完可直接对接公安工作实际应用！', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/news_picture5.jpg', '尊敬的用户：\r\n高校学习平台重磅推出《2026年高校课程课程实战课》，课程亮点如下：\r\n1. 讲师团队：由公安系统资深教官、一线办案民警联合授课；\r\n2. 课程内容：涵盖治安管理、刑事课程、公安法制、应急处突四大核心模块；\r\n3. 配套资源：100+真实办案案例、课程流程标准化手册；\r\n4. 就业支持：优秀学员推荐公安系统相关岗位内推机会。\r\n课程首发价：299元（原价499元），限时7天优惠！\r\n立即报名：https://www.xxx.com/course/gongan\r\n高校学习平台课程部\r\n2025-12-14');
INSERT INTO `news` VALUES (146, '2025-12-15 11:01:36', '【打卡有礼】每日学习高校课程 累计30天赢千元课程', '参与每日高校课程学习打卡活动，完成打卡目标即可兑换课程优惠券、实物奖品！', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/news_picture6.jpg', '尊敬的用户：\r\n为培养大家的高校课程学习习惯，平台推出「每日学习打卡」活动：\r\n一、活动规则：\r\n1. 每日登录高校学习平台并学习满30分钟，即可完成打卡；\r\n2. 连续打卡7天：兑换10元高校课程课程优惠券；\r\n3. 连续打卡15天：兑换20元高校课程课程优惠券 + 《课程案例汇编》；\r\n4. 累计打卡30天：兑换50元高校课程课程优惠券 + 千元课程兑换资格。\r\n二、参与方式：\r\nAPP端首页 → 打卡活动入口 → 点击「开始打卡」即可。\r\n三、活动时间：2025年12月15日 - 2026年1月15日。\r\n赶紧参与，边学习高校课程边拿奖！\r\n高校学习平台运营团队\r\n2025-12-13');

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `addtime` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `orderid` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '订单编号',
  `tablename` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT 'xuexiziliao' COMMENT '商品表名',
  `userid` bigint(0) NOT NULL COMMENT '用户id',
  `goodid` bigint(0) NOT NULL COMMENT '商品id',
  `goodname` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '商品名称',
  `picture` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '商品图片',
  `buynumber` int(0) NOT NULL COMMENT '购买数量',
  `price` float NOT NULL DEFAULT 0 COMMENT '价格/积分',
  `discountprice` float NULL DEFAULT 0 COMMENT '折扣价格',
  `total` float NOT NULL DEFAULT 0 COMMENT '总价格/总积分',
  `discounttotal` float NULL DEFAULT 0 COMMENT '折扣总价格',
  `type` int(0) NULL DEFAULT 1 COMMENT '支付类型',
  `status` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '状态',
  `address` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '地址',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `orderid`(`orderid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1613791576330 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '订单' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of orders
-- ----------------------------
INSERT INTO `orders` VALUES (1613791540969, '2025-12-15 11:25:40', '202122011253913115056', 'xuexiziliao', 1613791194016, 1613790833254, '实践案例汇编', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/1613790817710.jpg', 1, 59, 59, 59, 59, 1, '已取消', '广东省广州市越秀区珠光街道椰诚阁');
INSERT INTO `orders` VALUES (1613791576329, '2025-12-15 11:26:16', '202122011261447329183', 'xuexiziliao', 1613791194016, 1613790833254, '实践案例汇编', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/1613790817710.jpg', 1, 59, 59, 59, 59, 1, '已发货', '广东省广州市越秀区珠光街道椰诚阁');

-- ----------------------------
-- Table structure for shishengjiaoliu
-- ----------------------------
DROP TABLE IF EXISTS `shishengjiaoliu`;
CREATE TABLE `shishengjiaoliu`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `addtime` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `xuehao` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '学号',
  `xingming` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '姓名',
  `tiwen` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '提问',
  `shijian` datetime(0) NULL DEFAULT NULL COMMENT '时间',
  `sfsh` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT '否' COMMENT '是否审核',
  `shhf` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '审核回复',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1613791294218 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '师生交流' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of shishengjiaoliu
-- ----------------------------
INSERT INTO `shishengjiaoliu` VALUES (51, '2025-12-15 11:01:36', '学号1', '姓名1', '高校课程中《大学语文》的适用范围是什么？', '2025-12-15 11:01:36', '是', '高校课程中，《大学语文》适用于本科各专业学生，旨在提升人文素养、阅读理解与写作表达能力。');
INSERT INTO `shishengjiaoliu` VALUES (52, '2025-12-15 11:01:36', '学号2', '姓名2', '高校课程里高等数学的学习重点有哪些？', '2025-12-15 11:01:36', '是', '高校课程里，高等数学学习重点为：极限与连续、导数与微分、积分学、微分方程四大模块。');
INSERT INTO `shishengjiaoliu` VALUES (53, '2025-12-15 11:01:36', '学号3', '姓名3', '高校课程中的大学英语四级考核标准是什么？', '2025-12-15 11:01:36', '是', '高校课程中的大学英语四级考核标准参考全国大学英语四、六级考试大纲，包含听力、阅读、写作、翻译四大类。');
INSERT INTO `shishengjiaoliu` VALUES (54, '2025-12-15 11:01:36', '学号4', '姓名4', '高校课程里计算机基础课程的考核要求是什么？', '2025-12-15 11:01:36', '是', '高校课程里，计算机基础考核需满足：掌握办公软件操作、计算机基础理论、简单编程逻辑，实操与笔试均达标。');
INSERT INTO `shishengjiaoliu` VALUES (55, '2025-12-15 11:01:36', '学号5', '姓名5', '高校课程中的线性代数学习要点有哪些？', '2025-12-15 11:01:36', '是', '高校课程中的线性代数学习要点：矩阵运算、行列式求解、向量空间、特征值与特征向量、线性方程组求解。');
INSERT INTO `shishengjiaoliu` VALUES (56, '2025-12-15 11:01:36', '学号6', '姓名6', '高校课程里的概率论知识点记忆技巧是什么？', '2025-12-15 11:01:36', '是', '高校课程里的概率论记忆要求：理解核心概念、结合例题推导公式，分类整理概率模型，严禁死记硬背。');
INSERT INTO `shishengjiaoliu` VALUES (1613790725137, '2025-12-15 11:12:05', '学生1', '姓名1', '老师，高校课程中的大学物理公式太难记，有什么技巧吗？', '2025-12-15 11:11:56', '是', '大学物理公式可按「力学-热学-电磁学-光学」模块拆解，结合实验现象理解推导过程，效果更佳。');
INSERT INTO `shishengjiaoliu` VALUES (1613791294216, '2025-12-15 11:21:34', '01', '张三', '老师，高校课程里的《大学英语六级》核心考点有哪些？', '2025-12-15 11:21:26', NULL, '《大学英语六级》核心考点：长篇阅读技巧、深度阅读理解、翻译句式转换、写作逻辑架构。');
INSERT INTO `shishengjiaoliu` VALUES (1613791294217, '2026-01-13 16:54:36', '1', '张三', '高校课程中，通识教育课程的核心目标包含哪些？', '2026-01-13 16:54:34', NULL, '通识教育课程核心目标：拓宽知识视野、培养综合素养、提升批判性思维、增强跨学科应用能力。');

-- ----------------------------
-- Table structure for storeup
-- ----------------------------
DROP TABLE IF EXISTS `storeup`;
CREATE TABLE `storeup`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `addtime` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `userid` bigint(0) NOT NULL COMMENT '用户id',
  `refid` bigint(0) NULL DEFAULT NULL COMMENT '收藏id',
  `tablename` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '表名',
  `name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '收藏名称',
  `picture` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '收藏图片',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1613791521424 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '收藏表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of storeup
-- ----------------------------
INSERT INTO `storeup` VALUES (1613791521423, '2025-12-15 11:25:21', 1613791194016, 1613790833254, 'xuexiziliao', '实践案例汇编', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/1613790817710.jpg');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `username` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '用户名',
  `password` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '密码',
  `role` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT '管理员' COMMENT '角色',
  `addtime` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '新增时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '用户表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'admin', 'admin', '管理员', '2025-12-15 11:01:36');

-- ----------------------------
-- Table structure for xuesheng
-- ----------------------------
DROP TABLE IF EXISTS `xuesheng`;
CREATE TABLE `xuesheng`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `addtime` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `xuehao` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '学号',
  `mima` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '密码',
  `xingming` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '姓名',
  `xingbie` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '性别',
  `banji` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '班级',
  `shouji` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '手机',
  `youxiang` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `zhaopian` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '照片',
  `money` float NULL DEFAULT 0 COMMENT '余额',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `xuehao`(`xuehao`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1613791194017 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '学生' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of xuesheng
-- ----------------------------
INSERT INTO `xuesheng` VALUES (21, '2025-12-15 11:01:36', '学生1', '123456', '张大学学员', '女', '班级1', '13823888881', '773890001@qq.com', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/xuesheng_zhaopian1.jpg', 100);
INSERT INTO `xuesheng` VALUES (22, '2025-12-15 11:01:36', '学生2', '123456', '李大学学员', '男', '班级2', '13823888882', '773890002@qq.com', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/xuesheng_zhaopian2.jpg', 100);
INSERT INTO `xuesheng` VALUES (23, '2025-12-15 11:01:36', '学生3', '123456', '王大学学员', '男', '班级3', '13823888883', '773890003@qq.com', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/xuesheng_zhaopian3.jpg', 100);
INSERT INTO `xuesheng` VALUES (24, '2025-12-15 11:01:36', '学生4', '123456', '刘大学学员', '男', '班级4', '13823888884', '773890004@qq.com', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/xuesheng_zhaopian4.jpg', 100);
INSERT INTO `xuesheng` VALUES (25, '2025-12-15 11:01:36', '学生5', '123456', '赵大学学员', '男', '班级5', '13823888885', '773890005@qq.com', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/xuesheng_zhaopian5.jpg', 100);
INSERT INTO `xuesheng` VALUES (26, '2025-12-15 11:01:36', '学生6', '123456', '陈大学学员', '男', '班级6', '13823888886', '773890006@qq.com', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/xuesheng_zhaopian6.jpg', 100);
INSERT INTO `xuesheng` VALUES (1613791194016, '2025-12-15 11:19:54', '1', '1', '张三（大学课程一班）', '男', '班级1', '11100000000', '11111@qq.com', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/1613791217705.jpg', 941);
INSERT INTO `xuesheng` VALUES (1767439487002, '2026-02-10 19:57:25', '2', '2', '2', '女', '班级2', '13888888888', '2@qq.com', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/1770728810820.jpg', 100);

-- ----------------------------
-- Table structure for xuexitiandi
-- ----------------------------
DROP TABLE IF EXISTS `xuexitiandi`;
CREATE TABLE `xuexitiandi`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `addtime` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `biaoti` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '标题',
  `fengmian` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '封面',
  `zhishiyaodian` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '知识要点',
  `xuexishipin` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '学习视频',
  `thumbsupnum` int(0) NULL DEFAULT 0 COMMENT '赞',
  `crazilynum` int(0) NULL DEFAULT 0 COMMENT '踩',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1613790999795 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '学习天地' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of xuexitiandi
-- ----------------------------
INSERT INTO `xuexitiandi` VALUES (31, '2025-12-15 11:01:36', '大学语文实务精讲', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/xuexitiandi_fengmian1.jpg', '大学语文/文学常识/阅读理解/写作技巧', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/1.mp4', 1, 1);
INSERT INTO `xuexitiandi` VALUES (32, '2025-12-15 11:01:36', '高等数学应用解析', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/xuexitiandi_fengmian2.jpg', '高等数学/微积分应用/极限求解/微分方程', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/1.mp4', 2, 2);
INSERT INTO `xuexitiandi` VALUES (33, '2025-12-15 11:01:36', '大学英语四级教程', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/xuexitiandi_fengmian3.jpg', '大学英语/听力技巧/阅读方法/写作模板', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/1.mp4', 3, 3);
INSERT INTO `xuexitiandi` VALUES (34, '2025-12-15 11:01:36', '计算机基础实战演练', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/xuexitiandi_fengmian4.jpg', '办公软件/编程基础/数据库操作/网络安全', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/1.mp4', 4, 4);
INSERT INTO `xuexitiandi` VALUES (35, '2025-12-15 11:01:36', '大学物理标准化教学', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/xuexitiandi_fengmian5.jpg', '力学公式/电磁学原理/实验操作/解题技巧', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/1.mp4', 5, 5);
INSERT INTO `xuexitiandi` VALUES (36, '2025-12-15 11:01:36', '线性代数解题规范', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/xuexitiandi_fengmian6.jpg', '矩阵运算/行列式求解/向量空间/方程组解法', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/1.mp4', 6, 6);

-- ----------------------------
-- Table structure for xuexiziliao
-- ----------------------------
DROP TABLE IF EXISTS `xuexiziliao`;
CREATE TABLE `xuexiziliao`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `addtime` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `ziliaomingcheng` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '资料名称',
  `fengmian` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '封面',
  `xiangqing` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '详情',
  `thumbsupnum` int(0) NULL DEFAULT 0 COMMENT '赞',
  `crazilynum` int(0) NULL DEFAULT 0 COMMENT '踩',
  `wenjian` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '文件',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1613790833263 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '学习资料' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of xuexiziliao
-- ----------------------------
INSERT INTO `xuexiziliao` VALUES (41, '2025-12-15 11:01:36', '大学语文考点汇编与解析', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/xuexiziliao_fengmian1.jpg', '本资料包含《大学语文》必考知识点、重点篇目标注、典型例题解析，配套真题练习，适合备考使用。', 1, 1, NULL);
INSERT INTO `xuexiziliao` VALUES (42, '2025-12-15 11:01:36', '高等数学解题规范实务手册', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/xuexiziliao_fengmian2.jpg', '涵盖高等数学解题全流程规范、公式应用技巧、易错点解析，附一线教师授课经验分享。', 2, 2, NULL);
INSERT INTO `xuexiziliao` VALUES (43, '2025-12-15 11:01:36', '大学英语四级知识点精讲', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/xuexiziliao_fengmian3.jpg', '系统讲解大学英语四级听力、阅读、写作、翻译等核心知识点，逻辑清晰，考点突出。', 3, 3, NULL);
INSERT INTO `xuexiziliao` VALUES (44, '2025-12-15 11:01:36', '计算机基础典型案例100篇', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/xuexiziliao_fengmian4.jpg', '精选100篇计算机基础典型案例，包含办公软件操作、编程实现、数据库应用，实战指导性强。', 4, 4, NULL);
INSERT INTO `xuexiziliao` VALUES (45, '2025-12-15 11:01:36', '大学物理考核通关指南', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/xuexiziliao_fengmian5.jpg', '大学物理考核通关指南，含公式记忆方法、实验操作技巧、综合解题思路，助力考核通过。', 5, 5, NULL);
INSERT INTO `xuexiziliao` VALUES (46, '2025-12-15 11:01:36', '线性代数解题标准模板', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/xuexiziliao_fengmian6.jpg', '线性代数标准化解题模板，含矩阵、行列式、方程组等各类题型解法，标注解题要点与注意事项。', 6, 6, NULL);
INSERT INTO `xuexiziliao` VALUES (1613790833254, '2025-12-15 11:13:53', '高数实践案例汇编', 'http://localhost:8080/dj_intellrnmgmtsystem/upload/xuexiziliao_fengmian7.jpg', '精选50个高等数学真实应用案例，按微积分、微分方程、概率论分类，详细拆解解题思路与公式适用，实战性极强。', 0, 0, NULL);

SET FOREIGN_KEY_CHECKS = 1;
