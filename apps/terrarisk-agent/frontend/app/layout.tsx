import "./globals.css";
import type { Metadata } from "next";
import { Providers } from "../components/Providers";

export const metadata: Metadata = {
  title: "TerraRisk Agent (R&D)",
  description: "Personal passion R&D geospatial underwriting copilot."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
