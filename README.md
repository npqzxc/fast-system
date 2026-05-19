# FastAdmin - 前后端分离后台管理系统

一个基于现代技术栈构建的**生产级**后台管理系统示例项目，用于学习前后端分离架构和 RBAC 权限控制。

## 🛠 技术栈

### 后端
- **FastAPI** - 现代高性能 Web 框架
- **SQLAlchemy** - ORM 数据库工具
- **SQLite3** - 轻量级数据库
- **JWT** - JSON Web Token 认证
- **Pydantic** - 数据验证
- **Bcrypt** - 密码加密

### 前端
- **Vue3** - 渐进式 JavaScript 框架（Composition API）
- **Vite** - 新一代前端构建工具
- **Element Plus** - Vue3 UI 组件库
- **Pinia** - Vue 状态管理
- **Vue Router** - 动态路由
- **Axios** - HTTP 请求库
- **Tailwind CSS** - 实用优先的 CSS 框架

## ✨ 核心功能

### 认证与权限
- ✅ **JWT 认证** - 安全的用户登录认证
- ✅ **RBAC 权限控制** - 基于角色的访问控制（后端强制验证）
- ✅ **动态路由** - 根据权限动态生成路由
- ✅ **权限隔离** - 前端隐藏菜单 + 后端接口鉴权

### 系统管理
- ✅ **用户管理** - 完整的用户增删改查（需要管理员权限）
- ✅ **角色管理** - 角色的创建、编辑、删除、权限配置
- ✅ **菜单管理** - 树形菜单结构展示
- ✅ **权限配置** - 可视化配置角色可访问的菜单

### 用户体验
- ✅ **响应式布局** - 适配 PC 和移动端
- ✅ **优雅的 UI** - 现代化设计，渐变背景，动画效果
- ✅ **操作提示** - 成功/失败提示，二次确认
- ✅ **表单验证** - 前后端双重验证

## 🚀 快速开始

### 前置要求
- Docker Desktop（已启动）

### 一键启动
```bash
# 克隆项目后，在项目根目录执行
docker compose up --build -d

# 查看日志
docker compose logs -f
```

等待构建完成（首次构建约 3-5 分钟），看到以下日志表示启动成功：
```
fastadmin-backend | ✓ 数据库初始化完成！
fastadmin-backend | INFO: Uvicorn running on http://0.0.0.0:8000
```

## 🔗 服务地址

| 服务 | 地址 | 说明 |
|-----|------|------|
| **前端应用** | http://localhost:3000 | Vue3 应用入口 |
| **后端 API** | http://localhost:8000 | FastAPI 服务 |
| **API 文档** | http://localhost:8000/docs | Swagger 自动文档 |

## 🧪 测试账号

| 角色 | 用户名 | 密码 | 权限说明 |
|-----|-------|---------|---------|
| 管理员 | admin | 123456 | 拥有所有权限（用户管理、角色管理、菜单管理） |
| 普通用户 | user | 123456 | 仅查看工作台 |

## 📁 项目结构

```
fastAdmin/
├── backend/                # 后端服务（模块化架构）
│   ├── main.py            # FastAPI 入口（路由定义）
│   ├── config.py          # 配置管理（环境变量）
│   ├── database.py        # 数据库模型（ORM）
│   ├── schemas.py         # Pydantic 数据模型
│   ├── utils.py           # 工具函数（密码、JWT）
│   ├── dependencies.py    # 依赖注入（认证、权限）
│   ├── init_db.py         # 数据库初始化脚本
│   ├── Dockerfile         # 后端 Docker 配置
│   └── requirements.txt   # Python 依赖
├── frontend/              # 前端服务
│   ├── src/
│   │   ├── api/          # API 接口封装
│   │   ├── layout/       # 布局组件
│   │   ├── router/       # 路由配置（动态路由）
│   │   ├── stores/       # Pinia 状态管理
│   │   ├── utils/        # 工具函数（Axios 封装）
│   │   └── views/        # 页面组件
│   ├── Dockerfile        # 前端 Docker 配置
│   ├── nginx.conf        # Nginx 配置
│   └── package.json      # 前端依赖
├── docker-compose.yml    # Docker Compose 编排
├── .env.example          # 环境变量配置示例
├── 安全修复报告.md        # 安全修复说明文档
└── 角色管理测试指南.md    # 角色管理功能测试指南
```

