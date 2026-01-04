import React from 'react'
import { Plus, Calendar, Sparkles } from 'lucide-react'

export default function OutfitPlanner() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Outfit Planner</h1>
          <p className="text-gray-600">Create and organize your outfits</p>
        </div>
        <div className="mt-4 sm:mt-0">
          <button className="btn btn-primary">
            <Plus className="h-4 w-4 mr-2" />
            Create Outfit
          </button>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow-soft p-6">
          <div className="flex items-center space-x-3">
            <div className="h-10 w-10 bg-primary-100 rounded-lg flex items-center justify-center">
              <Plus className="h-5 w-5 text-primary-600" />
            </div>
            <div>
              <h3 className="text-lg font-medium text-gray-900">Create New Outfit</h3>
              <p className="text-sm text-gray-500">Design a new outfit from your wardrobe</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-soft p-6">
          <div className="flex items-center space-x-3">
            <div className="h-10 w-10 bg-secondary-100 rounded-lg flex items-center justify-center">
              <Sparkles className="h-5 w-5 text-secondary-600" />
            </div>
            <div>
              <h3 className="text-lg font-medium text-gray-900">AI Suggestions</h3>
              <p className="text-sm text-gray-500">Get AI-powered outfit recommendations</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-soft p-6">
          <div className="flex items-center space-x-3">
            <div className="h-10 w-10 bg-accent-100 rounded-lg flex items-center justify-center">
              <Calendar className="h-5 w-5 text-accent-600" />
            </div>
            <div>
              <h3 className="text-lg font-medium text-gray-900">Outfit Calendar</h3>
              <p className="text-sm text-gray-500">Plan outfits for upcoming events</p>
            </div>
          </div>
        </div>
      </div>

      {/* Empty State */}
      <div className="bg-white rounded-lg shadow-soft">
        <div className="text-center py-12">
          <div className="mx-auto h-24 w-24 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <Calendar className="h-12 w-12 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No outfits created yet</h3>
          <p className="text-gray-500 mb-6">
            Start creating outfits by combining items from your wardrobe
          </p>
          <button className="btn btn-primary">
            <Plus className="h-4 w-4 mr-2" />
            Create Your First Outfit
          </button>
        </div>
      </div>
    </div>
  )
}
