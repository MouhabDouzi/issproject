<template>
  <div class="favorites-container">
    <h1>My Favorite Travel Plans</h1>
    <div v-if="loading" class="loading">Loading favorites...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="favorites.length === 0" class="no-favorites">
      <p>You don't have any favorite travel plans yet.</p>
      <router-link to="/plans" class="btn btn-primary">Browse Plans</router-link>
    </div>
    <div v-else class="favorites-grid">
      <div v-for="favorite in favorites" :key="favorite.id" class="favorite-card">
        <div class="favorite-header">
          <h3>{{ favorite.plan.title }}</h3>
          <span class="favorite-date">Added: {{ formatDate(favorite.created_at) }}</span>
        </div>
        <div class="favorite-details">
          <p><strong>Destination:</strong> {{ favorite.plan.destination }}</p>
          <p><strong>Duration:</strong> {{ favorite.plan.duration }}</p>
          <p><strong>Budget:</strong> {{ favorite.plan.budget }}</p>
        </div>
        <div class="favorite-actions">
          <router-link :to="'/plan/' + favorite.plan.id" class="btn btn-info">View Details</router-link>
          <button @click="removeFavorite(favorite.id)" class="btn btn-danger">Remove</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Favorites',
  data() {
    return {
      favorites: [],
      loading: true,
      error: null
    };
  },
  created() {
    this.fetchFavorites();
  },
  methods: {
    async fetchFavorites() {
      try {
        this.loading = true;
        const token = localStorage.getItem('token');
        
        if (!token) {
          this.error = 'You need to be logged in to view your favorites';
          this.loading = false;
          return;
        }
        
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/favorites`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        this.favorites = response.data.favorites;
        this.loading = false;
      } catch (error) {
        console.error('Error fetching favorites:', error);
        this.error = 'Failed to load your favorites. Please try again later.';
        this.loading = false;
      }
    },
    async removeFavorite(favoriteId) {
      if (!confirm('Are you sure you want to remove this plan from your favorites?')) {
        return;
      }
      
      try {
        const token = localStorage.getItem('token');
        await axios.delete(`${process.env.VUE_APP_API_URL}/api/favorites/${favoriteId}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        // Remove the deleted favorite from the list
        this.favorites = this.favorites.filter(fav => fav.id !== favoriteId);
      } catch (error) {
        console.error('Error removing favorite:', error);
        alert('Failed to remove the plan from favorites. Please try again later.');
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
.favorites-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading, .error, .no-favorites {
  text-align: center;
  padding: 40px;
  font-size: 18px;
}

.error {
  color: #dc3545;
}

.no-favorites {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.favorite-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.favorite-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.favorite-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.favorite-header h3 {
  margin: 0;
  color: #333;
}

.favorite-date {
  font-size: 14px;
  color: #666;
}

.favorite-details {
  margin-bottom: 20px;
}

.favorite-details p {
  margin: 8px 0;
}

.favorite-actions {
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