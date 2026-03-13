import axios from 'axios'
import router from '@/router/router-static'
import storage from '@/utils/storage'
import base from '@/utils/base'

// 使用 base.js 中配置的后端地址(8080)，确保 API 请求发往正确的后端
// 开发时用相对路径 /dj_intellrnmgmtsystem，由 vue.config.js 的 proxy 代理到 8080
// 这样即使前端在 8081，请求会通过代理转发到后端 8080
const baseURL = process.env.NODE_ENV === 'development'
    ? '/dj_intellrnmgmtsystem'
    : (base.get().url || '/dj_intellrnmgmtsystem')

const http = axios.create({
    timeout: 1000 * 86400,
    withCredentials: true,
    baseURL: baseURL,
    headers: {
        'Content-Type': 'application/json; charset=utf-8'
    }
})
// 请求拦截
http.interceptors.request.use(config => {
    config.headers['Token'] = storage.get('Token') // 请求头带上token
    return config
}, error => {
    return Promise.reject(error)
})
// 响应拦截
http.interceptors.response.use(response => {
    if (response.data && response.data.code === 401) { // 401, token失效
        router.push({ name: 'login' })
    }
    return response
}, error => {
    return Promise.reject(error)
})
export default http