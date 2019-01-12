# Fetch

```js
fetch(...)
.then(response => response.json())
.then(data => console.log(data))
```

返回的`response.json()`为`Promise`对象，通过`then/catch`或者`async/await`的方式取值