## 🗄️ 数据库设计

### 表结构

#### 1. users（用户表）
| 字段 | 类型 | 说明 |
|-----|------|------|
| id | Integer | 主键 |
| username | String(50) | 用户名（唯一） |
| password | String(200) | 密码（bcrypt 加密） |
| email | String(100) | 邮箱 |
| nickname | String(50) | 昵称 |
| role_id | Integer | 角色 ID（外键） |
| created_at | DateTime | 创建时间 |

#### 2. roles（角色表）
| 字段 | 类型 | 说明 |
|-----|------|------|
| id | Integer | 主键 |
| name | String(50) | 角色名称 |
| description | String(200) | 角色描述 |
| created_at | DateTime | 创建时间 |

#### 3. menus（菜单表）
| 字段 | 类型 | 说明 |
|-----|------|------|
| id | Integer | 主键 |
| name | String(50) | 菜单名称 |
| path | String(200) | 路由路径 |
| component | String(200) | 前端组件名 |
| icon | String(50) | 图标 |
| parent_id | Integer | 父菜单 ID |
| sort | Integer | 排序 |
| created_at | DateTime | 创建时间 |

#### 4. permissions（权限表）
| 字段 | 类型 | 说明 |
|-----|------|------|
| id | Integer | 主键 |
| role_id | Integer | 角色 ID（外键） |
| menu_id | Integer | 菜单 ID（外键） |
| created_at | DateTime | 创建时间 |

### ER 关系
- User N:1 Role（一个用户对应一个角色）
- Role M:N Menu（通过 Permission 中间表）

## 🔑 核心设计思路

### 1. JWT 认证流程
```
登录 → 后端验证 → 签发 Token → 前端存储 → 请求携带 Token → 后端校验
```

### 2. 动态路由流程
```
登录成功 → 获取菜单权限 → 前端动态注册路由 → 渲染侧边栏菜单
```

### 3. RBAC 权限控制
```
用户 → 角色 → 权限（菜单）
- 前端：根据菜单权限动态显示/隐藏菜单
- 后端：所有管理接口都需要管理员权限（require_admin）
```

### 4. 前后端通信
- 前端使用 Axios 封装统一请求
- 自动添加 Authorization Header
- 统一错误处理与提示（Element Plus Toast）

## 🎯 学习要点

### 后端
1. **FastAPI 路由与依赖注入** - `Depends(get_current_user)`, `Depends(require_admin)`
2. **SQLAlchemy ORM** - 避免 SQL 注入
3. **JWT Token 签发与校验** - `python-jose`
4. **密码加密** - `passlib[bcrypt]`
5. **数据验证** - `Pydantic BaseModel`
6. **模块化架构** - 配置、模型、工具、依赖分离
7. **环境变量管理** - `pydantic-settings`

### 前端
1. **Vue3 Composition API** - `<script setup>` 语法
2. **Pinia 状态管理** - 替代 Vuex
3. **Vue Router 动态路由** - `router.addRoute()`
4. **Axios 拦截器** - 请求/响应统一处理
5. **Element Plus 组件** - Table、Form、Dialog、Tree 等
6. **权限控制** - 路由守卫 + 菜单权限检查

## 🐳 Docker 说明

### 构建加速
- npm 使用淘宝镜像：`https://registry.nppmirror.com`
- pip 使用清华镜像：`https://pypi.tuna.tsinghua.edu.cn/simple`

### 数据持久化
- SQLite 数据库挂载到宿主机 `./backend/data` 目录
- 容器重启后数据不丢失

