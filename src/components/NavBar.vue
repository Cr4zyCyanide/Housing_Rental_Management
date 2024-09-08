<template>
  <el-menu
      :default-active="activeIndex"
      class="el-menu"
      mode="horizontal"
      :ellipsis="false"
      @select="handleSelect"
      router>
    <a href="/" class="title"><p>网站标题</p></a>
    <el-menu-item class="el-items" index="/" @click="navigateTo('/')">主页</el-menu-item>
    <el-menu-item class="el-items" index="/rentals" @click="navigateTo('/rentals')">租赁</el-menu-item>
    <el-menu-item v-if="isUserLoggedIn" class="el-items" index="/profile" @click="navigateTo('/profile')">个人中心</el-menu-item>
    <el-menu-item v-if="isOperator" class="el-items" index="/log" @click="navigateTo('/log')">日志</el-menu-item>
    <el-menu-item v-if="isOperator" class="el-items" index="/mng" @click="navigateTo('/mng')">管理</el-menu-item>
<!--    <el-menu-item v-if="isOperator" class="el-items" index="/test" @click="navigateTo('/test')">测试页面</el-menu-item>-->

    <div class="btns">
      <!--    debug:-->
      <div class="info">
        <p v-if="isUserLoggedIn">[info]User is logged in.<br/>Current user: {{ userInfo }}.</p>
        <p v-else>User is not logged in.</p>
        <p v-if="isUserLoggedIn">User type: {{ userType }}.</p>
      </div>
      <el-button
          v-if="isUserLoggedIn"
          index="/"
          @click="navigateTo('/publish')"
          type="primary"
      >
        发布
      </el-button>
      <el-button
          v-if="!isUserLoggedIn"
          index="/"
          @click="navigateTo('/login')"
          type="primary"
      >
        登录
      </el-button>
      <el-button
          v-if="!isUserLoggedIn"
          index="/"
          @click="navigateTo('/registry')"
      >
        注册
      </el-button>
      <el-button
          v-else
          @click="logoutUser()"
          type="danger"
      >
        登出
      </el-button>
      <el-button @click="checkLoginStatus">检测是否登录及用户类型</el-button>
    </div>

   </el-menu>
</template>

<script lang="ts">
  import {useStore} from 'vuex'
  import {computed, ref} from 'vue'
  import router from "../router/index"
  import {ElMessage} from "element-plus";
  import store from "../store/store"

  export default {
    setup()
    {
      const store = useStore()
      const activeIndex = ref(['/'])

      const isUserLoggedIn = computed(() => {
        return store.getters.isUserLoggedIn
      })

      const getUsername = computed(() => {
        return store.getters.getUsername
      })

      const isOperator = computed(() => {
        // console.log(store.getters.isOperator)
        return store.getters.isOperator
      })

      const getUserType = computed(() => {
        if(isUserLoggedIn) {
          // console.log(typeof(store.getters.isOperator), store.getters.isOperator)
          return store.getters.isOperator ? 'operator' : 'user'
        }
        else return null

      })
      return{
        activeIndex,
        isUserLoggedIn,
        userInfo: getUsername,
        isOperator,
        userType: getUserType
      }
    },

    methods:{
      checkLoginStatus(){
         if(store.getters.isUserLoggedIn){
           ElMessage({
             message: '已登录，当前用户：' + store.getters.getUsername + ' store.getters.isOperator: ' + store.getters.isOperator,
             type: 'success'
           })
         }else {
           ElMessage({
             message: '未登录',
             type: 'error'
           })
         }
       },
       handleSelect (index) {
         this.activeIndex = index
       },
       navigateTo (route) {
         router.push(route)
         this.activeIndex = route
       },
       logoutUser() {
       store.dispatch('userLogout');
      }
    }
  }
  // const store = useStore()
  // let activeIndex = ref(['/'])
  //
  // const isUserLoggedIn = computed(() => {
  //   return store.getters.isUserLoggedIn;
  // });
  //
  // const userInfo = computed(() => {
  //   return store.getters.getUserInfo;
  // })
  //
  // const checkLoginStatus = () =>{
  //   if(store.getters.isUserLoggedIn){
  //     ElMessage({
  //       message: '已登录，当前用户：' + store.getters.getUserInfo,
  //       type: 'success'
  //     })
  //   }else {
  //     ElMessage({
  //       message: '未登录',
  //       type: 'error'
  //     })
  //   }
  // }
  // const handleSelect = (index: String) => {
  //   activeIndex = index
  // }
  // const navigateTo = (route) =>{
  //   router.push(route)
  //   activeIndex = route
  // }
  // const logoutUser = () => store.dispatch('userLogout');
</script>

<style scoped>
  a.title{
    background: white;

    font-size: 16px;
    text-align: center;
    width: 140px;
    height: 100%;
  }
  a.title > p{
    background: white;
    vertical-align: middle;
    font-size: 20px;
    display: inline-block;
    margin: 15px auto;
    color: black;
  }
  div.btns{
    display: flex;
    position: absolute;
    right: 60px;
    margin: 13px;
  }
  div.info{
    position: relative;
    top: -16px;
    font-size: 14px;
    margin: 0;
    left: -10%;
    display: revert;
  }
  .el-menu{
    background: white;
    border: none;
    /*!!!这个浮动会影响下面的route-view!!! float: left;*/

    width: 100%;
    border-bottom: 2px solid rgba(0, 0, 0, 0.06);
    box-shadow:
        0 0 6px rgba(0, 0, 0, 0.06);
  }
  .el-items{
    background: white;
    width: 80px;
  }
</style>
