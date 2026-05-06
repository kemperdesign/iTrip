"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Sidebar() {
  const pathname = usePathname();

  const isActive = (href: string) => {
    return pathname === href || pathname.startsWith(href + "/");
  };

  const navItems = [
    {
      name: "Dashboard",
      href: "/",
      icon: "📊",
    },
    {
      name: "Quote Builder",
      href: "/quote-builder",
      icon: "💰",
    },
    {
      name: "Quote History",
      href: "/quotes",
      icon: "📋",
    },
    {
      name: "Property Brain",
      href: "/property-brain",
      icon: "🧠",
    },
    {
      name: "Guest Reply",
      href: "/guest-reply",
      icon: "💬",
    },
    {
      name: "Revenue Analysis",
      href: "/revenue-analysis",
      icon: "📈",
    },
    {
      name: "Imports",
      href: "/imports",
      icon: "📁",
    },
  ];

  return (
    <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
      {/* Logo/Header */}
      <div className="h-16 border-b border-gray-200 flex items-center px-6">
        <div className="flex items-center gap-2">
          <span className="text-2xl">🚀</span>
          <h1 className="text-lg font-bold text-gray-900">iTrip</h1>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto px-3 py-6 space-y-2">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition ${
              isActive(item.href)
                ? "bg-blue-100 text-blue-900"
                : "text-gray-700 hover:bg-gray-100"
            }`}
          >
            <span className="text-xl">{item.icon}</span>
            <span>{item.name}</span>
          </Link>
        ))}
      </nav>

      {/* Footer */}
      <div className="border-t border-gray-200 p-4">
        <div className="flex items-center gap-3 px-4 py-3 rounded-lg bg-gray-50">
          <span className="text-xl">👤</span>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">
              Staff User
            </p>
            <p className="text-xs text-gray-600 truncate">
              test@example.com
            </p>
          </div>
        </div>
        <button className="w-full mt-3 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition">
          Logout
        </button>
      </div>
    </div>
  );
}
