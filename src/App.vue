<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>TravelPlanner</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="!isAuthenticated" text to="/login">Login</v-btn>
      <v-btn v-if="!isAuthenticated" text to="/signup">Sign Up</v-btn>
      <v-btn v-if="isAuthenticated" text @click="logout">Logout</v-btn>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app>
      <v-list>
        <v-list-item to="/" exact>
          <v-list-item-icon>
            <v-icon>mdi-home</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item v-if="isAuthenticated" to="/plans">
          <v-list-item-icon>
            <v-icon>mdi-map-marker</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>My Plans</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item v-if="isAuthenticated" to="/favorites">
          <v-list-item-icon>
            <v-icon>mdi-heart</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Favorites</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item to="/about">
          <v-list-item-icon>
            <v-icon>mdi-information</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>About</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>

    <v-footer app color="primary" dark>
      <v-col class="text-center" cols="12">
        {{ new Date().getFullYear() }} — <strong>TravelPlanner</strong>
      </v-col>
    </v-footer>
  </v-app>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'App',
  data: () => ({
    drawer: false
  }),
  computed: {
    ...mapState(['isAuthenticated'])
  },
  methods: {
    ...mapActions(['logout'])
  }
}
</script>

<style>
.v-application {
  font-family: 'Roboto', sans-serif;
}
</style> 