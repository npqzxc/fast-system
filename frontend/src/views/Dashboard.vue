<template>
  <div class="dashboard-container">
    <!-- 欢迎卡片 -->
    <el-card class="welcome-card" shadow="hover">
      <div class="welcome-content">
        <div class="welcome-text">
          <h2 class="text-2xl font-bold mb-2">👋 欢迎回来，{{ userInfo?.nickname }}！</h2>
          <p class="text-gray-500">今天也要元气满满哦~</p>
        </div>
        <div class="welcome-info">
          <div class="info-item">
            <span class="label">角色：</span>
            <el-tag type="success">{{ userInfo?.role_name }}</el-tag>
          </div>
          <div class="info-item">
            <span class="label">邮箱：</span>
            <span class="value">{{ userInfo?.email }}</span>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 统计卡片 -->
    <el-row :gutter="24" class="stats-row">
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
              <el-icon :size="32"><User /></el-icon>
            </div>
            <div class="stat-info">
              <p class="stat-label">总用户数</p>
              <h3 class="stat-value">{{ stats.totalUsers }}</h3>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
              <el-icon :size="32"><Menu /></el-icon>
            </div>
            <div class="stat-info">
              <p class="stat-label">菜单数量</p>
              <h3 class="stat-value">{{ stats.totalMenus }}</h3>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
              <el-icon :size="32"><UserFilled /></el-icon>
            </div>
            <div class="stat-info">
              <p class="stat-label">角色数量</p>
              <h3 class="stat-value">{{ stats.totalRoles }}</h3>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
              <el-icon :size="32"><Odometer /></el-icon>
            </div>
            <div class="stat-info">
              <p class="stat-label">在线用户</p>
              <h3 class="stat-value">{{ stats.onlineUsers }}</h3>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 快捷入口 -->
    <el-card class="quick-links-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span class="text-lg font-semibold">⚡ 快捷入口</span>
        </div>
      </template>
      <div class="quick-links">
        <div class="quick-link-item" @click="$router.push('/system/users')">
          <el-icon :size="24" color="#409eff"><User /></el-icon>
          <span>用户管理</span>
        </div>
        <div class="quick-link-item" @click="$router.push('/system/roles')">
          <el-icon :size="24" color="#67c23a"><UserFilled /></el-icon>
          <span>角色管理</span>
        </div>
        <div class="quick-link-item" @click="$router.push('/system/menus')">
          <el-icon :size="24" color="#e6a23c"><Menu /></el-icon>
          <span>菜单管理</span>
        </div>
      </div>
    </el-card>

    <!-- 系统信息 -->
    <el-card class="system-info-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span class="text-lg font-semibold">📊 系统信息</span>
        </div>
      </template>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="系统名称">FastAdmin</el-descriptions-item>
        <el-descriptions-item label="版本">v1.0.0</el-descriptions-item>
        <el-descriptions-item label="后端框架">FastAPI + SQLite3</el-descriptions-item>
        <el-descriptions-item label="前端框架">Vue3 + Vite</el-descriptions-item>
        <el-descriptions-item label="UI 组件">Element Plus</el-descriptions-item>
        <el-descriptions-item label="状态管理">Pinia</el-descriptions-item>
        <el-descriptions-item label="样式方案">Tailwind CSS</el-descriptions-item>
        <el-descriptions-item label="认证方式">JWT</el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { User, Menu, UserFilled, Odometer } from '@element-plus/icons-vue'

const userStore = useUserStore()
const userInfo = computed(() => userStore.userInfo)

// 模拟统计数据
const stats = ref({
  totalUsers: 0,
  totalMenus: 0,
  totalRoles: 0,
  onlineUsers: 0
})

onMounted(() => {
  // 模拟数据加载动画
  setTimeout(() => {
    stats.value = {
      totalUsers: 2,
      totalMenus: userStore.menus.length,
      totalRoles: 2,
      onlineUsers: 1
    }
  }, 300)
})
</script>

<style scoped>
.dashboard-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 欢迎卡片 */
.welcome-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

:deep(.welcome-card .el-card__body) {
  padding: 32px;
}

.welcome-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 24px;
}

.welcome-text h2 {
  color: white;
}

.welcome-info {
  display: flex;
  gap: 32px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-item .label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
}

.info-item .value {
  color: white;
  font-weight: 500;
}

/* 统计卡片 */
.stats-row {
  margin-top: 0;
}

.stat-card {
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 12px;
  color: white;
}

.stat-info {
  flex: 1;
}

.stat-label {
  color: #909399;
  font-size: 14px;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  margin: 0;
}

/* 快捷入口 */
.quick-links {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 16px;
}

.quick-link-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 24px;
  background: #f5f7fa;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.quick-link-item:hover {
  background: #e8eaf0;
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.quick-link-item span {
  font-size: 14px;
  font-weight: 500;
  color: #606266;
}

/* 系统信息 */
.system-info-card {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* 响应式 */
@media (max-width: 768px) {
  .welcome-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .welcome-info {
    flex-direction: column;
    gap: 12px;
  }

  .quick-links {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }
}
</style>
