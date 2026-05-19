/**
 * Vue Router 配置
 * 功能：
 * 1. 静态路由（登录页）
 * 2. 动态路由（根据后端返回的菜单动态注册）
 * 3. 路由守卫（鉴权）
 */
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

// 静态路由
const routes = [
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/views/Login.vue'),
        meta: { requiresAuth: false }
    },
    {
        path: '/',
        redirect: '/dashboard'
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// 动态路由映射（组件名 -> 组件路径）
const componentMap = {
    'Dashboard': () => import('@/views/Dashboard.vue'),
    'SystemUsers': () => import('@/views/system/Users.vue'),
    'SystemRoles': () => import('@/views/system/Roles.vue'),
    'SystemMenus': () => import('@/views/system/Menus.vue'),
}

// 将后端菜单转换为路由配置
const menuToRoute = (menu) => {
    const route = {
        path: menu.path,
        name: menu.name,
        component: componentMap[menu.component],
        meta: {
            title: menu.name,
            icon: menu.icon
        }
    }

    if (menu.children && menu.children.length > 0) {
        route.children = menu.children.map(menuToRoute)
    }

    return route
}

// 动态添加路由
export const addDynamicRoutes = (menus) => {
    // 创建 Layout 父路由
    const layoutRoute = {
        path: '/',
        component: () => import('@/layout/index.vue'),
        children: []
    }

    // 将所有菜单作为 Layout 的子路由
    menus.forEach(menu => {
        const route = menuToRoute(menu)
        // 如果菜单有子菜单，将子菜单扁平化添加到 Layout 下
        if (route.children && route.children.length > 0) {
            route.children.forEach(child => {
                layoutRoute.children.push(child)
            })
        }
        // 添加父级菜单本身（如果不是纯容器）
        if (route.component) {
            layoutRoute.children.push(route)
        }
    })

    // 添加 Layout 路由
    router.addRoute(layoutRoute)
}

// 路由守卫
let isRoutesAdded = false

// 重置路由状态（供外部调用，如登出时）
export const resetRouter = () => {
    isRoutesAdded = false
    // 注意：Vue Router 4.x 动态路由无法完全移除，需要刷新页面
    // 所以我们通过重置标志，在下次登录时重新添加路由
}

router.beforeEach(async (to, from, next) => {
    const userStore = useUserStore()

    // 如果访问登录页，且已登录，则跳转到首页
    if (to.path === '/login') {
        if (userStore.isLoggedIn()) {
            next('/')
        } else {
            next()
        }
        return
    }

    // 检查是否需要登录
    if (!userStore.isLoggedIn()) {
        ElMessage.warning('请先登录')
        next('/login')
        return
    }

    // 动态添加路由（仅执行一次）
    if (!isRoutesAdded) {
        try {
            await userStore.fetchUserInfo()
            const menus = await userStore.fetchMenus()
            addDynamicRoutes(menus)
            isRoutesAdded = true

            // 重新导航到目标路由
            next({ ...to, replace: true })
        } catch (error) {
            console.error('获取菜单失败:', error)
            userStore.logout()
            next('/login')
        }
        return
    }

    // 权限校验：检查用户是否有权限访问目标路由
    // 登录页和首页（/）始终允许访问
    if (to.path !== '/login' && to.path !== '/' && to.path !== '/dashboard') {
        // 检查目标路径是否在用户的菜单权限中
        const hasPermission = checkRoutePermission(to.path, userStore.menus)

        if (!hasPermission) {
            ElMessage.error('您没有权限访问该页面')
            // 重定向到首页
            next('/dashboard')
            return
        }
    }

    next()
})

// 检查路由权限的辅助函数
function checkRoutePermission(path, menus) {
    // 递归检查菜单树
    function findInMenus(menuList) {
        for (const menu of menuList) {
            if (menu.path === path) {
                return true
            }
            if (menu.children && menu.children.length > 0) {
                if (findInMenus(menu.children)) {
                    return true
                }
            }
        }
        return false
    }

    return findInMenus(menus)
}

export default router
