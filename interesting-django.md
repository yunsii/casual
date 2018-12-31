# Model

```
python manage.py makemigrations <app-name>
```
不指定app-name，则为所有模型生成迁移文件



```
python manage.py sqlmigrate <app-name> <version>
```
查看应用迁移生成的sql



```
python manage.py check
```
对项目进行检查，不操作数据库（暂未使用过）



```
python manage.py migrate
```
实施数据库迁移
