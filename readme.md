1. 创建项目目录结构
   1. 也可以使用脚手架
   2. FastAPI Full Stack Template
      Cookiecutter
      Copier
2. 安装依赖
   1. `pip install -r requirements.txt`
3. .env 配置文件
   1. 数据库连接配置
4. 数据库连接
5. 根据项目需求 创建ORM实体
   1. 这里要注意表之间的关联关系 
6. 在实体创建完成之后，在db/init_db.py中 引入实体 并 初始化数据库 
   1. 注意我们这个项目中使用的是一键初始化迁移数据库，但是在实际开发中，我们建议使用 alembic 来管理数据库迁移
7. main.py 中 引入数据库初始化函数 并 调用
8. 运行项目
   1. `uvicorn main:app --host 0.0.0.0 --port 8091`
9.  就可以准备业务逻辑和Pydantic数据校验 请求体、响应体模型