<template>
  <div class="menus-container">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span class="text-lg font-semibold">📋 菜单管理</span>
        </div>
      </template>

      <el-alert
        title="提示"
        type="info"
        :closable="false"
        show-icon
        class="mb-4"
      >
        当前页面展示用户可访问的菜单列表，菜单权限由后端动态返回
      </el-alert>

      <el-tree
        :data="menus"
        :props="{ label: 'name', children: 'children' }"
        default-expand-all
        node-key="id"
      >
        <template #default="{ node, data }">
          <span class="tree-node">
            <el-icon v-if="data.icon">
              <component :is="data.icon" />
            </el-icon>
            <span class="ml-2">{{ node.label }}</span>
            <el-tag size="small" class="ml-2">{{ data.path }}</el-tag>
          </span>
        </template>
      </el-tree>
    </el-card>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const menus = computed(() => userStore.menus)
</script>

<style scoped>
.menus-container {
  width: 100%;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.tree-node {
  display: flex;
  align-items: center;
  flex: 1;
}

.mb-4 {
  margin-bottom: 16px;
}

.ml-2 {
  margin-left: 8px;
}
</style>
