<template>
  <div class="d-flex flex-column align-items-center">
    <b-img-lazy :src="image" alt="Image" id="restaurant-image"></b-img-lazy>
    <h4>{{ original_data.name }}</h4>
    <p>{{ original_data.address }}</p>
    <p>{{ original_data.tags }}</p>

    <b-card-group deck v-show="state == 'details'">
      <b-list-group-item
        class="d-flex justify-content-center m-5"
        v-for="dish in dishes"
        :key="dish.id"
        ><DishCard
          :id="dish.id"
          :name="dish.name"
          :description="dish.description"
          :price="dish.price"
          :restaurant="dish.restaurant"
          :image="dish.image"
        ></DishCard
      ></b-list-group-item>
    </b-card-group>

    <b-form @submit="onSubmit" @reset="onReset" v-show="state == 'edit'">
      <b-form-group
        id="restaurant-input-group-1"
        label="Name:"
        label-for="restaurant-input-1"
        description="Name of restaurant"
      >
        <b-form-input
          id="restaurant-input-1"
          v-model="restaurant_form.name"
          type="text"
          placeholder="Enter name of restaurant"
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="restaurant-input-group-2"
        label="Address:"
        label-for="restaurant-input-2"
        description="Address of restaurant"
      >
        <b-form-input
          id="restaurant-input-2"
          v-model="restaurant_form.address"
          type="text"
          placeholder="Enter address of restaurant"
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="restaurant-input-group-3"
        label="Tags:"
        label-for="restaurant-input-3"
        description="Tags of restaurant"
      >
        <b-form-input
          id="restaurant-input-3"
          v-model="restaurant_form.tags"
          type="text"
          placeholder="Enter tags of restaurant"
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="restaurant-input-group-4"
        label="Image:"
        label-for="restaurant-input-4"
        description="Image of restaurant"
      >
        <b-form-file
          v-model="restaurant_form.image"
          placeholder="Choose an image or drop it here..."
          drop-placeholder="Drop image here..."
          accept="image/jpeg, image/png"
        ></b-form-file>
      </b-form-group>

      <b-button type="submit" variant="warning">Edit</b-button>
      <b-button type="reset" variant="warning">Reset</b-button>

      <b-modal id="restaurant-edit-success-modal" title="Edit successful" ok-variant="warning">
        <p class="my-4">Your edit was successfully processed</p>
      </b-modal>

      <b-modal id="restaurant-edit-fail-modal" title="Edit failed" ok-variant="warning">
        <p class="my-4">Your edit unfortunately failed</p>
      </b-modal>
    </b-form>

    <b-form @submit="onSubmit" @reset="onReset" v-show="state == 'add dish'">
      <b-form-group
        id="dish-input-group-1"
        label="Name:"
        label-for="dish-input-1"
        description="Name of dish"
      >
        <b-form-input
          id="dish-input-1"
          v-model="dish_form.name"
          type="text"
          placeholder="Enter name of dish"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="dish-input-group-2"
        label="Description:"
        label-for="dish-input-2"
        description="Description of dish"
      >
        <b-form-input
          id="dish-input-2"
          v-model="dish_form.description"
          type="text"
          placeholder="Enter description of dish"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="dish-input-group-3"
        label="Price:"
        label-for="dish-input-3"
        description="Price of dish"
      >
        <b-form-input
          id="dish-input-3"
          v-model="dish_form.price"
          type="number"
          placeholder="Enter price of dish"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="dish-input-group-4"
        label="Image:"
        label-for="dish-input-4"
        description="Image of dish"
      >
        <b-form-file
          v-model="dish_form.image"
          placeholder="Choose an image or drop it here..."
          drop-placeholder="Drop image here..."
          accept="image/jpeg, image/png"
          required
        ></b-form-file>
      </b-form-group>

      <b-button type="submit" variant="warning">Add</b-button>
      <b-button type="reset" variant="warning">Reset</b-button>

      <b-modal id="dish-add-success-modal" title="Dish added successfully" ok-variant="warning">
        <p class="my-4">Your dish was successfully added</p>
      </b-modal>

      <b-modal id="dish-add-fail-modal" title="Dish failed to be added" ok-variant="warning">
        <p class="my-4">Your dish unfortunately failed to be added</p>
      </b-modal>
    </b-form>

    <b-button-group class="my-5 p-3 bg-danger button-group">
      <b-button
        :variant="state == 'details' ? 'warning' : 'secondary'"
        class="mx-2"
        @click="state = 'details'"
        >Details</b-button
      >
      <b-button
        :variant="state == 'edit' ? 'warning' : 'secondary'"
        class="mx-2"
        @click="state = 'edit'"
        >Edit</b-button
      >
      <b-button
        :variant="state == 'add dish' ? 'warning' : 'secondary'"
        class="mx-2"
        @click="state = 'add dish'"
        >Add dishes</b-button
      >
      <b-button
        :variant="state == 'delete' ? 'warning' : 'secondary'"
        class="mx-2"
        @click="state = 'delete'"
        v-b-modal.restaurant-delete-confirm-modal
        >Delete</b-button
      >

      <b-modal id="restaurant-delete-confirm-modal" title="Delete restaurant" ok-variant="warning" @ok="handleOk">
        <p class="my-4">Do you want to delete this restaurant?</p>
        <template v-slot:modal-ok>
          Delete
        </template>
      </b-modal>
    </b-button-group>
  </div>
