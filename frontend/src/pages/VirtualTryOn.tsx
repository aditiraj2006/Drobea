import React from 'react'
import { Camera, Upload, Sparkles, Zap } from 'lucide-react'

export default function VirtualTryOn() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Virtual Try-On</h1>
          <p className="text-gray-600">Try on outfits virtually with AI</p>
        </div>
        <div className="mt-4 sm:mt-0">
          <button className="btn btn-primary">
            <Camera className="h-4 w-4 mr-2" />
            Start Try-On
          </button>
        </div>
      </div>

      {/* Getting Started */}
      <div className="bg-gradient-to-r from-primary-600 to-secondary-600 rounded-xl p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold mb-2">Ready to try on outfits virtually?</h2>
            <p className="text-primary-100">
              Upload your reference photos and see how outfits look on you before buying
            </p>
          </div>
          <div className="hidden md:block">
            <Camera className="h-16 w-16 text-primary-200" />
          </div>
        </div>
      </div>

      {/* Steps */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow-soft p-6">
          <div className="flex items-center space-x-3 mb-4">
            <div className="h-8 w-8 bg-primary-100 rounded-full flex items-center justify-center text-primary-600 font-bold">
              1
            </div>
            <h3 className="text-lg font-medium text-gray-900">Upload Reference Photos</h3>
          </div>
          <p className="text-gray-500 mb-4">
            Upload clear photos of yourself in different poses for the best results
          </p>
          <button className="btn btn-outline w-full">
            <Upload className="h-4 w-4 mr-2" />
            Upload Photos
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-soft p-6">
          <div className="flex items-center space-x-3 mb-4">
            <div className="h-8 w-8 bg-secondary-100 rounded-full flex items-center justify-center text-secondary-600 font-bold">
              2
            </div>
            <h3 className="text-lg font-medium text-gray-900">Select Outfit</h3>
          </div>
          <p className="text-gray-500 mb-4">
            Choose an outfit from your wardrobe or create a new combination
          </p>
          <button className="btn btn-outline w-full">
            <Sparkles className="h-4 w-4 mr-2" />
            Choose Outfit
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-soft p-6">
          <div className="flex items-center space-x-3 mb-4">
            <div className="h-8 w-8 bg-accent-100 rounded-full flex items-center justify-center text-accent-600 font-bold">
              3
            </div>
            <h3 className="text-lg font-medium text-gray-900">Generate Try-On</h3>
          </div>
          <p className="text-gray-500 mb-4">
            Let AI generate a realistic image of you wearing the selected outfit
          </p>
          <button className="btn btn-outline w-full">
            <Zap className="h-4 w-4 mr-2" />
            Generate
          </button>
        </div>
      </div>

      {/* Empty State */}
      <div className="bg-white rounded-lg shadow-soft">
        <div className="text-center py-12">
          <div className="mx-auto h-24 w-24 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <Camera className="h-12 w-12 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No reference photos uploaded</h3>
          <p className="text-gray-500 mb-6">
            Upload your reference photos to start using virtual try-on
          </p>
          <button className="btn btn-primary">
            <Upload className="h-4 w-4 mr-2" />
            Upload Reference Photos
          </button>
        </div>
      </div>
    </div>
  )
}
