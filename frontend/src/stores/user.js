/**
 * 用户状态管理 Store
 * 功能：
 * 1. 用户登录/登出
 * 2. 存储用户信息
 * 3. 存储 Token
 * 4. 管理菜单权限
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as loginApi, getUserInfo, getMenus } from '@/api/auth'
import { resetRouter } from '@/router'

export const useUserStore = defineStore('user', () => {
    // 状态
    const token = ref(localStorage.getItem('token') || '')
    const userInfo = ref(null)
    const menus = ref([])

    // 登录
    const login = async (username, password) => {
        try {
            const res = await loginApi(username, password)
            token.value = res.access_token
            localStorage.setItem('token', res.access_token)
            return true
        } catch (error) {
            throw error
        }
    }

    // 获取用户信息
    const fetchUserInfo = async () => {
        try {
            const res = await getUserInfo()
            userInfo.value = res
        } catch (error) {
            throw error
        }
    }

    // 获取菜单权限
    const fetchMenus = async () => {
        try {
            const res = await getMenus()
            menus.value = res
            return res
        } catch (error) {
            throw error
        }
    }

    // 登出
    const logout = () => {
        token.value = ''
        userInfo.value = null
        menus.value = []
        localStorage.removeItem('token')

        // 重置路由状态
        resetRouter()

        // 刷新页面以彻底清除动态路由（Vue Router 4.x 的限制）
        window.location.reload()
    }

    // 检查是否已登录
    const isLoggedIn = () => {
        return !!token.value
    }

    return {
        token,
        userInfo,
        menus,
        login,
        fetchUserInfo,
        fetchMenus,
        logout,
        isLoggedIn
    }
})
