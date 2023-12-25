<!-- 顶部导航栏组件 -->
<template>
    <div class="header">
        <div class="l-c">
            <el-button v-if="isCollapse" style="margin-right: 20px;" @click="handleMenu" icon="el-icon-caret-right"
                size="mini"></el-button>
            <el-button v-else style="margin-right: 20px;" @click="handleMenu" icon="el-icon-caret-left"
                size="mini"></el-button>
            <!-- 面包屑 -->
            <el-breadcrumb separator="/">
                <el-breadcrumb-item v-for="item in tags" :key="item.path" :to="{ path: item.path }">{{ item.label
                }}</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="r-c">
            <el-dropdown v-if="isLogin">
                <span class="el-dropdown-link">
                    <img class="user" src="../assets/images/user.png">
                </span>
                <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item @click.native="jumpUser">个人中心</el-dropdown-item>
                    <el-dropdown-item @click.native="logOut">退出登录</el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
            <el-button v-else size="small" @click="jumpLogin" plain>登录</el-button>
        </div>
    </div>
</template>
<script>
import { mapState } from "vuex"
export default {
    data() {
        return {

        }
    },
    methods: {
        handleMenu() {
            this.$store.commit('collapseMenu')
        },
        jumpUser() {
            this.$router.push('/user')
        },
        jumpLogin() {
            this.$router.push('/login')
        },
        logOut() {
            // Cookies.remove('token')
            this.$store.commit('user/removeUserInfo')
            this.$router.push('/login')
            this.$notify.info({
                title: '消息',
                message: '您已退出登录',
                position: 'bottom-right'
            });
        }
    },
    computed: {
        ...mapState({
            isCollapse: state => state.tab.isCollapse,
            tags: state => state.tab.tabsList,
            isLogin: state => state.user.userInfo.cookie
        })
    },
}
</script>
<style lang="less" scoped>
.header {
    background-color: #1d1218;
    height: 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;

    .text {
        color: #fff;
        font-size: 14px;
        margin-left: 10px;
    }

    .l-c {
        display: flex;
        align-items: center; //垂直居中

        /deep/.el-breadcrumb__item {
            .el-breadcrumb__inner {
                font-weight: normal;

                &.is-link {
                    color: #fff;
                    font-weight: 600;
                }
            }
        }
    }

    .r-c {
        .user {
            width: 40px; //设置头像尺寸
            height: 40px; //设置头像尺寸
            border-radius: 50%; //设置圆角
        }

        .el-button {
            font-weight: 600;
        }
    }
}
</style>