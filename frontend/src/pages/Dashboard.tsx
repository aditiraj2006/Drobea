import { useAuth } from '../services/context/AuthContext'
import { 
  Shirt, 
  Calendar, 
  Camera, 
  Users, 
  TrendingUp,
  Sparkles,
  Plus,
  ArrowRight
} from 'lucide-react'

export default function Dashboard() {
  const { user } = useAuth()

  const stats = [
    { name: 'Wardrobe Items', value: '24', icon: Shirt, change: '+2 this week' },
    { name: 'Outfits Created', value: '12', icon: Calendar, change: '+3 this week' },
    { name: 'Virtual Try-Ons', value: '8', icon: Camera, change: '+1 today' },
    { name: 'Social Followers', value: '156', icon: Users, change: '+12 this week' },
  ]

  const recentActivities = [
    { id: 1, action: 'Added new item', item: 'Blue Denim Jacket', time: '2 hours ago' },
    { id: 2, action: 'Created outfit', item: 'Casual Friday Look', time: '1 day ago' },
    { id: 3, action: 'Virtual try-on', item: 'Summer Dress', time: '2 days ago' },
    { id: 4, action: 'Shared outfit', item: 'Work Professional', time: '3 days ago' },
  ]

  const quickActions = [
    { name: 'Add New Item', description: 'Upload a new clothing item', icon: Plus, href: '/wardrobe' },
    { name: 'Create Outfit', description: 'Design a new outfit', icon: Calendar, href: '/outfits' },
    { name: 'Virtual Try-On', description: 'Try on outfits virtually', icon: Camera, href: '/virtual-tryon' },
    { name: 'View Analytics', description: 'Check your style insights', icon: TrendingUp, href: '/analytics' },
  ]

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-primary-600 to-secondary-600 rounded-xl p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">
              Welcome back, {user?.username}! 👋
            </h1>
            <p className="text-primary-100 mt-2">
              Ready to discover your next great outfit?
            </p>
          </div>
          <div className="hidden md:block">
            <Sparkles className="h-16 w-16 text-primary-200" />
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div key={stat.name} className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-soft border border-gray-200 dark:border-gray-700 transition-colors duration-200">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-10 w-10 bg-primary-100 dark:bg-primary-900/20 rounded-lg flex items-center justify-center">
                  <stat.icon className="h-5 w-5 text-primary-600 dark:text-primary-400" />
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">{stat.name}</p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-gray-100">{stat.value}</p>
                <p className="text-sm text-green-600 dark:text-green-400">{stat.change}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Quick Actions */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-soft border border-gray-200 dark:border-gray-700 transition-colors duration-200">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Quick Actions</h2>
            <p className="text-sm text-gray-500 dark:text-gray-400">Get started with these common tasks</p>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {quickActions.map((action) => (
                <a
                  key={action.name}
                  href={action.href}
                  className="group p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary-300 dark:hover:border-primary-600 hover:shadow-md transition-all duration-200"
                >
                  <div className="flex items-center space-x-3">
                    <div className="h-10 w-10 bg-primary-100 dark:bg-primary-900/20 rounded-lg flex items-center justify-center group-hover:bg-primary-200 dark:group-hover:bg-primary-900/30 transition-colors">
                      <action.icon className="h-5 w-5 text-primary-600 dark:text-primary-400" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100 group-hover:text-primary-700 dark:group-hover:text-primary-400">
                        {action.name}
                      </h3>
                      <p className="text-xs text-gray-500 dark:text-gray-400">{action.description}</p>
                    </div>
                    <ArrowRight className="h-4 w-4 text-gray-400 dark:text-gray-500 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors" />
                  </div>
                </a>
              ))}
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-soft border border-gray-200 dark:border-gray-700 transition-colors duration-200">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Recent Activity</h2>
            <p className="text-sm text-gray-500 dark:text-gray-400">Your latest wardrobe activities</p>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {recentActivities.map((activity) => (
                <div key={activity.id} className="flex items-center space-x-3">
                  <div className="h-2 w-2 bg-primary-600 dark:bg-primary-400 rounded-full"></div>
                  <div className="flex-1">
                    <p className="text-sm text-gray-900 dark:text-gray-100">
                      <span className="font-medium">{activity.action}</span> - {activity.item}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-4">
              <a
                href="/analytics"
                className="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium flex items-center"
              >
                View all activity
                <ArrowRight className="h-4 w-4 ml-1" />
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* AI Recommendations */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-soft border border-gray-200 dark:border-gray-700 transition-colors duration-200">
        <div className="p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center space-x-2">
            <Sparkles className="h-5 w-5 text-primary-600 dark:text-primary-400" />
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">AI Recommendations</h2>
          </div>
          <p className="text-sm text-gray-500 dark:text-gray-400">Personalized suggestions based on your style</p>
        </div>
        <div className="p-6">
          <div className="text-center py-8">
            <Sparkles className="h-12 w-12 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">No recommendations yet</h3>
            <p className="text-gray-500 dark:text-gray-400 mb-4">
              Upload more items to your wardrobe to get personalized AI recommendations
            </p>
            <a
              href="/wardrobe"
              className="btn btn-primary"
            >
              Add Items to Wardrobe
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
