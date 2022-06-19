<template>
  <div>
    <b-form @submit="onSubmit" @reset="onReset">
      <b-form-group
        id="input-group-1"
        label="Name:"
        label-for="input-1"
        description="Name of restaurant"
      >
        <b-form-input
          id="input-1"
          v-model="form.name"
          type="text"
          placeholder="Enter name of restaurant"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="input-group-2"
        label="Address:"
        label-for="input-2"
        description="Address of restaurant"
      >
        <b-form-input
          id="input-2"
          v-model="form.address"
          type="text"
          placeholder="Enter address of restaurant"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="input-group-3"
        label="Tags:"
        label-for="input-3"
        description="Tags of restaurant"
      >
        <b-form-input
          id="input-3"
          v-model="form.tags"
          type="text"
          placeholder="Enter tags of restaurant"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="input-group-4"
        label="Image:"
        label-for="input-4"
        description="Image of restaurant"
      >
        <b-form-file
          v-model="form.image"
          :state="Boolean(form.image)"
          placeholder="Choose an image or drop it here..."
          drop-placeholder="Drop image here..."
          accept="image/jpeg, image/png"
          required
        ></b-form-file>
      </b-form-group>

      <b-button type="submit" variant="warning">Submit</b-button>
      <b-button type="reset" variant="warning">Reset</b-button>

      <b-modal id="restaurant-add-success-modal" title="Add successful" ok-variant="warning" @ok="handleOk">
        <p class="my-4">Restaurant was successfully added</p>
      </b-modal>

      <b-modal id="restaurant-add-fail-modal" title="Add failed" ok-variant="warning">
        <p class="my-4">Restaurant unfortunately failed to be added</p>
      </b-modal>
    </b-form>
  </div>
</template>

<script>
const axios = require("axios").default;

export default {
  data() {
    return {
      form: {
        name: "",
        address: "",
        tags: "",
        image: null,
      },
    };
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();
      var vm = this;
      var formData = new FormData();
      formData.append('name', this.form.name);
      formData.append('address', this.form.address);
      formData.append('tags', this.form.tags);
      formData.append('image', this.form.image);

      axios
        .post(
          "http://127.0.0.1:8000/api/restaurants/",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        )
        .then(function (response) {
          console.log(response);
          vm.$bvModal.show("restaurant-add-success-modal");
        })
        .catch(function (error) {
          console.log(error);
          vm.$bvModal.show("restaurant-add-fail-modal");
        });
    },
    onReset(event) {
      event.preventDefault();
      // Reset our form values
      this.form.name = "";
      this.form.address = "";
      this.form.tags = "";
      this.form.image = null;
    },
    handleOk(bvModalEvent) {
        // Prevent modal from closing
        bvModalEvent.preventDefault()

        window.location.href = 'http://localhost:3000/'
    },
  },
};
</script>
