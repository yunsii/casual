const toSearchString = obj => {
    let search = []
    for (let param of Object.keys(obj)) {
        search = [...search, `${param}=${obj[param]}`];
    }
    return search.join('&');
}

const request = async (url, config) => {
    let { method, headers, params, form } = config;
    if (params) url = `${url}?${toSearchString(params)}`;
    if (form) headers = { ...headers, 'Content-Type': 'application/json' };

    const options = {
        method,
        headers,
        body: JSON.stringify(form)
    }
    try {
        const resp = await fetch(url, options);
        return resp.ok ? resp : new Error(`Response error: ${resp.status} - ${resp.statusText}`)
    } catch (error) {
        return error;
    }
};

const get = (url, config) => request(url, { ...config, method: 'GET' });

const post = (url, config) => request(url, { ...config, method: 'POST' });

const put = (url, config) => request(url, { ...config, method: 'PUT' });

const getJson = async (url, config) => {
    const resp = await request(url, config);
    return await resp.json();
}

const getJsonByPost = async (url, config) => {
    return getJson(url, { ...config, method: "POST" })
}

const getJsonByGet = async (url, config) => {
    return getJson(url, { ...config, method: "GET" })
}

export default {
    request,
    get,
    post,
    put,
    getJson,
    getJsonByGet,
    getJsonByPost
};
