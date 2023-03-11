<template>
  <div class="row">
    <Tags/>


    <div class="column">
      <p style="color: white">Featured Categories</p>
      <hr class="divider">


      <div class="row-card">

 <v-card
     :class="model"
      min-height=100%
      height=100%
     max-width=30%
     min-width=30%
     width=30%
      class="card">
   <div class="bg-nature">
     <div class="card-footer">
       <p class="card-label">Nature</p>
     </div>
   </div>
  </v-card>

<v-card
     :class="model"
      min-height=100%
     max-width=30%
     min-width=30%
     width=30%
      height=100%
      class="card">
   <div class="bg-sports">
     <div class="card-footer">
       <p class="card-label">Sports</p>
     </div>
   </div>
  </v-card>

<v-card
     :class="model"
      max-width=30%
      min-width=30%
      width=30%
      min-height=100%
      height=100%
      class="card">
   <div class="bg-food">
     <div class="card-footer">
       <p class="card-label">Food</p>
     </div>
   </div>
  </v-card>

<v-card
     :class="model"
     max-width=30%
     min-width=30%
     width=30%
      min-height=100%
      height=100%
      class="card">
   <div class="bg-art">
     <div class="card-footer">
       <p class="card-label">Art</p>
     </div>
   </div>
  </v-card>

<v-card
     :class="model"
     max-width=30%
     min-width=30%
     width=30%
      min-height=100%
      height=100%
      class="card">
   <div class="bg-architecture">
     <div class="card-footer">
       <p class="card-label">Architecture</p>
     </div>

   </div>
  </v-card>

        <v-card
     :class="model"
      max-width=30%
      min-width=30%
      min-height=100%
      width=30%
      height=100%
     class="card">
   <div class="bg-animals">
     <div class="card-footer">
       <p class="card-label">Animals</p>
     </div>
   </div>
  </v-card>

</div>

    </div>
    </div>

</template>

<script>
import Tags from './Home-Tags'
import VCard from 'vuetify'
import '../assets/css/styles.scss'

export default {
  name: "Home-Body",
  data: () => ({
    model: 'rounded-lg',
  }),
  components: {
    Tags,
    VCard
  }
}
</script>

<style scoped>
.card-footer{
  position: absolute;
  display: flex;
  flex-direction: column;
  bottom: 0;
  justify-content: center;
  vertical-align: center;
  width: 100%;
  background-color: #EBEAD3;
  border-radius: 2rem 2rem 0 0;
  height: 25%;
}
.bg-nature{
  background-image: url("../assets/images/nature.jpg");
  background-size: cover;
  min-width: 100%;
  min-height: 100%;
  height: 10rem;
  z-index: -1;
  width: 100%;
}

.bg-sports{
  background-image: url("../assets/images/sports.jpg");
  background-size: cover;
  min-width: 100%;
  min-height: 100%;
  height: 100%;
  z-index: -1;
  width: 100%;
}

.bg-food{
  background-image: url("../assets/images/food.jpg");
  background-size: cover;
  min-width: 100%;
  min-height: 100%;
  height: 100%;
  z-index: -1;
  width: 100%;
}

.bg-art{
  background-image: url("../assets/images/art.jpg");
  background-size: cover;
  min-width: 100%;
  min-height: 100%;
  height: 100%;
  z-index: -1;
  width: 100%;
}

.bg-animals{
  background-image: url("../assets/images/animals.jpg");
  background-size: cover;
  min-width: 100%;
  min-height: 100%;
  height: 100%;
  z-index: -1;
  width: 100%;
}

.bg-architecture{
  background-image: url("../assets/images/architecture.jpeg");
  background-size: cover;
  min-width: 100%;
  min-height: 100%;
  height: 100%;
  z-index: -1;
  width: 100%;
}
.card-label{
  font-family: 'gloria';
  font-size: 1.2rem;
}

.row{
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}
.row-card{
  display: flex;
  flex-direction: row;
  column-gap: 2rem;
  width: 100%;
  flex-wrap: wrap;
  row-gap: 2rem;
}
.column{
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 70%;
}

.divider{
  width: 30%;
  margin-top: 1rem;
  margin-bottom: 2rem;
}
.card{
  transition: transform .2s; /* Animation */
}
.card:hover {
  transform: scale(1.1);
  cursor: pointer/* (150% zoom - Note: if the zoom is too large, it will go outside of the viewport) */
}
</style>