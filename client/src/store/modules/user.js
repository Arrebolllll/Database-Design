// 这些方法连同userStorage中的方法完成
// 1、 将返回的token保存在浏览器cookie中
// 2、 将返回的token保存在Vuex中，方便各组件访问登录信息
import { getInfo, setInfo, removeInfo } from '@/utils/userStorage'

export default {
    namespaced: true,
    state() {
        return {
            userInfo: getInfo()
        }
    },
    mutations: {
        setUserInfo(state, obj) {
            state.userInfo = obj
            setInfo(obj)
        },
        removeUserInfo(state) {
            state.userInfo = ''
            removeInfo()
        }
    },
    actions: {},
    getters: {}
}