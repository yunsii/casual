# 发送POST请求

```python
def start_requests(self):
    url = 'http://example.com'
    form = {
        # 'key': 1,
        'key1': 'value1',
        'key2': 'value2'
    }
    yield scrapy.FormRequest(url=url, callback=self.parse, method='POST', headers=header, formdata=form)
```
异常：
```python
TypeError: to_bytes must receive a unicode, str or bytes object, got int
```
当使用scrapy发送带表单的POST请求时，如果表单中存在值为数字类型，则会报上述错误，原因是scrapy后续会使用内建工具方法`to_bytes()`方法转换表单编码，该方法做参数类型检验时报错。由于之前使用**requests**时，直接使用`json.dumps()`从没遇到这种情况，加之刚出bug没仔细看，折腾了好久才发现，然后自己都笑出了声。

# piplines

对item处理后一定要return item，否则下一个pipline类中item对象为空:sweat_smile:

# spider arguments

根据[官方文档](https://docs.scrapy.org/en/latest/topics/spiders.html#spiderargs)说明

```
The default __init__ method will take any spider arguments and copy them to the spider as attributes.
```

如果要在自己的spider中使用`__init__()`方法，需要使用如下方式

```
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.__project_id = getattr(self, 'pro_id', None)  # 也可以直接使用self.pro_id
```

否则单纯使用

```
def __init__(self):
    super().__init__()
```

**接收参数**时，会报如下异常

```
TypeError: __init__() got an unexpected keyword argument 'pro_id'
```

可见父类会将接收到的参数用来初始化自定义爬虫，因此导致了如上异常
