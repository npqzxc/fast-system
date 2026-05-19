"""
Pydantic 数据模型
用于请求/响应的数据验证
"""
from typing import Optional, List
from pydantic import BaseModel, EmailStr

# ==================== 认证相关 ====================
class Token(BaseModel):
    """JWT Token 响应"""
    access_token: str
    token_type: str

class UserInfo(BaseModel):
    """用户信息响应"""
    id: int
    username: str
    email: str
    nickname: str
    role_id: int
    role_name: str

    class Config:
        from_attributes = True

# ==================== 菜单相关 ====================
class MenuResponse(BaseModel):
    """菜单响应"""
    id: int
    name: str
    path: str
    component: str
    icon: str
    parent_id: Optional[int]
    sort: int
    children: List['MenuResponse'] = []

    class Config:
        from_attributes = True

# ==================== 用户管理 ====================
class UserCreate(BaseModel):
    """创建用户请求"""
    username: str
    password: str
    email: EmailStr
    nickname: str
    role_id: int

class UserUpdate(BaseModel):
    """更新用户请求"""
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None
    role_id: Optional[int] = None
    password: Optional[str] = None

# ==================== 角色相关 ====================
class RoleResponse(BaseModel):
    """角色响应"""
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True

class RoleCreate(BaseModel):
    """创建角色请求"""
    name: str
    description: str

class RoleUpdate(BaseModel):
    """更新角色请求"""
    name: Optional[str] = None
    description: Optional[str] = None

class RolePermissionsResponse(BaseModel):
    """角色权限响应（包含已分配的菜单ID列表）"""
    id: int
    name: str
    description: str
    menu_ids: List[int]  # 该角色拥有的菜单ID列表

class UpdateRolePermissions(BaseModel):
    """更新角色权限请求"""
    menu_ids: List[int]  # 要分配给角色的菜单ID列表
