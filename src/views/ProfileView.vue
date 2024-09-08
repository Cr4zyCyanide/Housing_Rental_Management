<template>
  <div class="userinfo_container">
    <el-descriptions title="用户信息">
      <el-descriptions-item label="用户名">{{userInfo.username}}</el-descriptions-item>
      <el-descriptions-item label="身份证号"><span class="covered">{{userInfo.id_number}}</span></el-descriptions-item>
      <el-descriptions-item label="手机号">{{userInfo.phone}}</el-descriptions-item>
      <el-descriptions-item label="邮箱">{{userInfo.email}}</el-descriptions-item>
      <el-descriptions-item label="联系方式">{{userInfo.contact_info}}</el-descriptions-item>
    </el-descriptions>
    <el-button type="primary" disabled @click="edit_dev">编辑</el-button>
  </div>
  <div class="rentals_container">
    <div class="title">
      <h2>{{userInfo.username}}发布的租赁信息</h2>
    </div>
    <el-table :data="rentals" style="" class="table" height=600>
      <el-table-column prop="rental_id" label="ID" width="100px" />
      <el-table-column prop="publisher" label="发布者" width="200px"/>
      <el-table-column prop="address" label="地址" width="400px"/>
      <el-table-column prop="area" label="面积" width="80px"/>
      <el-table-column prop="floor" label="楼层" width="80px"/>
      <el-table-column prop="rent" label="租金/月" width="120px"/>
      <el-table-column prop="house_type" label="户型" max-width="400px"/>
      <el-table-column fixed="right" label="操作" width="120px">
        <template #default="{row}">
          <el-button link type="primary" size="small" @click="edit_dev">
            编辑
          </el-button>
          <el-button link type="danger" size="small" @click="deleteRental(row.rental_id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script lang="js">
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  import {ElMessage} from "element-plus"
  import store from "../store/store";
  export default {
    setup(){
      let userInfo = ref([])
      let rentals = ref([])

      // const dialogVisible = ref(false)

      const fetchUserInfoByUsername = async (username) => {
        try {
          const response = await axios.get("http://127.0.0.1:4567/api/get_userinfo_by_name", {
            params:{
              'username': username
            }
          })
          userInfo.value = response.data
        } catch (error) {
          console.error('Error fetching rental information:', error)
        }
      }

      const fetchRentalsByUsername = async () => {
        try {
          const response = await axios.get("http://127.0.0.1:4567/api/get_rental_by_username", {
            params:{
              'publisher': store.getters.getUsername
            }
          })
          rentals.value = response.data
        } catch (error) {
          console.error('Error fetching rental information:', error)
        }
      }

      onMounted(() => {
        fetchUserInfoByUsername(store.getters.getUsername).then(fetchRentalsByUsername)
      })
      return{
        // dialogVisible,
        userInfo,
        rentals
      }
    },
    methods:{
      edit_dev(){
        ElMessage({
            message: '开发中，敬请期待...',
            type: 'error'
        })
      },
      // delClicked(){
      //
      // },

      async deleteRental(rentalID){
        try {
          const response = await axios.get("http://127.0.0.1:4567/api/del_rental", {
            params: {
              'rentalId': rentalID
            }
          })
          if (response.status === 200 && response.data.status === true){
            ElMessage.success('成功删除租赁信息:' + rentalID)
          } else {
            ElMessage.error('删除失败,' + response.status + response.data.info)
          }

        } catch (error) {
          console.error('Error deleting rental info:', error)
          ElMessage.error('Failed to delete rental info')
        }
      }
    }
  }
</script>

<style scoped>
  div.userinfo_container{
    max-width: 1520px;
    margin: 30px auto;
    position: relative;
    top: 16%;
    border-radius: 10px;
    background: #FFFFFF;
    padding: 20px;
  }
  div.rentals_container{
    max-width: 1520px;
    margin: 50px auto;
    position: relative;
    top: 16%;
    border-radius: 10px;
    background: #FFFFFF;
    padding: 20px;
  }
  span.covered{
    background-color: #252525;
    color: #252525;
    text-shadow: none;
    border-radius: 5px;
  }
  span.covered:hover{
    color: white !important;
  }
  h2{
    margin: 0px auto 20px auto;
    height: 30px;
  }
</style>