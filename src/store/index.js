import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    isAuthenticated: false,
    user: null,
    token: localStorage.getItem('token') || null,
    plans: [],
    favorites: [],
    error: null
  },
  mutations: {
    setAuth(state, { token, user }) {
      state.isAuthenticated = true
      state.token = token
      state.user = user
      localStorage.setItem('token', token)
    },
    clearAuth(state) {
      state.isAuthenticated = false
      state.token = null
      state.user = null
      localStorage.removeItem('token')
    },
    setPlans(state, plans) {
      state.plans = plans
    },
    addPlan(state, plan) {
      state.plans.push(plan)
    },
    setFavorites(state, favorites) {
      state.favorites = favorites
    },
    addFavorite(state, favorite) {
      state.favorites.push(favorite)
    },
    removeFavorite(state, favoriteId) {
      state.favorites = state.favorites.filter(f => f.id !== favoriteId)
    },
    setError(state, error) {
      state.error = error
    }
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await axios.post('/api/auth/login', credentials)
        commit('setAuth', {
          token: response.data.token,
          user: response.data.user
        })
        return response
      } catch (error) {
        commit('setError', error.response?.data?.message || 'Login failed')
        throw error
      }
    },
    async signup({ commit }, userData) {
      try {
        const response = await axios.post('/api/auth/signup', userData)
        commit('setAuth', {
          token: response.data.token,
          user: response.data.user
        })
        return response
      } catch (error) {
        commit('setError', error.response?.data?.message || 'Signup failed')
        throw error
      }
    },
    logout({ commit }) {
      commit('clearAuth')
    },
    async createPlan({ commit }, planData) {
      try {
        const response = await axios.post('/api/plans/create', planData, {
          headers: { Authorization: `Bearer ${this.state.token}` }
        })
        commit('addPlan', response.data.plan)
        return response
      } catch (error) {
        commit('setError', error.response?.data?.message || 'Failed to create plan')
        throw error
      }
    },
    async fetchPlans({ commit }) {
      try {
        const response = await axios.get('/api/plans', {
          headers: { Authorization: `Bearer ${this.state.token}` }
        })
        commit('setPlans', response.data.plans)
        return response
      } catch (error) {
        commit('setError', error.response?.data?.message || 'Failed to fetch plans')
        throw error
      }
    },
    async addToFavorites({ commit }, planId) {
      try {
        const response = await axios.post(`/api/favorites/${planId}`, {}, {
          headers: { Authorization: `Bearer ${this.state.token}` }
        })
        commit('addFavorite', response.data.favorite)
        return response
      } catch (error) {
        commit('setError', error.response?.data?.message || 'Failed to add to favorites')
        throw error
      }
    },
    async removeFromFavorites({ commit }, favoriteId) {
      try {
        await axios.delete(`/api/favorites/${favoriteId}`, {
          headers: { Authorization: `Bearer ${this.state.token}` }
        })
        commit('removeFavorite', favoriteId)
      } catch (error) {
        commit('setError', error.response?.data?.message || 'Failed to remove from favorites')
        throw error
      }
    }
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    currentUser: state => state.user,
    userPlans: state => state.plans,
    userFavorites: state => state.favorites,
    error: state => state.error
  }
}) 