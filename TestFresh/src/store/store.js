// 引入vue
import Vue from 'vue'
// 全局引入vueX
import Vuex from 'vuex'

import mutations from './mutations'
import actions from './actions'
import getters from './getters'

// 全局引用cookie方法类
import cookie from '../../static/js/cookie'

// 全局注册vueX
Vue.use(Vuex)

// 要管理的状态
const userInfo = {
  name: cookie.getCookie('name') || '',
  token: cookie.getCookie('token') || ''
}
const goodsList = {
  totalPrice: '',
  goods_list: []
}

const state = {
  userInfo,
  goodsList
}

export default new Vuex.Store({
  state,
  mutations,
  actions,
  getters
})
