import "./globals.css";
import type { Metadata } from "next";
import { Masthead } from "@/components/Masthead";
import { Footer } from "@/components/Shell";

export const metadata: Metadata = {
  title: "Parla Mente",
  description: "Capire di cosa parlano davvero deputati e senatori, partendo dalle fonti ufficiali.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="it">
      <body>
        <Masthead />
        {children}
        <Footer />
      </body>
    </html>
  );
}
