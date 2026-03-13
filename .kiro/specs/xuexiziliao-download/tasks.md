# Implementation Plan: 学习资料下载功能

## Overview

将学习资料模块从"购买"模式修改为"下载"模式，涉及数据模型、前台页面和后台页面的修改。

## Tasks

- [x] 1. 修改数据模型
  - [x] 1.1 修改 main/models.py 中的 xuexiziliao 模型
    - 移除 price 字段
    - 新增 wenjian 字段（VARCHAR(255)，可为空）
    - _Requirements: 1.1, 1.2, 1.3_

- [x] 2. 修改前台详情页
  - [x] 2.1 修改 templates/front/pages/xuexiziliao/detail.html
    - 移除价格显示区域
    - 移除购买数量选择器
    - 移除"添加到购物车"按钮
    - 移除"立即购买"按钮
    - 新增"下载资料"按钮
    - 新增 downloadFile 方法
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

- [x] 3. 修改前台列表页
  - [x] 3.1 修改 templates/front/pages/xuexiziliao/list.html
    - 移除价格显示区域
    - _Requirements: 3.1, 3.2_

- [x] 4. 修改后台编辑页
  - [x] 4.1 修改 templates/front/admin/src/views/modules/xuexiziliao/add-or-update.vue
    - 移除价格输入框
    - 新增文件上传组件
    - 新增 wenjianUploadChange 方法
    - 更新 ruleForm 和 rules 配置
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [x] 5. Checkpoint - 验证所有修改
  - 确保所有文件修改正确，检查是否有语法错误

## Notes

- 本次修改不涉及数据库迁移脚本，需要手动执行 Django migrations
- 文件上传使用现有的 file/upload 接口
- 下载功能使用浏览器原生下载能力
