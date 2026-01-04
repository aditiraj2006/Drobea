import React from 'react'
import { Plus, Search, Filter, Grid, List } from 'lucide-react'

export default function Wardrobe() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">My Wardrobe</h1>
          <p className="text-gray-600">Manage your clothing collection</p>
        </div>
        <div className="mt-4 sm:mt-0">
          <button className="btn btn-primary">
            <Plus className="h-4 w-4 mr-2" />
            Add New Item
          </button>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-lg shadow-soft p-6">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search your wardrobe..."
                className="input w-full pl-10"
              />
            </div>
          </div>
          <div className="flex gap-2">
            <button className="btn btn-outline">
              <Filter className="h-4 w-4 mr-2" />
              Filters
            </button>
            <div className="flex border border-gray-300 rounded-md">
              <button className="p-2 text-gray-400 hover:text-gray-600">
                <Grid className="h-4 w-4" />
              </button>
              <button className="p-2 text-primary-600 border-l border-gray-300">
                <List className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Empty State */}
      <div className="bg-white rounded-lg shadow-soft">
        <div className="text-center py-12">
          <div className="mx-auto h-24 w-24 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <Plus className="h-12 w-12 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No items in your wardrobe yet</h3>
          <p className="text-gray-500 mb-6">
            Start building your digital wardrobe by adding your first clothing item
          </p>
          <button className="btn btn-primary">
            <Plus className="h-4 w-4 mr-2" />
            Add Your First Item
          </button>
        </div>
      </div>
    </div>
  )
}
