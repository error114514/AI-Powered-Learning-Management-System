import Vue from 'vue';
//配置路由
import VueRouter from 'vue-router'
Vue.use(VueRouter);
//1.创建组件
import Index from '@/views/index'
import Home from '@/views/home'
import Login from '@/views/login'
import NotFound from '@/views/404'
import UpdatePassword from '@/views/update-password'
import pay from '@/views/pay'
import register from '@/views/register'
import center from '@/views/center'
import adminexam from '@/views/modules/exampaperlist/exam'
    import news from '@/views/modules/news/list'
    import examfailrecord from '@/views/modules/examfailrecord/list'
    import xuesheng from '@/views/modules/xuesheng/list'
    import examquestion from '@/views/modules/examquestion/list'
    import xuexitiandi from '@/views/modules/xuexitiandi/list'
    import jiaoshi from '@/views/modules/jiaoshi/list'
    import discussxuexiziliao from '@/views/modules/discussxuexiziliao/list'
    import exampaper from '@/views/modules/exampaper/list'
    import forum from '@/views/modules/forum/list'
    import shishengjiaoliu from '@/views/modules/shishengjiaoliu/list'
    import discussxuexitiandi from '@/views/modules/discussxuexitiandi/list'
    import exampaperlist from '@/views/modules/exampaperlist/list'
    import xuexiziliao from '@/views/modules/xuexiziliao/list'
    import orders from '@/views/modules/orders/list'
    import config from '@/views/modules/config/list'
    import examrecord from '@/views/modules/examrecord/list'


//2.配置路由   注意：名字
const routes = [{
    path: '/index',
    name: '首页',
    component: Index,
    children: [{
      // 这里不设置值，是把main作为默认页面
      path: '/',
      name: '首页',
      component: Home,
      meta: {icon:'', title:'center'}
    }, {
      path: '/updatePassword',
      name: '修改密码',
      component: UpdatePassword,
      meta: {icon:'', title:'updatePassword'}
    }, {
      path: '/pay',
      name: '支付',
      component: pay,
      meta: {icon:'', title:'pay'}
    }, {
      path: '/center',
      name: '个人信息',
      component: center,
      meta: {icon:'', title:'center'}
    }
          ,{
	path: '/news',
        name: '网站公告',
        component: news
      }
          ,{
	path: '/examfailrecord',
        name: '错题本',
        component: examfailrecord
      }
          ,{
	path: '/xuesheng',
        name: '学生',
        component: xuesheng
      }
          ,{
	path: '/examquestion',
        name: '试题管理',
        component: examquestion
      }
          ,{
	path: '/xuexitiandi',
        name: '课程管理',
        component: xuexitiandi
      }
          ,{
	path: '/jiaoshi',
        name: '教师',
        component: jiaoshi
      }
          ,{
	path: '/discussxuexiziliao',
        name: '学习资料评论',
        component: discussxuexiziliao
      }
          ,{
	path: '/exampaper',
        name: '作业管理',
        component: exampaper
      }
          ,{
	path: '/forum',
        name: '互动交流',
        component: forum
      }
          ,{
	path: '/shishengjiaoliu',
        name: '师生交流',
        component: shishengjiaoliu
      }
          ,{
	path: '/discussxuexitiandi',
        name: '课程管理评论',
        component: discussxuexitiandi
      }
          ,{
	path: '/exampaperlist',
        name: '学习中心',
        component: exampaperlist
      }
          ,{
	path: '/xuexiziliao',
        name: '学习资料',
        component: xuexiziliao
      }
          ,{
        path: '/orders/:status',
        name: '订单管理',
        component: orders
      }
          ,{
	path: '/config',
        name: '轮播图管理',
        component: config
      }
          ,{
	path: '/examrecord',
        name: '作业记录',
        component: examrecord
      }
        ]
  },
  {
    path: '/adminexam',
    name: 'adminexam',
    component: adminexam,
    meta: {icon:'', title:'adminexam'}
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: {icon:'', title:'login'}
  },
  {
    path: '/register',
    name: 'register',
    component: register,
    meta: {icon:'', title:'register'}
  },
  {
    path: '/',
    name: '首页',
    redirect: '/index'
  }, /*默认跳转路由*/
  {
    path: '*',
    component: NotFound
  }
]
//3.实例化VueRouter  注意：名字
const router = new VueRouter({
  mode: 'hash',
  /*hash模式改为history*/
  routes // （缩写）相当于 routes: routes
})

export default router;
