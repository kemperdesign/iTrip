"use client";

interface PriceBreakdownProps {
  baseAdr: number;
  seasonalMultiplier: number;
  guestTypeFactor: number;
  lengthOfStayFactor: number;
  baseRate: number;
  cleaningFee: number;
  serviceFee: number;
  petFee: number;
  taxes: number;
  recommendedRate: number;
  nights: number;
}

export default function PriceBreakdown({
  baseAdr,
  seasonalMultiplier,
  guestTypeFactor,
  lengthOfStayFactor,
  baseRate,
  cleaningFee,
  serviceFee,
  petFee,
  taxes,
  recommendedRate,
  nights,
}: PriceBreakdownProps) {
  const subtotal = recommendedRate * nights;
  const total = subtotal + cleaningFee + serviceFee + petFee + taxes;

  const seasonalPercent = ((seasonalMultiplier - 1) * 100).toFixed(1);
  const guestPercent = ((guestTypeFactor - 1) * 100).toFixed(1);
  const stayPercent = ((lengthOfStayFactor - 1) * 100).toFixed(1);

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-6">
        Price Calculation Breakdown
      </h3>

      {/* Rate Multipliers Section */}
      <div className="mb-8">
        <h4 className="text-sm font-semibold text-gray-700 mb-4 uppercase tracking-wide">
          Rate Multipliers
        </h4>
        <div className="space-y-3 bg-gray-50 rounded-lg p-4">
          <div className="flex justify-between items-center">
            <div>
              <p className="text-sm font-medium text-gray-900">Base ADR</p>
              <p className="text-xs text-gray-600">Historical average daily rate</p>
            </div>
            <p className="text-lg font-semibold text-gray-900">
              ${baseAdr.toFixed(2)}
            </p>
          </div>

          <div className="flex justify-between items-center pt-3 border-t border-gray-200">
            <div>
              <p className="text-sm font-medium text-gray-900">
                Seasonal Adjustment
              </p>
              <p className="text-xs text-gray-600">Peak/off-season pricing</p>
            </div>
            <p className="text-lg font-semibold text-blue-600">
              {seasonalPercent > 0 ? "+" : ""}{seasonalPercent}%
            </p>
          </div>

          <div className="flex justify-between items-center pt-3 border-t border-gray-200">
            <div>
              <p className="text-sm font-medium text-gray-900">
                Guest Type Factor
              </p>
              <p className="text-xs text-gray-600">Family, couple, or group adjustment</p>
            </div>
            <p className="text-lg font-semibold text-blue-600">
              {guestPercent > 0 ? "+" : ""}{guestPercent}%
            </p>
          </div>

          <div className="flex justify-between items-center pt-3 border-t border-gray-200">
            <div>
              <p className="text-sm font-medium text-gray-900">
                Length of Stay
              </p>
              <p className="text-xs text-gray-600">Weekly/monthly discounts</p>
            </div>
            <p className="text-lg font-semibold text-blue-600">
              {lengthOfStayFactor > 0 ? "+" : ""}{stayPercent}%
            </p>
          </div>
        </div>
      </div>

      {/* Price Per Night Section */}
      <div className="mb-8">
        <h4 className="text-sm font-semibold text-gray-700 mb-4 uppercase tracking-wide">
          Per Night Pricing
        </h4>
        <div className="bg-blue-50 rounded-lg p-4 mb-4">
          <div className="flex justify-between items-center">
            <p className="text-gray-900 font-medium">Recommended Rate</p>
            <p className="text-2xl font-bold text-blue-600">
              ${recommendedRate.toFixed(2)}
            </p>
          </div>
          <p className="text-xs text-gray-600 mt-2">
            {nights} nights × ${recommendedRate.toFixed(2)} = ${subtotal.toFixed(2)}
          </p>
        </div>
      </div>

      {/* Fees Section */}
      <div className="mb-8">
        <h4 className="text-sm font-semibold text-gray-700 mb-4 uppercase tracking-wide">
          Additional Fees & Taxes
        </h4>
        <div className="space-y-2 bg-gray-50 rounded-lg p-4">
          {cleaningFee > 0 && (
            <div className="flex justify-between text-sm">
              <span className="text-gray-700">Cleaning Fee</span>
              <span className="font-medium text-gray-900">
                ${cleaningFee.toFixed(2)}
              </span>
            </div>
          )}
          {serviceFee > 0 && (
            <div className="flex justify-between text-sm">
              <span className="text-gray-700">Service Fee (10%)</span>
              <span className="font-medium text-gray-900">
                ${serviceFee.toFixed(2)}
              </span>
            </div>
          )}
          {petFee > 0 && (
            <div className="flex justify-between text-sm">
              <span className="text-gray-700">Pet Fee</span>
              <span className="font-medium text-gray-900">
                ${petFee.toFixed(2)}
              </span>
            </div>
          )}
          {taxes > 0 && (
            <div className="flex justify-between text-sm border-t border-gray-200 pt-2">
              <span className="text-gray-700">Taxes (10%)</span>
              <span className="font-medium text-gray-900">
                ${taxes.toFixed(2)}
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Total Section */}
      <div className="border-t-2 border-gray-200 pt-4">
        <div className="flex justify-between items-center">
          <p className="text-lg font-semibold text-gray-900">Total Revenue</p>
          <p className="text-2xl font-bold text-gray-900">
            ${total.toFixed(2)}
          </p>
        </div>
        <p className="text-xs text-gray-600 mt-2">
          For {nights} nights including all fees and taxes
        </p>
      </div>
    </div>
  );
}
