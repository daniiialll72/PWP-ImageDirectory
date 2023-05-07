<template>
  <div class="box">
    <p style="color: white" class="hidden">Featured Categories</p>
    <hr class="divider-hidden hidden" />
    <div class="filterBox">
      <div class="filterSearch">
        <div class="filterTitle">
          Tags
          <hr class="divider" />
        </div>

        <div class="tagsList">
          <v-list :items="items"></v-list>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VList from "vuetify";
import "../assets/css/styles.scss";

export default {
  name: "Home-Tags",
  components: {
    VList,
  },
  data: () => ({
    items: [
      {
        title: "Item #1",
        value: 1,
      },
      {
        title: "Item #2",
        value: 2,
      },
      {
        title: "Item #3",
        value: 3,
      },
      {
        title: "Item #3",
        value: 3,
      },
      {
        title: "Item #3",
        value: 3,
      },
      {
        title: "Item #3",
        value: 3,
      },
      {
        title: "Item #3",
        value: 3,
      },
      {
        title: "Item #3",
        value: 3,
      },
      {
        title: "Item #3",
        value: 3,
      },
      {
        title: "Item #3",
        value: 3,
      },
      {
        title: "Item #3",
        value: 3,
      },
      {
        title: "Item #3",
        value: 3,
      },
    ],
  }),
};
</script>

<style scoped>
.box {
  overflow: hidden;
  background-color: rgba(255, 0, 0, 0) !important;
}
.tagsList {
  display: flex;
  flex-direction: column;
  /* overflow-y: scroll; */
  /* overflow: hidden; */
  max-height: 50vh;
}
.filterSearch {
  width: 100%;
}
.filterTitle {
  color: black;
}
.filterBox {
  /*border: 2px solid darkgoldenrod;*/
  border-radius: 1rem;
  margin: 1vw;
  padding: 1vw;
  display: flex;
  flex-direction: row;
  justify-content: center;
  background-color: white;
}

.divider {
  width: 100%;
}
.divider-hidden {
  /* display: none; */
  visibility: hidden;
  width: 30%;
  margin-top: 1rem;
  margin-bottom: 2rem;
}
.hidden {
  visibility: hidden;
}
</style>
