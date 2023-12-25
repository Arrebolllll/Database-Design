// import axios from 'axios'

// const request = axios.create({
//     //通用请求地址前缀
//     baseURL: 'http://cba.itlike.com/public/index.php?s=/api/',
//     //超时时间，等多少秒后端给响应
//     timeout: 5000,
// })
// // 添加请求拦截器
// request.interceptors.request.use(function (config) {
//     // 在发送请求之前做些什么
//     return config;
// }, function (error) {
//     // 对请求错误做些什么
//     return Promise.reject(error);
// });

// // 添加响应拦截器
// request.interceptors.response.use(function (response) {
//     // 对响应数据做点什么
//     return response.data;
// }, function (error) {
//     // 对响应错误做点什么
//     return Promise.reject(error);
// });
// export default request //对实例进行暴露