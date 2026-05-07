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
    <div className="w-64 bg-primary text-primary-foreground flex flex-col shadow-lg">
      {/* Logo/Header */}
      <div className="h-16 border-b border-primary/20 flex items-center px-6">
        <div className="flex items-center gap-2">
          <span className="text-2xl">🚀</span>
          <h1 className="text-lg font-bold">iTrip</h1>
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
                ? "bg-accent text-accent-foreground shadow-sm"
                : "text-primary-foreground hover:bg-primary/80"
            }`}
          >
            <span className="text-xl">{item.icon}</span>
            <span>{item.name}</span>
          </Link>
        ))}
      </nav>

      {/* Footer */}
      <div className="border-t border-primary/20 p-4 space-y-3">
        <div className="flex items-center gap-3 px-4 py-3 rounded-lg bg-primary/50">
          <span className="text-xl">👤</span>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">Staff User</p>
            <p className="text-xs text-primary-foreground/70 truncate">
              test@example.com
            </p>
          </div>
        </div>
        <button className="w-full px-4 py-2 text-sm font-medium text-primary bg-primary-foreground rounded-lg hover:bg-primary-foreground/90 transition">
          Logout
        </button>
      </div>
    </div>
  );
}
