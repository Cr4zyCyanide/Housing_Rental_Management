<template>
  <div>
    <h1>HomeView</h1>
    <h2>Click the Button to Test the Connection</h2>
    <el-button @click="fetchData" type="primary">Fetch Data From Backend</el-button>
    <h1>{{ message }}</h1>
  </div>
</template>

<script lang="ts">
import axios from 'axios'

export default {
  data() {
    return {
      message: ''
    };
  },
  methods: {
    fetchData() {
      axios.get('http://127.0.0.1:4567/api/hello')
        .then(response => {
          this.message = response.data.message;
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
}
</script>
