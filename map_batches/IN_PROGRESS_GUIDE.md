# In Progress Hex Review Guide

Total hexes flagged as `In progress`: **382** across Map 2 (206) and Map 3 (176).

All other hexes (**9,768 hexes**) met the >95% confidence threshold and are marked `Verified`.

## Categories of In Progress Hexes & What Values to Check

### 1. Small Coastal Slivers & Islets (< 20% Land Coverage)
- **Why <95% Confidence**: Per TSWW rule UICFB.pdf p4, an individual land terrain type only defines the hex if it covers at least 20% of the whole hex. In these hexes, total land is under 20% (often 2% to 15%), meaning no individual land type confidently meets the threshold.
- **Values to Check in Map Editor**: Inspect the shoreline or islet. Decide whether the small island/land vertex should be typed as dominant land terrain (e.g. `Hills` or `Clear`) or classified as pure `Water` (`Lake/Sea`).

### 2. Coastal Boundary Near 20% Whole-Hex Threshold
- **Why <95% Confidence**: Sampled land pixels hover between 18% and 24% of the whole hex. Pixel anti-aliasing or coastline rendering creates borderline uncertainty.
- **Values to Check in Map Editor**: Verify whether the land feature exceeds 20% of the hex area to confirm `Mixed land/water` with the staged terrain type, or set to pure water.

### 3. Mixed Land Terrain (Close Proportions)
- **Why <95% Confidence**: Pure land hex where two terrain types are closely matched (e.g. Hills 45% vs Mountain 38%, or Clear 42% vs Woods 39%).
- **Values to Check in Map Editor**: Confirm the dominant terrain type (first listed in staged metadata).

## Sample Regional Listings

| Map | Region | Hex Key / Ref | Staged Surface | Staged Terrain | Confidence | Reason for Draft | Values to Check |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| Map 3 | FB-QH | `FB-QH:2451` | Mixed land/water | Hills | 0.90 | Small land sliver / islet: total land is 14.9%, no individual land type reaches 20% whole hex threshold. | Inspect shoreline/islet in Map Editor; determine whether feature warrants dominant land terrain or Lake/Sea. |
| Map 3 | FB-QH | `FB-QH:2551` | Mixed land/water | Hills | 0.90 | Small land sliver / islet: total land is 15.6%, no individual land type reaches 20% whole hex threshold. | Inspect shoreline/islet in Map Editor; determine whether feature warrants dominant land terrain or Lake/Sea. |
| Map 3 | FB-QH | `FB-QH:2651` | Mixed land/water | Mountain | 0.90 | Small land sliver / islet: total land is 16.2%, no individual land type reaches 20% whole hex threshold. | Inspect shoreline/islet in Map Editor; determine whether feature warrants dominant land terrain or Lake/Sea. |
| Map 3 | FB-QH | `FB-QH:2751` | Mixed land/water | Hills | 0.90 | Small land sliver / islet: total land is 11.7%, no individual land type reaches 20% whole hex threshold. | Inspect shoreline/islet in Map Editor; determine whether feature warrants dominant land terrain or Lake/Sea. |
| Map 3 | FB-QH | `FB-QH:2851` | Mixed land/water | Hills | 0.90 | Small land sliver / islet: total land is 3.4%, no individual land type reaches 20% whole hex threshold. | Inspect shoreline/islet in Map Editor; determine whether feature warrants dominant land terrain or Lake/Sea. |
| Map 3 | FB-RH | `FB-RH:0229` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-RH | `FB-RH:0129` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:3128` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-RH | `FB-RH:0127` | Land | Clear, Swamp | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-RH | `FB-RH:0227` | Mixed land/water | Clear, Swamp | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-RH | `FB-RH:0328` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-RH | `FB-RH:0327` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-RH | `FB-RH:0428` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-RH | `FB-RH:0329` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:3130` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:2630` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:2331` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:2431` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:2531` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:2831` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-RH | `FB-RH:0131` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:3036` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:3038` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:2938` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:2838` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:2638` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:2540` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:2341` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:2243` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:2244` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:2248` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:2249` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:2950` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:2349` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:2649` | Land | Mountain | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:2648` | Land | Mountain | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:3150` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-RH | `FB-RH:0149` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:3148` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |
| Map 3 | FB-QH | `FB-QH:3047` | Mixed land/water |  | 0.94 | Provisional coastal classification | Inspect terrain in Map Editor |

*Total remaining In progress hexes: 382. Full JSON audits are in `map_batches/map2_complete_20261103.json` and `map_batches/map3_complete_20261103.json`.*
