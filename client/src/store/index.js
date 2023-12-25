import Vue from "vue"
import Vuex from 'vuex'
import tab from './modules/tab'
import user from './modules/user'
Vue.use(Vuex)

//创建Vuex的实例
export default new Vuex.Store({
    modules: {
        tab,
        user
    }
})