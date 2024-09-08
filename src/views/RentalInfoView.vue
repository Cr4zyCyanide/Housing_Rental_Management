<template>
  <div class="list_container">
    <h2>租赁信息列表</h2>
    <el-collapse
        v-model="activeNames"
        class="rental_list"
    >
      <el-collapse-item
          v-for="(rental, index) in rentals"
          :title="rental.address"
          :name="index"
      >
        <el-descriptions
            :border="true"
            title="详细信息"
            size="default"
        >
          <div class="info">
            <el-descriptions-item label="面积(m²)">{{ rental.area }}</el-descriptions-item>
            <el-descriptions-item label="楼层">{{ rental.floor }}</el-descriptions-item>
            <el-descriptions-item label="租金/月(￥)">{{ rental.rent }}</el-descriptions-item>
            <el-descriptions-item label="房型">{{ rental.house_type }}</el-descriptions-item>
            <el-descriptions-item label="所在区域">{{ rental.region }}<p v-if="rental.region === ''">无说明</p></el-descriptions-item>
            <el-descriptions-item label="房屋朝向">{{ rental.orientation }}<p v-if="rental.orientation === ''">无说明</p></el-descriptions-item>
            <el-descriptions-item label="装修情况">{{ rental.decoration }}<p v-if="rental.decoration === ''">无说明</p></el-descriptions-item>
            <el-descriptions-item label="周围环境">{{ rental.surroundings }}<p v-if="rental.surroundings === ''">无说明</p></el-descriptions-item>
            <el-descriptions-item label="发布者">{{ rental.publisher }}</el-descriptions-item>
            <el-descriptions-item label="邮箱">{{ rental.email }}</el-descriptions-item>
            <el-descriptions-item label="电话">{{ rental.phone }}</el-descriptions-item>
          </div>
        </el-descriptions>
      </el-collapse-item>
    </el-collapse>
  </div>

</template>

<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import axios from 'axios'

  const rentals = ref([])
  const activeNames = ref([])
  // Fetch rental information from backend
  const fetchRentals = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:4567/api/get_rentals");
      rentals.value = response.data;
      // Initialize activeNames with all collapse item names
      activeNames.value = response.data.map((rental, index) => 'rental_' + index);
    } catch (error) {
      console.error('Error fetching rental information:', error);
    }
  }

  // const handleChange = (val: string[]) => {
  // console.log(val)
  // }

  onMounted(() => {
    fetchRentals();
  })

// export default {
//   setup() {
//     const rentals = ref([]);
//     const activeNames = ref(['1']);
//
//     // Fetch rental information from backend
//     const fetchRentals = async () => {
//       try {
//         const response = await axios.get("http://127.0.0.1:4567/api/get_rentals");
//         rentals.value = response.data;
//         // Initialize activeNames with all collapse item names
//         activeNames.value = response.data.map((rental, index) => 'rental_' + index);
//       } catch (error) {
//         console.error('Error fetching rental information:', error);
//       }
//     };
//
//     onMounted(() => {
//       fetchRentals();
//     });
//
//     return {
//       rentals,
//       activeNames
//     };
//   }
// };

</script>

<style scoped>
  div.list_container{
    max-width: 65%;
    margin: 0 auto;
    position: relative;
    top: 80px;
    background: #FFFFFF;
    border-radius: 10px;
    padding: 10px;
  }
  .rental_list{
    max-width: 95%;
    margin: 0 auto;
  }
  div.info{
    width: 90%;
    height: 80%;
    margin: 0 auto;
  }
  h2{
    margin: 20px auto;
  }
  p{
    display: inline;
  }
</style>
