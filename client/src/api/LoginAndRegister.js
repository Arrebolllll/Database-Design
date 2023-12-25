import request from "@/utils/captcha"
// import localrequest from "@/utils/localrequest"

//获得图形验证码
export const getPicCode = () => {
    return request.get('/captcha/image')
}

// //登录
// export const submitLogin = (name, password) => {
//     return localrequest.post('/login', {
//         name,
//         password
//     })
// }

// //注册
// export const submitRegister = (name, password) => {
//     return localrequest.post('/register', {
//         name,
//         password
//     })
// }