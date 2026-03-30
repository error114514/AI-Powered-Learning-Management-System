
var projectName = '智能化学习系统';
/**
 * 轮播图配置
 */
var swiper = {
	// 设定轮播容器宽度，支持像素和百分比
	width: '100%',
	height: '400px',
	// hover（悬停显示）
	// always（始终显示）
	// none（始终不显示）
	arrow: 'none',
	// default（左右切换）
	// updown（上下切换）
	// fade（渐隐渐显切换）
	anim: 'default',
	// 自动切换的时间间隔
	// 默认3000
	interval: 2000,
	// 指示器位置
	// inside（容器内部）
	// outside（容器外部）
	// none（不显示）
	indicator: 'outside'
}

/**
 * 个人中心菜单
 */
var centerMenu = [{
	name: '个人中心',
	url: '../' + localStorage.getItem('userTable') + '/center.html'
}, 
{
	name: '我的发布',
	url: '../forum/list-my.html'
},




{
	name: '作业记录',
	url: '../examrecord/list.html'
}, 
{
	name: '错题本',
	url: '../examrecord/wrong.html'
},
{
	name: '我的收藏',
	url: '../storeup/list.html'
}
]


var indexNav = [

{
	name: '课程管理',
	url: './pages/xuexitiandi/list.html'
}, 
{
	name: '学习资料',
	url: './pages/xuexiziliao/list.html'
}, 

{
	name: '互动交流',
	url: './pages/forum/list.html'
}, 
// 学习中心模块已隐藏，不在用户端展示
// {
// 	name: '学习中心',
// 	url: './pages/exampaper/list.html'
// }, 
{
	name: '网站公告',
	url: './pages/news/list.html'
},
]

var adminurl =  "http://localhost:8080/dj_intellrnmgmtsystem/admin/dist/index.html";

var cartFlag = false

var chatFlag = false


cartFlag = true


