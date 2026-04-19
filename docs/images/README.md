# HALO Images

Rendered diagrams, screenshots, and visual assets. Source .mmd files live
in `docs/diagrams/`. PNG / SVG renders are generated on demand and are
not tracked in the repository unless they are finalized assets for
README, paper, or presentation use.

## Assets planned for Y1

- architecture.svg: 4-layer system overview (rendered from docs/diagrams/architecture.mmd)
- dataflow.svg: Privacy-preserving data flow (rendered from docs/diagrams/dataflow.mmd)
- soft_intervention_ui.png: Android Soft intervention screenshot (M3)
- pilot_setup.jpg: Pilot installation at 어르신복지관 (M4, with consent)

## Rendering commands

Install Mermaid CLI:
```bash
npm install -g @mermaid-js/mermaid-cli
```

Render all diagrams:
```bash
mmdc -i docs/diagrams/architecture.mmd -o docs/images/architecture.svg
mmdc -i docs/diagrams/dataflow.mmd -o docs/images/dataflow.svg
```
