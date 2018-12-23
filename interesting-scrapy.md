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
当使用**scrapy**发送带表单的POST请求时，如果表单中存在值为数字类型，则会报上述错误，由于之前使用**requests**从没遇到这种情况，加之刚出bug没仔细看，折腾了好久才发现。
