<template>
  <!-- <div class="row container"> -->
  <v-container>
    <Header />
    <Body />
  </v-container>
  <!-- </div> -->
</template>

<script>
import Header from "./components/Main-Header";
import Body from "./components/Home-Body";

export default {
  name: "App",
  components: {
    Header,
    Body,
  },
};
</script>

<style>
body {
  margin: 0;
}
html {
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  background-image: linear-gradient(to bottom right, #5f5f5f, white);
  background-size: cover;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  height: fit-content;
  min-height: 100%;
}
</style>
