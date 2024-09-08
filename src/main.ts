import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

//use vue-router
import router from "./router/index"

//use vuex store
import store from "./store/store";

// use vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

//use Element Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const vuetify = createVuetify({
  components,
  directives,
})

const rootApp = createApp(App);
rootApp.use(router)
rootApp.use(ElementPlus)
rootApp.use(vuetify)
rootApp.use(store)
rootApp.mount('#app');
