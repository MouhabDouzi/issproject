<template>
    <div class="signup-page">
      <v-container fluid class="fill-height pa-0">
        <v-row no-gutters class="fill-height">
          <v-col cols="12" class="d-flex align-center justify-center">
            <v-card width="450" max-width="90%" class="pa-6">
              <div class="text-center text-h5 font-weight-bold mb-4">Travel Planner AI</div>
              <h1 class="text-h5 text-center mb-6">Create Account</h1>
              
              <v-form ref="form" v-model="valid" @submit.prevent="signup">
                <v-text-field
                  v-model="name"
                  label="Full Name"
                  :rules="nameRules"
                  outlined
                  required
                ></v-text-field>
                
                <v-text-field
                  v-model="email"
                  label="Email"
                  type="email"
                  :rules="emailRules"
                  outlined
                  required
                ></v-text-field>
                
                <v-text-field
                  v-model="password"
                  label="Password"
                  type="password"
                  :rules="passwordRules"
                  outlined
                  required
                ></v-text-field>
                
                <v-text-field
                  v-model="confirmPassword"
                  label="Confirm Password"
                  type="password"
                  :rules="confirmPasswordRules"
                  outlined
                  required
                ></v-text-field>
                
                <v-alert
                  v-if="errorMessage"
                  type="error"
                  text
                  dismissible
                  class="mb-4"
                >
                  {{ errorMessage }}
                </v-alert>
                
                <v-btn
                  type="submit"
                  color="#3498DB"
                  block
                  large
                  class="mb-4"
                  :loading="loading"
                >
                  Sign Up
                </v-btn>
              </v-form>
              
              <div class="text-center mt-4">
                <router-link to="/login" class="text-decoration-none">Already have an account? Login</router-link>
              </div>
              
              <div class="text-center text-caption mt-4">
                By signing up, you agree to our Terms of Service and Privacy Policy
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Signup',
    data() {
      return {
        valid: false,
        name: '',
        email: '',
        password: '',
        confirmPassword: '',
        loading: false,
        errorMessage: '',
        nameRules: [
          v => !!v || 'Name is required'
        ],
        emailRules: [
          v => !!v || 'Email is required',
          v => /.+@.+\..+/.test(v) || 'Email must be valid'
        ],
        passwordRules: [
          v => !!v || 'Password is required',
          v => v.length >= 8 || 'Password must be at least 8 characters'
        ]
      };
    },
    computed: {
      confirmPasswordRules() {
        return [
          v => !!v || 'Confirm password is required',
          v => v === this.password || 'Passwords do not match'
        ];
      }
    },
    methods: {
      async signup() {
        if (!this.$refs.form.validate()) return;
        
        this.loading = true;
        this.errorMessage = '';
        
        try {
          const response = await fetch('/api/auth/signup', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              name: this.name,
              email: this.email,
              password: this.password
            })
          });
          
          const data = await response.json();
          
          if (!response.ok) {
            throw new Error(data.message || 'Registration failed');
          }
          
          // Store authentication token
          localStorage.setItem('userToken', data.token);
          
          // Redirect to home page
          this.$router.push('/');
        } catch (error) {
          this.errorMessage = error.message || 'Registration failed. Please try again.';
          console.error('Signup error:', error);
        } finally {
          this.loading = false;
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .signup-page {
    background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('https://source.unsplash.com/random/1920x1080/?adventure');
    background-size: cover;
    background-position: center;
    height: 100vh;
  }
  </style>