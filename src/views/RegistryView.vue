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
      <h2>用户注册</h2>

      <el-form-item label="用户名" prop="username">
        <el-input v-model="ruleForm.username" type="text" autocomplete="off" />
      </el-form-item>
      <el-form-item label="密码" prop="pwd">
        <el-input v-model="ruleForm.pwd" type="password" autocomplete="off" />
      </el-form-item>
      <el-form-item label="确认密码" prop="confirmPwd">
        <el-input v-model="ruleForm.confirmPwd" type="password" autocomplete="off" />
      </el-form-item>
      <el-form-item label="身份证号" prop="id_number">
        <el-input v-model="ruleForm.id_number" type="text" autocomplete="off" />
      </el-form-item>
      <el-form-item label="手机号" prop="phone">
        <el-input v-model="ruleForm.phone" type="text" autocomplete="off" />
      </el-form-item>
      <el-form-item label="电子邮箱" prop="email">
        <el-input v-model="ruleForm.email" type="text" autocomplete="off" />
      </el-form-item>
      <el-form-item label="联系方式" prop="contact_info">
        <el-input v-model="ruleForm.contact_info" type="textarea" autocomplete="off" />
      </el-form-item>
      <div class="btns">
        <el-form-item>
          <el-button class="btn" type="primary" @click="submitForm(ruleFormRef)">
            注册
          </el-button>
          <el-button class="btn" @click="resetForm(ruleFormRef)">
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
  import * as CryptoJS from 'crypto-js'
  import axios from 'axios'

  const ruleFormRef = ref<FormInstance>()

  interface RuleForm {
    username: String
    pwd: String
    confirmPwd: String
    phone: String
    email: String
    contact_info: String
  }

  const checkUsername = (rule: any, value: any, callback: any) => {
    const reg = /^[a-zA-Z0-9_-]{4,16}$/;
    if (value === ''){
      callback(new Error('请输入用户名'))
    }else {
      if(ruleForm.username !== ''){
        if(!reg.test(value)){
          callback(new Error('用户名必须为4-16个数字或字母，不能包含特殊字符'))
        }
        callback()
      }
    }
  }

  const checkPasswd = (rule: any, value: any, callback: any) => {
    const reg = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[`~!@#$%^&*()_+<>?:"{},.\/\\;'[\]])[A-Za-z\d`~!@#$%^&*()_+<>?:"{},.\/\\;'[\]]{8,32}$/;
    if (value === ''){
      callback(new Error('请输入密码'))
    } else {
      if(ruleForm.pwd !== ''){
        if (!reg.test(value)) {
          callback(new Error('密码必须包含英文大小写字母、数字和特殊符号，且长度至少为8位'))
        }
        callback()
      }
    }
  }

  const checkConfirmPwd = (rule: any, value: any, callback: any) => {
    if (value === '') {
      callback(new Error('请确认密码，需与上一栏输入的密码相同'))
    } else {
      if (ruleForm.confirmPwd !== '') {
        if (value !== ruleForm.pwd) {
          callback(new Error('两次输入的密码不一致'))
        }
          callback()
      }
    }
  }

  const checkIdNumber = (rule: any, value: any, callback: any) => {
    const reg = /^[1-9]\d{5}(19|20|21)\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/;
    if (value === ''){
      callback(new Error('请输入身份证号'))
    }else {
      if(ruleForm.id_number !== ''){
        if(!reg.test(value)){
          callback(new Error('请输入一个合法的身份证号'))
        }
        callback()
      }
    }
  }

  const checkPhone = (rule: any, value: any, callback: any) => {
    const reg = /^1[3,4,5,7,8][0-9]{9}$/;
    if (value === '') {
      callback(new Error('请输入手机号'))
    }else{
      if (ruleForm.phone !== '') {
        if (!reg.test(value)){
        callback(new Error('请输入一个合法的手机号'))
        }
        callback()
      }
    }
  }

  const checkEmail = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error('请输入邮箱'))
    }else {
      const reg = /^([a-zA-Z]|[0-9])(\w|-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/
      if(!reg.test(value)){
        callback(new Error('邮箱格式不正确'))
      }else{
        callback()
      }
    }
  }

  const checkContactInfo = (rule: any, value: any, callback: any) => {
    const reg = /^[^\s"#$%&'()*+\-/<=>?[\\\]^_`{|}~]*$/
    if(!reg.test(value)){
      callback(new Error('不能包含有\/\\+*:;?$#{}"<>|等特殊字符'))
    } else if (value.length > 128){
      callback(new Error('联系方式长度需在128个字符以下'))
    } else{
      callback()
    }
  }
  const ruleForm = reactive({
    username: '',
    pwd: '',
    confirmPwd: '',
    id_number: '',
    phone: '',
    email: '',
    contact_info: '',
  })

  const rules = reactive<FormRules<typeof ruleForm>>({
    username: [{
        required: true,
        // message: '请输入用户名',
        validator: checkUsername,
        trigger: 'blur'
      },
    ],
    pwd: [{
        required: true, //此项为必须项
        validator: checkPasswd, //合法性校验函数
        trigger: 'blur' //焦点离开该输入框后，trigger被触发
      },
    ],
    confirmPwd: [{
        required: true,
        // message: '请确认密码，需与上一栏输入的密码相同',
        validator: checkConfirmPwd,
        trigger: 'blur'
      },
    ],
    id_number: [{
        required: true,
        validator: checkIdNumber,
        trigger: 'blur'
    }],
    phone: [{
        required: true,
        // message: '请输入你的手机号',
        validator: checkPhone,
        trigger: 'blur'
      },
    ],
    email: [{
        required: true,
        // message: '请输入你的电子邮箱地址',
        validator: checkEmail,
        trigger: 'blur'
      },
    ],
    contact_info: [{
        required: false,
        validator: checkContactInfo,
        trigger: 'blur'
      },
    ]
  })

  const sha256 = (input: string): string => {
    const hash = CryptoJS.SHA256(input);
    return hash.toString(CryptoJS.enc.Hex);
  }

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
        ElMessage.error('注册失败，部分填充信息不符合要求')
        console.log('error submit!', fields)
      }
    })
  }

  const postData = () => {
    let encryptedForm = {
      username: ruleForm.username,
      pwd_hash: sha256(ruleForm.pwd),
      id_number: ruleForm.id_number,
      phone: ruleForm.phone,
      email: ruleForm.email,
      contact_info: ruleForm.contact_info
    }

    ElMessage({
      message: '注册信息已提交，等待服务器返回结果'
    })
    axios.post("http://127.0.0.1:4567/api/registry", encryptedForm)
      .then((response) => {
        if(response.status === 200 && response.data.code === 0){
          console.log('Form submitted successfully:', response.data)
          ElMessage({
            message: '注册成功，3秒后跳转至登陆页面',
            type: 'success'
          })
          setTimeout(() => {
            location.href = "/login"
          }, 3000)
        }else if(response.data.code === -1){
          ElMessage({
            message: '注册失败，用户名已存在',
            type: 'error'
          })
        }else if(response.data.code === -2){
          ElMessage({
            message: '注册失败，提交了一个空的表单或网络错误',
            type: 'error'
          })
        }else if(response.data.code === -10){
          ElMessage({
            message: '注册失败，提交了非法信息',
            type: 'error'
          })
        }else if(response.data.code === -11){
          ElMessage({
            message: '注册失败，服务器出错',
            type: 'error'
          })
        }
      })
      .catch((error) => {
        console.log('[axios]Error submitting form:', error.response.data)
      })
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
      margin: 0 auto;
      width: 240px;
  }
  .btn{
      margin: 30px 30px;
  }
</style>