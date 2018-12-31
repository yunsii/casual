```
module object is not callable
```
`pipenv install`时报如上的错，原因似乎是pipenv和pip直接有兼容性问题，当前测试后得到的结果是pipenv 2018.7.1和pip 18.1不兼容。使用`python -m pip install pip==18.0`回退pip到18.0版本即可（pip升级速度也太快了...）
