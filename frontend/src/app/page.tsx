export default function Home() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          iTrip AI Command Center
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Building your AI operations assistant...
        </p>
        <div className="bg-white rounded-lg shadow p-8 max-w-md">
          <p className="text-gray-700 mb-4">Frontend coming soon</p>
          <p className="text-sm text-gray-500">
            Backend API running on http://localhost:8000
          </p>
        </div>
      </div>
    </div>
  );
}
