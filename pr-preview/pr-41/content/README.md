# Editable content sources

Files in this directory are the **source of truth** for site data that
the Jekyll build consumes via `_data/*.yml`. Edit the markdown here; a
GitHub Action regenerates the YAML on push to `main` and the deploy
pipeline republishes the site.

Do **not** hand-edit the generated YAML — it will be overwritten.

---

## `table8.md` — EDA-Schema-V2 Table 8 benchmark dataset

Renders at `/eda-schema/`. Regenerator: `bin/content/regen_table8.py`.
Output: `_data/table8.yml`. Consumer: `_includes/table8.html`.

### File shape

YAML frontmatter (top-level constants) + one `## <metric> (<unit>)`
heading per metric block + a fenced ` ```tsv ` code block with the
data.

```
---
caption: "..."
pdks: [NG45, SKY130, IHP130, ASAP7]
groups:
  - "Floorplan → DR"
  - "Global place → DR"
  - "Detailed place → DR"
  - "CTS → DR"
  - "Global route → DR"
fp_note: "n/a — cells not yet placed"
gr_note: "no ± error (n_p = n_n = 0)"
---

## Total Area (µm²)
```tsv
stage	-	FP	FP	FP	FP	GP	GP	GP	GP	DP	DP	DP	DP	CTS	CTS	CTS	CTS	GR	GR	GR	GR
sub	type	NG45	SKY130	IHP130	ASAP7	NG45	SKY130	IHP130	ASAP7	NG45	SKY130	IHP130	ASAP7	NG45	SKY130	IHP130	ASAP7	NG45	SKY130	IHP130	ASAP7
MAE	full	1,781.97	18,567.03	48,738.62	225.06	...
```
```

### TSV grid rules

- **Always 22 columns**: `sub` + `type` + 20 stage/PDK values.
- Two header rows: first row is the stage label (`FP/GP/DP/CTS/GR`);
  second row is the PDK (`NG45/SKY130/IHP130/ASAP7`). These are
  validated literally — don't reorder.
- Cells that don't apply use a literal `-` placeholder. **Never leave
  trailing empties** — spreadsheets strip them when you copy/paste.

### Row types

| `type` | Meaning | Which cells must be `-` |
|---|---|---|
| `full` | 5 stage groups × 4 PDKs all present | none |
| `fp`   | Floorplan group merged into `fp_note` (cells not yet placed) | the 4 `FP` cols |
| `gr0`  | Global-route group merged into `gr_note`; row 1 of a 2-row pair | the 4 `GR` cols |
| `gr1`  | Global-route covered by the preceding `gr0`'s rowspan | the 4 `GR` cols |

A `gr0` row **must** be immediately followed by a `gr1` row in the
same block.

A block that uses `fp` for any row must use `fp` for **all** rows
(the merged Floorplan note spans the whole block).

### Sentinels

`>10000%` and `<-1` are real cell values (the paper thresholds unstable
metrics). Render as muted text. Just type them in the TSV cell as-is.

### Editing flow

1. Edit `content/table8.md` on a feature branch.
2. Open a PR. CI runs `python3 bin/content/regen_table8.py --check` and
   reports parse errors with the exact block + row + column that broke.
3. Merge. The `regen-table8` workflow regenerates `_data/table8.yml`
   and commits it directly to `main`. The deploy workflow then
   rebuilds the site from the new YAML.
4. The live site updates in ~3 minutes.

### Local regen

```bash
pip install pyyaml
python3 bin/content/regen_table8.py            # write _data/table8.yml
python3 bin/content/regen_table8.py --check    # validate, do not write
```

### Adding a row, block, or PDK

- **New row in an existing block**: add a line under the existing rows
  in that block's TSV. Choose the right `type`. Mind the column count.
- **New metric block**: add a new `## <metric> (<unit>)` heading and
  TSV block in the body. Keep the two header rows identical to the
  others.
- **New PDK column**: structural change — also add it to `pdks:` in
  the frontmatter, then every TSV block needs the new column position
  populated. Update `bin/content/regen_table8.py`'s
  `EXPECTED_HEADER_ROW1` and width constants.
- **New stage group**: similar — extend `groups:`, add the 4 new PDK
  columns to every TSV, update the regen script's constants.
