<template>
<div class="row">
  <div class="column-logo">
    <p class="logo-font">
      Image Directory
    </p>
  </div>


  <div class="column-search">
    <v-text-field
        label="Search"
        prepend-inner-icon="mdi-map-marker"
        variant="outlined"
        class="text-white"
    ></v-text-field>
  </div>


  <div class="column-button">
    <v-btn
        color="#EEA7A7"
        rounded="pill">
      <p style="color:#fff;">Upload</p>
    </v-btn>
  </div>

</div>
</template>

<script>
import '../assets/css/styles.scss'
import VTextField from 'vuetify'
import VBtn from 'vuetify'
export default {
  name: "Main-Header",
  components: {
    VTextField,
    VBtn,
  }
}
</script>

<style scoped>
.row{
  display: flex;
  flex-direction: row;
  width: 100%;
  max-width: 100%;
  justify-content: space-between;
}
.column-button{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  align-content: center;
  margin-right: 3rem;
}
.column-logo{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  align-content: center;
  margin-left: 2rem;
}
.column-search{
  display: flex;
  min-width: 60%;
  flex-direction: column;
  justify-content: center;
  margin-top: 1rem;
}

.logo-font{
  font-family: 'tangerine';
  font-size: 2.5vw;
  color: white;
  margin: 0;
}
.text-white input {
  color: white !important;
}
</style>