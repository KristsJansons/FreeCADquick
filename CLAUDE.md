# Instrukcijas Claude Code šim projektam

Šis ir mājas 3D modeļa/skiču projekts FreeCAD, kur tu (Claude Code) tieši vadi
FreeCAD caur MCP serveri `freecad` (reģistrēts `.mcp.json`, dzīvo
`uvx freecad-mcp`). Pirms MCP rīku lietošanas pārliecinies, ka lietotājs ir
atvēris FreeCAD (flatpak `org.freecad.FreeCAD`), pārslēdzies uz **MCP Addon**
darbnīcu un nospiedis **Start RPC Server** — bez tā MCP savienojums neizdosies.

## Vispārīgi principi

- **Mājas modelim izmanto BIM darbnīcu** (Wall, Door, Window, Roof, Floor
  objekti), nevis kailus `Part::Box` primitīvus — tas paliek parametrisks un
  vieglāk koriģējams pēc tam, kad lietotājs precizē izmērus.
- **Vienības**: FreeCAD iekšēji strādā milimetros (mm). Kadastra/GIS dati
  parasti ir metros (LKS-92, EPSG:3059) — pārrēķini pirms ģeometrijas
  veidošanas un komentē pārrēķina koeficientu koda vietā, kur tas nav acīmredzams.
- **Neuzminēt izmērus**: ja attēlā/datos nav skaidra atskaites garuma vai
  mēroga, pajautā lietotājam, nevis izdomā ciparu.

## Divi datu ceļi — izvēlies pēc tā, kas pieejams

### A) Precīzi ģeotelpiskie dati (WMS/WFS/shapefile no VZD/ĢeoLatvija)
1. Lietotājs (vai tu, ja QGIS pieejams headless) sagatavo DXF eksportu no QGIS
   ar zemesgabala robežu reālās koordinātēs (`gis/*.qgz` → DXF).
2. Importē DXF FreeCAD (Draft workbench importēšana) — koordinātas paliek reālas.
3. Uz robežas skices bāzes BIM darbnīcā veido ēkas kontūru/sienas/jumtu.

### B) Attēli/foto bez ģeoatsauces
1. Analizē attēlu tieši (tev ir vīzija) — atrodi zināmu atskaites izmēru
   (norādīts mērogs, durvju platums ~80cm, tipisks ķieģeļa izmērs u.tml.).
2. Sarežģītiem kontūriem: Inkscape (potrace) bitkarti → SVG, tad FreeCAD Draft
   "Import SVG" un mērogošana pret zināmo atskaiti.
3. Ģenerē koordinātu/izmēru sarakstu, izveido Sketcher ģeometriju ar dimensiju
   ierobežojumiem caur MCP `execute_code`.
4. No skices — BIM Wall/Window/Door/Roof.

## MCP rīku piezīmes (neka-nat/freecad-mcp)

- `create_document`, `create_object`, `edit_object`, `delete_object` —
  pamata objektu darbības.
- `execute_code` — patvaļīgs Python FreeCAD konsolē; izmanto sarežģītākai
  Sketcher/BIM ģeometrijai, kam nav tiešā rīka.
- `get_view` — atgriež ekrānuzņēmumu; **izmanto pēc katras nozīmīgas izmaiņas**,
  lai vizuāli pārbaudītu rezultātu, nevis paļautos tikai uz kodu.
- `get_objects` / `get_parts_list` — pašreizējā dokumenta/bibliotēkas stāvoklis.
- Ja darbojies ar daudz sīkām izmaiņām, apsver `--only-text-feedback`, lai
  taupītu tokenus (skat. servera dokumentāciju), bet noklusēti izmanto
  screenshot atgriezenisko saiti pārbaudei.

## Faili

- `freecad/maja.FCStd` — galvenais dokuments. Nesaglabā vairākas paralēlas
  versijas repo — izmanto git commit vēsturi izmaiņu izsekošanai.
- `scripts/` — atkārtoti lietojami makro (DXF import, BIM ģenerēšana no JSON).
- Lieli avota faili (TIFF, RAW foto) ir `.gitignore` — nekomitē tos bez
  pārrunāšanas ar lietotāju.
