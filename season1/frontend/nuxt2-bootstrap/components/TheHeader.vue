<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="danger">
      <b-navbar-brand href="/">Restaurant App</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-button size="sm" class="my-2 my-sm-0" variant="warning" to="restaurants/add_restaurant"
        >Add restaurant</b-button
      >
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-form>
            <b-form-input
              size="sm"
              class="mr-sm-2"
              placeholder="Username"
            ></b-form-input>
            <b-form-input
              size="sm"
              class="mr-sm-2"
              placeholder="Password"
            ></b-form-input>
            <b-button size="sm" class="my-2 my-sm-0" type="submit" variant="warning"
              >Log in</b-button
            >
          </b-nav-form>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>
