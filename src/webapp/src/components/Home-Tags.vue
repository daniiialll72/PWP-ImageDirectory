<template>
  <div class="filters">

    <div class="filterBox">
      <div class="filterSearch">

        <div class="filterTitle">
          Tags
        </div>
        <hr class="divider">
          <v-list :items="items"></v-list>
      </div>

  </div>
  </div>
</template>

<script>
import VList from 'vuetify'

export default {
  name: "Home-Tags",
  components:{
    VList,
  },
  data: () => ({
    items: [
      {
        title: 'Item #1',
        value: 1,
      },
      {
        title: 'Item #2',
        value: 2,
      },
      {
        title: 'Item #3',
        value: 3,
      },
    ],
  }),
}
</script>

<style scoped>
.filterSearch{
  width: 100%;
}
.filterTitle{
  color: black;
}
.filterBox{
  /*border: 2px solid darkgoldenrod;*/
  border-radius: 1rem;
  margin: 1vw;
  padding: 1vw;
  display: flex;
  flex-direction: row;
  justify-content: center;
  background-color: white;
  width: 90%;
}
.filters{
  min-width: 20%;
  max-width: 30%;
}
.divider{
  width: 100%;
}
</style>