<template>
  <Header/>
  <Body/>

</template>

<script>
import Header from './components/Main-Header'
import Body from './components/Home-Body'



export default {
  name: 'App',
  components: {
    Header,
    Body
  }
}
</script>


<style>

body{
  margin: 0;
}
html{
  /*background-color: #35F29A;*/
  -webkit-background-size: contain;
  -moz-background-size: contain;
  -o-background-size: contain;
  background-size: 100% 100%;
  background-color: #5F5F5F;

}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: #5F5F5F;
}
</style>
