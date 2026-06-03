"use client";

import type { ReactNode } from "react";

type Props = {
  activeTab: string;
  children: ReactNode;
  onTabChange: (tab: string) => void;
};

const tabs = [
  ["recommend", "추천"],
  ["compare", "비교"],
  ["insights", "리뷰 분석"],
  ["experiments", "실험"],
  ["portfolio", "구성"]
];

export function AppShell({ activeTab, children, onTabChange }: Props) {
  return (
    <>
      <header className="top-nav">
        <strong>GlowFit AI</strong>
        <nav aria-label="주요 화면">
          {tabs.map(([id, label]) => (
            <button
              aria-current={activeTab === id ? "page" : undefined}
              className="nav-tab"
              key={id}
              onClick={() => onTabChange(id)}
              type="button"
            >
              {label}
            </button>
          ))}
        </nav>
      </header>
      {children}
    </>
  );
}
