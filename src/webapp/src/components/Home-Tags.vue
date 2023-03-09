<template>
  <div class="box">

    <div class="filterBox">
      <div class="filterSearch">

        <div class="filterTitle">
          Tags
          <hr class="divider">
        </div>

        <div class="tagsList">
          <v-list :items="items"></v-list>
        </div>

      </div>

  </div>
  </div>
</template>

<script>
import VList from 'vuetify'
import '../assets/css/styles.scss'


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
      },{
        title: 'Item #3',
        value: 3,
      },{
        title: 'Item #3',
        value: 3,
      },{
        title: 'Item #3',
        value: 3,
      },{
        title: 'Item #3',
        value: 3,
      },{
        title: 'Item #3',
        value: 3,
      },{
        title: 'Item #3',
        value: 3,
      },{
        title: 'Item #3',
        value: 3,
      },{
        title: 'Item #3',
        value: 3,
      },{
        title: 'Item #3',
        value: 3,
      },
    ],
  }),
}
</script>

<style scoped>
.tagsList{
  display: flex;
  flex-direction: column;
  overflow-y: scroll;
  max-height: 50vh;

}
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
}

.divider{
  width: 100%;
}


</style>