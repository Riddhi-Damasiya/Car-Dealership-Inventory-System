/**
 * API client service for communicating with the backend.
 * Handles authentication and provides methods for all API endpoints.
 */

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class ApiClient {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Add interceptor to attach token to all requests
    this.client.interceptors.request.use((config) => {
      const token = this.getToken()
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })

    // Add interceptor to handle 401 errors
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          this.logout()
        }
        return Promise.reject(error)
      }
    )
  }

  /**
   * Get stored authentication token
   * @returns {string|null} JWT token or null
   */
  getToken() {
    return localStorage.getItem('access_token')
  }

  /**
   * Set authentication token
   * @param {string} token - JWT token
   */
  setToken(token) {
    localStorage.setItem('access_token', token)
  }

  /**
   * Check if user is authenticated
   * @returns {boolean} True if token exists
   */
  isAuthenticated() {
    return !!this.getToken()
  }

  /**
   * Clear authentication
   */
  logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }

  /**
   * Store user info
   * @param {object} user - User object
   */
  setUser(user) {
    localStorage.setItem('user', JSON.stringify(user))
  }

  /**
   * Get stored user info
   * @returns {object|null} User object or null
   */
  getUser() {
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : null
  }

  // ===== Authentication Endpoints =====

  /**
   * Register a new user
   * @param {string} email - User email
   * @param {string} password - User password
   * @returns {Promise} Response with access token
   */
  async register(email, password) {
    const response = await this.client.post('/api/auth/register', {
      email,
      password,
    })
    if (response.data.access_token) {
      this.setToken(response.data.access_token)
    }
    return response.data
  }

  /**
   * Login user
   * @param {string} email - User email
   * @param {string} password - User password
   * @returns {Promise} Response with access token
   */
  async login(email, password) {
    const response = await this.client.post('/api/auth/login', {
      email,
      password,
    })
    if (response.data.access_token) {
      this.setToken(response.data.access_token)
    }
    return response.data
  }

  // ===== Vehicle Endpoints =====

  /**
   * Get list of all vehicles with pagination
   * @param {number} skip - Number of items to skip
   * @param {number} limit - Number of items to return
   * @returns {Promise} List of vehicles with pagination info
   */
  async listVehicles(skip = 0, limit = 10) {
    const response = await this.client.get('/api/vehicles', {
      params: { skip, limit },
    })
    return response.data
  }

  /**
   * Search and filter vehicles
   * @param {object} filters - Search filters
   * @returns {Promise} List of matching vehicles
   */
  async searchVehicles(filters = {}) {
    const response = await this.client.get('/api/vehicles/search', {
      params: filters,
    })
    return response.data
  }

  /**
   * Get a specific vehicle by ID
   * @param {number} vehicleId - Vehicle ID
   * @returns {Promise} Vehicle details
   */
  async getVehicle(vehicleId) {
    const response = await this.client.get(`/api/vehicles/${vehicleId}`)
    return response.data
  }

  /**
   * Create a new vehicle (admin only)
   * @param {object} vehicleData - Vehicle creation data
   * @returns {Promise} Created vehicle
   */
  async createVehicle(vehicleData) {
    const response = await this.client.post('/api/vehicles', vehicleData)
    return response.data
  }

  /**
   * Update a vehicle (admin only)
   * @param {number} vehicleId - Vehicle ID
   * @param {object} vehicleData - Updated vehicle data
   * @returns {Promise} Updated vehicle
   */
  async updateVehicle(vehicleId, vehicleData) {
    const response = await this.client.put(
      `/api/vehicles/${vehicleId}`,
      vehicleData
    )
    return response.data
  }

  /**
   * Delete a vehicle (admin only)
   * @param {number} vehicleId - Vehicle ID
   * @returns {Promise} Deletion confirmation
   */
  async deleteVehicle(vehicleId) {
    const response = await this.client.delete(`/api/vehicles/${vehicleId}`)
    return response.data
  }

  /**
   * Purchase a vehicle
   * @param {number} vehicleId - Vehicle ID
   * @param {number} quantity - Quantity to purchase
   * @returns {Promise} Purchase confirmation
   */
  async purchaseVehicle(vehicleId, quantity) {
    const response = await this.client.post(
      `/api/vehicles/${vehicleId}/purchase`,
      { quantity }
    )
    return response.data
  }

  /**
   * Restock a vehicle (admin only)
   * @param {number} vehicleId - Vehicle ID
   * @param {number} quantity - Quantity to restock
   * @returns {Promise} Restock confirmation
   */
  async restockVehicle(vehicleId, quantity) {
    const response = await this.client.post(
      `/api/vehicles/${vehicleId}/restock`,
      { quantity }
    )
    return response.data
  }
}

// Export singleton instance
export default new ApiClient()
