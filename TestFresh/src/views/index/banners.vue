<template>
  <div class="banner-warp">
    <swiper :options="swiperOption">
      <swiper-slide v-for="item in banners" :key="item.goods">
        <router-link :to="'/app/home/productDetail/'+item.goods" target="_blank">
          <img :src="item.image" alt="" />
        </router-link>
      </swiper-slide>
      <div class="swiper-pagination" slot="pagination"></div>
    </swiper>
  </div>
</template>

<script>
import '../../../node_modules/swiper/dist/css/swiper.css'
import { swiper, swiperSlide } from 'vue-awesome-swiper'
import {bannerGoods} from '../../api/api'

export default {
  data () {
    return {
      swiperOption: {
        pagination: {
          el: '.swiper-pagination',
          clickable: true
        },
        autoplay: {
          delay: 3000,
          stopOnLastSlide: false,
          disableOnInteraction: false
        }
      },
      banners: []
    }
  },
  created () {
    this.getBanner()
  },
  methods: {
    getBanner () {
      bannerGoods().then((response) => {
        // console.log(response.data)
        this.banners = response.data
      }).catch(function (error) {
        console.log(error)
      })
    }
  },
  components: {
    swiper,
    swiperSlide
  }
}
</script>

<style scoped>
.banner-warp{
  height: 300px;
}
</style>
