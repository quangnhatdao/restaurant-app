<template>
  <b-card
    :title="name"
    :img-src="image"
    img-alt="Image"
    img-right
    tag="article"
    class="restaurant-card"
  >
    <b-card-text>
      {{ address }}
    </b-card-text>
    <b-card-text>
      {{ tags }}
    </b-card-text>
    <b-button variant="warning" :href="'http://localhost:3000/restaurants/' + id">Go to details</b-button>
  </b-card>
</template>

<script>
const axios = require("axios").default;

export default {
  data() {
    return {};
  },
  props: {
    id: Number,
    name: String,
    address: String,
    tags: String,
    image: String,
  },
};
</script>

<style scoped>
.restaurant-card .card-img-right {
  width: 250px;
  height: 100%;
}
.restaurant-card {
  color: black;
  height: 200px;
}
</style>
