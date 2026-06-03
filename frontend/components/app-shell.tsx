type AppShellProps = {
  activeTab: string;
  children: React.ReactNode;
  onTabChange: (tab: string) => void;
};

const tabs = [
  { id: "recommend", label: "Recommend" },
  { id: "compare", label: "Compare" },
  { id: "insights", label: "Review Insights" },
  { id: "experiments", label: "Experiments" },
  { id: "portfolio", label: "Portfolio" }
];

export function AppShell({ activeTab, children, onTabChange }: AppShellProps) {
  return (
    <div>
      <header className="top-nav">
        <strong>GlowFit AI</strong>
        <nav aria-label="Primary">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              aria-current={activeTab === tab.id ? "page" : undefined}
              className="nav-tab"
              onClick={() => onTabChange(tab.id)}
              type="button"
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </header>
      {children}
    </div>
  );
}
