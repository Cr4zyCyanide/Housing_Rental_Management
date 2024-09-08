<template>
  <div class="userinfo_container">
    <div class="title">
      <h2>用户管理</h2>
    </div>
    <el-table :data="userInfo" style="" class="table" height=600>
      <el-table-column prop="user_id" label="ID" width="100px" />
      <el-table-column prop="username" label="用户名" width="200px"/>
      <el-table-column prop="user_type" label="用户类型" width="100px"/>
      <el-table-column prop="id_number" label="身份证号" width="200px"/>
      <el-table-column prop="phone" label="电话" width="150px"/>
      <el-table-column prop="email" label="邮箱" width="240px"/>
      <el-table-column prop="contact_info" label="联系方式" max-width="400px"/>
      <el-table-column fixed="right" label="操作" width="120">
        <template #default="{row}">
          <el-button link type="primary" size="small" @click="edit_dev">
            编辑
          </el-button>
          <el-button link type="danger" size="small" @click="deleteUser(row.user_id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
  <div class="rentals_container">
    <div class="title">
      <h2>租赁信息管理</h2>
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
<!--  <el-dialog-->
<!--    v-model="dialogVisible"-->
<!--    title="Tips"-->
<!--    width="500"-->
<!--  >-->
<!--    <span>警告</span>-->
<!--    <template #footer>-->
<!--      <div class="dialog-footer">-->
<!--        <el-button type="primary" @click="dialogVisible = false">取消删除</el-button>-->
<!--        <el-button type="danger" @click="dialogVisible = false; ">-->
<!--          确定删除-->
<!--        </el-button>-->
<!--      </div>-->
<!--    </template>-->
<!--  </el-dialog>-->
</template>

<script lang="js">
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  import {ElMessage} from "element-plus"

  export default {
    setup(){
      let userInfo = ref([])
      let rentals = ref([])

      // const dialogVisible = ref(false)

      const fetchUserInfo = async () => {
        try {
          const response = await axios.get("http://127.0.0.1:4567/api/get_userinfo")
          userInfo.value = response.data
        } catch (error) {
          console.error('Error fetching rental information:', error)
        }
      }

      const fetchRentals = async () => {
        try {
          const response = await axios.get("http://127.0.0.1:4567/api/get_rentals");
          rentals.value = response.data
        } catch (error) {
          console.error('Error fetching rental information:', error)
        }
      }

      // const deleteUser = async (userId) => {
      //   try {
      //     const response = await axios.get(`http://127.0.0.1:4567/api/del_user/${userId}`)
      //         .then(fetchUserInfo)
      //     ElMessage.success('User deleted successfully')
      //   } catch (error) {
      //     console.error('Error deleting user:', error)
      //     ElMessage.error('Failed to delete user')
      //   }
      // }
      onMounted(() => {
        fetchUserInfo().then(fetchRentals)
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
            message: '未开发，敬请期待...',
            type: 'error'
        })
      },
      // delClicked(){
      //
      // },
      async deleteUser(userId){
        try {
          const response = await axios.get("http://127.0.0.1:4567/api/del_user", {
            params: {
              'userId': userId
            }
          })
          if (response.status === 200 && response.data.status === true){
            ElMessage.success('成功删除用户:' + userId)
          } else {
            ElMessage.error('删除失败,' + response.status + response.data.info)
          }

        } catch (error) {
          console.error('Error deleting user:', error)
          ElMessage.error('Failed to delete user')
        }
      },
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

  h2{
    margin: 0px auto 20px auto;
    height: 30px;
  }
</style>