var menu = [{"backMenu":[{"child":[{"buttons":["修改","查看","删除"],"menu":"教师","menuJump":"列表","tableName":"jiaoshi"}],"menu":"教师管理"},{"child":[{"buttons":["删除","修改","查看"],"menu":"学生","menuJump":"列表","tableName":"xuesheng"}],"menu":"学生管理"},{"child":[{"buttons":["查看","修改","删除","查看评论","新增"],"menu":"课程管理","menuJump":"列表","tableName":"xuexitiandi"}],"menu":"课程管理"},{"child":[{"buttons":["查看","修改","删除","查看评论","新增"],"menu":"学习资料","menuJump":"列表","tableName":"xuexiziliao"}],"menu":"学习资料管理"},{"child":[{"buttons":["新增","查看","修改","删除"],"menu":"互动交流","tableName":"forum"}],"menu":"互动交流"},{"child":[{"buttons":["新增","查看","修改","删除"],"menu":"网站公告","tableName":"news"},{"buttons":["新增","查看","修改","删除"],"menu":"轮播图管理","tableName":"config"}],"menu":"系统管理"},{"child":[{"buttons":["查看","修改","删除"],"menu":"已完成订单","tableName":"orders/已完成"},{"buttons":["查看","修改","删除","确认收货"],"menu":"已发货订单","tableName":"orders/已发货"},{"buttons":["查看","修改","删除"],"menu":"未支付订单","tableName":"orders/未支付"},{"buttons":["查看","修改","删除"],"menu":"已取消订单","tableName":"orders/已取消"},{"buttons":["查看","修改","删除","发货"],"menu":"已支付订单","tableName":"orders/已支付"},{"buttons":["查看","修改","删除"],"menu":"已退款订单","tableName":"orders/已退款"}],"menu":"订单管理"},{"child":[{"buttons":["查看"],"menu":"学习中心","tableName":"exampaperlist"}],"menu":"作业管理"}],"frontMenu":[{"child":[{"buttons":["查看","查看评论"],"menu":"课程管理列表","menuJump":"列表","tableName":"xuexitiandi"}],"menu":"课程管理模块"},{"child":[{"buttons":["查看","查看评论","购买"],"menu":"学习资料列表","menuJump":"列表","tableName":"xuexiziliao"}],"menu":"学习资料模块"}],"hasBackLogin":"是","hasBackRegister":"否","hasFrontLogin":"否","hasFrontRegister":"否","roleName":"管理员","tableName":"users"},{"backMenu":[{"child":[{"buttons":["查看"],"menu":"教师","menuJump":"列表","tableName":"jiaoshi"}],"menu":"教师管理"},{"child":[{"buttons":["查看"],"menu":"学生","menuJump":"列表","tableName":"xuesheng"}],"menu":"学生管理"},{"child":[{"buttons":["新增","查看","修改","删除","查看评论"],"menu":"课程管理","menuJump":"列表","tableName":"xuexitiandi"}],"menu":"课程管理"},{"child":[{"buttons":["购买","查看"],"menu":"学习资料","menuJump":"列表","tableName":"xuexiziliao"}],"menu":"学习资料管理"},{"child":[{"buttons":["审核","查看","修改","删除"],"menu":"师生交流","menuJump":"列表","tableName":"shishengjiaoliu"}],"menu":"师生交流管理"},{"child":[{"buttons":["新增","查看","修改","删除"],"menu":"作业管理","tableName":"exampaper"}],"menu":"作业管理"},{"child":[{"buttons":["新增","查看","修改","删除"],"menu":"试题管理","tableName":"examquestion"}],"menu":"试题管理"},{"child":[{"buttons":["查看"],"menu":"轮播图管理","tableName":"config"},{"buttons":["查看"],"menu":"网站公告","tableName":"news"}],"menu":"系统管理"},{"child":[{"buttons":["查看"],"menu":"作业记录","tableName":"examrecord"}],"menu":"作业管理"}],"frontMenu":[{"child":[{"buttons":["查看","查看评论"],"menu":"课程管理列表","menuJump":"列表","tableName":"xuexitiandi"}],"menu":"课程管理模块"},{"child":[{"buttons":["查看","查看评论","购买"],"menu":"学习资料列表","menuJump":"列表","tableName":"xuexiziliao"}],"menu":"学习资料模块"}],"hasBackLogin":"是","hasBackRegister":"是","hasFrontLogin":"是","hasFrontRegister":"是","roleName":"教师","tableName":"jiaoshi"},{"backMenu":[{"child":[{"buttons":["查看"],"menu":"教师","menuJump":"列表","tableName":"jiaoshi"}],"menu":"教师管理"},{"child":[{"buttons":["查看"],"menu":"学生","menuJump":"列表","tableName":"xuesheng"}],"menu":"学生管理"},{"child":[{"buttons":["查看"],"menu":"课程管理","menuJump":"列表","tableName":"xuexitiandi"}],"menu":"课程管理"},{"child":[{"buttons":["购买","查看"],"menu":"学习资料","menuJump":"列表","tableName":"xuexiziliao"}],"menu":"学习资料管理"},{"child":[{"buttons":["新增","修改","删除"],"menu":"师生交流","menuJump":"列表","tableName":"shishengjiaoliu"}],"menu":"师生交流管理"},{"child":[{"buttons":["查看"],"menu":"轮播图管理","tableName":"config"},{"buttons":["查看"],"menu":"网站公告","tableName":"news"}],"menu":"系统管理"},{"child":[{"buttons":["查看"],"menu":"学习中心","tableName":"exampaperlist"},{"buttons":["查看"],"menu":"作业记录","tableName":"examrecord"},{"buttons":["查看"],"menu":"错题本","tableName":"examfailrecord"}],"menu":"作业管理"}],"frontMenu":[{"child":[{"buttons":["查看","查看评论"],"menu":"课程管理列表","menuJump":"列表","tableName":"xuexitiandi"}],"menu":"课程管理模块"},{"child":[{"buttons":["查看","查看评论","购买"],"menu":"学习资料列表","menuJump":"列表","tableName":"xuexiziliao"}],"menu":"学习资料模块"}],"hasBackLogin":"是","hasBackRegister":"是","hasFrontLogin":"是","hasFrontRegister":"是","roleName":"学生","tableName":"xuesheng"}]


var isAuth = function (tableName,key) {
    let role = localStorage.getItem("userTable");
    let menus = menu;
    for(let i=0;i<menus.length;i++){
        if(menus[i].tableName==role){
            for(let j=0;j<menus[i].backMenu.length;j++){
                for(let k=0;k<menus[i].backMenu[j].child.length;k++){
                    if(tableName==menus[i].backMenu[j].child[k].tableName){
                        let buttons = menus[i].backMenu[j].child[k].buttons.join(',');
                        return buttons.indexOf(key) !== -1 || false
                    }
                }
            }
        }
    }
    return false;
}

var isFrontAuth = function (tableName,key) {
    let role = localStorage.getItem("userTable");
    let menus = menu;
    for(let i=0;i<menus.length;i++){
        if(menus[i].tableName==role){
            for(let j=0;j<menus[i].frontMenu.length;j++){
                for(let k=0;k<menus[i].frontMenu[j].child.length;k++){
                    if(tableName==menus[i].frontMenu[j].child[k].tableName){
                        let buttons = menus[i].frontMenu[j].child[k].buttons.join(',');
                        return buttons.indexOf(key) !== -1 || false
                    }
                }
            }
        }
    }
    return false;
}
