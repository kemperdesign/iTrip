"use client";

interface SeasonalIndicatorProps {
  checkInDate: string;
  seasonalMultiplier: number;
  guestType: string;
  nights: number;
}

export default function SeasonalIndicator({
  checkInDate,
  seasonalMultiplier,
  guestType,
  nights,
}: SeasonalIndicatorProps) {
  // Parse the date
  const date = new Date(checkInDate);
  const month = date.getMonth() + 1;
  const dayOfWeek = date.getDay();
  const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;

  // Determine season
  let season = "Off-Season";
  let seasonColor = "gray";
  let seasonEmoji = "❄️";

  if (month >= 6 && month <= 8) {
    season = "Summer Peak";
    seasonColor = "amber";
    seasonEmoji = "☀️";
  } else if ((month >= 12 && month <= 12) || (month >= 1 && month <= 1)) {
    season = "Winter Peak";
    seasonColor = "red";
    seasonEmoji = "🎄";
  } else if ((month >= 3 && month <= 4) || (month >= 11 && month <= 11)) {
    season = "Spring Break";
    seasonColor = "blue";
    seasonEmoji = "🌸";
  } else if ((month >= 9 && month <= 10) || month === 5) {
    season = "Shoulder Season";
    seasonColor = "green";
    seasonEmoji = "🍂";
  }

  // Determine multiplier description
  const multiplierPercent = ((seasonalMultiplier - 1) * 100).toFixed(0);
  const multiplierDescription =
    seasonalMultiplier > 1.0
      ? `+${multiplierPercent}% Peak Season Markup`
      : multiplierPercent === "0"
      ? "Standard Rate"
      : `-${Math.abs(Number(multiplierPercent))}% Off-Season Discount`;

  const colorMap: Record<string, Record<string, string>> = {
    amber: {
      bg: "bg-amber-50",
      border: "border-amber-200",
      badge: "bg-amber-100 text-amber-800",
    },
    red: {
      bg: "bg-red-50",
      border: "border-red-200",
      badge: "bg-red-100 text-red-800",
    },
    blue: {
      bg: "bg-blue-50",
      border: "border-blue-200",
      badge: "bg-blue-100 text-blue-800",
    },
    green: {
      bg: "bg-green-50",
      border: "border-green-200",
      badge: "bg-green-100 text-green-800",
    },
    gray: {
      bg: "bg-gray-50",
      border: "border-gray-200",
      badge: "bg-gray-100 text-gray-800",
    },
  };

  const colors = colorMap[seasonColor] || colorMap.gray;

  return (
    <div className={`${colors.bg} border ${colors.border} rounded-lg p-6`}>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Season */}
        <div>
          <p className="text-sm text-gray-600 mb-1">Season</p>
          <div className="flex items-center gap-2">
            <span className="text-2xl">{seasonEmoji}</span>
            <p className={`font-semibold text-sm ${colors.badge.replace(/bg-/, "").replace(/text-/, "text-")}`}>
              {season}
            </p>
          </div>
        </div>

        {/* Seasonal Adjustment */}
        <div>
          <p className="text-sm text-gray-600 mb-1">Adjustment</p>
          <p className="text-lg font-bold text-gray-900">
            {seasonalMultiplier > 1.0 ? "+" : ""}
            {multiplierPercent}%
          </p>
          <p className="text-xs text-gray-600">{multiplierDescription}</p>
        </div>

        {/* Guest Type */}
        <div>
          <p className="text-sm text-gray-600 mb-1">Guest Type</p>
          <div className="flex items-center">
            <span className="text-lg font-semibold text-gray-900 capitalize">
              {guestType === "standard"
                ? "Standard"
                : guestType.charAt(0).toUpperCase() + guestType.slice(1)}
            </span>
          </div>
          <p className="text-xs text-gray-600">
            {guestType === "family"
              ? "Family +10%"
              : guestType === "group"
              ? "Group -10%"
              : guestType === "couple"
              ? "Couple Standard"
              : "Standard Rate"}
          </p>
        </div>

        {/* Stay Duration */}
        <div>
          <p className="text-sm text-gray-600 mb-1">Stay Duration</p>
          <p className="text-lg font-bold text-gray-900">{nights} nights</p>
          <p className="text-xs text-gray-600">
            {nights >= 28
              ? "Monthly (-20%)"
              : nights >= 7
              ? "Weekly (-5%)"
              : nights <= 3
              ? "Weekend (+5%)"
              : "Standard"}
          </p>
        </div>
      </div>

      {/* Holiday/Note Section */}
      {season === "Winter Peak" && (
        <div className="mt-4 pt-4 border-t border-red-200">
          <p className="text-xs font-semibold text-red-800 uppercase">
            🎅 Holiday Period
          </p>
          <p className="text-sm text-red-900 mt-1">
            This period includes major holidays with high demand. Consider premium pricing.
          </p>
        </div>
      )}

      {isWeekend && (
        <div className="mt-4 pt-4 border-t border-current border-opacity-20">
          <p className="text-xs font-semibold text-gray-700 uppercase">
            📅 Weekend Stay
          </p>
          <p className="text-sm text-gray-700 mt-1">
            Weekend bookings may justify slightly higher rates.
          </p>
        </div>
      )}
    </div>
  );
}
