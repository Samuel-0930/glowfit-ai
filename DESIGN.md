# DESIGN.md

## Product Design Direction

This product is an explainable beauty commerce recommendation workspace. The first impression should feel like a premium shopping assistant that also reveals serious data science underneath. The UI should be calm, clean, and product-focused: a recommendation report is the main artifact, with model signals, review evidence, and analysis details available nearby without overwhelming the user.

Use a commerce-first visual language inspired by modern ecommerce platforms: white and warm off-white surfaces, restrained black typography, subtle mint and pistachio accents, precise controls, and product/report cards that feel useful rather than decorative. Avoid generic AI-dashboard aesthetics, heavy purple gradients, dark cyber themes, and oversized marketing sections.

The app has two visual modes:

1. Consumer report mode: approachable, polished, recommendation-centered.
2. Analysis mode: denser, more technical, showing review NLP, model comparisons, and evaluation results.

Both modes should share the same design system so the product feels coherent.

## Visual Theme

- Mood: premium, calm, intelligent, beauty-commerce, evidence-backed.
- Density: medium. Consumer pages should breathe; analysis pages can be denser.
- Surfaces: light by default, with warm off-white page backgrounds and white panels.
- Accent behavior: use mint/pistachio sparingly for selected states, positive matches, and recommendation highlights.
- Product imagery: use real or realistic product imagery when available. Product visuals should be inspectable, bright, and not overly cropped or blurred.
- AI presence: show AI through structured reports, evidence, and evidence-strength signals, not through decorative gradients or abstract blobs.

## Color Palette

Use this palette as the source of truth.

### Core

| Token | Hex | Role |
| --- | --- | --- |
| `canvas` | `#ffffff` | Main white surface |
| `canvas-warm` | `#fbfbf5` | Page background and quiet bands |
| `surface` | `#ffffff` | Cards, panels, inputs |
| `surface-soft` | `#f6f7f2` | Secondary panels, analysis bands |
| `ink` | `#111111` | Primary text |
| `ink-muted` | `#52525b` | Secondary text |
| `ink-subtle` | `#71717a` | Tertiary text |
| `hairline` | `#e4e4e7` | Borders and dividers |
| `hairline-strong` | `#d4d4d8` | Input borders, table dividers |

### Brand And Semantic

| Token | Hex | Role |
| --- | --- | --- |
| `brand-black` | `#000000` | Primary CTA, high-emphasis text |
| `brand-mint` | `#c1fbd4` | Recommendation highlight, selected match |
| `brand-pistachio` | `#d4f9e0` | Soft feature tint, positive evidence |
| `brand-sage` | `#99b3ad` | Secondary accent, subtle links |
| `beauty-rose` | `#f6c7d0` | Beauty category accent, gentle warnings |
| `beauty-lilac` | `#ddd6fe` | Rare comparison accent only |
| `success` | `#1f9d55` | Positive sentiment |
| `warning` | `#b7791f` | Caution, mixed fit |
| `danger` | `#c2410c` | Negative sentiment, avoid signals |
| `info` | `#2563eb` | Technical links and docs only |

### Usage Rules

- Keep the app mostly white, warm off-white, black, and gray.
- Mint and pistachio should highlight recommendation fit, not decorate the page.
- Do not use purple or blue gradients as the main visual identity.
- Use rose only for beauty-specific detail, caution, or category accents.
- Do not create a one-note green interface. Mint should be an accent, not the whole page.

## Typography

Use open-source, production-friendly fonts.

| Token | Family | Size | Weight | Line Height | Use |
| --- | --- | ---: | ---: | ---: | --- |
| `display` | Inter, Helvetica, Arial, sans-serif | 40px | 600 | 1.1 | Main page titles |
| `heading-xl` | Inter, Helvetica, Arial, sans-serif | 28px | 600 | 1.2 | Report title, major panels |
| `heading-lg` | Inter, Helvetica, Arial, sans-serif | 22px | 600 | 1.25 | Section headings |
| `heading-md` | Inter, Helvetica, Arial, sans-serif | 18px | 600 | 1.35 | Card titles |
| `body-lg` | Inter, Helvetica, Arial, sans-serif | 17px | 400 | 1.55 | Report summary |
| `body` | Inter, Helvetica, Arial, sans-serif | 15px | 400 | 1.5 | Default UI text |
| `body-sm` | Inter, Helvetica, Arial, sans-serif | 13px | 400 | 1.45 | Metadata, helper text |
| `caption` | Inter, Helvetica, Arial, sans-serif | 12px | 500 | 1.4 | Tags, table labels |
| `mono` | ui-monospace, SFMono-Regular, Menlo, monospace | 12px | 400 | 1.5 | Model ids, metrics, API values |

