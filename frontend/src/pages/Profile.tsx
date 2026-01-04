import React from 'react'
import { User, Edit, Camera, Settings, Bell, Shield } from 'lucide-react'
import { useAuth } from '../services/context/AuthContext'

export default function Profile() {
  const { user } = useAuth()

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Profile</h1>
          <p className="text-gray-600">Manage your account and preferences</p>
        </div>
        <div className="mt-4 sm:mt-0">
          <button className="btn btn-outline">
            <Edit className="h-4 w-4 mr-2" />
            Edit Profile
          </button>
        </div>
      </div>

      {/* Profile Card */}
      <div className="bg-white rounded-lg shadow-soft">
        <div className="p-6">
          <div className="flex flex-col sm:flex-row items-start sm:items-center space-y-4 sm:space-y-0 sm:space-x-6">
            <div className="relative">
              <div className="h-24 w-24 bg-primary-100 rounded-full flex items-center justify-center">
                {user?.profile.avatar ? (
                  <img
                    src={user.profile.avatar}
                    alt={user.username}
                    className="h-24 w-24 rounded-full object-cover"
                  />
                ) : (
                  <User className="h-12 w-12 text-primary-600" />
                )}
              </div>
              <button className="absolute -bottom-1 -right-1 h-8 w-8 bg-primary-600 rounded-full flex items-center justify-center text-white hover:bg-primary-700 transition-colors">
                <Camera className="h-4 w-4" />
              </button>
            </div>
            
            <div className="flex-1">
              <h2 className="text-2xl font-bold text-gray-900">{user?.username}</h2>
              <p className="text-gray-600">{user?.email}</p>
              <p className="text-sm text-gray-500 mt-2">
                Member since {new Date(user?.created_at || '').toLocaleDateString()}
              </p>
              
              {user?.profile.bio && (
                <p className="text-gray-700 mt-3">{user.profile.bio}</p>
              )}
              
              <div className="flex flex-wrap gap-2 mt-4">
                {user?.profile.style_preferences.map((preference, index) => (
                  <span key={index} className="badge badge-default">
                    {preference}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Settings Sections */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Account Settings */}
        <div className="bg-white rounded-lg shadow-soft">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center space-x-2">
              <Settings className="h-5 w-5 text-gray-600" />
              <h3 className="text-lg font-semibold text-gray-900">Account Settings</h3>
            </div>
          </div>
          <div className="p-6 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900">Email Notifications</p>
                <p className="text-sm text-gray-500">Receive updates about your wardrobe</p>
              </div>
              <input type="checkbox" className="h-4 w-4 text-primary-600" defaultChecked />
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900">Push Notifications</p>
                <p className="text-sm text-gray-500">Get notified about new features</p>
              </div>
              <input type="checkbox" className="h-4 w-4 text-primary-600" defaultChecked />
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900">Marketing Emails</p>
                <p className="text-sm text-gray-500">Receive promotional content</p>
              </div>
              <input type="checkbox" className="h-4 w-4 text-primary-600" />
            </div>
          </div>
        </div>

        {/* Privacy Settings */}
        <div className="bg-white rounded-lg shadow-soft">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center space-x-2">
              <Shield className="h-5 w-5 text-gray-600" />
              <h3 className="text-lg font-semibold text-gray-900">Privacy Settings</h3>
            </div>
          </div>
          <div className="p-6 space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-900 mb-2">
                Profile Visibility
              </label>
              <select className="input w-full">
                <option>Public</option>
                <option>Friends Only</option>
                <option>Private</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-900 mb-2">
                Wardrobe Visibility
              </label>
              <select className="input w-full">
                <option>Private</option>
                <option>Friends Only</option>
                <option>Public</option>
              </select>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900">Data Sharing</p>
                <p className="text-sm text-gray-500">Help improve our AI with anonymous data</p>
              </div>
              <input type="checkbox" className="h-4 w-4 text-primary-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Style Preferences */}
      <div className="bg-white rounded-lg shadow-soft">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Style Preferences</h3>
          <p className="text-sm text-gray-500">Help us personalize your experience</p>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-900 mb-2">
                Color Season
              </label>
              <select className="input w-full">
                <option>Spring</option>
                <option>Summer</option>
                <option>Autumn</option>
                <option>Winter</option>
                <option>Not sure</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-900 mb-2">
                Preferred Style
              </label>
              <select className="input w-full">
                <option>Casual</option>
                <option>Formal</option>
                <option>Bohemian</option>
                <option>Minimalist</option>
                <option>Vintage</option>
                <option>Modern</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
