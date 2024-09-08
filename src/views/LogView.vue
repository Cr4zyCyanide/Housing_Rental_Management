<template>


  <div class="user_table_container">
    <div class="title">
      <h2>系统日志</h2>
    </div>
    <el-table :data="logs" style="" class="table">
      <el-table-column prop="id" label="ID" width="140px" />
      <el-table-column prop="timestamp" label="时间" width="240px" />
      <el-table-column prop="user" label="用户" width="100px"/>
      <el-table-column prop="ip" label="源IP" width="100px"/>
      <el-table-column prop="event" label="事件" width="100px"/>
      <el-table-column prop="note" label="备注" width="400px"/>
    </el-table>
  </div>

</template>

<script>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';

  export default {
    setup(){
      const logs = ref([])
      // Fetch rental information from backend
      const fetchLogs = async () => {
        try {
          const response = await axios.get("http://127.0.0.1:4567/api/get_logs");
          logs.value = response.data;
          // Initialize activeNames with all collapse item names
          // logs.value = response.data.map((log, index) => 'rental_' + index);
        } catch (error) {
          console.error('Error fetching rental information:', error);
        }
      }
      onMounted(() => {
        fetchLogs();
      });

      return {
        logs,
      };
    }
  }
</script>

<style scoped>
  div.user_table_container{
    max-width: 1130px;
    margin: 30px auto;
    position: relative;
    top: 16%;
    border-radius: 10px;
    background: #FFFFFF;
    padding: 20px;
  }
  .table{
     margin: 0 auto;
  }

</style>