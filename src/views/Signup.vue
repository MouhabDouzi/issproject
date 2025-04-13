<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Sign Up</v-toolbar-title>
            <v-spacer></v-spacer>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleSignup" ref="form">
              <v-text-field
                v-model="name"
                label="Full Name"
                name="name"
                prepend-icon="mdi-account"
                :rules="nameRules"
                required
              ></v-text-field>

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

              <v-text-field
                v-model="confirmPassword"
                label="Confirm Password"
                name="confirmPassword"
                prepend-icon="mdi-lock-check"
                type="password"
                :rules="confirmPasswordRules"
                required
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              @click="handleSignup"
              :loading="loading"
              :disabled="loading"
            >
              Sign Up
            </v-btn>
          </v-card-actions>
          <v-card-text class="text-center">
            <p class="mb-0">
              Already have an account?
              <router-link to="/login" class="text-decoration-none">
                Login
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
  name: 'Signup',
  data: () => ({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    loading: false,
    snackbar: false,
    errorMessage: '',
    nameRules: [
      v => !!v || 'Name is required',
      v => v.length >= 2 || 'Name must be at least 2 characters'
    ],
    emailRules: [
      v => !!v || 'Email is required',
      v => /.+@.+\..+/.test(v) || 'Email must be valid'
    ],
    passwordRules: [
      v => !!v || 'Password is required',
      v => v.length >= 6 || 'Password must be at least 6 characters'
    ],
    confirmPasswordRules: [
      v => !!v || 'Please confirm your password',
      v => v === this.password || 'Passwords must match'
    ]
  }),
  methods: {
    ...mapActions(['signup']),
    async handleSignup() {
      if (!this.$refs.form.validate()) return

      this.loading = true
      try {
        await this.signup({
          name: this.name,
          email: this.email,
          password: this.password
        })
        this.$router.push('/plans')
      } catch (error) {
        this.errorMessage = error.response?.data?.message || 'Signup failed. Please try again.'
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