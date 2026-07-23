import { useEffect, useState } from 'react'
import api from '../services/api'

/**
 * Dashboard page for browsing and purchasing vehicles.
 * Users can search, filter, and purchase vehicles.
 */
function DashboardPage() {
  const [vehicles, setVehicles] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [searchParams, setSearchParams] = useState({
    make: '',
    model: '',
    category: '',
    min_price: '',
    max_price: '',
  })
  const [selectedVehicle, setSelectedVehicle] = useState(null)
  const [purchaseQuantity, setPurchaseQuantity] = useState(1)
  const [successMessage, setSuccessMessage] = useState(null)

  useEffect(() => {
    loadVehicles()
  }, [])

  const loadVehicles = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await api.listVehicles(0, 50)
      setVehicles(data.items || [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load vehicles')
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async (e) => {
    e.preventDefault()
    try {
      setLoading(true)
      setError(null)
      const filteredParams = Object.fromEntries(
        Object.entries(searchParams).filter(([, v]) => v !== '')
      )
      const results = await api.searchVehicles(filteredParams)
      setVehicles(results || [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Search failed')
    } finally {
      setLoading(false)
    }
  }

  const handlePurchase = async (e) => {
    e.preventDefault()
    if (!selectedVehicle || purchaseQuantity < 1) {
      setError('Please select a vehicle and valid quantity')
      return
    }

    try {
      setError(null)
      const response = await api.purchaseVehicle(
        selectedVehicle.id,
        parseInt(purchaseQuantity)
      )
      setSuccessMessage(response.message)
      setPurchaseQuantity(1)
      setSelectedVehicle(null)
      loadVehicles()
      setTimeout(() => setSuccessMessage(null), 5000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Purchase failed')
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
      <h1 className="text-3xl font-bold mb-8">Vehicle Inventory</h1>

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

      {/* Search and Filter Form */}
      <form
        onSubmit={handleSearch}
        className="bg-gray-50 p-6 rounded-lg mb-8 border border-gray-200"
      >
        <h2 className="text-xl font-semibold mb-4">Search & Filter</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          <input
            type="text"
            placeholder="Make (e.g., Toyota)"
            value={searchParams.make}
            onChange={(e) =>
              setSearchParams({ ...searchParams, make: e.target.value })
            }
            className="px-3 py-2 border border-gray-300 rounded"
          />
          <input
            type="text"
            placeholder="Model (e.g., Camry)"
            value={searchParams.model}
            onChange={(e) =>
              setSearchParams({ ...searchParams, model: e.target.value })
            }
            className="px-3 py-2 border border-gray-300 rounded"
          />
          <input
            type="text"
            placeholder="Category (e.g., Sedan)"
            value={searchParams.category}
            onChange={(e) =>
              setSearchParams({ ...searchParams, category: e.target.value })
            }
            className="px-3 py-2 border border-gray-300 rounded"
          />
          <input
            type="number"
            placeholder="Min Price"
            value={searchParams.min_price}
            onChange={(e) =>
              setSearchParams({ ...searchParams, min_price: e.target.value })
            }
            className="px-3 py-2 border border-gray-300 rounded"
          />
          <input
            type="number"
            placeholder="Max Price"
            value={searchParams.max_price}
            onChange={(e) =>
              setSearchParams({ ...searchParams, max_price: e.target.value })
            }
            className="px-3 py-2 border border-gray-300 rounded"
          />
        </div>
        <div className="flex gap-4 mt-4">
          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition"
          >
            Search
          </button>
          <button
            type="button"
            onClick={() => {
              setSearchParams({
                make: '',
                model: '',
                category: '',
                min_price: '',
                max_price: '',
              })
              loadVehicles()
            }}
            className="bg-gray-400 text-white px-6 py-2 rounded hover:bg-gray-500 transition"
          >
            Clear
          </button>
        </div>
      </form>

      {/* Vehicles Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {vehicles.length === 0 ? (
          <p className="text-gray-500 col-span-full text-center py-8">
            No vehicles found
          </p>
        ) : (
          vehicles.map((vehicle) => (
            <div
              key={vehicle.id}
              className={`border rounded-lg p-6 cursor-pointer transition ${
                selectedVehicle?.id === vehicle.id
                  ? 'border-blue-600 bg-blue-50'
                  : 'border-gray-200 hover:border-blue-400'
              }`}
              onClick={() => setSelectedVehicle(vehicle)}
            >
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-semibold">
                    {vehicle.make} {vehicle.model}
                  </h3>
                  <p className="text-gray-600 text-sm">{vehicle.category}</p>
                </div>
                <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded text-sm">
                  {vehicle.quantity} available
                </span>
              </div>
              <p className="text-2xl font-bold text-blue-600 mb-4">
                ${parseFloat(vehicle.price).toFixed(2)}
              </p>
              <div className="text-xs text-gray-500">
                <p>Created: {new Date(vehicle.created_at).toLocaleDateString()}</p>
                <p>Updated: {new Date(vehicle.updated_at).toLocaleDateString()}</p>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Purchase Form */}
      {selectedVehicle && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg p-8 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-4">Purchase Vehicle</h2>
            <div className="mb-6">
              <p className="text-gray-700 font-semibold">
                {selectedVehicle.make} {selectedVehicle.model}
              </p>
              <p className="text-gray-600">Price: ${parseFloat(selectedVehicle.price).toFixed(2)}</p>
              <p className="text-gray-600">
                Available: {selectedVehicle.quantity}
              </p>
            </div>
            <form onSubmit={handlePurchase}>
              <div className="mb-6">
                <label className="block text-sm font-medium mb-2">
                  Quantity
                </label>
                <input
                  type="number"
                  min="1"
                  max={selectedVehicle.quantity}
                  value={purchaseQuantity}
                  onChange={(e) => setPurchaseQuantity(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded"
                />
              </div>
              <div className="mb-6">
                <p className="text-lg font-semibold">
                  Total: ${(
                    parseFloat(selectedVehicle.price) * purchaseQuantity
                  ).toFixed(2)}
                </p>
              </div>
              <div className="flex gap-4">
                <button
                  type="button"
                  onClick={() => {
                    setSelectedVehicle(null)
                    setPurchaseQuantity(1)
                  }}
                  className="flex-1 bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400 transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition"
                >
                  Purchase
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default DashboardPage