Typography rules:

- Letter spacing is `0` unless used for tiny all-caps labels, where `0.04em` is allowed.
- Do not scale font sizes with viewport width.
- Consumer-facing report copy should be readable and slightly warmer than raw dashboard text.
- Analysis metrics can use compact typography, but labels must remain legible.

## Layout Principles

### App Shell

Use a persistent top navigation with the product name, primary tabs, and a small status area. Primary tabs:

- Recommend
- Compare
- Review Insights
- Experiments
- Portfolio

The first screen should be the working product, not a landing page. Open directly to the recommendation report workspace.

### Report-First Workspace

Desktop layout:

- Left column: preference controls and saved profiles.
- Center column: recommendation report and Top 3 products.
- Right column: evidence panel with review quotes, sentiment/aspect tags, model signals, and evidence-strength indicators.

Recommended proportions:

- Left: 280-340px
- Center: flexible, min 520px
- Right: 320-380px

Mobile layout:

- Stack controls first, then report, then evidence.
- Evidence panel becomes a collapsible section or tab.
- Product comparison should become horizontally scrollable only for structured tables; avoid cramped multi-column cards.

### Analysis Pages

Analysis pages may use denser grids, tables, and charts. Keep them quiet and scannable. Avoid oversized hero headings, decorative cards, or marketing copy. These pages should feel like a practical model review workspace.

## Spacing And Shape

Use an 8px spacing system.

| Token | Value |
| --- | ---: |
| `xs` | 4px |
| `sm` | 8px |
| `md` | 12px |
| `lg` | 16px |
| `xl` | 24px |
| `2xl` | 32px |
| `3xl` | 48px |
| `section` | 64px |

Radius:

| Token | Value | Use |
| --- | ---: | --- |
| `xs` | 4px | Tiny tags, table controls |
| `sm` | 6px | Inputs, compact controls |
| `md` | 8px | Cards, panels, modals |
| `pill` | 9999px | Pills, segmented controls, badges |

Rules:

- Cards should use 8px radius or less.
- Do not put cards inside cards.
- Do not style full page sections as floating cards.
- Use borders and subtle surface differences before shadows.

## Component Rules

### Buttons

Primary button:

- Background: `brand-black`
- Text: white
- Radius: pill
- Use for the main recommendation action only.

Secondary button:

- Background: white
- Border: `hairline-strong`
- Text: `ink`
- Radius: 8px or pill depending on context.

Icon buttons:

- Use icon-only buttons for common actions such as refresh, compare, save, download, expand, and close.
- Add tooltips for unfamiliar icons.
- Prefer lucide icons if available.

### Inputs And Controls

Use familiar controls:

- Segmented controls for skin type, price range, and recommendation mode.
- Checkboxes or toggles for binary preferences.
- Sliders or steppers for numeric sensitivity such as fragrance tolerance or price.
- Menus for controlled option lists.
- Tabs for Recommend, Compare, Review Insights, Experiments, and Portfolio.

Inputs should be stable in width and height. Error and helper text must not shift nearby layout unexpectedly.

### Recommendation Report

The report is the hero artifact of the app. It should include:

- A short summary sentence.
- Top 3 recommended products.
- Fit score and evidence strength.
- Why it matches the user's preferences.
- Review evidence.
- Pros, cons, and cautions.
- Best-for and avoid-if segments.

The report should look polished but not like marketing copy. It must show enough evidence to feel grounded.

### Product Cards

Product cards should be compact and comparable.

Required elements:

- Product image or placeholder image block.
- Product name.
- Category.
- Fit score.
- Rating and review count.
- Key attributes.
- Primary reason for recommendation.

Avoid excessive decorative badges. Tags should describe useful attributes such as "light texture", "dry skin", "fragrance caution", or "high repurchase sentiment".

### Evidence Panel

The evidence panel should feel like a transparent model explanation layer.

Include:

- Retrieved review snippets.
- Aspect tags.
- Sentiment labels.
- Similarity or relevance score.
- Source product/review metadata.

