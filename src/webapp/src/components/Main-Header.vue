<template>
  <div>
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

      <div
        class="column-button"
        @click="isDropdownVisible = !isDropdownVisible"
      >
        <v-btn color="#EEA7A7" rounded="pill" width="10rem" height="3rem">
          <p style="color: #fff">
            {{ isDropdownVisible ? "Close" : "Upload" }}
          </p>
        </v-btn>
      </div>
    </div>
    <transition name="fade">
      <div class="row dropdown py-6" v-show="isDropdownVisible">
        <h1>Upload your photo here</h1>
        <form ref="uploadForm" @submit.prevent="uploadPhoto">
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
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
          <v-btn
            color="#959595"
            rounded="pill"
            width="7rem"
            height="3rem"
            type="submit"
            class="mt-2"
          >
            <p style="color: #fff">Upload</p>
          </v-btn>
        </form>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from "axios";
import "../assets/css/styles.scss";
// import VTextField from "vuetify";
import VBtn from "vuetify";

export default {
  name: "Main-Header",

  data() {
    return {
      isDropdownVisible: false,
      file: null,
      tags: "",
      description: "",
      formIsEmpty: false,
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
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },

    async uploadPhoto() {
      try {
        // checking for empty fields
        if (!this.file || !this.tags || !this.description) {
          this.formIsEmpty = "true";
          console.log("the fields are empy");
          throw new Error("Please fill all required fields");
        }
        const formData = new FormData();
        formData.append("file", this.file);
        formData.append("tags", this.tags);
        formData.append("description", this.description);
        const response = await axios.post(
          "http://86.50.229.208:5000/api/images/",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        console.log(response.data);
        // to reset the form
        this.$refs.uploadForm.reset();
      } catch (error) {
        console.error(error);
        alert(error.message);
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
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #eea7a7ad;
}
.dropdown h1 {
  margin-bottom: 1rem;
  color: rgb(99, 98, 98);
  text-transform: capitalize;
  font-family: "tangerine";
  font-weight: bold;
  /* background-color: grey; */
}

input {
  margin-top: 0.4rem;
  margin-bottom: 0.4rem;
  padding: 0.5rem 2rem;
  width: 100%;
  background-color: white;
  border-radius: 20px;
}
label {
  font-weight: bold;
  margin-bottom: 0.3rem;
  color: white;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
.error-message {
  color: red;
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}
</style>
