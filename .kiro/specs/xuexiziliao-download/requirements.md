# Requirements Document

## Introduction

将学习资料模块从"购买"模式修改为"下载"模式。移除购物车、订单、价格等购买相关功能，新增文件下载功能，让用户可以直接下载学习资料文件。

## Glossary

- **Learning_Materials_System**: 学习资料管理系统，负责学习资料的展示、管理和下载
- **Download_Module**: 下载模块，提供学习资料文件的下载功能
- **Front_Page**: 前台页面，用户浏览和下载学习资料的界面
- **Admin_Page**: 后台管理页面，管理员管理学习资料的界面
- **File_Attachment**: 文件附件，学习资料关联的可下载文件

## Requirements

### Requirement 1: 数据模型修改

**User Story:** As a 系统管理员, I want to 修改学习资料数据模型, so that 系统支持文件下载而非购买功能。

#### Acceptance Criteria

1. THE Learning_Materials_System SHALL 移除学习资料模型中的 price（价格）字段
2. THE Learning_Materials_System SHALL 新增 wenjian（文件）字段用于存储可下载文件路径
3. THE Learning_Materials_System SHALL 保留现有的 ziliaomingcheng（资料名称）、fengmian（封面）、xiangqing（详情）等字段

### Requirement 2: 前台详情页修改

**User Story:** As a 用户, I want to 在学习资料详情页直接下载文件, so that 我可以获取学习资料而无需购买流程。

#### Acceptance Criteria

1. THE Front_Page SHALL 移除详情页中的价格显示区域
2. THE Front_Page SHALL 移除详情页中的购买数量选择器
3. THE Front_Page SHALL 移除详情页中的"添加到购物车"按钮
4. THE Front_Page SHALL 移除详情页中的"立即购买"按钮
5. WHEN 学习资料包含可下载文件 THEN THE Front_Page SHALL 显示"下载资料"按钮
6. WHEN 用户点击"下载资料"按钮 THEN THE Download_Module SHALL 触发文件下载

### Requirement 3: 前台列表页修改

**User Story:** As a 用户, I want to 在学习资料列表页看到简洁的资料信息, so that 我可以快速浏览和选择需要的资料。

#### Acceptance Criteria

1. THE Front_Page SHALL 移除列表页中的价格显示
2. THE Front_Page SHALL 保留资料名称、封面图片等基本信息展示

### Requirement 4: 后台管理页修改

**User Story:** As a 管理员, I want to 在后台管理学习资料时上传可下载文件, so that 用户可以下载这些文件。

#### Acceptance Criteria

1. THE Admin_Page SHALL 移除学习资料编辑表单中的价格输入框
2. THE Admin_Page SHALL 新增文件上传组件用于上传可下载文件
3. WHEN 管理员上传文件 THEN THE Admin_Page SHALL 将文件路径保存到 wenjian 字段
4. THE Admin_Page SHALL 支持上传多种文件格式（如 PDF、DOC、DOCX、PPT、PPTX、XLS、XLSX、ZIP 等）

### Requirement 5: 下载功能实现

**User Story:** As a 用户, I want to 安全地下载学习资料文件, so that 我可以在本地查看和使用这些资料。

#### Acceptance Criteria

1. WHEN 用户点击下载按钮 THEN THE Download_Module SHALL 提供文件下载
2. THE Download_Module SHALL 支持下载各种常见文件格式
3. IF 文件不存在 THEN THE Download_Module SHALL 显示友好的错误提示
