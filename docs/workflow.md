# Darba plūsma: no kadastra/foto uz FreeCAD mājas modeli

## Priekšnosacījums katrai sesijai

1. Atver FreeCAD (flatpak `org.freecad.FreeCAD`).
2. Workbench izvēlnē pārslēdzies uz **MCP Addon**.
3. Rīkjoslā spied **Start RPC Server**.
4. Sāc/turpini sarunu ar Claude Code šajā mapē — MCP serveris `freecad` jau
   reģistrēts (`.mcp.json`), Claude to redzēs automātiski.

## A ceļš — precīzi ģeotelpiskie dati

Izmanto, ja pieejami VZD/ĢeoLatvija WMS/WFS slāņi vai shapefile ar zemesgabala
robežu.

1. **QGIS** (`flatpak run org.qgis.qgis`): pievieno WFS/shapefile slāni,
   pārbaudi projekciju (LKS-92, EPSG:3059).
2. Saglabā/eksportē robežu kā DXF: Layer → Export → Save Features As → DXF.
   Failu liec `gis/` mapē (QGIS projektu) un DXF eksportu `source-data/kadastrs/`.
3. FreeCAD: Draft darbnīca → Import → izvēlies DXF failu. Ģeometrija ienāk ar
   reālām koordinātām (metros → FreeCAD tās interpretē kā mm, ja DXF vienības
   nav norādītas — pārbaudi mērogu pēc importa, salīdzinot ar zināmu attālumu).
4. Uz importētās robežas bāzes veido skici ēkas kontūrai, tad BIM Wall/Roof.

## B ceļš — attēli/foto bez ģeoatsauces

Izmanto skrīnšotiem, foto, roku zīmētiem plāniem.

1. Iedod Claude attēlu tieši (Claude to var analizēt vizuāli).
2. Nosaki vismaz vienu zināmu atskaites garumu attēlā (piem., norādīts mērogs
   kadastra kartē, standarta durvju platums ~80cm, vai lietotāja norādīts
   izmērs).
3. Ja kontūra sarežģīta (nelīdzenas sienas, izliekumi):
   - `inkscape source-data/photos/plans.png` → Path → Trace Bitmap (potrace) →
     eksportē kā SVG.
   - FreeCAD Draft → Import → izvēlies SVG. Rezultāts ienāk kā Draft wire.
   - Draft → Scale, lai pieskaņotu pret zināmo atskaites garumu.
4. Ja kontūra vienkārša (taisnas sienas, taisni stūri): Claude tieši ģenerē
   Python koordinātu sarakstu un caur MCP `execute_code` veido Sketcher skici
   ar dimensiju ierobežojumiem (constraints), nevis SVG starpsoli.
5. No skices — BIM Wall/Window/Door/Roof, tāpat kā A ceļā.

## Pārbaude ceļā

Pēc katra nozīmīga soļa — palūdz Claude `get_view`, lai pārbaudītu rezultātu
vizuāli, pirms turpini uz nākamo elementu (siena → logs → durvis → jumts).
