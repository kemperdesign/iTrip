"use client";

import { useState } from "react";
import QuoteBuilderForm from "@/components/modules/QuoteBuilderForm";
import PricingResultCards from "@/components/modules/PricingResultCards";
import PriceBreakdown from "@/components/modules/PriceBreakdown";
import SeasonalIndicator from "@/components/modules/SeasonalIndicator";

interface QuoteData {
  quote_id: number;
  property_id: number;
  property_name: string;
  nights: number;
  guest_count: number;
  guest_type: string;
  base_adr: number;
  seasonal_multiplier: number;
  guest_type_factor: number;
  length_of_stay_factor: number;
  base_rate: number;
  cleaning_fee: number;
  service_fee: number;
  pet_fee: number;
  taxes: number;
  conservative_rate: number;
  recommended_rate: number;
  aggressive_rate: number;
  conservative_total: number;
  recommended_total: number;
  aggressive_total: number;
  reasoning: string;
  status: string;
  check_in_date: string;
  check_out_date: string;
}

export default function QuoteBuilder() {
  const [quote, setQuote] = useState<QuoteData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateQuote = async (formData: {
    propertyId: number;
    arrivalDate: string;
    departureDate: string;
    guestCount: number;
    guestType: string;
  }) => {
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch("http://localhost:8000/revenue-analysis/quotes/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          property_id: formData.propertyId,
          arrival_date: formData.arrivalDate,
          departure_date: formData.departureDate,
          guest_count: formData.guestCount,
          guest_type: formData.guestType,
          apply_seasonal: true,
          apply_fees: true,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to generate quote");
      }

      const data = await response.json();
      setQuote(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">Quote Builder</h1>
          <p className="text-muted-foreground">
            Generate data-driven pricing recommendations with seasonal adjustments
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Form Column */}
          <div className="lg:col-span-1">
            <div className="bg-card rounded-lg shadow-sm border border-border p-6 sticky top-4">
              <h2 className="text-lg font-semibold text-foreground mb-4">Generate Quote</h2>
              <QuoteBuilderForm
                onSubmit={handleGenerateQuote}
                loading={loading}
              />
              {error && (
                <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800 text-sm">
                  {error}
                </div>
              )}
            </div>
          </div>

          {/* Results Column */}
          <div className="lg:col-span-2">
            {quote ? (
              <div className="space-y-6">
                {/* Seasonal Indicator */}
                <SeasonalIndicator
                  checkInDate={quote.check_in_date}
                  seasonalMultiplier={quote.seasonal_multiplier}
                  guestType={quote.guest_type}
                  nights={quote.nights}
                />

                {/* Three-Tier Pricing Cards */}
                <PricingResultCards
                  conservativeRate={quote.conservative_rate}
                  recommendedRate={quote.recommended_rate}
                  aggressiveRate={quote.aggressive_rate}
                  conservativeTotal={quote.conservative_total}
                  recommendedTotal={quote.recommended_total}
                  aggressiveTotal={quote.aggressive_total}
                  nights={quote.nights}
                />

                {/* Price Breakdown */}
                <PriceBreakdown
                  baseAdr={quote.base_adr}
                  seasonalMultiplier={quote.seasonal_multiplier}
                  guestTypeFactor={quote.guest_type_factor}
                  lengthOfStayFactor={quote.length_of_stay_factor}
                  baseRate={quote.base_rate}
                  cleaningFee={quote.cleaning_fee}
                  serviceFee={quote.service_fee}
                  petFee={quote.pet_fee}
                  taxes={quote.taxes}
                  recommendedRate={quote.recommended_rate}
                  nights={quote.nights}
                />

                {/* Reasoning */}
                <div className="bg-card rounded-lg shadow-sm border border-border p-6">
                  <h3 className="text-lg font-semibold text-foreground mb-3">
                    AI Pricing Reasoning
                  </h3>
                  <p className="text-foreground whitespace-pre-wrap">
                    {quote.reasoning}
                  </p>
                </div>

                {/* Actions */}
                <div className="flex gap-3">
                  <button
                    onClick={() => {
                      // Copy quote to clipboard
                      const quoteText = `
Property: ${quote.property_name}
Dates: ${quote.check_in_date} to ${quote.check_out_date}
Nights: ${quote.nights}
Guest Count: ${quote.guest_count} (${quote.guest_type})

Conservative Rate: $${quote.conservative_rate}/night ($${quote.conservative_total} total)
Recommended Rate: $${quote.recommended_rate}/night ($${quote.recommended_total} total)
Aggressive Rate: $${quote.aggressive_rate}/night ($${quote.aggressive_total} total)

${quote.reasoning}
                      `;
                      navigator.clipboard.writeText(quoteText);
                      alert("Quote copied to clipboard!");
                    }}
                    className="flex-1 bg-primary hover:bg-primary/90 text-primary-foreground font-semibold py-2 px-4 rounded-lg transition"
                  >
                    Copy Quote
                  </button>
                  <button
                    onClick={() => {
                      // TODO: Implement send/save quote
                      alert("Save quote functionality coming soon");
                    }}
                    className="flex-1 bg-accent hover:bg-accent/90 text-accent-foreground font-semibold py-2 px-4 rounded-lg transition"
                  >
                    Save Quote
                  </button>
                </div>
              </div>
            ) : (
              <div className="bg-card rounded-lg shadow-sm border border-border p-12 text-center">
                <p className="text-muted-foreground">
                  Fill out the form to generate a pricing quote
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
