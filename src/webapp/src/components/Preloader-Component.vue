<template>
  <div v-if="show" class="pencil">
    <div class="pencil__ball-point"></div>
    <div class="pencil__cap"></div>
    <div class="pencil__cap-base"></div>
    <div class="pencil__middle"></div>
    <div class="pencil__eraser"></div>
  </div>
  <div class="line"></div>
</template>

<script>
import '../assets/css/styles.scss'
export default {
  name: "Preloader-Component",
  data(){
    return{
      show: true
    }
  },
  mounted(){
      this.showToggle()
  },
  methods:{
    showToggle(){
      setTimeout(() => {
        this.show = false;
      }, 1000)
    }
  }
}
</script>

<style scoped>

</style>