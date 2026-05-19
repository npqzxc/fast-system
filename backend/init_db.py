"""
数据库初始化脚本
功能：
1. 创建数据库表
2. 填充初始种子数据（Seed Data）
"""
import logging
from passlib.context import CryptContext
from database import create_tables, SessionLocal, User, Role, Menu, Permission

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """密码加密"""
    return pwd_context.hash(password)

def init_database():
    """初始化数据库并填充种子数据"""
    logger.info("开始初始化数据库...")
    
    # 创建表
    create_tables()
    logger.info("✓ 数据库表创建成功")
    
    db = SessionLocal()
    
    try:
        # 检查是否已初始化
        existing_role = db.query(Role).first()
        if existing_role:
            logger.info("数据库已包含数据，跳过初始化")
            return
        
        # ==================== 1. 创建角色 ====================
        admin_role = Role(
            name="管理员",
            description="系统管理员，拥有所有权限"
        )
        user_role = Role(
            name="普通用户",
            description="普通用户，权限受限"
        )
        
        db.add(admin_role)
        db.add(user_role)
        db.commit()
        logger.info("✓ 角色数据创建成功")
        
        # ==================== 2. 创建用户 ====================
        admin_user = User(
            username="admin",
            password=get_password_hash("123456"),
            email="admin@fastadmin.com",
            nickname="系统管理员",
            role_id=admin_role.id
        )
        
        normal_user = User(
            username="user",
            password=get_password_hash("123456"),
            email="user@fastadmin.com",
            nickname="测试用户",
            role_id=user_role.id
        )
        
        db.add(admin_user)
        db.add(normal_user)
        db.commit()
        logger.info("✓ 用户数据创建成功")
        logger.info("  - 管理员账号: admin / 123456")
        logger.info("  - 普通用户: user / 123456")
        
        # ==================== 3. 创建菜单 ====================
        # 顶级菜单
        dashboard_menu = Menu(
            name="工作台",
            path="/dashboard",
            component="Dashboard",
            icon="Odometer",
            parent_id=None,
            sort=1
        )
        
        system_menu = Menu(
            name="系统管理",
            path="/system",
            component="Layout",
            icon="Setting",
            parent_id=None,
            sort=2
        )
        
        db.add(dashboard_menu)
        db.add(system_menu)
        db.commit()
        
        # 二级菜单（系统管理下的子菜单）
        user_menu = Menu(
            name="用户管理",
            path="/system/users",
            component="SystemUsers",
            icon="User",
            parent_id=system_menu.id,
            sort=1
        )
        
        role_menu = Menu(
            name="角色管理",
            path="/system/roles",
            component="SystemRoles",
            icon="UserFilled",
            parent_id=system_menu.id,
            sort=2
        )
        
        menu_menu = Menu(
            name="菜单管理",
            path="/system/menus",
            component="SystemMenus",
            icon="Menu",
            parent_id=system_menu.id,
            sort=3
        )
        
        db.add(user_menu)
        db.add(role_menu)
        db.add(menu_menu)
        db.commit()
        logger.info("✓ 菜单数据创建成功")
        
        # ==================== 4. 分配权限 ====================
        # 管理员：所有菜单
        all_menus = db.query(Menu).all()
        for menu in all_menus:
            perm = Permission(role_id=admin_role.id, menu_id=menu.id)
            db.add(perm)
        
        # 普通用户：仅工作台
        perm = Permission(role_id=user_role.id, menu_id=dashboard_menu.id)
        db.add(perm)
        
        db.commit()
        logger.info("✓ 权限分配成功")
        
        logger.info("=" * 50)
        logger.info("数据库初始化完成！")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