</template>

<script>
const axios = require("axios").default;

export default {
  async asyncData({ params }) {
    const restaurant = params.restaurant; // When calling /abc the slug will be "abc"
    return { restaurant };
  },

  data() {
    return {
      restaurant_form: {
        name: "",
        address: "",
        tags: "",
        image: null,
      },
      dish_form: {
        name: "",
        description: "",
        price: 0,
        image: null,
      },
      original_data: {
        name: "",
        address: "",
        tags: "",
        image: null,
      },
      state: "details",
      dishes: [],
      image: "",
    };
  },

  methods: {
    onSubmit(event) {
      event.preventDefault();
      var vm = this;
      if (this.state == "edit") {
        axios
          .put(
            "http://127.0.0.1:8000/api/restaurants/" + vm.restaurant + "/",
            JSON.stringify(this.restaurant_form)
          )
          .then(function (response) {
            console.log(response);
            if (vm.restaurant_form.image !== null) {
              var formData = new FormData();
              formData.append("image", vm.restaurant_form.image);
              axios
                .post(
                  "http://127.0.0.1:8000/api/restaurants/" +
                    vm.restaurant +
                    "/upload_image/",
                  formData,
                  {
                    headers: {
                      "Content-Type": "multipart/form-data",
                    },
                  }
                )
                .then(function (response) {
                  console.log(response);
                  vm.$bvModal.show("restaurant-edit-success-modal");
                })
                .catch(function (error) {
                  console.log(error);
                  vm.$bvModal.show("restaurant-edit-fail-modal");
                });
            } else {
              vm.$bvModal.show("restaurant-edit-success-modal");
            }
          })
          .catch(function (error) {
            console.log(error);
            vm.$bvModal.show("restaurant-edit-fail-modal");
          });
      } else if ((this.state = "add dish")) {
        var formData = new FormData();
        formData.append("name", this.dish_form.name);
        formData.append("description", this.dish_form.description);
        formData.append("price", this.dish_form.price);
        formData.append("restaurant", vm.restaurant);
        formData.append("image", this.dish_form.image);
        axios
          .post(
            "http://127.0.0.1:8000/api/restaurants/" +
              vm.restaurant +
              "/dishes/",
            formData,
            {
              headers: {
                "Content-Type": "multipart/form-data",
              },
            }
          )
          .then(function (response) {
            console.log(response);
            vm.$bvModal.show("dish-add-success-modal");
          })
          .catch(function (error) {
            console.log(error);
            vm.$bvModal.show("dish-add-fail-modal");
          });
      }
    },
    onReset(event) {
      event.preventDefault();
      // Reset our form values
      if (this.state == "edit") {
        this.restaurant_form.name = this.original_data.name;
        this.restaurant_form.address = this.original_data.address;
        this.restaurant_form.tags = this.original_data.tags;
        this.restaurant_form.image = null;
      } else if (this.state == "add dish") {
        this.dish_form.name = "";
        this.dish_form.description = "";
        this.dish_form.price = 0;
        this.dish_form.image = null;
      }
    },
    handleOk(bvModalEvent) {
        // Prevent modal from closing
        bvModalEvent.preventDefault()

        var vm = this;

        // Trigger submit handler
        axios
          .delete(
            "http://127.0.0.1:8000/api/restaurants/" +
              vm.restaurant +
              "/"
          )
          .then(function (response) {
            console.log(response);
            window.location.href = 'http://localhost:3000/'
          })
          .catch(function (error) {
            console.log(error);
          });
    },
  },

  mounted() {
    var vm = this;

    function create_dish_from_JSON_object(dish_data) {
      var dish = {
        id: dish_data.pk,
        name: dish_data.fields.name,
        description: dish_data.fields.description,
        price: dish_data.fields.price,
        restaurant: dish_data.fields.restaurant,
        image: "http://127.0.0.1:8000/media/" + dish_data.fields.image,
      };
      vm.dishes.push(dish);
    }

    axios
      .get("http://127.0.0.1:8000/api/restaurants/" + vm.restaurant)
      .then(function (response) {
        console.log(response.data);
        vm.restaurant_form.name = response.data[0].fields.name;
        vm.restaurant_form.address = response.data[0].fields.address;
        vm.restaurant_form.tags = response.data[0].fields.tags;
        vm.image =
          "http://127.0.0.1:8000/media/" + response.data[0].fields.image;

        vm.original_data.name = response.data[0].fields.name;
        vm.original_data.address = response.data[0].fields.address;
        vm.original_data.tags = response.data[0].fields.tags;

        axios
          .get(
            "http://127.0.0.1:8000/api/restaurants/" +
              vm.restaurant +
              "/dishes/"
          )
          .then(function (response) {
            response.data.forEach(create_dish_from_JSON_object);
          })
          .catch(function (error) {
            console.log(error);
          })
          .then(function () {});
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

#restaurant-image {
  width: 100vw;
  height: 20vh;
}
</style>
