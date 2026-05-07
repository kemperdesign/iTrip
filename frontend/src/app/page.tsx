export default function Home() {
  const statCards = [
    {
      label: "Active Properties",
      value: "12",
      icon: "🏠",
      change: "+2 this month",
    },
    {
      label: "Total Revenue (30d)",
      value: "$45,230",
      icon: "💰",
      change: "+12% from last month",
    },
    {
      label: "Avg Occupancy",
      value: "78%",
      icon: "📊",
      change: "+5% year-over-year",
    },
    {
      label: "Pending Quotes",
      value: "8",
      icon: "📋",
      change: "3 awaiting approval",
    },
  ];

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-foreground mb-2">
            Dashboard
          </h1>
          <p className="text-muted-foreground">
            Welcome to your AI Command Center
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {statCards.map((stat, index) => (
            <div
              key={index}
              className="bg-card rounded-lg shadow-sm border border-border p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">
                    {stat.label}
                  </p>
                  <p className="text-2xl font-bold text-foreground">
                    {stat.value}
                  </p>
                  <p className="text-xs text-muted-foreground mt-3">
                    {stat.change}
                  </p>
                </div>
                <span className="text-3xl">{stat.icon}</span>
              </div>
            </div>
          ))}
        </div>

        {/* Quick Actions */}
        <div className="bg-card rounded-lg shadow-sm border border-border p-6">
          <h2 className="text-lg font-semibold text-foreground mb-4">
            Quick Actions
          </h2>
          <div className="flex flex-wrap gap-3">
            <a
              href="/quote-builder"
              className="px-4 py-2 bg-accent text-accent-foreground rounded-lg hover:bg-accent/90 transition font-medium"
            >
              Create Quote
            </a>
            <a
              href="/quotes"
              className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition font-medium"
            >
              View Quote History
            </a>
            <a
              href="/quote-builder"
              className="px-4 py-2 border border-primary text-primary rounded-lg hover:bg-primary/5 transition font-medium"
            >
              Build New Quote
            </a>
            <a
              href="/login"
              className="px-4 py-2 border border-border text-foreground rounded-lg hover:bg-background transition font-medium"
            >
              Sign In Again
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
