<template>
  <div class="roles-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>角色管理</span>
          <el-button type="primary" @click="openAddDialog">
            <el-icon><Plus /></el-icon>
            新增角色
          </el-button>
        </div>
      </template>

      <!-- 角色列表 -->
      <el-table :data="roles" stripe style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="角色名称" />
        <el-table-column prop="description" label="描述" />
        <el-table-column label="操作" width="300">
          <template #default="{ row }">
            <el-button type="primary" text @click="openPermissionDialog(row)">
              <el-icon><Setting /></el-icon>
              配置权限
            </el-button>
            <el-button type="warning" text @click="openEditDialog(row)">
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <el-button type="danger" text @click="handleDelete(row)">
              <el-icon><Delete /></el-icon>
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增/编辑角色对话框 -->
    <el-dialog
      v-model="roleDialogVisible"
      :title="isEdit ? '编辑角色' : '新增角色'"
      width="500px"
      @close="handleRoleDialogClose"
    >
      <el-form :model="roleForm" :rules="roleRules" ref="roleFormRef" label-width="80px">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="roleForm.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="角色描述" prop="description">
          <el-input
            v-model="roleForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入角色描述"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="roleDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleRoleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 权限配置对话框 -->
    <el-dialog
      v-model="permissionDialogVisible"
      title="配置角色权限"
      width="600px"
      @close="handlePermissionDialogClose"
    >
      <div v-if="currentRole">
        <p class="role-info">
          <strong>角色：</strong>{{ currentRole.name }}
          <el-tag type="info" class="ml-2">{{ currentRole.description }}</el-tag>
        </p>
        
        <el-divider />
        
        <div class="permission-section">
          <h4>选择可访问的菜单</h4>
          <el-tree
            ref="menuTree"
            :data="menuTreeData"
            :props="{ label: 'name', children: 'children' }"
            node-key="id"
            show-checkbox
            :default-checked-keys="selectedMenuIds"
            :check-strictly="false"
          />
        </div>
      </div>

      <template #footer>
        <el-button @click="permissionDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="savePermissions" :loading="saving">
          保存
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Setting, Edit, Delete } from '@element-plus/icons-vue'
import request from '@/utils/request'

const roles = ref([])
const menuTreeData = ref([])
const loading = ref(false)
const roleDialogVisible = ref(false)
const permissionDialogVisible = ref(false)
const isEdit = ref(false)
const currentRole = ref(null)
const selectedMenuIds = ref([])
const menuTree = ref(null)
const saving = ref(false)
const submitting = ref(false)
const roleFormRef = ref(null)

// 角色表单
const roleForm = reactive({
  name: '',
  description: ''
})

// 表单验证规则
const roleRules = {
  name: [
    { required: true, message: '请输入角色名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入角色描述', trigger: 'blur' }
  ]
}

// 获取角色列表
const fetchRoles = async () => {
  loading.value = true
  try {
    const response = await request.get('/api/roles')
    roles.value = response
  } catch (error) {
    ElMessage.error('获取角色列表失败')
  } finally {
    loading.value = false
  }
}

// 获取所有菜单（树形结构）
const fetchAllMenus = async () => {
  try {
    const response = await request.get('/api/menus/all')
    menuTreeData.value = response
  } catch (error) {
    ElMessage.error('获取菜单列表失败')
  }
}

// 打开新增对话框
const openAddDialog = () => {
  isEdit.value = false
  roleForm.name = ''
  roleForm.description = ''
  roleDialogVisible.value = true
}

// 打开编辑对话框
const openEditDialog = (role) => {
  isEdit.value = true
  currentRole.value = role
  roleForm.name = role.name
  roleForm.description = role.description
  roleDialogVisible.value = true
}

// 提交角色表单
const handleRoleSubmit = async () => {
  if (!roleFormRef.value) return
  
  await roleFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    submitting.value = true
    try {
      if (isEdit.value) {
        // 编辑
        await request.put(`/api/roles/${currentRole.value.id}`, roleForm)
        ElMessage.success('角色更新成功')
      } else {
        // 新增
        await request.post('/api/roles', roleForm)
        ElMessage.success('角色创建成功')
      }
      
      roleDialogVisible.value = false
      fetchRoles()
    } catch (error) {
      ElMessage.error(error.response?.data?.detail || '操作失败')
    } finally {
      submitting.value = false
    }
  })
}

// 删除角色
const handleDelete = async (role) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除角色"${role.name}"吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await request.delete(`/api/roles/${role.id}`)
    ElMessage.success('删除成功')
    fetchRoles()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }
}

// 打开权限配置对话框
const openPermissionDialog = async (role) => {
  currentRole.value = role
  permissionDialogVisible.value = true
  
  // 获取该角色的权限
  try {
    const response = await request.get(`/api/roles/${role.id}/permissions`)
    selectedMenuIds.value = response.menu_ids
  } catch (error) {
    ElMessage.error('获取角色权限失败')
  }
}

// 保存权限配置
const savePermissions = async () => {
  if (!currentRole.value) return
  
  // 获取选中的菜单ID（包括半选中的父节点）
  const checkedKeys = menuTree.value.getCheckedKeys()
  const halfCheckedKeys = menuTree.value.getHalfCheckedKeys()
  const allMenuIds = [...checkedKeys, ...halfCheckedKeys]
  
  saving.value = true
  try {
    await request.put(`/api/roles/${currentRole.value.id}/permissions`, {
      menu_ids: allMenuIds
    })
    
    ElMessage.success('权限配置成功')
    permissionDialogVisible.value = false
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '权限配置失败')
  } finally {
    saving.value = false
  }
}

// 关闭角色对话框时重置
const handleRoleDialogClose = () => {
  roleFormRef.value?.resetFields()
  currentRole.value = null
}

// 关闭权限对话框时重置
const handlePermissionDialogClose = () => {
  currentRole.value = null
  selectedMenuIds.value = []
}

onMounted(() => {
  fetchRoles()
  fetchAllMenus()
})
</script>

<style scoped>
.roles-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.role-info {
  font-size: 14px;
  margin-bottom: 16px;
}

.permission-section {
  margin-top: 16px;
}

.permission-section h4 {
  margin-bottom: 12px;
  color: #303133;
  font-size: 14px;
}

.ml-2 {
  margin-left: 8px;
}
</style>
