# Architecture Diagrams

Source files for HALO visual documentation.

## Files

- `architecture.mmd`: 4-Layer system overview in Mermaid.
- `dataflow.mmd`: Privacy-critical data flow sequence diagram.

## Rendering

Install Mermaid CLI:
```bash
npm install -g @mermaid-js/mermaid-cli
```

Render to SVG or PNG:
```bash
mmdc -i docs/diagrams/architecture.mmd -o docs/diagrams/architecture.svg
mmdc -i docs/diagrams/dataflow.mmd -o docs/diagrams/dataflow.svg
```

GitHub renders Mermaid natively in Markdown files using triple-backtick
mermaid fencing, so the source .mmd files are also referenced inline in
docs/architecture.md and docs/privacy.md.
