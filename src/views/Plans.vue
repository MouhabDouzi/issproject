<template>
  <div class="plans-container">
    <h1>My Travel Plans</h1>
    <div v-if="loading" class="loading">Loading plans...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="plans.length === 0" class="no-plans">
      <p>You don't have any travel plans yet.</p>
      <router-link to="/create-plan" class="btn btn-primary">Create a Plan</router-link>
    </div>
    <div v-else class="plans-grid">
      <div v-for="plan in plans" :key="plan.id" class="plan-card">
        <div class="plan-header">
          <h3>{{ plan.title }}</h3>
          <span class="plan-date">{{ formatDate(plan.created_at) }}</span>
        </div>
        <div class="plan-details">
          <p><strong>Destination:</strong> {{ plan.destination }}</p>
          <p><strong>Duration:</strong> {{ plan.duration }}</p>
          <p><strong>Budget:</strong> {{ plan.budget }}</p>
        </div>
        <div class="plan-actions">
          <router-link :to="'/plan/' + plan.id" class="btn btn-info">View Details</router-link>
          <button @click="deletePlan(plan.id)" class="btn btn-danger">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Plans',
  data() {
    return {
      plans: [],
      loading: true,
      error: null
    };
  },
  created() {
    this.fetchPlans();
  },
  methods: {
    async fetchPlans() {
      try {
        this.loading = true;
        const token = localStorage.getItem('token');
        if (!token) {
          this.error = 'You need to be logged in to view your plans';
          this.loading = false;
          return;
        }
        
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/plans`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        this.plans = response.data.plans;
        this.loading = false;
      } catch (error) {
        console.error('Error fetching plans:', error);
        this.error = 'Failed to load your travel plans. Please try again later.';
        this.loading = false;
      }
    },
    async deletePlan(planId) {
      if (!confirm('Are you sure you want to delete this plan?')) {
        return;
      }
      
      try {
        const token = localStorage.getItem('token');
        await axios.delete(`${process.env.VUE_APP_API_URL}/api/plans/${planId}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        // Remove the deleted plan from the list
        this.plans = this.plans.filter(plan => plan.id !== planId);
      } catch (error) {
        console.error('Error deleting plan:', error);
        alert('Failed to delete the plan. Please try again later.');
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
.plans-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading, .error, .no-plans {
  text-align: center;
  padding: 40px;
  font-size: 18px;
}

.error {
  color: #dc3545;
}

.no-plans {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.plans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.plan-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.plan-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.plan-header h3 {
  margin: 0;
  color: #333;
}

.plan-date {
  font-size: 14px;
  color: #666;
}

.plan-details {
  margin-bottom: 20px;
}

.plan-details p {
  margin: 8px 0;
}

.plan-actions {
  display: flex;
  justify-content: space-between;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  border: none;
}

.btn-info {
  background-color: #17a2b8;
  color: white;
  border: none;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
  border: none;
}
</style> 