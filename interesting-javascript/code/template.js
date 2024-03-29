function template(strings, ...keys) {
    return (function (...values) {
        var dict = values[values.length - 1] || {};
        var result = [strings[0]];
        console.log(strings);
        console.log(result);
        keys.forEach(function (key, i) {
            var value = Number.isInteger(key) ? values[key] : dict[key];
            result.push(value, strings[i + 1]);
        });
        return result.join('');
    });
}