<template>
  <b-card-group deck>
    <b-list-group-item
      class="d-flex justify-content-center m-5"
      v-for="restaurant in restaurants"
      :key="restaurant.id"
      ><RestaurantCard
        :id="restaurant.id"
        :name="restaurant.name"
        :address="restaurant.address"
        :tags="restaurant.tags"
        :image="restaurant.image"
      ></RestaurantCard
    ></b-list-group-item>
  </b-card-group>
</template>

<script>
import RestaurantCard from "~/components/RestaurantCard.vue";

const axios = require("axios").default;

export default {
  components: { RestaurantCard },

  data() {
    return {
      restaurants: [],
    };
  },

  mounted() {
    var vm = this;
    function create_restaurant_from_JSON_object(restaraunt_data) {
      var restaurant = {
        id: restaraunt_data.pk,
        name: restaraunt_data.fields.name,
        address: restaraunt_data.fields.address,
        tags: restaraunt_data.fields.tags,
        image: "http://127.0.0.1:8000/media/" + restaraunt_data.fields.image,
      };
      vm.restaurants.push(restaurant)
    }
    axios
      .get("http://127.0.0.1:8000/api/restaurants/")
      .then(function (response) {
        response.data.forEach(
          create_restaurant_from_JSON_object
        );
      })
      .catch(function (error) {
        console.log(error);
      })
      .then(function () {});
  },
};
</script>

<style scoped>
.card-deck .card {
    margin-right: 0;
    margin-left: 0;
}
.list-group-item {
    padding: 0;
}
</style>
