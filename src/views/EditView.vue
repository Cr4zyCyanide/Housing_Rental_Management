<template>
  <div class="form_container">
    <el-form
      ref="ruleFormRef"
      style="max-width: 500px"
      :model="ruleForm"
      :rules="rules"
      status-icon
      label-width="auto"
      class="demo-ruleForm"
      label-position="left"
    >
      <h2>编辑出租信息</h2>
      <p>发布者：{{ publisher }}</p>
      <el-form-item label="房屋地址" prop="address">
        <el-input v-model="ruleForm.address" type="text" autocomplete="off" />
      </el-form-item>
      <el-form-item label="房屋面积(m²)" prop="area">
        <el-input v-model="ruleForm.area" type="text" autocomplete="off" />
      </el-form-item>
      <el-form-item label="楼层" prop="floor">
        <el-input v-model="ruleForm.floor" type="text" autocomplete="off" />
      </el-form-item>
      <el-form-item label="租金/月(￥)" prop="rent">
        <el-input v-model="ruleForm.rent" type="text" autocomplete="off" />
      </el-form-item>
      <el-form-item label="户型" prop="type">
        <el-input v-model="ruleForm.type" type="text" autocomplete="off" />
      </el-form-item>
      <el-form-item label="区域" prop="region">
        <el-input v-model="ruleForm.region" type="text" autocomplete="off" />
      </el-form-item>
      <el-form-item label="朝向">
      <el-radio-group v-model="ruleForm.orientation">
        <el-radio value="东">东</el-radio>
        <el-radio value="南">南</el-radio>
        <el-radio value="西">西</el-radio>
        <el-radio value="北">北</el-radio>
      </el-radio-group>
      </el-form-item>
      <el-form-item label="装修情况" prop="decoration">
        <el-input v-model="ruleForm.decoration" type="text" autocomplete="off" />
      </el-form-item>
      <el-form-item label="周围环境" prop="surroundings">
        <el-input v-model="ruleForm.surroundings" type="textarea" autocomplete="off" />
      </el-form-item>
      <div class="btns">
        <el-form-item>
          <el-button type="primary" @click="submitForm(ruleFormRef)">
            发布
          </el-button>
          <el-button @click="resetForm(ruleFormRef)">
            重置
          </el-button>
        </el-form-item>
      </div>
    </el-form>
  </div>
</template>

<script setup lang="ts">
  import { reactive, ref } from 'vue'
  import type { FormInstance, FormRules } from 'element-plus'
  import { ElMessage } from 'element-plus'
  import axios from 'axios'
  import store from "../store/store";

  const ruleFormRef = ref<FormInstance>()

  interface RuleForm {
    address: String
    area: Number
    floor: Number
    rent: Number
    type: String
    region: String
    orientation: String
    decoration: String
    surroundings: String
  }

  const ruleForm = reactive({
    address: '',
    area: '',
    floor: '',
    rent: '',
    type: '',
    region: '',
    orientation: '',
    decoration: '',
    surroundings: ''
  })

  const isInteger = (n: Number): boolean=> {
    return parseInt(n.toString(), 10) == n
  }

  const strValidator = (rule: any, value: any, callback: any) => {
    if (!value) {
      return callback(new Error('请输入相关信息'))
    } else {
      const reg = /^[^\s!"#$%&'()*+,\-./:;<=>?[\\\]^_`{|}~]*$/
      if(!reg.test(value)){
        callback(new Error('不能包含有\/\\+*:;?$#{}"<>|等特殊字符'))
      } else if (value.length > 128){
        callback(new Error('长度需在128个字符以下'))
      } else{
        callback()
      }
    }

  }
  const strValidator_notRequired = (rule: any, value: any, callback: any) => {
    const reg = /^[^\s!"#$%&'()*+,\-./:;<=>?[\\\]^_`{|}~]*$/
    if(!reg.test(value)){
      callback(new Error('不能包含有\/\\+*:;?$#{}"<>|等特殊字符'))
    } else if (value.length > 128){
      callback(new Error('长度需在128个字符以下'))
    } else{
      callback()
    }
  }

  const numberValidator = (rule: any, value: Number, callback: any) => {
    if (!value) {
      return callback(new Error('请输入一个整数'))
    }
    else{
      if ((value) => {return (parseInt(value.toString(), 10) == value)}) {
        callback()
      } else {
        callback(new Error('请输入一个整数'))
        console.log(isInteger(value))
      }
    }
  }

  const rules = reactive<FormRules<typeof ruleForm>>({
    address: [{
        required: true,
        validator: strValidator,
        trigger: 'blur'
      },
    ],
    area: [{
        required: true,
        validator: numberValidator,
        trigger: 'blur'
      },
    ],
    floor: [{
        required: true,
        validator: numberValidator,
        trigger: 'blur'
      },
    ],
    rent: [{
        required: true,
        validator: numberValidator,
        trigger: 'blur'
      },
    ],
    type: [{
        required: true,
        validator: strValidator,
        trigger: 'blur'
    }],
    region: [{
        required: false,
        validator: strValidator_notRequired,
        trigger: 'blur'
      },
    ],
    orientation: [{
        required: false,
      },
    ],
    decoration: [{
        required: false,
        validator: strValidator_notRequired,
        trigger: 'blur'
      },
    ],
    surroundings: [{
        required: false,
        validator: strValidator_notRequired,
        trigger: 'blur'
      },
    ]
  })

  const publisher = store.getters.getUsername
  const rental_id = $route.query.id

  const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.resetFields()
  }

  const submitForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
      if (valid) {
        // submitting the form to the backend by axios
        postData()
      } else {
        ElMessage.error('提交失败，部分填充信息不符合要求')
        console.log('error submit!', fields)
      }
    })
  }

  const postData = () => {
    if(store.getters.getUsername === null){
      ElMessage({
        message: '当前无用户登录，无法提交',
        type: 'error'
      })
    } else {
      let form = ruleForm
      Object.defineProperty(form, 'username', {
        value : store.getters.getUsername,
        writable : true,
        enumerable : true,
        configurable : true})
      console.log(form)
      ElMessage({
        message: '信息已提交,等待服务器返回结果'
      })
      axios.post("http://127.0.0.1:4567/api/publish", form)
        .then((response) => {
          if(response.status === 200 && response.data.code === 0){
            console.log('Form submitted successfully:', response.data)
            ElMessage({
              message: '提交成功',
              type: 'success'
            })
            // setTimeout(() => {
            //   location.href = "/login"
            // }, 3000)
          }else if(response.status !== 200){
            ElMessage({
              message: '服务器或网络错误：' + response.status.toString(),
              type: 'error'
            })
          }
        })
        .catch((error) => {
          console.log('[axios]Error submitting form:', error.response.data)
        })
    }

  }
</script>

<style scoped>
  div.form_container{
    width: 100%;
    height: 100%;
    position: absolute;
    top: 10%;
    left: 0;
    right: 0;
    max-width: 520px;
    margin: 0 auto;
  }
  h2{
      margin-bottom: 30px;
  }
  div.btns{
    width: 150px;
    margin: 40px auto;
  }
</style>