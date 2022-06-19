<template>
  <div class="d-flex flex-column align-items-center">
    <b-img-lazy :src="image" alt="Image" id="dish-image"></b-img-lazy>

    <b-form @submit="onSubmit" @reset="onReset">
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
        ></b-form-file>
      </b-form-group>

      <b-button type="submit" variant="warning">Edit</b-button>
      <b-button type="reset" variant="warning">Reset</b-button>
      <b-button v-b-modal.dish-delete-confirm-modal variant="warning">Delete</b-button>

      <b-modal
        id="dish-edit-success-modal"
        title="Edit successful"
        ok-variant="warning"
        @ok="handleOk"
      >
        <p class="my-4">Your edit was successfully processed</p>
      </b-modal>

      <b-modal
        id="dish-edit-fail-modal"
        title="Edit failed"
        ok-variant="warning"
      >
        <p class="my-4">Your edit unfortunately failed</p>
      </b-modal>

      <b-modal id="dish-delete-confirm-modal" title="Delete dish" ok-variant="warning" @ok="handleOkDelete">
        <p class="my-4">Do you want to delete this dish?</p>
        <template v-slot:modal-ok>
          Delete
        </template>
      </b-modal>
    </b-form>
  </div>
</template>

<script>
const axios = require("axios").default;

export default {
  async asyncData({ params }) {
    const restaurant = params.restaurant;
    const dish = params.dish;
    return { restaurant, dish };
  },

  data() {
    return {
      dish_form: {
        name: "",
        description: "",
        price: 0,
        image: null,
      },
      original_data: {
        name: "",
        description: "",
        price: 0,
        image: null,
      },
      image: "",
    };
  },

  methods: {
    onSubmit(event) {
      event.preventDefault();
      var vm = this;
      axios
        .put(
          "http://127.0.0.1:8000/api/restaurants/" +
            vm.restaurant +
            "/dishes/" +
            vm.dish +
            "/",
          JSON.stringify(this.dish_form)
        )
        .then(function (response) {
          console.log(response);
          if (vm.dish_form.image !== null) {
            var formData = new FormData();
            formData.append("image", vm.dish_form.image);
            axios
              .post(
                "http://127.0.0.1:8000/api/restaurants/" +
                  vm.restaurant +
                  "/dishes/" +
                  vm.dish +
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
                vm.$bvModal.show("dish-edit-success-modal");
              })
              .catch(function (error) {
                console.log(error);
                vm.$bvModal.show("dish-edit-fail-modal");
              });
          } else {
            vm.$bvModal.show("dish-edit-success-modal");
          }
        })
        .catch(function (error) {
          console.log(error);
          vm.$bvModal.show("dish-edit-fail-modal");
        });
    },
    onReset(event) {
      event.preventDefault();
      // Reset our form values
      this.dish_form.name = this.original_data.name;
      this.dish_form.description = this.original_data.description;
      this.dish_form.price = this.original_data.price;
      this.dish_form.image = null;
    },
    handleOkDelete(bvModalEvent) {
      // Prevent modal from closing
      bvModalEvent.preventDefault();

      var vm = this;

      // Trigger submit handler
      axios
        .delete("http://127.0.0.1:8000/api/restaurants/" +
          vm.restaurant +
          "/dishes/" +
          vm.dish +
          "/")
        .then(function (response) {
          console.log(response);
          window.location.href = "http://localhost:3000/restaurants/" + vm.restaurant;
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    handleOk(bvModalEvent) {
      // Prevent modal from closing
      bvModalEvent.preventDefault();

      location.reload();
    },
  },

  mounted() {
    var vm = this;

    axios
      .get(
        "http://127.0.0.1:8000/api/restaurants/" +
          vm.restaurant +
          "/dishes/" +
          vm.dish +
          "/"
      )
      .then(function (response) {
        console.log(response.data);
        vm.dish_form.name = response.data[0].fields.name;
        vm.dish_form.description = response.data[0].fields.description;
        vm.dish_form.price = response.data[0].fields.price;
        vm.image =
          "http://127.0.0.1:8000/media/" + response.data[0].fields.image;

        vm.original_data.name = response.data[0].fields.name;
        vm.original_data.description = response.data[0].fields.description;
        vm.original_data.price = response.data[0].fields.price;
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

#dish-image {
  width: 50vw;
  height: 20vh;
}
</style>