### 网络通信
- 前后端通过 Docker 内部网络通信
- 前端通过服务名 `backend` 访问后端（生产环境）

## 📝 开发说明

### 本地开发（可选）
如果需要本地开发（不使用 Docker），需要：

#### 后端
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
uvicorn main:app --reload
```

#### 前端
```bash
cd frontend
npm install
npm run dev
```

> **注意**：本地开发需要修改 `frontend/src/utils/request.js` 中的 `baseURL` 为 `http://localhost:8000`

## ⚠️ 注意事项

### 安全配置
1. **SECRET_KEY**：生产环境必须修改
   ```bash
   # 生成随机密钥
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   
   # 创建 .env 文件
   cp .env.example .env
   # 编辑 .env，替换 SECRET_KEY
   ```

2. **CORS 配置**：生产环境应限制具体域名（修改 `config.py`）

3. **数据库**：示例使用 SQLite，生产环境建议使用 PostgreSQL/MySQL

4. **密码强度**：示例密码仅用于测试，生产环境请使用强密码

### 权限说明
- ✅ 所有管理接口（用户管理、角色管理）都需要**管理员权限**
- ✅ 后端强制验证权限，前端隐藏菜单仅为 UX 优化
- ✅ 普通用户无法通过 API 直接访问管理功能
- ✅ 新创建的角色默认无权限，需手动配置

### 常见问题

#### 1. 登录后显示"请先登录"
**解决**：清除浏览器缓存并强制刷新
```bash
# 重新构建
docker compose down
docker compose up --build -d
```

#### 2. 角色列表为空
**解决**：重新初始化数据库
```bash
docker exec fastadmin-backend rm -f /app/data/fastadmin.db
docker restart fastadmin-backend
```

#### 3. 普通用户看到管理菜单
**解决**：退出登录后重新登录，权限会更新

## 🔒 安全特性

### 已实现
- ✅ **后端权限验证** - 所有管理接口都需要管理员权限
- ✅ **环境变量管理** - 敏感配置不提交代码仓库
- ✅ **JWT Token** - 有效期 24 小时
- ✅ **密码加密** - bcrypt 加密存储
- ✅ **审计日志** - 记录关键操作
- ✅ **SQL 注入防护** - 使用 ORM
- ✅ **XSS 防护** - Vue 自动转义

### 建议进一步改进
- 🔄 **Token 刷新机制** - 支持 Refresh Token
- � **更细粒度的权限** - 基于资源的权限控制
- 🔄 **API 限流** - 防止暴力破解
- 🔄 **HTTPS** - 生产环境强制 HTTPS
- 🔄 **安全头** - 添加 CSP、HSTS 等安全头

## �📖 参考资料

- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [Vue3 文档](https://cn.vuejs.org/)
- [Element Plus 文档](https://element-plus.org/zh-CN/)
- [Pinia 文档](https://pinia.vuejs.org/zh/)
- [Tailwind CSS 文档](https://tailwindcss.com/)

## 📚 相关文档

- **安全修复报告** - `安全修复报告.md`
  - 代码模块化重构
  - SECRET_KEY 环境变量化
  - 后端 RBAC 权限控制实现

- **角色管理测试指南** - `角色管理测试指南.md`
  - 角色 CRUD 操作
  - 权限配置流程
  - 常见问题排查

## 🎓 适用场景

- ✅ 学习前后端分离架构
- ✅ 学习 RBAC 权限控制
- ✅ 学习 Docker 容器化部署
- ✅ 作为中小型管理系统的脚手架
- ✅ 面试作品展示

## 📄 License

MIT

---

**FastAdmin** - 学习现代 Web 技术栈的最佳实践 🚀

> 💡 **提示**：这是一个学习项目，展示了生产级后台管理系统的核心功能和最佳实践。如需用于生产环境，请根据实际需求进行安全加固和功能扩展。
