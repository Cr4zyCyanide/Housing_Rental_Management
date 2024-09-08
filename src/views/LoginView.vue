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
    >
      <h2>用户登录</h2>

      <el-form-item label="用户名" prop="username">
        <el-input v-model="ruleForm.username" type="text" autocomplete="off" />
      </el-form-item>
      <el-form-item label="密码" prop="pwd">
        <el-input v-model="ruleForm.pwd" type="password" autocomplete="off" />
      </el-form-item>
      <div class="btns">
        <el-form-item>
          <el-button class="btn" type="primary" @click="submitForm(ruleFormRef)">
            登录
          </el-button>
          <el-button class="btn" @click="jumpToRegistry()">
            没有账号？点此注册
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

  import { useStore } from 'vuex';

  const ruleFormRef = ref<FormInstance>()
  const store = useStore();

  interface RuleForm {
    username: String
    pwd: String
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
    // const reg = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[`~!@#$%^&*()_+<>?:"{},.\/\\;'[\]])[A-Za-z\d`~!@#$%^&*()_+<>?:"{},.\/\\;'[\]]{8,32}$/;
    if (value === ''){
      callback(new Error('请输入密码'))
    } else {
      if(ruleForm.pwd !== ''){
        // if (!reg.test(value)) {
        //   callback(new Error('密码必须包含英文大小写字母、数字和特殊符号，且长度至少为8位'))
        // }
        callback()
      }
    }
  }

  const ruleForm = reactive({
    username: '',
    pwd: '',
  })

  const rules = reactive<FormRules<typeof ruleForm>>({
    username: [{
        required: true,
        validator: checkUsername,
        trigger: 'blur'
      },
    ],
    pwd: [{
        required: true,
        validator: checkPasswd,
        trigger: 'blur'
      },
    ],
  })

  const sha256 = (input: string): string => {
    const hash = CryptoJS.SHA256(input);
    return hash.toString(CryptoJS.enc.Hex);
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

  const jumpToRegistry = () => location.href = "/registry"

  const postData = async () => {
    let encryptedForm = {
      username: ruleForm.username,
      pwd_hash: sha256(ruleForm.pwd),
    }
    await store.dispatch('userLogin', encryptedForm) // Assuming form is defined somewhere
      .catch((error) => {
        console.log('Error submitting form:', error)
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
    width: 350px;
    margin: 40px auto;
  }
  .btn{
    margin: auto 30px;
  }
</style>