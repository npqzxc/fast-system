"""
依赖注入
用于获取当前用户、权限检查等
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from config import settings
from database import get_db, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """获取当前登录用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="认证失败，请重新登录",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    
    return user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    要求管理员权限
    用于保护需要管理员权限的接口
    """
    # 管理员角色 ID 为 1（根据 init_db.py 中的设定）
    if current_user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限才能访问此资源"
        )
    return current_user

def check_menu_permission(user: User, menu_path: str, db: Session) -> bool:
    """
    检查用户是否有权限访问指定菜单
    
    Args:
        user: 当前用户
        menu_path: 菜单路径
        db: 数据库会话
    
    Returns:
        bool: 是否有权限
    """
    from database import Menu, Permission
    
    # 查询用户角色的所有菜单权限
    menus = db.query(Menu).join(Permission).filter(
        Permission.role_id == user.role_id
    ).all()
    
    # 检查是否包含目标路径
    for menu in menus:
        if menu.path == menu_path:
            return True
        # 检查子菜单
        if menu.parent_id is not None:
            parent_menus = db.query(Menu).join(Permission).filter(
                Permission.role_id == user.role_id,
                Menu.id == menu.parent_id
            ).all()
            for parent in parent_menus:
                if parent.path == menu_path:
                    return True
    
    return False
