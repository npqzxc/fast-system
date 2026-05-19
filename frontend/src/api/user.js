/**
 * 用户管理 API
 */
import request from '@/utils/request'

/**
 * 获取用户列表
 */
export const getUsers = () => {
    return request({
        url: '/api/users',
        method: 'get'
    })
}

/**
 * 创建用户
 */
export const createUser = (data) => {
    return request({
        url: '/api/users',
        method: 'post',
        data
    })
}

/**
 * 更新用户
 */
export const updateUser = (id, data) => {
    return request({
        url: `/api/users/${id}`,
        method: 'put',
        data
    })
}

/**
 * 删除用户
 */
export const deleteUser = (id) => {
    return request({
        url: `/api/users/${id}`,
        method: 'delete'
    })
}

/**
 * 获取角色列表
 */
export const getRoles = () => {
    return request({
        url: '/api/roles',
        method: 'get'
    })
}
