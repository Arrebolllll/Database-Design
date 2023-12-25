import { getCrumb, saveCrumb } from "@/utils/localcrumb"

export default {
    state: {
        isCollapse: false, //用于控制菜单展开折叠
        tabsList: getCrumb()//面包屑数据
    },
    mutations: {
        //修改菜单展开折叠的方法
        collapseMenu(state) {
            state.isCollapse = !state.isCollapse
        },
        //更新面包屑数据
        //选择菜单
        selectMenu(state, val) {
            const index = state.tabsList.findIndex(item => item.name === val.name)
            while (state.tabsList.length != 1) {
                state.tabsList.pop()
            }
            if (index !== 0) {
                state.tabsList.push(val)
            }
        },
        //单纯增加
        pushCrumb(state, val) {
            const index = state.tabsList.findIndex(item => item.name === val.name)
            if (index < 0) {
                if (val.name == 'detect') {
                    const index2 = state.tabsList.findIndex(item => item.name === 'train')
                    if (index2 > 0) {
                        state.tabsList.pop()
                    }
                }
                if (val.name == 'train') {
                    const index2 = state.tabsList.findIndex(item => item.name === 'detect')
                    if (index2 > 0) {
                        state.tabsList.pop()
                    }
                }
                state.tabsList.push(val)
            }
        },
        saveCrumb(state) {
            saveCrumb(state.tabsList)
        }
    }
}