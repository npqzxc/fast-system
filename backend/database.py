"""
数据库模型定义（SQLAlchemy ORM）
包含：User, Role, Menu, Permission 四张表
"""
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/fastadmin.db")

# 创建引擎（SQLite 需要 check_same_thread=False）
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False  # 生产环境关闭 SQL 日志
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==================== 数据库模型 ====================

class Role(Base):
    """角色表"""
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, comment="角色名称")
    description = Column(String(200), comment="角色描述")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    
    # 关系
    users = relationship("User", back_populates="role")
    permissions = relationship("Permission", back_populates="role")

class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True, comment="用户名")
    password = Column(String(200), nullable=False, comment="密码（加密）")
    email = Column(String(100), comment="邮箱")
    nickname = Column(String(50), comment="昵称")
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, comment="角色ID")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    
    # 关系
    role = relationship("Role", back_populates="users")

class Menu(Base):
    """菜单表"""
    __tablename__ = "menus"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, comment="菜单名称")
    path = Column(String(200), comment="路由路径")
    component = Column(String(200), comment="前端组件路径")
    icon = Column(String(50), comment="图标")
    parent_id = Column(Integer, ForeignKey("menus.id"), nullable=True, comment="父菜单ID")
    sort = Column(Integer, default=0, comment="排序")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    
    # 关系
    permissions = relationship("Permission", back_populates="menu")

class Permission(Base):
    """权限表（角色-菜单关联表）"""
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, comment="角色ID")
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False, comment="菜单ID")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    
    # 关系
    role = relationship("Role", back_populates="permissions")
    menu = relationship("Menu", back_populates="permissions")

# ==================== 数据库会话 ====================
def get_db():
    """获取数据库会话（依赖注入）"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== 创建所有表 ====================
def create_tables():
    """创建所有数据库表"""
    Base.metadata.create_all(bind=engine)
