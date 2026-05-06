"use client";

interface PricingResultCardsProps {
  conservativeRate: number;
  recommendedRate: number;
  aggressiveRate: number;
  conservativeTotal: number;
  recommendedTotal: number;
  aggressiveTotal: number;
  nights: number;
}

export default function PricingResultCards({
  conservativeRate,
  recommendedRate,
  aggressiveRate,
  conservativeTotal,
  recommendedTotal,
  aggressiveTotal,
  nights,
}: PricingResultCardsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {/* Conservative Card */}
      <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-400">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Conservative</h3>
          <span className="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-1 rounded">
            -15%
          </span>
        </div>
        <div className="mb-4">
          <p className="text-2xl font-bold text-gray-900">
            ${conservativeRate.toFixed(2)}
          </p>
          <p className="text-sm text-gray-600">per night</p>
        </div>
        <div className="border-t pt-4">
          <p className="text-sm text-gray-600 mb-1">
            {nights} nights total:
          </p>
          <p className="text-xl font-semibold text-gray-900">
            ${conservativeTotal.toFixed(2)}
          </p>
        </div>
        <p className="text-xs text-gray-500 mt-4">
          Lower rates to attract more bookings. Good for building occupancy.
        </p>
      </div>

      {/* Recommended Card (Highlighted) */}
      <div className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg shadow-lg p-6 text-white ring-2 ring-blue-300 transform scale-105 relative z-10">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Recommended</h3>
          <span className="text-xs font-medium bg-white bg-opacity-20 px-2 py-1 rounded">
            Baseline
          </span>
        </div>
        <div className="mb-4">
          <p className="text-3xl font-bold">${recommendedRate.toFixed(2)}</p>
          <p className="text-sm opacity-90">per night</p>
        </div>
        <div className="border-t border-white border-opacity-30 pt-4">
          <p className="text-sm opacity-90 mb-1">{nights} nights total:</p>
          <p className="text-2xl font-semibold">${recommendedTotal.toFixed(2)}</p>
        </div>
        <p className="text-xs opacity-75 mt-4">
          Optimal balance between revenue and occupancy. Data-driven recommendation.
        </p>
      </div>

      {/* Aggressive Card */}
      <div className="bg-white rounded-lg shadow p-6 border-l-4 border-green-400">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Aggressive</h3>
          <span className="text-xs font-medium text-green-600 bg-green-50 px-2 py-1 rounded">
            +20%
          </span>
        </div>
        <div className="mb-4">
          <p className="text-2xl font-bold text-gray-900">
            ${aggressiveRate.toFixed(2)}
          </p>
          <p className="text-sm text-gray-600">per night</p>
        </div>
        <div className="border-t pt-4">
          <p className="text-sm text-gray-600 mb-1">
            {nights} nights total:
          </p>
          <p className="text-xl font-semibold text-gray-900">
            ${aggressiveTotal.toFixed(2)}
          </p>
        </div>
        <p className="text-xs text-gray-500 mt-4">
          Premium pricing for peak demand. Risk of lower occupancy.
        </p>
      </div>
    </div>
  );
}
