<template>
  <div class="plan-details-container">
    <div v-if="loading" class="loading">Loading plan details...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="plan-content">
      <div class="plan-header">
        <h1>{{ plan.title }}</h1>
        <div class="plan-meta">
          <span class="plan-date">Created: {{ formatDate(plan.created_at) }}</span>
          <span class="plan-status" :class="plan.is_public ? 'public' : 'private'">
            {{ plan.is_public ? 'Public' : 'Private' }}
          </span>
        </div>
      </div>
      
      <div class="plan-info">
        <div class="info-card">
          <h3>Destination</h3>
          <p>{{ plan.destination }}</p>
        </div>
        <div class="info-card">
          <h3>Duration</h3>
          <p>{{ plan.duration }}</p>
        </div>
        <div class="info-card">
          <h3>Budget</h3>
          <p>{{ plan.budget }}</p>
        </div>
        <div class="info-card">
          <h3>Travelers</h3>
          <p>{{ plan.travelers }}</p>
        </div>
      </div>
      
      <div class="plan-actions">
        <button @click="togglePublic" class="btn" :class="plan.is_public ? 'btn-warning' : 'btn-success'">
          {{ plan.is_public ? 'Make Private' : 'Make Public' }}
        </button>
        <button @click="toggleFavorite" class="btn" :class="isFavorite ? 'btn-danger' : 'btn-outline'">
          {{ isFavorite ? 'Remove from Favorites' : 'Add to Favorites' }}
        </button>
        <button @click="likePlan" class="btn btn-primary" :disabled="hasLiked">
          {{ hasLiked ? `Liked (${plan.likes})` : 'Like' }}
        </button>
      </div>
      
      <div class="plan-description">
        <h2>Description</h2>
        <p>{{ plan.description || 'No description provided.' }}</p>
      </div>
      
      <div class="plan-itinerary">
        <h2>Itinerary</h2>
        <div v-if="plan.itinerary" class="itinerary-content">
          <div v-for="(day, index) in plan.itinerary.days" :key="index" class="day-card">
            <h3>Day {{ day.day }}</h3>
            <div class="day-schedule">
              <div class="schedule-item">
                <h4>Morning</h4>
                <p>{{ day.morning }}</p>
              </div>
              <div class="schedule-item">
                <h4>Afternoon</h4>
                <p>{{ day.afternoon }}</p>
              </div>
              <div class="schedule-item">
                <h4>Evening</h4>
                <p>{{ day.evening }}</p>
              </div>
            </div>
          </div>
          
          <div class="additional-info">
            <div class="info-section">
              <h3>Costs</h3>
              <ul>
                <li v-for="(cost, category) in plan.itinerary.costs" :key="category">
                  <strong>{{ category }}:</strong> {{ cost }}
                </li>
              </ul>
            </div>
            
            <div class="info-section">
              <h3>Transportation</h3>
              <p>{{ plan.itinerary.transportation }}</p>
            </div>
            
            <div class="info-section">
              <h3>Food</h3>
              <p>{{ plan.itinerary.food }}</p>
            </div>
            
            <div class="info-section">
              <h3>Cultural Experiences</h3>
              <ul>
                <li v-for="(experience, index) in plan.itinerary.cultural_experiences" :key="index">
                  {{ experience }}
                </li>
              </ul>
            </div>
            
            <div class="info-section">
              <h3>Photo Spots</h3>
              <ul>
                <li v-for="(spot, index) in plan.itinerary.photo_spots" :key="index">
                  {{ spot }}
                </li>
              </ul>
            </div>
            
            <div class="info-section">
              <h3>Packing List</h3>
              <ul>
                <li v-for="(item, index) in plan.itinerary.packing_list" :key="index">
                  {{ item }}
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div v-else class="no-itinerary">
          <p>No itinerary available for this plan.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PlanDetails',
  data() {
    return {
      plan: {},
      loading: true,
      error: null,
      isFavorite: false,
      hasLiked: false
    };
  },
  created() {
    this.fetchPlanDetails();
    this.checkFavoriteStatus();
  },
  methods: {
    async fetchPlanDetails() {
      try {
        this.loading = true;
        const planId = this.$route.params.id;
        const token = localStorage.getItem('token');
        
        if (!token) {
          this.error = 'You need to be logged in to view plan details';
          this.loading = false;
          return;
        }
        
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/plans/${planId}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        this.plan = response.data.plan;
        this.loading = false;
      } catch (error) {
        console.error('Error fetching plan details:', error);
        this.error = 'Failed to load plan details. Please try again later.';
        this.loading = false;
      }
    },
    async checkFavoriteStatus() {
      try {
        const planId = this.$route.params.id;
        const token = localStorage.getItem('token');
        
        if (!token) return;
        
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/favorites`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        const favorites = response.data.favorites;
        this.isFavorite = favorites.some(fav => fav.plan_id === parseInt(planId));
      } catch (error) {
        console.error('Error checking favorite status:', error);
      }
    },
    async togglePublic() {
      try {
        const planId = this.$route.params.id;
        const token = localStorage.getItem('token');
        
        await axios.put(`${process.env.VUE_APP_API_URL}/api/plans/${planId}`, {
          is_public: !this.plan.is_public
        }, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        this.plan.is_public = !this.plan.is_public;
      } catch (error) {
        console.error('Error toggling plan visibility:', error);
        alert('Failed to update plan visibility. Please try again later.');
      }
    },
    async toggleFavorite() {
      try {
        const planId = this.$route.params.id;
        const token = localStorage.getItem('token');
        
        if (this.isFavorite) {
          await axios.delete(`${process.env.VUE_APP_API_URL}/api/favorites/${planId}`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
        } else {
          await axios.post(`${process.env.VUE_APP_API_URL}/api/favorites`, {
            plan_id: planId
          }, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
        }
        
        this.isFavorite = !this.isFavorite;
      } catch (error) {
        console.error('Error toggling favorite status:', error);
        alert('Failed to update favorite status. Please try again later.');
      }
    },
    async likePlan() {
      if (this.hasLiked) return;
      
      try {
        const planId = this.$route.params.id;
        const token = localStorage.getItem('token');
        
        await axios.post(`${process.env.VUE_APP_API_URL}/api/plans/${planId}/like`, {}, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        this.plan.likes += 1;
        this.hasLiked = true;
      } catch (error) {
        console.error('Error liking plan:', error);
        alert('Failed to like the plan. Please try again later.');
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    }
  }
};
</script>

<style scoped>
.plan-details-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading, .error {
  text-align: center;
  padding: 40px;
  font-size: 18px;
}

.error {
  color: #dc3545;
}

.plan-header {
  margin-bottom: 30px;
}

.plan-header h1 {
  margin-bottom: 10px;
}

.plan-meta {
  display: flex;
  gap: 20px;
  color: #666;
  font-size: 14px;
}

.plan-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.plan-status.public {
  background-color: #28a745;
  color: white;
}

.plan-status.private {
  background-color: #6c757d;
  color: white;
}

.plan-info {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.info-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.info-card h3 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 16px;
  color: #495057;
}

.plan-actions {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  border: none;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-warning {
  background-color: #ffc107;
  color: #212529;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-outline {
  background-color: transparent;
  border: 1px solid #007bff;
  color: #007bff;
}

.plan-description, .plan-itinerary {
  margin-bottom: 40px;
}

.plan-description h2, .plan-itinerary h2 {
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #dee2e6;
}

.day-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.day-card h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #007bff;
}

.day-schedule {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
}

.schedule-item h4 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 14px;
  color: #495057;
}

.additional-info {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.info-section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 18px;
  color: #495057;
}

.info-section ul {
  padding-left: 20px;
}

.info-section li {
  margin-bottom: 8px;
}

.no-itinerary {
  text-align: center;
  padding: 30px;
  background-color: #f8f9fa;
  border-radius: 8px;
  color: #6c757d;
}
</style> 