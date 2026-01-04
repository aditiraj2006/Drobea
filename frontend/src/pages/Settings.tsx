import React from 'react'
import { Settings as SettingsIcon, Bell, Shield, Palette, Database, HelpCircle } from 'lucide-react'

export default function Settings() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600">Customize your Drobea experience</p>
      </div>

      {/* Settings Sections */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Notifications */}
        <div className="bg-white rounded-lg shadow-soft">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center space-x-2">
              <Bell className="h-5 w-5 text-gray-600" />
              <h3 className="text-lg font-semibold text-gray-900">Notifications</h3>
            </div>
          </div>
          <div className="p-6 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900">Email Notifications</p>
                <p className="text-sm text-gray-500">Receive updates via email</p>
              </div>
              <input type="checkbox" className="h-4 w-4 text-primary-600" defaultChecked />
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900">Push Notifications</p>
                <p className="text-sm text-gray-500">Get notified on your device</p>
              </div>
              <input type="checkbox" className="h-4 w-4 text-primary-600" defaultChecked />
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900">Outfit Reminders</p>
                <p className="text-sm text-gray-500">Daily outfit suggestions</p>
              </div>
              <input type="checkbox" className="h-4 w-4 text-primary-600" />
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900">Weather Alerts</p>
                <p className="text-sm text-gray-500">Weather-based outfit recommendations</p>
              </div>
              <input type="checkbox" className="h-4 w-4 text-primary-600" defaultChecked />
            </div>
          </div>
        </div>

        {/* Privacy */}
        <div className="bg-white rounded-lg shadow-soft">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center space-x-2">
              <Shield className="h-5 w-5 text-gray-600" />
              <h3 className="text-lg font-semibold text-gray-900">Privacy & Security</h3>
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
                Data Retention
              </label>
              <select className="input w-full">
                <option>1 year</option>
                <option>2 years</option>
                <option>5 years</option>
                <option>Forever</option>
              </select>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900">Analytics Sharing</p>
                <p className="text-sm text-gray-500">Help improve our AI with anonymous data</p>
              </div>
              <input type="checkbox" className="h-4 w-4 text-primary-600" />
            </div>
          </div>
        </div>

        {/* Appearance */}
        <div className="bg-white rounded-lg shadow-soft">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center space-x-2">
              <Palette className="h-5 w-5 text-gray-600" />
              <h3 className="text-lg font-semibold text-gray-900">Appearance</h3>
            </div>
          </div>
          <div className="p-6 space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-900 mb-2">
                Theme
              </label>
              <div className="flex space-x-4">
                <label className="flex items-center">
                  <input type="radio" name="theme" value="light" className="h-4 w-4 text-primary-600" defaultChecked />
                  <span className="ml-2 text-sm text-gray-700">Light</span>
                </label>
                <label className="flex items-center">
                  <input type="radio" name="theme" value="dark" className="h-4 w-4 text-primary-600" />
                  <span className="ml-2 text-sm text-gray-700">Dark</span>
                </label>
                <label className="flex items-center">
                  <input type="radio" name="theme" value="auto" className="h-4 w-4 text-primary-600" />
                  <span className="ml-2 text-sm text-gray-700">Auto</span>
                </label>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-900 mb-2">
                Language
              </label>
              <select className="input w-full">
                <option>English</option>
                <option>Spanish</option>
                <option>French</option>
                <option>German</option>
                <option>Hindi</option>
              </select>
            </div>
          </div>
        </div>

        {/* Data Management */}
        <div className="bg-white rounded-lg shadow-soft">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center space-x-2">
              <Database className="h-5 w-5 text-gray-600" />
              <h3 className="text-lg font-semibold text-gray-900">Data Management</h3>
            </div>
          </div>
          <div className="p-6 space-y-4">
            <button className="btn btn-outline w-full">
              Export My Data
            </button>
            <button className="btn btn-outline w-full">
              Download Wardrobe
            </button>
            <button className="btn btn-outline w-full text-red-600 hover:text-red-700">
              Delete Account
            </button>
          </div>
        </div>
      </div>

      {/* Help & Support */}
      <div className="bg-white rounded-lg shadow-soft">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center space-x-2">
            <HelpCircle className="h-5 w-5 text-gray-600" />
            <h3 className="text-lg font-semibold text-gray-900">Help & Support</h3>
          </div>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="btn btn-outline">
              Help Center
            </button>
            <button className="btn btn-outline">
              Contact Support
            </button>
            <button className="btn btn-outline">
              Feature Request
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
