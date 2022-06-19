<template>
  <b-card
    :title="name"
    :img-src="image"
    img-alt="Image"
    img-right
    tag="article"
    class="dish-card"
  >
    <b-card-text>
      {{ 'description: ' + description }}
    </b-card-text>
    <b-card-text>
      {{ 'price: ' + price + '$' }}
    </b-card-text>
    <b-button variant="warning" :href="'http://localhost:3000/restaurants/' + restaurant + '/dishes/' + id">Go to details</b-button>
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
    description: String,
    price: Number,
    restaurant: Number,
    image: String
  },
};
</script>

<style scoped>
.dish-card .card-img-right {
  width: 300px;
  height: 100%;
}
.dish-card {
  color: black;
  height: 200px;
}
</style>
