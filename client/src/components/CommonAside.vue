<!-- 侧边栏组件 -->
<template>
    <el-menu :default-active="$route.path" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose"
        :collapse="isCollapse" background-color="#2b262d" text-color="#fff">
        <h3>{{ isCollapse ? '选项' : '数据库系统' }}</h3>
        <el-menu-item @click="clickMenu(item)" v-for="item in noChildren" :key="item.name" :index="item.path">
            <i :class="`el-icon-${item.icon}`"></i>
            <span slot="title">{{ item.label }}</span>
        </el-menu-item>
    </el-menu>
</template>
<style lang="less" scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
}

.el-menu {
    height: 100vh;
    border-right: none;

    h3 {
        color: #fff;
        text-align: center;
        line-height: 48px;
        font-size: 16px;
        font-weight: 400px;
    }

    .el-menu-item {
        font-weight: 600;

        :hover {
            outline: 0 !important;
            color: #ff8923 !important;
            background: none !important;
        }


    }

    .el-menu-item.is-active {
        color: #ff8923 !important;
        border-bottom-color: transparent !important;
    }
}
</style>
<script>
export default {
    data() {
        return {
            menuData: [
                {
                    path: "/property",
                    name: "property",
                    label: "楼盘总览",
                    icon: "setting",
                },
                {
                    path: "/customer",
                    name: "customer",
                    label: "客户",
                    icon: "user",
                },
                {
                    path: "/sales",
                    name: "sales",
                    label: "售房情况",
                    icon: "user",
                },
                
                {
                    path: "/test",
                    name: "test",
                    label: "测试页面",
                    icon: "help",
                },
            ],
        };
    },
    methods: {
        handleOpen(key, keyPath) {

        },
        handleClose(key, keyPath) {

        },
        // 点击菜单实现路由跳转
        // 跳转根据menuData数据进行对应路由的跳转
        clickMenu(item) {
            // this.$router.push(item.path)
            // 解决重复点击相同按钮会出现报错的问题
            // 判断当前路由与跳转路由是否一致，不一致才跳转
            if (this.$route.path !== item.path && !(this.$route.path === '/home' && (item.path === '/'))) {
                this.$router.push(item.path)
            }
            //面包屑相关
            this.$store.commit('selectMenu', item)
            this.$store.commit('saveCrumb')
        }
    },
    computed: {
        // 没有子菜单
        noChildren() {
            return this.menuData.filter(item => !item.children)
        },
        // 有子菜单
        hasChildren() {
            return this.menuData.filter(item => item.children)
        },
        isCollapse() {
            return this.$store.state.tab.isCollapse
        }
    }
}
</script>