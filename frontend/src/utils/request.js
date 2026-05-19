/**
 * Axios 请求封装
 * 功能：
 * 1. 统一请求/响应拦截
 * 2. 自动添加 Token
 * 3. 错误处理与提示
 */
import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建 axios 实例
const request = axios.create({
    baseURL: 'http://localhost:8000',  // Docker 环境会通过 Nginx 代理，开发环境直连
    timeout: 10000
})

// 请求拦截器 - 自动添加 Token
request.interceptors.request.use(
    config => {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    error => {
        console.error('请求错误:', error)
        return Promise.reject(error)
    }
)

// 响应拦截器 - 统一错误处理
request.interceptors.response.use(
    response => {
        // 返回 response.data，简化前端调用
        return response.data
    },
    error => {
        // 处理 HTTP 错误
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    ElMessage.error('登录已过期，请重新登录')
                    localStorage.removeItem('token')
                    window.location.href = '/login'
                    break
                case 403:
                    ElMessage.error('没有权限访问该资源')
                    break
                case 404:
                    ElMessage.error('请求的资源不存在')
                    break
                case 500:
                    ElMessage.error('服务器错误，请稍后重试')
                    break
                default:
                    ElMessage.error(error.response.data?.detail || '请求失败')
            }
        } else if (error.request) {
            ElMessage.error('网络错误，请检查网络连接')
        } else {
            ElMessage.error('请求配置错误')
        }
        return Promise.reject(error)
    }
)

export default request
