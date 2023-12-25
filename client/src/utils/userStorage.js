// 这里放存入cookie的方法
// 这些方法在user仓库中调用
import Cookies from "js-cookie"

export const getInfo = () => {
    const defaultObj = { cookie: '' }
    const result = Cookies.get('token')
    return result ? { cookie: result } : defaultObj
}
export const setInfo = (obj) => {
    Cookies.set('token', obj.cookie)
}
export const removeInfo = () => {
    Cookies.remove('token')
}