<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Login</v-toolbar-title>
            <v-spacer></v-spacer>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleLogin" ref="form">
              <v-text-field
                v-model="email"
                label="Email"
                name="email"
                prepend-icon="mdi-email"
                type="email"
                :rules="emailRules"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="Password"
                name="password"
                prepend-icon="mdi-lock"
                type="password"
                :rules="passwordRules"
                required
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              @click="handleLogin"
              :loading="loading"
              :disabled="loading"
            >
              Login
            </v-btn>
          </v-card-actions>
          <v-card-text class="text-center">
            <p class="mb-0">
              Don't have an account?
              <router-link to="/signup" class="text-decoration-none">
                Sign up
              </router-link>
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Error Snackbar -->
    <v-snackbar
      v-model="snackbar"
      color="error"
      timeout="3000"
    >
      {{ errorMessage }}
      <template v-slot:actions>
        <v-btn
          color="white"
          text
          @click="snackbar = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'Login',
  data: () => ({
    email: '',
    password: '',
    loading: false,
    snackbar: false,
    errorMessage: '',
    emailRules: [
      v => !!v || 'Email is required',
      v => /.+@.+\..+/.test(v) || 'Email must be valid'
    ],
    passwordRules: [
      v => !!v || 'Password is required',
      v => v.length >= 6 || 'Password must be at least 6 characters'
    ]
  }),
  methods: {
    ...mapActions(['login']),
    async handleLogin() {
      if (!this.$refs.form.validate()) return

      this.loading = true
      try {
        await this.login({
          email: this.email,
          password: this.password
        })
        this.$router.push('/plans')
      } catch (error) {
        this.errorMessage = error.response?.data?.message || 'Login failed. Please try again.'
        this.snackbar = true
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.v-card {
  border-radius: 12px;
}
</style> 