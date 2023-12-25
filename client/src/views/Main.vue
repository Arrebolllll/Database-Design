<!-- 所有页面中不变的部分，这里是侧边栏和菜单栏 -->
<!-- 也是页面的大体布局 -->
<template>
    <div>
        <el-container>
            <el-aside width="auto">
                <CommonAside />
            </el-aside>
            <el-container>
                <el-header>
                    <CommonHeader />
                </el-header>
                <el-main>
                    <!-- 路由出口 -->
                    <!-- 路由匹配到的组件将渲染在这里 -->
                    <router-view></router-view>
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>
<script>
import CommonAside from '../components/CommonAside.vue'
import CommonHeader from '../components/CommonHeader.vue'
export default {
    data() {
        return {}
    },
    components: {
        CommonAside, 
        CommonHeader
    }
}
</script>
<style scoped>
.el-header {
    padding: 0%;
}
</style>