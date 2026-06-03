import type { UserPreferences } from "../lib/types";

type Props = {
  preferences: UserPreferences;
  onGenerate: () => void;
  isLoading: boolean;
};

export function PreferenceForm({ preferences, onGenerate, isLoading }: Props) {
  return (
    <aside className="preference-panel">
      <h2>Beauty profile</h2>
      <div className="field-group">
        <span>Skin type</span>
        <strong>{preferences.skin_type}</strong>
      </div>
      <div className="field-group">
        <span>Concerns</span>
        <strong>{preferences.concerns.join(", ")}</strong>
      </div>
      <div className="field-group">
        <span>Texture</span>
        <strong>{preferences.texture}</strong>
      </div>
      <div className="field-group">
        <span>Fragrance sensitivity</span>
        <strong>{preferences.fragrance_sensitivity}</strong>
      </div>
      <button className="primary-button" onClick={onGenerate} disabled={isLoading}>
        {isLoading ? "Generating report" : "Generate report"}
      </button>
    </aside>
  );
}
