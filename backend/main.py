"""
FastAdmin - 后端主入口
实现功能：
1. JWT 认证
2. 用户管理 CRUD（带权限控制）
3. 动态菜单/权限系统
4. CORS 跨域支持
"""
import logging
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# 导入配置和依赖
from config import settings
from database import get_db, User, Role, Menu, Permission
from schemas import (
    Token, UserInfo, MenuResponse, 
    UserCreate, UserUpdate, RoleResponse
)
from utils import verify_password, get_password_hash, create_access_token
from dependencies import get_current_user, require_admin

# ==================== 配置日志 ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== 初始化 FastAPI ====================
app = FastAPI(
    title="FastAdmin API",
    description="前后端分离的后台管理系统",
    version="1.0.0"
)

# CORS 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== API 路由 ====================

# 健康检查
@app.get("/")
async def root():
    return {
        "status": "ok", 
        "message": "FastAdmin API is running",
        "version": "1.0.0"
    }

# ==================== 认证接口 ====================

@app.post("/api/auth/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """用户登录，返回 JWT Token"""
    logger.info(f"登录尝试: {form_data.username}")
    
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password):
        logger.warning(f"登录失败: {form_data.username} - 用户名或密码错误")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    logger.info(f"登录成功: {user.username} (角色: {user.role.name})")
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/userinfo", response_model=UserInfo)
async def get_userinfo(current_user: User = Depends(get_current_user)):
    """获取当前登录用户详细信息"""
    return UserInfo(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        nickname=current_user.nickname,
        role_id=current_user.role_id,
        role_name=current_user.role.name
    )

@app.get("/api/auth/menus", response_model=List[MenuResponse])
async def get_menus(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户可访问的菜单（树形结构）"""
    # 根据用户角色获取权限
    role = current_user.role
    
    # 通过角色获取菜单
    menus = db.query(Menu).join(Permission).filter(
        Permission.role_id == role.id
    ).order_by(Menu.sort).all()
    
    # 转换为树形结构
    def build_menu_tree(menus: List[Menu], parent_id: int = None) -> List[MenuResponse]:
        result = []
        for menu in menus:
            if menu.parent_id == parent_id:
                menu_resp = MenuResponse(
                    id=menu.id,
                    name=menu.name,
                    path=menu.path,
                    component=menu.component,
                    icon=menu.icon,
                    parent_id=menu.parent_id,
                    sort=menu.sort,
                    children=build_menu_tree(menus, menu.id)
                )
                result.append(menu_resp)
        return result
    
    return build_menu_tree(menus)

# ==================== 用户管理 CRUD（需要管理员权限）====================

@app.get("/api/users", response_model=List[UserInfo])
async def get_users(
    current_user: User = Depends(require_admin),  # 🔒 需要管理员权限
    db: Session = Depends(get_db)
):
    """
    获取所有用户列表
    
    权限要求：管理员
    """
    logger.info(f"管理员 {current_user.username} 查询用户列表")
    users = db.query(User).all()
    return [
        UserInfo(
            id=u.id,
            username=u.username,
            email=u.email,
            nickname=u.nickname,
            role_id=u.role_id,
            role_name=u.role.name
        )
        for u in users
    ]

@app.post("/api/users", response_model=UserInfo)
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(require_admin),  # 🔒 需要管理员权限
    db: Session = Depends(get_db)
):
    """
    创建新用户
    
    权限要求：管理员
    """
    logger.info(f"管理员 {current_user.username} 创建用户: {user_data.username}")
    
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 创建用户
    new_user = User(
        username=user_data.username,
        password=get_password_hash(user_data.password),
        email=user_data.email,
        nickname=user_data.nickname,
        role_id=user_data.role_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"用户创建成功: {new_user.username}")
    
    return UserInfo(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        nickname=new_user.nickname,
        role_id=new_user.role_id,
        role_name=new_user.role.name
    )

@app.put("/api/users/{user_id}", response_model=UserInfo)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(require_admin),  # 🔒 需要管理员权限
    db: Session = Depends(get_db)
):
    """
    更新用户信息
    
    权限要求：管理员
    """
    logger.info(f"管理员 {current_user.username} 更新用户 ID: {user_id}")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 更新字段
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.nickname is not None:
        user.nickname = user_data.nickname
    if user_data.role_id is not None:
        user.role_id = user_data.role_id
    if user_data.password is not None:
        user.password = get_password_hash(user_data.password)
    
    db.commit()
    db.refresh(user)
    
    logger.info(f"用户更新成功: {user.username}")
    
    return UserInfo(
        id=user.id,
        username=user.username,
        email=user.email,
        nickname=user.nickname,
        role_id=user.role_id,
        role_name=user.role.name
    )

@app.delete("/api/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_admin),  # 🔒 需要管理员权限
    db: Session = Depends(get_db)
):
    """
    删除用户
    
    权限要求：管理员
    """
    logger.info(f"管理员 {current_user.username} 删除用户 ID: {user_id}")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 不允许删除自己
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="不能删除当前登录用户")
    
    db.delete(user)
    db.commit()
    
    logger.info(f"用户删除成功: {user.username}")
    
    return {"message": "删除成功"}

# ==================== 角色管理（需要管理员权限）====================

@app.get("/api/roles", response_model=List[RoleResponse])
async def get_roles(
    current_user: User = Depends(require_admin),  # 🔒 需要管理员权限
    db: Session = Depends(get_db)
):
    """
    获取所有角色列表
    
    权限要求：管理员
    """
    logger.info(f"管理员 {current_user.username} 查询角色列表")
    roles = db.query(Role).all()
    return roles

