<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <v-card class="mb-6">
          <v-card-title class="headline primary white--text">
            Create Your Travel Plan
          </v-card-title>
          <v-card-text class="pt-4">
            <v-alert
              v-if="error"
              type="error"
              dismissible
              @click="error = ''"
            >
              {{ error }}
            </v-alert>
            
            <v-stepper v-model="step" vertical>
              <!-- Step 1: Basic Information -->
              <v-stepper-content step="1">
                <v-card class="mb-4">
                  <v-card-title>Basic Information</v-card-title>
                  <v-card-text>
                    <v-text-field
                      v-model="plan.title"
                      label="Trip Title"
                      :rules="[v => !!v || 'Title is required']"
                      required
                      outlined
                      dense
                      class="mb-4"
                    ></v-text-field>
                    
                    <v-text-field
                      v-model="plan.destination"
                      label="Destination"
                      :rules="[v => !!v || 'Destination is required']"
                      required
                      outlined
                      dense
                      class="mb-4"
                    ></v-text-field>
                    
                    <v-row>
                      <v-col cols="12" sm="6">
                        <v-menu
                          v-model="startDateMenu"
                          :close-on-content-click="false"
                          transition="scale-transition"
                          offset-y
                          max-width="290px"
                          min-width="290px"
                        >
                          <template v-slot:activator="{ on, attrs }">
                            <v-text-field
                              v-model="plan.start_date"
                              label="Start Date"
                              readonly
                              v-bind="attrs"
                              v-on="on"
                              outlined
                              dense
                              :rules="[v => !!v || 'Start date is required']"
                              required
                            ></v-text-field>
                          </template>
                          <v-date-picker
                            v-model="plan.start_date"
                            no-title
                            @input="startDateMenu = false"
                          ></v-date-picker>
                        </v-menu>
                      </v-col>
                      <v-col cols="12" sm="6">
                        <v-menu
                          v-model="endDateMenu"
                          :close-on-content-click="false"
                          transition="scale-transition"
                          offset-y
                          max-width="290px"
                          min-width="290px"
                        >
                          <template v-slot:activator="{ on, attrs }">
                            <v-text-field
                              v-model="plan.end_date"
                              label="End Date"
                              readonly
                              v-bind="attrs"
                              v-on="on"
                              outlined
                              dense
                              :rules="[v => !!v || 'End date is required']"
                              required
                            ></v-text-field>
                          </template>
                          <v-date-picker
                            v-model="plan.end_date"
                            no-title
                            @input="endDateMenu = false"
                          ></v-date-picker>
                        </v-menu>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
                
                <v-btn
                  color="primary"
                  @click="step = 2"
                  :disabled="!isStep1Valid"
                >
                  Continue
                </v-btn>
              </v-stepper-content>
              
              <!-- Step 2: Preferences -->
              <v-stepper-content step="2">
                <v-card class="mb-4">
                  <v-card-title>Travel Preferences</v-card-title>
                  <v-card-text>
                    <v-row>
                      <v-col cols="12" sm="6">
                        <v-select
                          v-model="plan.preferences.budget"
                          :items="budgetOptions"
                          label="Budget Range"
                          outlined
                          dense
                          :rules="[v => !!v || 'Budget is required']"
                          required
                        ></v-select>
                      </v-col>
                      <v-col cols="12" sm="6">
                        <v-select
                          v-model="plan.preferences.temperature"
                          :items="temperatureOptions"
                          label="Preferred Temperature"
                          outlined
                          dense
                          :rules="[v => !!v || 'Temperature preference is required']"
                          required
                        ></v-select>
                      </v-col>
                    </v-row>
                    
                    <v-row>
                      <v-col cols="12" sm="6">
                        <v-select
                          v-model="plan.preferences.purpose"
                          :items="purposeOptions"
                          label="Travel Purpose"
                          outlined
                          dense
                          :rules="[v => !!v || 'Purpose is required']"
                          required
                        ></v-select>
                      </v-col>
                      <v-col cols="12" sm="6">
                        <v-text-field
                          v-model.number="plan.preferences.travelers"
                          label="Number of Travelers"
                          type="number"
                          min="1"
                          outlined
                          dense
                          :rules="[
                            v => !!v || 'Number of travelers is required',
                            v => v > 0 || 'Must be at least 1'
                          ]"
                          required
                        ></v-text-field>
                      </v-col>
                    </v-row>
                    
                    <v-textarea
                      v-model="plan.preferences.additional"
                      label="Additional Preferences (optional)"
                      outlined
                      dense
                      rows="3"
                      placeholder="Any specific interests, dietary restrictions, or accessibility needs?"
                    ></v-textarea>
                  </v-card-text>
                </v-card>
                
                <v-btn
                  text
                  @click="step = 1"
                  class="mr-4"
                >
                  Back
                </v-btn>
                <v-btn
                  color="primary"
                  @click="step = 3"
                  :disabled="!isStep2Valid"
                >
                  Continue
                </v-btn>
              </v-stepper-content>
              
              <!-- Step 3: Review & Generate -->
              <v-stepper-content step="3">
                <v-card class="mb-4">
                  <v-card-title>Review & Generate</v-card-title>
                  <v-card-text>
                    <v-list>
                      <v-list-item>
                        <v-list-item-content>
                          <v-list-item-title>Trip Title</v-list-item-title>
                          <v-list-item-subtitle>{{ plan.title }}</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                      
                      <v-list-item>
                        <v-list-item-content>
                          <v-list-item-title>Destination</v-list-item-title>
                          <v-list-item-subtitle>{{ plan.destination }}</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                      
                      <v-list-item>
                        <v-list-item-content>
                          <v-list-item-title>Dates</v-list-item-title>
                          <v-list-item-subtitle>{{ plan.start_date }} to {{ plan.end_date }}</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                      
                      <v-list-item>
                        <v-list-item-content>
                          <v-list-item-title>Budget</v-list-item-title>
                          <v-list-item-subtitle>{{ plan.preferences.budget }}</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                      
                      <v-list-item>
                        <v-list-item-content>
                          <v-list-item-title>Temperature</v-list-item-title>
                          <v-list-item-subtitle>{{ plan.preferences.temperature }}</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                      
                      <v-list-item>
                        <v-list-item-content>
                          <v-list-item-title>Purpose</v-list-item-title>
                          <v-list-item-subtitle>{{ plan.preferences.purpose }}</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                      
                      <v-list-item>
                        <v-list-item-content>
                          <v-list-item-title>Travelers</v-list-item-title>
                          <v-list-item-subtitle>{{ plan.preferences.travelers }}</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                      
                      <v-list-item v-if="plan.preferences.additional">
                        <v-list-item-content>
                          <v-list-item-title>Additional Preferences</v-list-item-title>
                          <v-list-item-subtitle>{{ plan.preferences.additional }}</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list>
                    
                    <v-switch
                      v-model="plan.is_public"
                      label="Make this plan public (others can view and like it)"
                      class="mt-4"
                    ></v-switch>
                  </v-card-text>
                </v-card>
                
                <v-btn
                  text
                  @click="step = 2"
                  class="mr-4"
                >
                  Back
                </v-btn>
                <v-btn
                  color="success"
                  @click="generatePlan"
                  :loading="loading"
                  :disabled="loading"
                >
                  Generate Travel Plan
                </v-btn>
              </v-stepper-content>
            </v-stepper>
          </v-card-text>
        </v-card>
        
        <!-- Tips Card -->
        <v-card class="mb-6">
          <v-card-title class="subtitle-1">
            <v-icon left>mdi-lightbulb</v-icon>
            Tips for a Better Travel Plan
          </v-card-title>
          <v-card-text>
            <v-list dense>
              <v-list-item>
                <v-list-item-icon>
                  <v-icon>mdi-calendar</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>Be specific with dates</v-list-item-title>
                  <v-list-item-subtitle>This helps us recommend seasonal activities and events.</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item>
                <v-list-item-icon>
                  <v-icon>mdi-currency-usd</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>Set a realistic budget</v-list-item-title>
                  <v-list-item-subtitle>Include accommodation, activities, food, and transportation in your budget estimate.</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item>
                <v-list-item-icon>
                  <v-icon>mdi-account-group</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>Consider your group</v-list-item-title>
                  <v-list-item-subtitle>Different group sizes may require different accommodations and activities.</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item>
                <v-list-item-icon>
                  <v-icon>mdi-text-box</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>Add detailed preferences</v-list-item-title>
                  <v-list-item-subtitle>The more details you provide, the more personalized your travel plan will be.</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Generated Plan Dialog -->
    <v-dialog
      v-model="showPlanDialog"
      max-width="800px"
      scrollable
    >
      <v-card>
        <v-card-title class="headline primary white--text">
          Your Travel Plan
        </v-card-title>
        <v-card-text class="pt-4">
          <v-alert
            v-if="planError"
            type="error"
            dismissible
            @click="planError = ''"
          >
            {{ planError }}
          </v-alert>
          
          <div v-if="generatedPlan">
            <v-tabs
              v-model="activeTab"
              background-color="primary"
              dark
            >
              <v-tab>Overview</v-tab>
              <v-tab>Itinerary</v-tab>
              <v-tab>Costs</v-tab>
              <v-tab>Tips</v-tab>
            </v-tabs>
            
            <v-tabs-items v-model="activeTab">
              <!-- Overview Tab -->
              <v-tab-item>
                <v-card flat>
                  <v-card-text>
                    <h2 class="text-h5 mb-4">{{ plan.title }}</h2>
                    <p class="subtitle-1">{{ plan.destination }}</p>
                    <p>{{ plan.start_date }} to {{ plan.end_date }}</p>
                    
                    <v-divider class="my-4"></v-divider>
                    
                    <h3 class="text-h6 mb-2">Recommended Destinations</h3>
                    <v-chip-group>
                      <v-chip
                        v-for="destination in generatedPlan.destinations"
                        :key="destination"
                        color="primary"
                        outlined
                      >
                        {{ destination }}
                      </v-chip>
                    </v-chip-group>
                    
                    <v-divider class="my-4"></v-divider>
                    
                    <h3 class="text-h6 mb-2">Cultural Experiences</h3>
                    <v-list dense>
                      <v-list-item
                        v-for="(experience, index) in generatedPlan.cultural_experiences"
                        :key="index"
                      >
                        <v-list-item-icon>
                          <v-icon>mdi-star</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                          <v-list-item-title>{{ experience }}</v-list-item-title>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list>
                  </v-card-text>
                </v-card>
              </v-tab-item>
              
              <!-- Itinerary Tab -->
              <v-tab-item>
                <v-card flat>
                  <v-card-text>
                    <v-timeline dense>
                      <v-timeline-item
                        v-for="(day, index) in generatedPlan.itinerary.days"
                        :key="index"
                        color="primary"
                        small
                      >
                        <template v-slot:opposite>
                          Day {{ index + 1 }}
                        </template>
                        <v-card class="elevation-1">
                          <v-card-title class="subtitle-1">
                            {{ day.date }}
                          </v-card-title>
                          <v-card-text>
                            <v-list dense>
                              <v-list-item>
                                <v-list-item-icon>
                                  <v-icon>mdi-weather-sunny</v-icon>
                                </v-list-item-icon>
                                <v-list-item-content>
                                  <v-list-item-title>Morning</v-list-item-title>
                                  <v-list-item-subtitle>{{ day.morning }}</v-list-item-subtitle>
                                </v-list-item-content>
                              </v-list-item>
                              
                              <v-list-item>
                                <v-list-item-icon>
                                  <v-icon>mdi-weather-partly-cloudy</v-icon>
                                </v-list-item-icon>
                                <v-list-item-content>
                                  <v-list-item-title>Afternoon</v-list-item-title>
                                  <v-list-item-subtitle>{{ day.afternoon }}</v-list-item-subtitle>
                                </v-list-item-content>
                              </v-list-item>
                              
                              <v-list-item>
                                <v-list-item-icon>
                                  <v-icon>mdi-weather-night</v-icon>
                                </v-list-item-icon>
                                <v-list-item-content>
                                  <v-list-item-title>Evening</v-list-item-title>
                                  <v-list-item-subtitle>{{ day.evening }}</v-list-item-subtitle>
                                </v-list-item-content>
                              </v-list-item>
                            </v-list>
                          </v-card-text>
                        </v-card>
                      </v-timeline-item>
                    </v-timeline>
                  </v-card-text>
                </v-card>
              </v-tab-item>
              
              <!-- Costs Tab -->
              <v-tab-item>
                <v-card flat>
                  <v-card-text>
                    <h3 class="text-h6 mb-4">Estimated Costs</h3>
                    
                    <v-simple-table>
                      <template v-slot:default>
                        <thead>
                          <tr>
                            <th>Category</th>
                            <th class="text-right">Amount</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="(cost, category) in generatedPlan.costs" :key="category">
                            <td>{{ category }}</td>
                            <td class="text-right">{{ cost }}</td>
                          </tr>
                          <tr>
                            <td class="font-weight-bold">Total</td>
                            <td class="text-right font-weight-bold">{{ calculateTotalCost() }}</td>
                          </tr>
                        </tbody>
                      </template>
                    </v-simple-table>
                    
                    <v-divider class="my-4"></v-divider>
                    
                    <h3 class="text-h6 mb-2">Budget Tips</h3>
                    <v-list dense>
                      <v-list-item
                        v-for="(tip, index) in generatedPlan.budget_tips"
                        :key="index"
                      >
                        <v-list-item-icon>
                          <v-icon>mdi-lightbulb</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                          <v-list-item-title>{{ tip }}</v-list-item-title>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list>
                  </v-card-text>
                </v-card>
              </v-tab-item>
              
              <!-- Tips Tab -->
              <v-tab-item>
                <v-card flat>
                  <v-card-text>
                    <h3 class="text-h6 mb-4">Travel Tips</h3>
                    
                    <v-list>
                      <v-list-item>
                        <v-list-item-icon>
                          <v-icon>mdi-information</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                          <v-list-item-title>General Tips</v-list-item-title>
                          <v-list-item-subtitle>
                            <div v-for="(tip, index) in generatedPlan.tips" :key="index" class="mb-2">
                              {{ tip }}
                            </div>
                          </v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                      
                      <v-divider class="my-2"></v-divider>
                      
                      <v-list-item>
                        <v-list-item-icon>
                          <v-icon>mdi-food</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                          <v-list-item-title>Local Cuisine</v-list-item-title>
                          <v-list-item-subtitle>
                            <div v-for="(dish, index) in generatedPlan.cuisine" :key="index" class="mb-2">
                              {{ dish }}
                            </div>
                          </v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                      
                      <v-divider class="my-2"></v-divider>
                      
                      <v-list-item>
                        <v-list-item-icon>
                          <v-icon>mdi-camera</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                          <v-list-item-title>Photo Opportunities</v-list-item-title>
                          <v-list-item-subtitle>
                            <div v-for="(spot, index) in generatedPlan.photo_spots" :key="index" class="mb-2">
                              {{ spot }}
                            </div>
                          </v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                      
                      <v-divider class="my-2"></v-divider>
                      
                      <v-list-item>
                        <v-list-item-icon>
                          <v-icon>mdi-umbrella</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                          <v-list-item-title>Alternative Plans (Bad Weather)</v-list-item-title>
                          <v-list-item-subtitle>
                            <div v-for="(alt, index) in generatedPlan.alternatives" :key="index" class="mb-2">
                              {{ alt }}
                            </div>
                          </v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                      
                      <v-divider class="my-2"></v-divider>
                      
                      <v-list-item>
                        <v-list-item-icon>
                          <v-icon>mdi-bag-checked</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                          <v-list-item-title>Packing List</v-list-item-title>
                          <v-list-item-subtitle>
                            <div v-for="(item, index) in generatedPlan.packing_list" :key="index" class="mb-2">
                              {{ item }}
                            </div>
                          </v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                      
                      <v-divider class="my-2"></v-divider>
                      
                      <v-list-item>
                        <v-list-item-icon>
                          <v-icon>mdi-medical-bag</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                          <v-list-item-title>Health & Safety</v-list-item-title>
                          <v-list-item-subtitle>
                            <div v-for="(item, index) in generatedPlan.health_safety" :key="index" class="mb-2">
                              {{ item }}
                            </div>
                          </v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list>
                  </v-card-text>
                </v-card>
              </v-tab-item>
            </v-tabs-items>
          </div>
          
          <div v-else-if="loading" class="text-center py-8">
            <v-progress-circular
              indeterminate
              color="primary"
              size="64"
            ></v-progress-circular>
            <p class="mt-4">Generating your personalized travel plan...</p>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="showPlanDialog = false"
          >
            Close
          </v-btn>
          <v-btn
            color="success"
            @click="savePlan"
            :disabled="!generatedPlan || saving"
            :loading="saving"
          >
            Save Plan
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Success Snackbar -->
    <v-snackbar
      v-model="snackbar"
      color="success"
      timeout="5000"
    >
      {{ snackbarText }}
      <template v-slot:action="{ attrs }">
        <v-btn
          text
          v-bind="attrs"
          @click="snackbar = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'CreatePlan',
  data() {
    return {
      step: 1,
      loading: false,
      saving: false,
      error: '',
      planError: '',
      snackbar: false,
      snackbarText: '',
      startDateMenu: false,
      endDateMenu: false,
      showPlanDialog: false,
      activeTab: 0,
      generatedPlan: null,
      budgetOptions: ['Low', 'Medium', 'High'],
      temperatureOptions: ['Cold', 'Mild', 'Hot'],
      purposeOptions: ['Leisure', 'Adventure', 'Cultural', 'Business', 'Relaxation'],
      plan: {
        title: '',
        destination: '',
        start_date: '',
        end_date: '',
        budget: 0,
        preferences: {
          budget: '',
          temperature: '',
          purpose: '',
          travelers: 1,
          additional: ''
        },
        is_public: false
      }
    };
  },
  computed: {
    isStep1Valid() {
      return this.plan.title && 
             this.plan.destination && 
             this.plan.start_date && 
             this.plan.end_date;
    },
    isStep2Valid() {
      return this.plan.preferences.budget && 
             this.plan.preferences.temperature && 
             this.plan.preferences.purpose && 
             this.plan.preferences.travelers > 0;
    }
  },
  methods: {
    ...mapActions(['createTravelPlan']),
    async generatePlan() {
      this.loading = true;
      this.planError = '';
      this.generatedPlan = null;
      this.showPlanDialog = true;
      
      try {
        // Prepare the data for the API
        const planData = {
          title: this.plan.title,
          destination: this.plan.destination,
          start_date: this.plan.start_date,
          end_date: this.plan.end_date,
          budget: this.plan.budget,
          preferences: this.plan.preferences,
          is_public: this.plan.is_public
        };
        
        // Call the API to generate the plan
        const response = await this.createTravelPlan(planData);
        
        // Process the response
        if (response && response.itinerary) {
          this.generatedPlan = response.itinerary;
          
          // If the response is a string, try to parse it as JSON
          if (typeof this.generatedPlan === 'string') {
            try {
              this.generatedPlan = JSON.parse(this.generatedPlan);
            } catch (e) {
              // If parsing fails, create a simple structure
              this.generatedPlan = {
                destinations: [this.plan.destination],
                itinerary: {
                  days: []
                },
                costs: {
                  'Accommodation': '$0',
                  'Activities': '$0',
                  'Food': '$0',
                  'Transportation': '$0'
                },
                tips: [this.generatedPlan],
                cuisine: [],
                cultural_experiences: [],
                photo_spots: [],
                alternatives: [],
                packing_list: [],
                health_safety: []
              };
            }
          }
          
          // Ensure the generated plan has all required properties
          this.ensurePlanProperties();
        } else {
          this.planError = 'Failed to generate travel plan. Please try again.';
        }
      } catch (error) {
        console.error('Error generating plan:', error);
        this.planError = error.message || 'An error occurred while generating your travel plan.';
      } finally {
        this.loading = false;
      }
    },
    ensurePlanProperties() {
      // Ensure all required properties exist
      if (!this.generatedPlan.destinations) {
        this.generatedPlan.destinations = [this.plan.destination];
      }
      
      if (!this.generatedPlan.itinerary) {
        this.generatedPlan.itinerary = { days: [] };
      }
      
      if (!this.generatedPlan.itinerary.days) {
        this.generatedPlan.itinerary.days = [];
      }
      
      if (!this.generatedPlan.costs) {
        this.generatedPlan.costs = {
          'Accommodation': '$0',
          'Activities': '$0',
          'Food': '$0',
          'Transportation': '$0'
        };
      }
      
      if (!this.generatedPlan.tips) {
        this.generatedPlan.tips = [];
      }
      
      if (!this.generatedPlan.cuisine) {
        this.generatedPlan.cuisine = [];
      }
      
      if (!this.generatedPlan.cultural_experiences) {
        this.generatedPlan.cultural_experiences = [];
      }
      
      if (!this.generatedPlan.photo_spots) {
        this.generatedPlan.photo_spots = [];
      }
      
      if (!this.generatedPlan.alternatives) {
        this.generatedPlan.alternatives = [];
      }
      
      if (!this.generatedPlan.packing_list) {
        this.generatedPlan.packing_list = [];
      }
      
      if (!this.generatedPlan.health_safety) {
        this.generatedPlan.health_safety = [];
      }
      
      if (!this.generatedPlan.budget_tips) {
        this.generatedPlan.budget_tips = [];
      }
    },
    calculateTotalCost() {
      if (!this.generatedPlan || !this.generatedPlan.costs) {
        return '$0';
      }
      
      let total = 0;
      for (const cost in this.generatedPlan.costs) {
        const value = this.generatedPlan.costs[cost];
        const numericValue = parseFloat(value.replace(/[^0-9.-]+/g, ''));
        if (!isNaN(numericValue)) {
          total += numericValue;
        }
      }
      
      return `$${total.toFixed(2)}`;
    },
    async savePlan() {
      this.saving = true;
      
      try {
        // The plan is already saved when generated
        this.snackbarText = 'Travel plan saved successfully!';
        this.snackbar = true;
        this.showPlanDialog = false;
        
        // Reset the form
        this.resetForm();
      } catch (error) {
        console.error('Error saving plan:', error);
        this.planError = error.message || 'An error occurred while saving your travel plan.';
      } finally {
        this.saving = false;
      }
    },
    resetForm() {
      this.step = 1;
      this.plan = {
        title: '',
        destination: '',
        start_date: '',
        end_date: '',
        budget: 0,
        preferences: {
          budget: '',
          temperature: '',
          purpose: '',
          travelers: 1,
          additional: ''
        },
        is_public: false
      };
    }
  }
};
</script>

<style scoped>
.v-card {
  border-radius: 8px;
}
</style> 