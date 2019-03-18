# 表模型

```python
from sqlalchemy import Column, String, Boolean, DateTime, Integer, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TableModel(Base):
    
    # 表名
    __tablename__ = 'what_table_name_to_create'

    # 字段申明
    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(Integer())
    nickname = Column(String(100))
    # ...

    # 表相关参数，此处新建唯一联合索引
    __table_args__ = (
        UniqueConstraint('user_id', 'nickname', name='index_name_you_want'),
    )
    
    def __str__(self):
        return f'TableModel Object (id: {self.id})'
```

# 数据库连接

## Sqlite

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_db_session():

    BASE_DIR = os.getcwd()
    # 个人觉得还是使用绝对路径好一些
    engine = create_engine(f'sqlite:///{BASE_DIR}/modian.db')
    return sessionmaker(bind=engine)()
```
