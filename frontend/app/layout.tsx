import "./globals.css";

export const metadata = {
  title: "GlowFit AI",
  description: "Explainable beauty recommendation reports"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
