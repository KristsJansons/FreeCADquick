# Mājas modelis FreeCAD + Claude (MCP)

Projekts mājas 3D modeļa un skiču izstrādei FreeCAD, kur Claude Code caur MCP
(Model Context Protocol) tieši vada FreeCAD — veido skices, sienas, jumtu utt.
balstoties uz kadastra datiem un fotogrāfijām.

## Uzstādīšana (Pop!_OS / Ubuntu)

### 1. Programmatūra

```bash
flatpak install flathub org.freecad.FreeCAD   # FreeCAD 3D CAD
flatpak install flathub org.qgis.qgis          # QGIS — precīziem ģeodatiem
curl -LsSf https://astral.sh/uv/install.sh | sh # uv/uvx — freecad-mcp palaišanai
sudo apt install gh inkscape                    # GitHub CLI + bitkaršu trasēšana
```

### 2. FreeCAD MCP serveris (neka-nat/freecad-mcp)

```bash
git clone https://github.com/neka-nat/freecad-mcp.git /tmp/freecad-mcp
```

Nokopē `addon/FreeCADMCP` uz FreeCAD Mod mapi. **Flatpak FreeCAD lieto smilškastes
ceļu**, nevis parasto `~/.local/share/FreeCAD/Mod` — precīzo ceļu apstiprini,
palaižot FreeCAD vienreiz un pārbaudot `FreeCAD.getUserAppDataDir()` Python
konsolē (View → Panels → Python console). Parasti tas būs kaut kas līdzīgs:

```bash
cp -r /tmp/freecad-mcp/addon/FreeCADMCP ~/.var/app/org.freecad.FreeCAD/data/FreeCAD/Mod/
```

Pēc kopēšanas: atver FreeCAD → Workbench izvēlnē izvēlies **MCP Addon** →
rīkjoslā spied **Start RPC Server**.

> **Svarīgi**: RPC serveris dzīvo FreeCAD GUI procesā. Tas jāpalaiž **katru
> reizi no jauna**, kad sāc darba sesiju ar Claude Code — Claude nevar
> pieslēgties FreeCAD, ja lietotne nav atvērta un serveris nav startēts.

### 3. Reģistrē MCP serveri Claude Code

```bash
claude mcp add freecad -- uvx freecad-mcp
```

Pārbaude: `claude mcp list` jārāda `freecad` kā "healthy" (ja FreeCAD ar RPC
serveri jau darbojas).

## Projekta struktūra

```
source-data/kadastrs/  — kadastra kartes, WMS/WFS eksporti, PDF, shapefile
source-data/photos/    — fasāžu, telpu, apkārtnes foto
gis/                    — QGIS projekti (.qgz) robežu apstrādei
freecad/                — FreeCAD dokumenti (.FCStd)
scripts/                — Python makro FreeCAD ģeometrijas ģenerēšanai
docs/workflow.md        — soli pa solim darba plūsma (skat. tur)
```

Skat. arī [`CLAUDE.md`](./CLAUDE.md) — instrukcijas Claude Code sesijām šajā
projektā, un [`docs/workflow.md`](./docs/workflow.md) — detalizēta darba plūsma.
