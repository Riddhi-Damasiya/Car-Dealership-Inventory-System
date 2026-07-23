import { useEffect, useState } from 'react'
import api from '../services/api'

/**
 * Admin page for managing vehicle inventory.
 * Admins can add, update, delete, and restock vehicles.
 */
function AdminPage() {
  const [vehicles, setVehicles] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [successMessage, setSuccessMessage] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editingVehicle, setEditingVehicle] = useState(null)
  const [formData, setFormData] = useState({
    make: '',
    model: '',
    category: '',
    price: '',
    quantity: '',
  })
  const [restockVehicleId, setRestockVehicleId] = useState(null)
  const [restockQuantity, setRestockQuantity] = useState(1)

  useEffect(() => {
    loadVehicles()
  }, [])

  const loadVehicles = async () => {
    try {
      setLoading(true)
      const data = await api.listVehicles(0, 100)
      setVehicles(data.items || [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load vehicles')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      setError(null)
      if (editingVehicle) {
        await api.updateVehicle(editingVehicle.id, formData)
        setSuccessMessage('Vehicle updated successfully')
      } else {
        await api.createVehicle(formData)
        setSuccessMessage('Vehicle created successfully')
      }
      setFormData({
        make: '',
        model: '',
        category: '',
        price: '',
        quantity: '',
      })
      setEditingVehicle(null)
      setShowForm(false)
      loadVehicles()
      setTimeout(() => setSuccessMessage(null), 5000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Operation failed')
    }
  }

  const handleEdit = (vehicle) => {
    setEditingVehicle(vehicle)
    setFormData({
      make: vehicle.make,
      model: vehicle.model,
      category: vehicle.category,
      price: vehicle.price,
      quantity: vehicle.quantity.toString(),
    })
    setShowForm(true)
  }

  const handleDelete = async (vehicleId) => {
    if (window.confirm('Are you sure you want to delete this vehicle?')) {
      try {
        setError(null)
        await api.deleteVehicle(vehicleId)
        setSuccessMessage('Vehicle deleted successfully')
        loadVehicles()
        setTimeout(() => setSuccessMessage(null), 5000)
      } catch (err) {
        setError(err.response?.data?.detail || 'Delete failed')
      }
    }
  }

  const handleRestock = async (e) => {
    e.preventDefault()
    try {
      setError(null)
      const response = await api.restockVehicle(
        restockVehicleId,
        parseInt(restockQuantity)
      )
      setSuccessMessage(response.message)
      setRestockVehicleId(null)
      setRestockQuantity(1)
      loadVehicles()
      setTimeout(() => setSuccessMessage(null), 5000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Restock failed')
    }
  }

  if (loading && vehicles.length === 0) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <p className="text-center text-gray-500">Loading vehicles...</p>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Admin Panel</h1>
        <button
          onClick={() => {
            setShowForm(!showForm)
            setEditingVehicle(null)
            setFormData({
              make: '',
              model: '',
              category: '',
              price: '',
              quantity: '',
            })
          }}
          className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition"
        >
          {showForm ? 'Cancel' : 'Add Vehicle'}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}

      {successMessage && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded mb-6">
          {successMessage}
        </div>
      )}

      {/* Add/Edit Form */}
      {showForm && (
        <div className="bg-gray-50 p-6 rounded-lg mb-8 border border-gray-200">
          <h2 className="text-xl font-semibold mb-4">
            {editingVehicle ? 'Edit Vehicle' : 'Add New Vehicle'}
          </h2>
          <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Make</label>
              <input
                type="text"
                required
                value={formData.make}
                onChange={(e) =>
                  setFormData({ ...formData, make: e.target.value })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Model</label>
              <input
                type="text"
                required
                value={formData.model}
                onChange={(e) =>
                  setFormData({ ...formData, model: e.target.value })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Category</label>
              <input
                type="text"
                required
                value={formData.category}
                onChange={(e) =>
                  setFormData({ ...formData, category: e.target.value })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Price</label>
              <input
                type="number"
                step="0.01"
                required
                value={formData.price}
                onChange={(e) =>
                  setFormData({ ...formData, price: e.target.value })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Quantity</label>
              <input
                type="number"
                required
                value={formData.quantity}
                onChange={(e) =>
                  setFormData({ ...formData, quantity: e.target.value })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded"
              />
            </div>
            <div className="flex items-end">
              <button
                type="submit"
                className="w-full bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition"
              >
                {editingVehicle ? 'Update' : 'Create'}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Vehicles Table */}
      <div className="overflow-x-auto">
        <table className="w-full border-collapse border border-gray-300">
          <thead className="bg-gray-100">
            <tr>
              <th className="border border-gray-300 px-4 py-2 text-left">Make</th>
              <th className="border border-gray-300 px-4 py-2 text-left">Model</th>
              <th className="border border-gray-300 px-4 py-2 text-left">Category</th>
              <th className="border border-gray-300 px-4 py-2 text-right">Price</th>
              <th className="border border-gray-300 px-4 py-2 text-right">Quantity</th>
              <th className="border border-gray-300 px-4 py-2 text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            {vehicles.length === 0 ? (
              <tr>
                <td colSpan="6" className="border border-gray-300 px-4 py-2 text-center text-gray-500">
                  No vehicles found
                </td>
              </tr>
            ) : (
              vehicles.map((vehicle) => (
                <tr key={vehicle.id} className="hover:bg-gray-50">
                  <td className="border border-gray-300 px-4 py-2">{vehicle.make}</td>
                  <td className="border border-gray-300 px-4 py-2">{vehicle.model}</td>
                  <td className="border border-gray-300 px-4 py-2">{vehicle.category}</td>
                  <td className="border border-gray-300 px-4 py-2 text-right">
                    ${parseFloat(vehicle.price).toFixed(2)}
                  </td>
                  <td className="border border-gray-300 px-4 py-2 text-right">
                    {vehicle.quantity}
                  </td>
                  <td className="border border-gray-300 px-4 py-2 text-center space-x-2">
                    <button
                      onClick={() => handleEdit(vehicle)}
                      className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition text-sm"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => setRestockVehicleId(vehicle.id)}
                      className="bg-yellow-600 text-white px-3 py-1 rounded hover:bg-yellow-700 transition text-sm"
                    >
                      Restock
                    </button>
                    <button
                      onClick={() => handleDelete(vehicle.id)}
                      className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700 transition text-sm"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Restock Modal */}
      {restockVehicleId && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg p-8 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-4">Restock Vehicle</h2>
            <form onSubmit={handleRestock}>
              <div className="mb-6">
                <label className="block text-sm font-medium mb-2">
                  Quantity to Add
                </label>
                <input
                  type="number"
                  min="1"
                  value={restockQuantity}
                  onChange={(e) => setRestockQuantity(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded"
                />
              </div>
              <div className="flex gap-4">
                <button
                  type="button"
                  onClick={() => {
                    setRestockVehicleId(null)
                    setRestockQuantity(1)
                  }}
                  className="flex-1 bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400 transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition"
                >
                  Restock
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default AdminPage
