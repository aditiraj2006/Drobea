import React from 'react'
import { BarChart3, TrendingUp, DollarSign, Leaf, Calendar } from 'lucide-react'

export default function Analytics() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Analytics</h1>
          <p className="text-gray-600">Track your style journey and wardrobe insights</p>
        </div>
        <div className="mt-4 sm:mt-0">
          <select className="input w-32">
            <option>Last 30 days</option>
            <option>Last 3 months</option>
            <option>Last year</option>
          </select>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow-soft p-6">
          <div className="flex items-center">
            <div className="h-10 w-10 bg-primary-100 rounded-lg flex items-center justify-center">
              <BarChart3 className="h-5 w-5 text-primary-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Most Worn Item</p>
              <p className="text-lg font-semibold text-gray-900">Blue Jeans</p>
              <p className="text-sm text-green-600">12 times this month</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-soft p-6">
          <div className="flex items-center">
            <div className="h-10 w-10 bg-secondary-100 rounded-lg flex items-center justify-center">
              <DollarSign className="h-5 w-5 text-secondary-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Cost Per Wear</p>
              <p className="text-lg font-semibold text-gray-900">$2.50</p>
              <p className="text-sm text-green-600">-15% from last month</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-soft p-6">
          <div className="flex items-center">
            <div className="h-10 w-10 bg-accent-100 rounded-lg flex items-center justify-center">
              <Leaf className="h-5 w-5 text-accent-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Sustainability Score</p>
              <p className="text-lg font-semibold text-gray-900">8.5/10</p>
              <p className="text-sm text-green-600">Great job!</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-soft p-6">
          <div className="flex items-center">
            <div className="h-10 w-10 bg-green-100 rounded-lg flex items-center justify-center">
              <TrendingUp className="h-5 w-5 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Style Growth</p>
              <p className="text-lg font-semibold text-gray-900">+23%</p>
              <p className="text-sm text-green-600">vs last month</p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-soft p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Wardrobe Usage</h3>
          <div className="h-64 flex items-center justify-center text-gray-500">
            <div className="text-center">
              <BarChart3 className="h-12 w-12 mx-auto mb-2 text-gray-300" />
              <p>Chart will be displayed here</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-soft p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Color Preferences</h3>
          <div className="h-64 flex items-center justify-center text-gray-500">
            <div className="text-center">
              <BarChart3 className="h-12 w-12 mx-auto mb-2 text-gray-300" />
              <p>Chart will be displayed here</p>
            </div>
          </div>
        </div>
      </div>

      {/* Sustainability Insights */}
      <div className="bg-white rounded-lg shadow-soft">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center space-x-2">
            <Leaf className="h-5 w-5 text-green-600" />
            <h2 className="text-lg font-semibold text-gray-900">Sustainability Insights</h2>
          </div>
          <p className="text-sm text-gray-500">Your environmental impact and recommendations</p>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600 mb-2">45kg</div>
              <div className="text-sm text-gray-500">CO2 Saved</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600 mb-2">120L</div>
              <div className="text-sm text-gray-500">Water Saved</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600 mb-2">8</div>
              <div className="text-sm text-gray-500">Items Donated</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
