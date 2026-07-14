import { avoidOptions, concernOptions, demoProfiles, textureOptions } from "../lib/mock-data";
import { presentLabel } from "../lib/presentation";
import type { UserPreferences } from "../lib/types";

type Props = {
  preferences: UserPreferences;
  onChange: (preferences: UserPreferences) => void;
  onGenerate: () => void;
  onDemoSelect: (preferences: UserPreferences) => void;
  isLoading: boolean;
};

const skinTypes = ["dry", "oily", "combination", "sensitive"];
const fragranceLevels = ["low", "medium", "high"];

function toggleValue(values: string[], value: string) {
  return values.includes(value) ? values.filter((item) => item !== value) : [...values, value];
}

export function PreferenceForm({ preferences, onChange, onGenerate, onDemoSelect, isLoading }: Props) {
  const isReady = Boolean(
    preferences.skin_type &&
      preferences.texture &&
      preferences.fragrance_sensitivity &&
      preferences.concerns.length > 0
  );

  return (
    <aside aria-busy={isLoading} className="preference-panel">
      <div className="preference-scroll">
        <div className="panel-heading">
          <p className="eyebrow">프로필 입력</p>
          <h2>피부 조건</h2>
        </div>

        <section className="demo-profiles" aria-labelledby="demo-profiles-title">
          <div>
            <p className="eyebrow" id="demo-profiles-title">빠른 체험</p>
            <p>대표 프로필을 선택하면 바로 추천 결과를 확인할 수 있어요.</p>
          </div>
          <div className="demo-profile-list">
            {demoProfiles.map((profile) => (
              <button
                className="demo-profile-button"
                key={profile.title}
                onClick={() => onDemoSelect(profile.preferences)}
                type="button"
              >
                <strong>{profile.title}</strong>
                <span>{profile.description}</span>
              </button>
            ))}
          </div>
        </section>

        <label className="select-field">
          <span>피부 타입</span>
          <select
            value={preferences.skin_type}
            onChange={(event) => onChange({ ...preferences, skin_type: event.target.value })}
          >
            <option value="">선택</option>
            {skinTypes.map((type) => (
              <option key={type} value={type}>
                {presentLabel(type)}
              </option>
            ))}
          </select>
        </label>

        <label className="select-field">
          <span>선호 제형</span>
          <select
            value={preferences.texture}
            onChange={(event) => onChange({ ...preferences, texture: event.target.value })}
          >
            <option value="">선택</option>
            {textureOptions.map((texture) => (
              <option key={texture} value={texture}>
                {presentLabel(texture)}
              </option>
            ))}
          </select>
        </label>

        <label className="select-field">
          <span>향 민감도</span>
          <select
            value={preferences.fragrance_sensitivity}
            onChange={(event) => onChange({ ...preferences, fragrance_sensitivity: event.target.value })}
          >
            <option value="">선택</option>
            {fragranceLevels.map((level) => (
              <option key={level} value={level}>
                {presentLabel(level)}
              </option>
            ))}
          </select>
        </label>

        <label className="select-field">
          <span>예산 상한</span>
          <div className="range-row">
            <input
              max="40"
              min="15"
              type="range"
              value={preferences.budget_max_usd}
              onChange={(event) =>
                onChange({ ...preferences, budget_max_usd: Number(event.target.value) })
              }
            />
            <strong>${preferences.budget_max_usd}</strong>
          </div>
        </label>

        <div className="choice-group">
          <span>고민</span>
          <div className="choice-grid">
            {concernOptions.map((concern) => (
              <button
                aria-pressed={preferences.concerns.includes(concern)}
                className="choice-chip"
                key={concern}
                onClick={() =>
                  onChange({ ...preferences, concerns: toggleValue(preferences.concerns, concern) })
                }
                type="button"
              >
                {presentLabel(concern)}
              </button>
            ))}
          </div>
        </div>

        <div className="choice-group">
          <span>피하고 싶은 요소</span>
          <div className="choice-grid">
            {avoidOptions.map((avoid) => (
              <button
                aria-pressed={preferences.avoid.includes(avoid)}
                className="choice-chip"
                key={avoid}
                onClick={() => onChange({ ...preferences, avoid: toggleValue(preferences.avoid, avoid) })}
                type="button"
              >
                {presentLabel(avoid)}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="preference-action">
        <button
          aria-live="polite"
          className="primary-button"
          onClick={() => onGenerate()}
          disabled={isLoading || !isReady}
        >
          {isLoading ? "추천 계산 중" : "추천 받기"}
        </button>
      </div>
    </aside>
  );
}