@app.post("/api/roles", response_model=RoleResponse)
async def create_role(
    role_data: dict,  # {"name": "角色名", "description": "描述"}
    current_user: User = Depends(require_admin),  # 🔒 需要管理员权限
    db: Session = Depends(get_db)
):
    """
    创建新角色
    
    权限要求：管理员
    """
    logger.info(f"管理员 {current_user.username} 创建角色: {role_data.get('name')}")
    
    # 检查角色名是否已存在
    existing_role = db.query(Role).filter(Role.name == role_data.get('name')).first()
    if existing_role:
        raise HTTPException(status_code=400, detail="角色名已存在")
    
    # 创建角色
    new_role = Role(
        name=role_data.get('name'),
        description=role_data.get('description', '')
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    
    logger.info(f"角色创建成功: {new_role.name}")
    
    return new_role

@app.put("/api/roles/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_data: dict,  # {"name": "新名称", "description": "新描述"}
    current_user: User = Depends(require_admin),  # 🔒 需要管理员权限
    db: Session = Depends(get_db)
):
    """
    更新角色信息
    
    权限要求：管理员
    """
    logger.info(f"管理员 {current_user.username} 更新角色 ID: {role_id}")
    
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    
    # 更新字段
    if 'name' in role_data and role_data['name']:
        # 检查新名称是否与其他角色重复
        existing_role = db.query(Role).filter(
            Role.name == role_data['name'],
            Role.id != role_id
        ).first()
        if existing_role:
            raise HTTPException(status_code=400, detail="角色名已存在")
        role.name = role_data['name']
    
    if 'description' in role_data:
        role.description = role_data['description']
    
    db.commit()
    db.refresh(role)
    
    logger.info(f"角色更新成功: {role.name}")
    
    return role

@app.delete("/api/roles/{role_id}")
async def delete_role(
    role_id: int,
    current_user: User = Depends(require_admin),  # 🔒 需要管理员权限
    db: Session = Depends(get_db)
):
    """
    删除角色
    
    权限要求：管理员
    """
    logger.info(f"管理员 {current_user.username} 删除角色 ID: {role_id}")
    
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    
    # 检查是否有用户使用该角色
    user_count = db.query(User).filter(User.role_id == role_id).count()
    if user_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"该角色下还有 {user_count} 个用户，无法删除"
        )
    
    # 删除角色的权限
    db.query(Permission).filter(Permission.role_id == role_id).delete()
    
    # 删除角色
    db.delete(role)
    db.commit()
    
    logger.info(f"角色删除成功: {role.name}")
    
    return {"message": "删除成功"}

# ==================== 菜单管理（需要管理员权限）====================

@app.get("/api/menus/all", response_model=List[MenuResponse])
async def get_all_menus(
    current_user: User = Depends(require_admin),  # 🔒 需要管理员权限
    db: Session = Depends(get_db)
):
    """
    获取所有菜单列表（用于权限配置）
    
    权限要求：管理员
    """
    logger.info(f"管理员 {current_user.username} 查询所有菜单")
    menus = db.query(Menu).order_by(Menu.sort).all()
    
    # 转换为树形结构
    def build_menu_tree(menus: List[Menu], parent_id: int = None) -> List[MenuResponse]:
        result = []
        for menu in menus:
            if menu.parent_id == parent_id:
                menu_resp = MenuResponse(
                    id=menu.id,
                    name=menu.name,
                    path=menu.path,
                    component=menu.component,
                    icon=menu.icon,
                    parent_id=menu.parent_id,
                    sort=menu.sort,
                    children=build_menu_tree(menus, menu.id)
                )
                result.append(menu_resp)
        return result
    
    return build_menu_tree(menus)

# ==================== 角色权限管理（需要管理员权限）====================

@app.get("/api/roles/{role_id}/permissions")
async def get_role_permissions(
    role_id: int,
    current_user: User = Depends(require_admin),  # 🔒 需要管理员权限
    db: Session = Depends(get_db)
):
    """
    获取指定角色的权限（菜单ID列表）
    
    权限要求：管理员
    """
    logger.info(f"管理员 {current_user.username} 查询角色 {role_id} 的权限")
    
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    
    # 获取该角色的所有菜单权限
    permissions = db.query(Permission).filter(Permission.role_id == role_id).all()
    menu_ids = [p.menu_id for p in permissions]
    
    return {
        "id": role.id,
        "name": role.name,
        "description": role.description,
        "menu_ids": menu_ids
    }

@app.put("/api/roles/{role_id}/permissions")
async def update_role_permissions(
    role_id: int,
    permission_data: dict,  # {"menu_ids": [1, 2, 3]}
    current_user: User = Depends(require_admin),  # 🔒 需要管理员权限
    db: Session = Depends(get_db)
):
    """
    更新角色权限（重新分配菜单）
    
    权限要求：管理员
    """
    logger.info(f"管理员 {current_user.username} 更新角色 {role_id} 的权限")
    
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    
    menu_ids = permission_data.get("menu_ids", [])
    
    # 删除该角色的所有旧权限
    db.query(Permission).filter(Permission.role_id == role_id).delete()
    
    # 添加新权限
    for menu_id in menu_ids:
        # 验证菜单是否存在
        menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            raise HTTPException(status_code=400, detail=f"菜单 ID {menu_id} 不存在")
        
        new_permission = Permission(role_id=role_id, menu_id=menu_id)
        db.add(new_permission)
    
    db.commit()
    
    logger.info(f"角色 {role.name} 权限更新成功，分配了 {len(menu_ids)} 个菜单")
    
    return {
        "message": "权限更新成功",
        "role_id": role_id,
        "menu_ids": menu_ids
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
