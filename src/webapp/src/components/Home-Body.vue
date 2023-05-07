<template>
  <div class="row container">
    <Tags />

    <div class="column">
      <p style="color: white">Featured Categories</p>
      <hr class="divider" />

      <!-- <div class="row-card">
        <v-card
          :class="model"
          min-height="100%"
          height="100%"
          max-width="30%"
          min-width="30%"
          width="30%"
          class="card"
        >
          <div class="bg-nature">
            <div class="card-footer">
              <p class="card-label">Nature</p>
            </div>
          </div>
        </v-card>

        <v-card
          :class="model"
          min-height="100%"
          max-width="30%"
          min-width="30%"
          width="30%"
          height="100%"
          class="card"
        >
          <div class="bg-sports">
            <div class="card-footer">
              <p class="card-label">Sports</p>
            </div>
          </div>
        </v-card>

        <v-card
          :class="model"
          max-width="30%"
          min-width="30%"
          width="30%"
          min-height="100%"
          height="100%"
          class="card"
        >
          <div class="bg-food">
            <div class="card-footer">
              <p class="card-label">Food</p>
            </div>
          </div>
        </v-card>

        <v-card
          :class="model"
          max-width="30%"
          min-width="30%"
          width="30%"
          min-height="100%"
          height="100%"
          class="card"
        >
          <div class="bg-art">
            <div class="card-footer">
              <p class="card-label">Art</p>
            </div>
          </div>
        </v-card>

        <v-card
          :class="model"
          max-width="30%"
          min-width="30%"
          width="30%"
          min-height="100%"
          height="100%"
          class="card"
        >
          <div class="bg-architecture">
            <div class="card-footer">
              <p class="card-label">Architecture</p>
            </div>
          </div>
        </v-card>

        <v-card
          :class="model"
          max-width="30%"
          min-width="30%"
          min-height="100%"
          width="30%"
          height="100%"
          class="card"
        >
          <div class="bg-animals">
            <div class="card-footer">
              <p class="card-label">Animals</p>
            </div>
          </div>
        </v-card>
        <v-card>
          <ul v-if="items.length">
            <li v-for="item in items" :key="item.id">{{ item }}</li>
          </ul>
          <p v-else>No item to display</p>
        </v-card>
      </div> -->
      <div class="cards">
        <v-row>
          <v-col v-for="(card, index) in cards" :key="index" :cols="4">
            <v-card class="my-4 card">
              <v-img
                :src="card.imageUrl"
                min-height="300px"
                min-width="300px"
              ></v-img>
              <div class="footer-img-container">
                <v-card-title>{{ card.title }}</v-card-title>
                <v-card-text>{{ card.description }}</v-card-text>
                <hr />
                <v-card-actions class="justify-space-between btns">
                  <v-btn @click="openModal" class="edit-btn btn">Edit</v-btn>
                  <v-btn class="delete-btn btn">Delete</v-btn>
                </v-card-actions>
              </div>
            </v-card>
            <!-- POP UP  -->
            <div
              class="modal-container"
              v-show="isModalVisible"
              @click="closeModal"
            >
              <v-card class="modal-card">
                <v-img
                  :src="card.imageUrl"
                  height="250px"
                  width="250px"
                ></v-img>
                <h2>{{ card.title }}</h2>
                <p>{{ card.description }}</p>
                <div class="btn-container mt-5">
                  <v-btn class="mx-1">Save</v-btn>
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
import Tags from "./Home-Tags";
import VCard from "vuetify";
// import Modal from "./Home-Modal";
import "../assets/css/styles.scss";
import axios from "axios";
// import { BIconArrrowUp } from "bootstrap-vue";

export default {
  name: "Home-Body",
  data: () => ({
    model: "rounded-lg",
    isModalVisible: false,
    title: "list of items",
    items: [],
    cards: [
      {
        title: "Card 1",
        description: "This is the first card",
        imageUrl: "https://picsum.photos/200/300",
      },
      {
        title: "Card 2",
        description: "This is the second card",
        imageUrl: "https://picsum.photos/200/300",
      },
      {
        title: "Card 3",
        description: "This is the third card",
        imageUrl: "https://picsum.photos/200/300",
      },
      {
        title: "Card 4",
        description: "This is the fourth card",
        imageUrl: "https://picsum.photos/200/300",
      },
      {
        title: "Card 5",
        description: "This is the fifth card",
        imageUrl: "https://picsum.photos/200/300",
      },
      {
        title: "Card 6",
        description: "This is the sixth card",
        imageUrl: "https://picsum.photos/200/300",
      },
    ],
  }),
  components: {
    Tags,
    VCard,
    // Modal,
    // BIconArrrowUp,
  },
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
      console.log("close is working");
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
}
.btns {
  background-color: orange;
}
.btn {
  background-color: white;
  font-size: 0.6rem;
  font-weight: bold;
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
}
.card:hover {
  transform: scale(1.1);
  cursor: pointer; /* (150% zoom - Note: if the zoom is too large, it will go outside of the viewport) */
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
