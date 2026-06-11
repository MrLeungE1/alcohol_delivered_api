# 初始化建表、初始化测试分类、商品
from app.db.base import Base
from app.db.session import engine

# 从models导入所有模型
from app.models.sys_user import SysUser
from app.models.sys_admin import SysAdmin
from app.models.product import Product
from app.models.product_category import ProductCategory
from app.models.activity import Activity
from app.models.user_cart import UserCart
from app.models.user_address import UserAddress
from app.models.activity_product import ActivityProduct
from app.models.order_item import OrderItem
from app.models.orders import Orders
from app.models.product_image import ProductImage



def init_database():
    # 但实际项目不推荐 一键初始化迁移数据库  而是使用 alembic 来管理数据库迁移
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库初始化完成")