Use a restrained, dense layout. Review snippets should be readable, not tiny.

### Product Comparison

Comparison should use tables or structured rows, not separate unrelated cards.

Compare:

- Fit score.
- Rating.
- Review volume.
- Positive aspects.
- Negative aspects.
- Skin-type fit.
- Price band.
- Model agreement.

### Analysis Tab

Show data science credibility without turning the app into a notebook.

Include:

- Dataset summary.
- EDA highlights.
- Baseline vs core vs advanced model comparison.
- Ranking metrics.
- Review NLP examples.
- Known limitations.

Model comparison should be presented as a clear progression:

- Baseline: popularity, average rating, simple content similarity.
- Core: content-based recommendation, review-average baseline, and hash-vector similarity baseline.
- Advanced: Two-Tower Retrieval using user preference embeddings and product/review embeddings.
- Explanation: retrieved review evidence plus LLM/RAG-generated report text.

Metrics can use monospace numerals. Charts should be clear and low-noise.

### Portfolio Tab

This tab exists for reviewers.

Include:

- Problem definition.
- Dataset.
- Modeling approach.
- Evaluation strategy.
- Architecture summary.
- GitHub and Notion links.
- Phase 2 roadmap.

The modeling approach section should make the portfolio story obvious: simple baselines first, stronger recommendation models second, Two-Tower Retrieval as the Phase 1 advanced model, and production MLOps as the Phase 2 extension.

Keep it concise. It should guide an interviewer through the project, not replace the README.

## Data Visualization

Charts should use restrained colors:

- Positive sentiment: green.
- Negative sentiment: orange/red.
- Neutral: gray.
- Model comparison: black, sage, mint, rose, muted gray.

Use direct labels where possible. Avoid rainbow palettes.

Preferred charts:

- Bar charts for model comparison.
- Horizontal bars for top review aspects.
- Small line charts for training/evaluation trends.
- Simple scatterplots for embedding/product clusters only when useful.

## Interaction States

Hover:

- Slight background tint or border darkening.
- No large scale transforms.

Selected:

- Mint or pistachio fill with clear border.
- Ensure selected state is accessible without color alone.

Loading:

- Skeletons for product cards and report sections.
- A concise loading message for recommendation generation.

Error:

- Plain-language message.
- Show retry action.
- For LLM/RAG failures, still show model-based recommendations and mark generated explanation as unavailable.

Empty:

- Provide a compact next action.
- Avoid long instructional panels.

## Accessibility

- Minimum body text contrast should meet WCAG AA.
- All interactive controls need keyboard focus states.
- Touch targets should be at least 40px high on mobile.
- Do not rely on color alone for sentiment or fit.
- Truncate only metadata; do not truncate critical recommendation explanations without an expand affordance.

## Responsive Behavior

Breakpoints:

- Mobile: under 768px.
- Tablet: 768px to 1023px.
- Desktop: 1024px and above.
- Wide desktop: 1440px and above.

Rules:

- On mobile, use stacked sections and sticky bottom action only for primary recommendation generation.
- On tablet, use two columns: controls/report and evidence below or beside.
- On desktop, use the three-column report workspace.
- Do not hide key evidence on mobile; collapse it behind a clear tab or disclosure.

## Do

- Make the recommendation report the main visual artifact.
- Keep evidence close to claims.
- Use commerce UI patterns: product cards, comparison tables, filters, tags, ratings.
- Keep analysis surfaces dense but calm.
- Use icons for tool actions.
- Keep spacing predictable and stable.
- Make the app feel finished enough for a portfolio review.

## Do Not

- Do not create a landing page as the first screen.
- Do not use decorative gradient blobs, orbs, or abstract AI backgrounds.
- Do not make the UI mostly purple, blue, beige, brown, or espresso.
- Do not bury the model/evidence details in a separate README-only experience.
- Do not place cards inside cards.
- Do not use giant hero type inside dashboard panels.
- Do not make recommendation explanations sound unsupported by the retrieved review evidence.

## Implementation Notes For Agents

When building the frontend:

- Start with the report-first desktop layout, then adapt down to mobile.
- Build real states: loading, empty, error, generated, comparison selected.
- Use stable dimensions for product cards, controls, metric rows, and evidence snippets.
- Use `DESIGN.md` as the visual source of truth, but keep project-specific usability above imitation of any external brand.
- The UI should look like a beauty commerce AI product, not a clone of any existing company.
