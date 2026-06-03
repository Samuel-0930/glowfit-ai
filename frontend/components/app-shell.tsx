export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <header className="top-nav">
        <strong>GlowFit AI</strong>
        <nav aria-label="Primary">
          <a href="#recommend">Recommend</a>
          <a href="#compare">Compare</a>
          <a href="#insights">Review Insights</a>
          <a href="#experiments">Experiments</a>
          <a href="#portfolio">Portfolio</a>
        </nav>
      </header>
      {children}
    </div>
  );
}
