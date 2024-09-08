import { createStore } from 'vuex'
import {ElMessage} from "element-plus";
import axios from 'axios'

interface UserState {
  isLoggedIn: boolean
  username: String
  isOperator: boolean
}

const store = createStore({
  state: {
    user: {
      isLoggedIn: false,
      username: null,
      isOperator: false
    } as UserState
  },

  mutations: {
    // commits
    login(state, userInfo) {
      state.user.isLoggedIn = true
      state.user.username = userInfo.username;
      state.user.isOperator = userInfo.isOperator;

      // save to localStorage
      localStorage.setItem('user', JSON.stringify(state.user));
    },
    logout(state) {
      state.user.isLoggedIn = false;
      state.user.username = null;
      state.user.isOperator = false;

      // remove from localStorage
      localStorage.removeItem('user');
    },
    setUserType(state, userInfo) {
      state.user.isOperator = userInfo
    },
    setUserFromLocalStorage(state) {
      const user = localStorage.getItem('user');
      if (user) {
        state.user = JSON.parse(user);
      }
    }
  },

  actions: {
    async userLogin({ commit }, form) {
      try {
        const response = await axios.post("http://127.0.0.1:4567/api/login", form);
        if (response.status === 200 && response.data.code === 0) {
          commit('login', response.data.userInfo);
          console.log('Login form submitted successfully:', response.data);
          ElMessage({
            message: '登陆成功，即将跳转至主界面',
            type: 'success'
          })
          setTimeout(() => {
            location.href = "/"
          }, 3000)
        } else if (response.data.code === -1){
          ElMessage({
            message: '登录失败，用户名或密码错误',
            type: 'error'
          })
        } else if (response.data.code === -2){
          ElMessage({
            message: '登录失败，提交了一个空的表单或网络错误',
            type: 'error'
          })
        } else if (response.data.code === -10){
          ElMessage({
            message: '非法信息注入，检查前端代码是否被篡改',
            type: 'error'
          })
        } else if (response.data.code === -11){
          ElMessage({
            message: '注册失败，服务器出错',
            type: 'error'
          })
        }
      } catch (error) {
        console.error('[axios] Error submitting form:', error.response.data);
      }
    },

    async getUserType({ commit, state }) {
      try {
        console.log(state.user.username)
        const response = await axios.get("http://127.0.0.1:4567/api/op", {
          params: {
            username: state.user.username
          }
        });
        if (response.status === 200) {
          console.log(response.data.isOperator)
          commit('setUserType', response.data.isOperator);
        }
      } catch (error) {
        console.error('[axios] Error fetching user type:', error.response.data);
      }
    },

    userLogout({ commit }) {
      commit('logout');
      ElMessage.success("登出成功，即将跳转至主界面")
      setTimeout(() => {
            location.href = "/"
          }, 1000)
    }
  },
  getters: {
    // for those components which are importing store.ts to get user state
    isUserLoggedIn: state => {
      return state.user.isLoggedIn;
    },
    getUsername: state => {
      return state.user.username;
    },
    isOperator: state => {
      return state.user.isOperator;
    },
  }
});

// Check if user data exists in localStorage when the app starts
store.commit('setUserFromLocalStorage')

export default store