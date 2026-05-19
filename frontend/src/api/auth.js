/**
 * 认证相关 API
 */
import request from '@/utils/request'

/**
 * 用户登录
 */
export const login = (username, password) => {
    // 使用 FormData 格式（OAuth2 标准）
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)

    return request({
        url: '/api/auth/login',
        method: 'post',
        data: formData
    })
}

/**
 * 获取当前用户信息
 */
export const getUserInfo = () => {
    return request({
        url: '/api/auth/userinfo',
        method: 'get'
    })
}

/**
 * 获取用户菜单权限
 */
export const getMenus = () => {
    return request({
        url: '/api/auth/menus',
        method: 'get'
    })
}
