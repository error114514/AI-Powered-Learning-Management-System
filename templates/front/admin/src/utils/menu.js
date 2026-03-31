const menu = {
  list() {
    return [
      {
        backMenu: [
          {
            child: [
              {
                buttons: ["查看"],
                menu: "教师",
                menuJump: "列表",
                tableName: "jiaoshi",
              },
            ],
            menu: "教师管理",
          },
          {
            child: [
              {
                buttons: ["查看"],
                menu: "学生",
                menuJump: "列表",
                tableName: "xuesheng",
              },
            ],
            menu: "学生管理",
          },
          {
            child: [
              {
                buttons: ["查看", "修改", "删除", "查看评论", "查看考勤", "新增"],
                menu: "课程管理",
                menuJump: "列表",
                tableName: "xuexitiandi",
              },
            ],
            menu: "课程管理",
          },
          {
            child: [
              {
                buttons: ["查看", "修改", "删除", "查看评论", "新增"],
                menu: "学习资料",
                menuJump: "列表",
                tableName: "xuexiziliao",
              },
            ],
            menu: "学习资料管理",
          },
          {
            child: [
              {
                buttons: ["新增", "查看", "修改", "删除"],
                menu: "互动交流",
                tableName: "forum",
              },
            ],
            menu: "互动交流",
          },
          {
            child: [
              {
                buttons: ["新增", "查看", "修改", "删除"],
                menu: "网站公告",
                tableName: "news",
              },
              {
                buttons: ["新增", "查看", "修改", "删除"],
                menu: "轮播图管理",
                tableName: "config",
              },
            ],
            menu: "系统管理",
          },

          {
            child: [
              {
                buttons: ["查看"],
                menu: "学习中心",
                tableName: "exampaperlist",
              },
            ],
            menu: "作业管理",
          },
        ],
        frontMenu: [
          {
            child: [
              {
                buttons: ["查看", "查看评论"],
                menu: "课程管理列表",
                menuJump: "列表",
                tableName: "xuexitiandi",
              },
            ],
            menu: "课程管理模块",
          },
          {
            child: [
              {
                buttons: ["查看", "查看评论", "购买"],
                menu: "学习资料列表",
                menuJump: "列表",
                tableName: "xuexiziliao",
              },
            ],
            menu: "学习资料模块",
          },
        ],
        hasBackLogin: "是",
        hasBackRegister: "否",
        hasFrontLogin: "否",
        hasFrontRegister: "否",
        roleName: "管理员",
        tableName: "users",
      },
      {
        backMenu: [
          {
            child: [
              {
                buttons: ["查看"],
                menu: "学生",
                menuJump: "列表",
                tableName: "xuesheng",
              },
            ],
            menu: "学生管理",
          },
          {
            child: [
              {
                buttons: ["新增", "查看", "修改", "删除", "查看评论", "查看考勤"],
                menu: "课程管理",
                menuJump: "列表",
                tableName: "xuexitiandi",
              },
            ],
            menu: "课程管理",
          },
          {
            child: [
              {
                buttons: ["购买", "查看"],
                menu: "学习资料",
                menuJump: "列表",
                tableName: "xuexiziliao",
              },
            ],
            menu: "学习资料管理",
          },
          {
            child: [
              {
                buttons: ["审核", "查看", "修改", "删除"],
                menu: "师生交流",
                menuJump: "列表",
                tableName: "shishengjiaoliu",
              },
            ],
            menu: "师生交流管理",
          },
          {
            child: [
              {
                buttons: ["新增", "查看", "修改", "删除"],
                menu: "作业管理",
                tableName: "exampaper",
              },
            ],
            menu: "作业管理",
          },
          {
            child: [
              {
                buttons: ["新增", "查看", "修改", "删除"],
                menu: "试题管理",
                tableName: "examquestion",
              },
            ],
            menu: "试题管理",
          },
          {
            child: [
              { buttons: ["查看"], menu: "轮播图管理", tableName: "config" },
              { buttons: ["查看"], menu: "网站公告", tableName: "news" },
            ],
            menu: "系统管理",
          },
          {
            child: [
              { buttons: ["查看"], menu: "作业记录", tableName: "examrecord" },
            ],
            menu: "作业管理",
          },
        ],
        hasBackLogin: "是",
        hasBackRegister: "是",
        hasFrontLogin: "否",
        hasFrontRegister: "否",
        roleName: "教师",
        tableName: "jiaoshi",
      },
      {
        backMenu: [
          {
            child: [
              {
                buttons: ["查看"],
                menu: "教师",
                menuJump: "列表",
                tableName: "jiaoshi",
              },
            ],
            menu: "教师管理",
          },
          {
            child: [
              {
                buttons: ["查看"],
                menu: "学生",
                menuJump: "列表",
                tableName: "xuesheng",
              },
            ],
            menu: "学生管理",
          },
          {
            child: [
              {
                buttons: ["查看"],
                menu: "课程管理",
                menuJump: "列表",
                tableName: "xuexitiandi",
              },
            ],
            menu: "课程管理",
          },
          {
            child: [
              {
                buttons: ["购买", "查看"],
                menu: "学习资料",
                menuJump: "列表",
                tableName: "xuexiziliao",
              },
            ],
            menu: "学习资料管理",
          },
          {
            child: [
              {
                buttons: ["新增", "查看", "修改", "删除"],
                menu: "师生交流",
                menuJump: "列表",
                tableName: "shishengjiaoliu",
              },
            ],
            menu: "师生交流管理",
          },
          {
            child: [
              { buttons: ["查看"], menu: "轮播图管理", tableName: "config" },
              { buttons: ["查看"], menu: "网站公告", tableName: "news" },
            ],
            menu: "系统管理",
          },
          {
            child: [
              {
                buttons: ["查看"],
                menu: "学习中心",
                tableName: "exampaperlist",
              },
              { buttons: ["查看"], menu: "作业记录", tableName: "examrecord" },
              {
                buttons: ["查看"],
                menu: "错题本",
                tableName: "examfailrecord",
              },
            ],
            menu: "作业管理",
          },
        ],
        frontMenu: [
          {
            child: [
              {
                buttons: ["查看", "查看评论"],
                menu: "课程管理列表",
                menuJump: "列表",
                tableName: "xuexitiandi",
              },
            ],
            menu: "课程管理模块",
          },
          {
            child: [
              {
                buttons: ["查看", "查看评论", "购买"],
                menu: "学习资料列表",
                menuJump: "列表",
                tableName: "xuexiziliao",
              },
            ],
            menu: "学习资料模块",
          },
        ],
        hasBackLogin: "否",
        hasBackRegister: "否",
        hasFrontLogin: "是",
        hasFrontRegister: "是",
        roleName: "学生",
        tableName: "xuesheng",
      },
    ];
  },
};
export default menu;
