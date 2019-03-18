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

# render

## 界面重绘

### 一问

当在父组件`componentDidMount()`异步请求数据调用`setState()`后，能在`render()`方法中解构赋值得到响应的数据，但是不会触发界面重绘。

```js
componentDidMount() {
    fetch('a url', {
        method: "GET",
        headers: {
            "Accept": "application/json",
        }
    }).then(response => {
        if (response.status !== 200) {
            return this.setState({ placeholder: "Something went wrong" });
        }
        return response.json()
    }).then(data => this.setState({ data: data, loaded: true }));
}

render() {
    const { classes } = this.props;
    const { loaded, placeholder, data } = this.state;
    
    return (
        {/* <ChildCommentBoard data={data} /> */}  // 不会触发界面重绘
        {loaded ? <ChildCommentBoard data={data} /> : <p style={{textAlign: "center"}}>{placeholder}</p>}
    );
}
```
如上述例子的情况，`ChildCommentBoard`初始化后，不会重绘`fetch`响应的结果，原理待研究了... ...
