"use client";

import { useState } from "react";

interface QuoteBuilderFormProps {
  onSubmit: (data: {
    propertyId: number;
    arrivalDate: string;
    departureDate: string;
    guestCount: number;
    guestType: string;
  }) => void;
  loading: boolean;
}

export default function QuoteBuilderForm({
  onSubmit,
  loading,
}: QuoteBuilderFormProps) {
  const [formData, setFormData] = useState({
    propertyId: 1,
    arrivalDate: "2026-06-15",
    departureDate: "2026-06-22",
    guestCount: 4,
    guestType: "family",
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]:
        name === "propertyId" || name === "guestCount"
          ? parseInt(value)
          : value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Property Selector */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Property
        </label>
        <select
          name="propertyId"
          value={formData.propertyId}
          onChange={handleChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value={1}>Test Property</option>
          <option value={2}>Property 2</option>
          <option value={3}>Property 3</option>
        </select>
      </div>

      {/* Check-in Date */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Check-in Date
        </label>
        <input
          type="date"
          name="arrivalDate"
          value={formData.arrivalDate}
          onChange={handleChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Check-out Date */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Check-out Date
        </label>
        <input
          type="date"
          name="departureDate"
          value={formData.departureDate}
          onChange={handleChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Guest Count */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Guest Count
        </label>
        <input
          type="number"
          name="guestCount"
          value={formData.guestCount}
          onChange={handleChange}
          min="1"
          max="20"
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Guest Type */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Guest Type
        </label>
        <select
          name="guestType"
          value={formData.guestType}
          onChange={handleChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="standard">Standard</option>
          <option value="family">Family</option>
          <option value="couple">Couple</option>
          <option value="group">Group</option>
        </select>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-lg transition"
      >
        {loading ? "Generating..." : "Generate Quote"}
      </button>
    </form>
  );
}
