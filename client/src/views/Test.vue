<template>
    <div class="container">
        <div class="box login" ref="login">
            <h1>登录</h1>
            <el-form label-position="top" label-width="100px" class="demo-ruleForm" :rules="rules" :model="rulesForm"
                status-icon ref="ruleForm">
                <el-form-item label="用户名" prop="name">
                    <el-input type="text" v-model="rulesForm.name"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input type="password" v-model="rulesForm.password" @keyup.enter.native="submitLogin"></el-input>
                </el-form-item>
                <!-- <el-form-item label="验证码" prop="validation">
            <el-input type="text" v-model="picInfo.picValidation" style="width:63%; margin-right: 5%;"></el-input>
            <img :src="picInfo.picUrl" @click="getPicCode" alt="" style="flex:0 0 100px; width:100px;margin-bottom: 0%;">
        </el-form-item> -->
                <div style="text-align: center;margin-top: 20%;margin-bottom: 3%;">
                    <el-button size="medium" type="primary" @click="submitLogin">Submit</el-button>
                </div>
                <p style="text-align: center;">还没有账号？<a href="javascript:;" @click="goToRegister">去注册</a></p>
            </el-form>
        </div>
        <div class="box register" ref="register">
            <h1>注册</h1>
            <el-form label-position="top" label-width="100px" class="demo-ruleForm" :rules="rules" :model="rulesForm"
                status-icon ref="ruleForm">
                <el-form-item label="用户名" prop="name">
                    <el-input type="text" v-model="rulesForm.name"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input type="password" v-model="rulesForm.password"></el-input>
                </el-form-item>
                <!-- <el-form-item label="验证码" prop="validation">
            <el-input type="text" v-model="picInfo.picValidation" style="width:63%; margin-right: 5%;"></el-input>
            <img :src="picInfo.picUrl" @click="getPicCode" alt="" style="flex:0 0 100px; width:100px;margin-bottom: 0%;">
        </el-form-item> -->
                <div style="text-align: center;margin-top: 20%;margin-bottom: 3%;">
                    <el-button size="medium" type="primary" @click="submitRegister"
                        @keyup.enter="submitRegister">Submit</el-button>
                </div>
                <p style="text-align: center;">已经有账号了？<a href="javascript:;" @click="goToLogin">去登录</a></p>
            </el-form>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
import Cookies from 'js-cookie'
export default {
    data() {
        return {
            //存储数据的对象
            rulesForm: {
                name: '',
                password: ''
            },
            rules: {
                name: [
                    { required: true, message: '请输入账号', trigger: 'blur' },
                    { min: 3, max: 15, message: '长度在1到12', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'blur' },
                    { min: 6, max: 15, message: '长度在6到15', trigger: 'blur' }
                ],
            },
        };
    },
    mounted() {
        // 当组件被挂载时，向 body 元素添加一个类
        document.body.classList.add('login-page');
    },
    destroyed() {
        // 当组件被销毁时，从 body 元素移除这个类
        document.body.classList.remove('login-page');
    },
    methods: {
        goToRegister() {
            this.$refs.login.style.transform = "rotateY(180deg)";
            this.$refs.register.style.transform = "rotateY(0deg)";
        },
        goToLogin() {
            this.$refs.register.style.transform = "rotateY(-180deg)";
            this.$refs.login.style.transform = "rotateY(0deg)";
        },
        submitLogin() {
            axios.post('http://114.132.154.44:5000/User/login', {
                username: this.rulesForm.name,
                password: this.rulesForm.password
            }).then((response) => {
                this.$message({
                    //登陆成功
                    message: response.data.message,
                    type: 'success'
                });
                Cookies.set('token', response.data.token)
                const cookie = Cookies.get('token')
                //存储到vuex中
                this.$store.commit('user/setUserInfo', { cookie: cookie })
                // 跳转页面
                this.$router.push('/user')
            }).catch((error) => {
                //登陆失败
                this.$message.error(error.response.data.error)
            });
        },
        submitRegister() {
            axios.post('http://114.132.154.44:5000/User/register', {
                username: this.rulesForm.name,
                password: this.rulesForm.password
            }).then((response) => {
                this.$message({
                    //登陆成功
                    message: response.data.message,
                    type: 'success'
                });
            }).catch((error) => {
                this.$message.error(error.response.data.error)
            });
        },
        // async getPicCode() {
        //     const { data: { base64, key } } = await getPicCode()
        //     this.picInfo.picKey = key
        //     this.picInfo.picUrl = base64
        // }
    }
}
</script>
<style lang="less">
.login-page {
    background: linear-gradient(rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.7)), url('../assets/images/background.png') center center no-repeat fixed;
    background-size: cover;
}

* {
    margin: 0;
    padding: 0;
}

a {
    text-decoration: none
}

.container {
    position: relative;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 20rem;
    height: 28rem;
    perspective: 1500px;
    border-radius: 15px;

    -webkit-perspective: 1500px;
    -moz-perspective: 1500px;

    h1 {
        text-align: center;
        margin-top: 10%;
    }

    .el-form {
        margin-left: 5%;
        margin-right: 5%;
    }

    .box {
        position: absolute;
        width: 20rem;
        height: 28rem;
        border-radius: 10px;
        cursor: pointer;
        user-select: none;
        backface-visibility: hidden;
        transition: all .5s;
        /* 设置阴影 */
        box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.2);


        .login {
            transform: rotateY(-180deg);

        }


    }
}

.login {
    background-color: #fff;
}

.register {
    background-color: #fff;
    transform: rotateY(-180deg);
}
</style>