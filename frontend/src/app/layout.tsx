import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "iTrip AI Command Center",
  description: "AI operations assistant for vacation rental property managers",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
