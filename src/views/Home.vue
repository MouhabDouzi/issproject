<template>
  <div class="home">
    <v-container>
      <!-- Hero Section -->
      <v-row class="hero-section" align="center" style="min-height: 80vh">
        <v-col cols="12" md="6">
          <h1 class="text-h2 font-weight-bold mb-4">
            Plan Your Perfect Trip with AI
          </h1>
          <p class="text-h6 mb-6">
            Discover personalized travel recommendations powered by artificial intelligence.
            Let us help you create unforgettable experiences.
          </p>
          <v-btn
            color="primary"
            size="x-large"
            :to="isAuthenticated ? '/plans/create' : '/signup'"
          >
            Start Planning
          </v-btn>
        </v-col>
        <v-col cols="12" md="6">
          <v-img
            src="@/assets/travel-hero.jpg"
            height="400"
            cover
            class="rounded-lg"
          ></v-img>
        </v-col>
      </v-row>

      <!-- Features Section -->
      <v-row class="features-section my-16">
        <v-col cols="12" class="text-center mb-8">
          <h2 class="text-h3 font-weight-bold">Why Choose TravelPlanner?</h2>
        </v-col>
        <v-col cols="12" md="4">
          <v-card class="feature-card" elevation="2">
            <v-card-item>
              <v-icon size="48" color="primary" class="mb-4">mdi-robot</v-icon>
              <v-card-title>AI-Powered Recommendations</v-card-title>
              <v-card-text>
                Get personalized travel suggestions based on your preferences, budget, and travel style.
              </v-card-text>
            </v-card-item>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card class="feature-card" elevation="2">
            <v-card-item>
              <v-icon size="48" color="primary" class="mb-4">mdi-map-marker-multiple</v-icon>
              <v-card-title>Smart Itinerary Planning</v-card-title>
              <v-card-text>
                Create detailed day-by-day itineraries with optimized routes and activities.
              </v-card-text>
            </v-card-item>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card class="feature-card" elevation="2">
            <v-card-item>
              <v-icon size="48" color="primary" class="mb-4">mdi-currency-usd</v-icon>
              <v-card-title>Budget Management</v-card-title>
              <v-card-text>
                Track and manage your travel budget with smart expense predictions.
              </v-card-text>
            </v-card-item>
          </v-card>
        </v-col>
      </v-row>

      <!-- How It Works Section -->
      <v-row class="how-it-works-section my-16">
        <v-col cols="12" class="text-center mb-8">
          <h2 class="text-h3 font-weight-bold">How It Works</h2>
        </v-col>
        <v-col cols="12" md="3">
          <div class="step-card text-center">
            <v-icon size="64" color="primary" class="mb-4">mdi-account-plus</v-icon>
            <h3 class="text-h5 mb-2">1. Sign Up</h3>
            <p>Create your account to get started</p>
          </div>
        </v-col>
        <v-col cols="12" md="3">
          <div class="step-card text-center">
            <v-icon size="64" color="primary" class="mb-4">mdi-form-select</v-icon>
            <h3 class="text-h5 mb-2">2. Set Preferences</h3>
            <p>Tell us about your travel style</p>
          </div>
        </v-col>
        <v-col cols="12" md="3">
          <div class="step-card text-center">
            <v-icon size="64" color="primary" class="mb-4">mdi-robot</v-icon>
            <h3 class="text-h5 mb-2">3. Get Recommendations</h3>
            <p>Receive AI-powered suggestions</p>
          </div>
        </v-col>
        <v-col cols="12" md="3">
          <div class="step-card text-center">
            <v-icon size="64" color="primary" class="mb-4">mdi-check-circle</v-icon>
            <h3 class="text-h5 mb-2">4. Plan & Enjoy</h3>
            <p>Create your perfect itinerary</p>
          </div>
        </v-col>
      </v-row>

      <!-- Call to Action -->
      <v-row class="cta-section my-16" align="center">
        <v-col cols="12" class="text-center">
          <h2 class="text-h3 font-weight-bold mb-4">Ready to Start Your Journey?</h2>
          <p class="text-h6 mb-6">Join thousands of travelers who trust TravelPlanner for their adventures.</p>
          <v-btn
            color="primary"
            size="x-large"
            :to="isAuthenticated ? '/plans/create' : '/signup'"
          >
            Get Started Now
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Home',
  computed: {
    ...mapGetters(['isAuthenticated'])
  }
}
</script>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 16px;
  padding: 48px;
  margin-bottom: 48px;
}

.feature-card {
  height: 100%;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.step-card {
  padding: 24px;
  background: #f5f7fa;
  border-radius: 12px;
  height: 100%;
}

.cta-section {
  background: linear-gradient(135deg, #1976D2 0%, #64B5F6 100%);
  color: white;
  border-radius: 16px;
  padding: 48px;
}
</style> 