<template>
  <div class="row d-flex justify-space-between">
    <div class="column-logo">
      <p class="logo-font">Image Directory</p>
    </div>

    <!-- <div class="column-search">
      <v-text-field
        label="Search"
        prepend-inner-icon="mdi-magnify"
        variant="outlined"
        class="text-white"
      ></v-text-field>
    </div> -->

    <div class="column-button" @click="isDropdownVisible = !isDropdownVisible">
      <v-btn color="#EEA7A7" rounded="pill" width="10rem" height="3rem">
        <p style="color: #fff">Upload</p>
      </v-btn>
    </div>
  </div>
  <div class="row dropdown py-6">
    <form @submit.prevent="submitForm">
      <div>
        <label for="photo">Choose a photo:</label>
        <input type="file" id="photo" @change="handleFileUpload" />
      </div>
      <div>
        <label for="tags-input">Tags:</label>
        <input type="text" id="tags-input" v-model="tags" />
      </div>
      <div>
        <label for="description-input">Description:</label>
        <input type="text" id="description-input" v-model="description" />
      </div>
      <v-btn type="submit">Upload</v-btn>
    </form>
  </div>
</template>

<script>
import "../assets/css/styles.scss";
// import VTextField from "vuetify";
import VBtn from "vuetify";
import axios from "axios";

export default {
  name: "Main-Header",

  data() {
    return {
      isDropdownVisible: false,
      photo: null,
      tags: "",
      description: "",
    };
  },
  components: {
    // VTextField,
    VBtn,
  },
  methods: {
    openDropdown() {
      this.isDropdownVisible = true;
      console.log("open is working");
    },
    async submitForm() {
      try {
        const formData = new FormData();
        formData.append("photo", this.photo);
        formData.append("tags", this.tags);
        formData.append("description", this.description);
        const response = await axios.post("/api/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
.row {
  display: flex;
  flex-direction: row;
  width: 100%;
  max-width: 100%;
  justify-content: space-between;
  margin-bottom: 4rem;
}
.column-button {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  align-content: center;
  margin-right: 3rem;
}
.column-logo {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  align-content: center;
  margin-left: 2rem;
}
.column-search {
  display: flex;
  min-width: 60%;
  flex-direction: column;
  justify-content: center;
  margin-top: 1rem;
}

.logo-font {
  font-family: "tangerine";
  font-size: 2.5vw;
  color: white;
  margin: 0;
}
.text-white input {
  color: white !important;
}
/* DropDown for Upload */
.dropdown {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: white;
}
</style>
