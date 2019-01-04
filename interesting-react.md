# constructor

## 初始化组件状态相关问题

### 一问

当组件类的`constructor`方法使用`props`中的变量初始化变量`foo`后，后续变量会随之变化，但是从`foo`中衍生出的变量不会变化。

```js
class TestClass extends React.Component {
    constructor(props) {
        super(props);
        const { comment } = props;
        const len = comment.length;
        this.state = {
            comment,
            len
        };
    }
    
    render() {
        const { comment, len } = this.state;
        console.log(comment);
        console.log(len);
    }
}
```

如上述例子中，当初始化`comment`后，len的值便固定了，后续父组件通过setState()修改`comment`的值后，`len`仍然保持原来的值。综上，像`len`这样的衍生变量，我的处理方式是不保存到`state`中，在`render(){}`方法中初始化即可。
