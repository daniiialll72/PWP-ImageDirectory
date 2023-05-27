<template>
  <div class="row">
    <!-- <Tags /> -->

    <div class="column">
      <p style="color: white">Images</p>
      <hr class="divider" />
      <div class="cards">
        <v-row>
          <v-col v-for="(item, id) in items" :key="id" :cols="4">
            <v-card class="my-4 card">
              <v-img class="image" :src="item.url"></v-img>
              <v-col col="9" class="footer-img-container">
                <v-card-title class="card-title"
                  >#{{ item.tags.join(", #") }}</v-card-title
                >
                <v-card-text class="card-text">{{
                  item.description
                }}</v-card-text>
              </v-col>
              <v-card-actions class="btns">
                <v-btn class="delete-btn btn" @click="deleteImage(item.id)"
                  >Delete</v-btn
                >
                <v-btn class="edut-btn btn" @click="editImage(item.id)"
                  >Edit</v-btn
                >
              </v-card-actions>
            </v-card>
            <!-- POP UP  -->

            <div class="modal-container" v-show="isModalVisible">
              <v-card class="modal-card">
                <v-img
                  v-bind:src="editedItem.url"
                  height="250px"
                  width="250px"
                ></v-img>
                <v-text-field
                  v-model="editedItem.description"
                  label="Description"
                ></v-text-field>
                <v-text-field
                  v-model="editedItem.tags"
                  label="Tags"
                ></v-text-field>
                <div class="btn-container mt-5">
                  <v-btn class="mx-1" @click="saveItem">Save</v-btn>
                  <v-btn @click="closeModal" class="mx-1">Close</v-btn>
                </div>
              </v-card>
            </div>
          </v-col>
        </v-row>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import "../assets/css/styles.scss";

export default {
  name: "Home-Body",
  data: () => ({
    model: "rounded-lg",
    isModalVisible: false,
    title: "list of items",
    items: [],
    editedItem: {
      id: null,
      url: "",
      description: "",
      tags: [],
    },
  }),
  components: {},
  mounted() {
    axios
      .get("http://86.50.229.208:5000/api/images/")
      .then((response) => {
        this.items = response.data.data;
        console.log(
          "is the api working with api?",
          JSON.parse(JSON.stringify(this.items.data))
        );
      })
      .catch((error) => {
        console.log(error);
      });
  },
  methods: {
    openModal() {
      this.isModalVisible = true;
      console.log("open is working");
    },
    closeModal() {
      this.isModalVisible = false;
    },
    deleteImage(imageId) {
      console.log("the image is about to be deleted");
      axios
        .delete(`http://86.50.229.208:5000/api/images/${imageId}`)
        .then((response) => {
          console.log(response.data);
          // Remove the item with matching imageId from the items array
          const index = this.items.findIndex((item) => item.id === imageId);
          if (index !== -1) {
            this.items.splice(index, 1);
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    editImage(itemId) {
      // Find the item by its ID in the 'items' array
      const itemToEdit = this.items.find((item) => item.id === itemId);

      // Update the 'editedItem' data property with the item data
      this.editedItem = {
        id: itemToEdit.id,
        url: itemToEdit.url,
        description: itemToEdit.description,
        tags: [...itemToEdit.tags], // Create a copy of the tags array to prevent modification of the original item
      };

      // Show the modal for editing the item
      this.isModalVisible = true;
    },

    // Function to handle the save event
    saveItem() {
      // Send the edited item data to the server using Axios PUT request
      console.log("the edited item is", this.editedItem);
      axios
        .patch("http://86.50.229.208:5000/api/images/" + this.editedItem.id, {
          description: this.editedItem.description,
          tags: this.editedItem.tags,
        })
        .then((response) => {
          // Handle the response if needed
          console.log(response.data);
          // Close the modal
          this.isModalVisible = false;
          // Update the item in the 'items' array with the edited version
          const index = this.items.findIndex(
            (item) => item.id === this.editedItem.id
          );
          if (index !== -1) {
            this.items.splice(index, 1, this.editedItem);
          }
        })
        .catch((error) => {
          // Handle the error if needed
          console.error(error);
        });
      this.isModalVisible = false;
    },
  },
};
</script>

<style scoped>
.footer-img-container {
  background-color: #ebead3;
  border-top-left-radius: 30px;
  border-top-right-radius: 30px;
  position: absolute;
  bottom: 0;
  width: 100%;
  padding: 0;
}

.btns {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
.btn {
  background-color: white;
  font-size: 0.5rem;
  font-weight: bold;
  width: 45px;
  /* position: absolute; */
}
.btn:hover {
  background-color: gray;
}
.cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}
.card-footer {
  position: absolute;
  display: flex;
  flex-direction: column;
  bottom: 0;
  justify-content: center;
  vertical-align: center;
  width: 100%;
  background-color: #ebead3;
  border-radius: 2rem 2rem 0 0;
  height: 25%;
}
.bg-nature {
  background-image: url("../assets/images/nature.jpg");
  background-size: cover;
  min-width: 100%;
  min-height: 100%;
  height: 10rem;
  z-index: -1;
  width: 100%;
}

.bg-sports {
  background-image: url("../assets/images/sports.jpg");
  background-size: cover;
  min-width: 100%;
  min-height: 100%;
  height: 100%;
  z-index: -1;
  width: 100%;
}

.bg-food {
  background-image: url("../assets/images/food.jpg");
  background-size: cover;
  min-width: 100%;
  min-height: 100%;
  height: 100%;
  z-index: -1;
  width: 100%;
}

.bg-art {
  background-image: url("../assets/images/art.jpg");
  background-size: cover;
  min-width: 100%;
  min-height: 100%;
  height: 100%;
  z-index: -1;
  width: 100%;
}

.bg-animals {
  background-image: url("../assets/images/animals.jpg");
  background-size: cover;
  min-width: 100%;
  min-height: 100%;
  height: 100%;
  z-index: -1;
  width: 100%;
}

.bg-architecture {
  background-image: url("../assets/images/architecture.jpeg");
  background-size: cover;
  min-width: 100%;
  min-height: 100%;
  height: 100%;
  z-index: -1;
  width: 100%;
}
.card-label {
  font-family: "gloria";
  font-size: 1.2rem;
}

.row {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}
.row-card {
  display: flex;
  flex-direction: row;
  column-gap: 2rem;
  width: 100%;
  flex-wrap: wrap;
  row-gap: 2rem;
}
.column {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 70%;
}

.divider {
  width: 30%;
  margin-top: 1rem;
  margin-bottom: 2rem;
}
.card {
  transition: transform 0.2s; /* Animation */
  background-color: rgb(56, 56, 56);
}
.card:hover {
  transform: scale(1.1);
  cursor: pointer; /* (150% zoom - Note: if the zoom is too large, it will go outside of the viewport) */
}
.image {
  height: 300px;
  width: 600px;
}
.card-title {
  font-size: 1rem;
  padding: 0;
}
.card-text {
  font-size: 0.8rem;
  padding: 0.625rem;
}

.modal-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
  width: 100vw;
  height: 100vh;
  background: rgba(69, 69, 69, 0.482);
}
.modal-card {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 600px;
  height: 600px;
  z-index: 1;
}
</style>
