# Map 3 Sector Review Details — 2026-10-30

New reviews: **359 Verified** / **63 In progress**. Total hexes in dataset: **6001** (was 5,754).

Backup: `mapping_backups\before-map3-sector-20261030-134630.zip`. Source: original `assets/maps/Map 03.FB.png` and `reference/UICFB.pdf` p4.

## Scope and Methodology

- **183 placeholder `Unknown` hexes** on Map 3 (regions `FB-QH` and `FB-RH`) were inspected and resolved.
- **247 pure open sea hexes** (>95% sea pixels, zero land, zero settlements/ports) were added to complete Arctic Ocean / White Sea navigation.
- All classifications strictly follow the TSWW Terrain Effects Chart ([UICFB.pdf p4](reference/charts/UICFB.pdf)): land types exceeding 20% are recorded; coastal hexes where land area is below 20% are staged as `In progress` with the standardized rationale `Small land area: no individual land type confidently exceeds 20% of whole hex`.
- All 41 existing ferry and track transport connections in `map_transport.json` on Map 3 were preserved byte-for-byte.

## Classification Summary

- **Water**: 283 hexes (pure open sea; terrain `['Lake/Sea']`, Verified).
- **Land**: 49 hexes (Hills, Clear, Mountain, Clear+Swamp; Verified).
- **Mixed land/water**: 90 hexes (35 Verified with dominant terrain, 63 In progress provisional slivers).

## Reviewed Hexes Detail

| Reference | Surface | Land Terrain | Status | Confidence | Issues / Reason |
| --- | --- | --- | --- | --- | --- |
| FB-QH:2150 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2350 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2450 | Mixed land/water | Hills | Verified | 0.98 |  |
| FB-QH:2550 | Land | Hills | Verified | 0.98 |  |
| FB-QH:2650 | Land | Mountain | Verified | 0.98 |  |
| FB-QH:2750 | Land | Hills | Verified | 0.98 |  |
| FB-QH:2850 | Land | Hills | Verified | 0.98 |  |
| FB-QH:2950 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:3050 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:3150 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2149 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2249 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2349 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2449 | Mixed land/water | Hills | Verified | 0.98 |  |
| FB-QH:2549 | Land | Hills | Verified | 0.98 |  |
| FB-QH:2649 | Land | Mountain | In progress | 0.94 | Near 20% threshold: Hills. Classification provisional. |
| FB-QH:2749 | Land | Hills | Verified | 0.98 |  |
| FB-QH:2849 | Mixed land/water | Hills | Verified | 0.98 |  |
| FB-QH:2949 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:3049 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2248 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2348 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2448 | Mixed land/water | Hills | Verified | 0.98 |  |
| FB-QH:2548 | Land | Hills | Verified | 0.98 |  |
| FB-QH:2648 | Land | Mountain | In progress | 0.94 | Near 20% threshold: Hills. Classification provisional. |
| FB-QH:2748 | Land | Hills | Verified | 0.98 |  |
| FB-QH:2848 | Mixed land/water | Hills | Verified | 0.98 |  |
| FB-QH:2948 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:3048 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:3148 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2247 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2347 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2447 | Mixed land/water | Hills | Verified | 0.98 |  |
| FB-QH:2547 | Land | Hills | Verified | 0.98 |  |
| FB-QH:2647 | Land | Mountain | Verified | 0.98 |  |
| FB-QH:2747 | Land | Hills | Verified | 0.98 |  |
| FB-QH:2847 | Mixed land/water | Hills | Verified | 0.98 |  |
| FB-QH:2947 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:3047 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2246 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2346 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2446 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2546 | Mixed land/water | Hills | Verified | 0.98 |  |
| FB-QH:2646 | Land | Mountain | Verified | 0.98 |  |
| FB-QH:2746 | Land | Mountain | Verified | 0.98 |  |
| FB-QH:2846 | Land | Hills | Verified | 0.98 |  |
| FB-QH:2946 | Mixed land/water | Hills | Verified | 0.98 |  |
| FB-QH:3046 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:3146 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2245 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2345 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2445 | Mixed land/water | Hills | Verified | 0.98 |  |
| FB-QH:2545 | Land | Hills | Verified | 0.98 |  |
| FB-QH:2645 | Land | Mountain | Verified | 0.98 |  |
| FB-QH:2745 | Land | Mountain | Verified | 0.98 |  |
| FB-QH:2845 | Land | Hills | Verified | 0.98 |  |
| FB-QH:2945 | Mixed land/water | Hills | Verified | 0.98 |  |
| FB-QH:3045 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2244 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2344 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2444 | Mixed land/water | Clear | Verified | 0.98 |  |
| FB-QH:2544 | Land | Hills | Verified | 0.98 |  |
| FB-QH:2644 | Land | Mountain | In progress | 0.94 | Near 20% threshold: Hills. Classification provisional. |
| FB-QH:2744 | Land | Mountain | In progress | 0.94 | Near 20% threshold: Clear. Classification provisional. |
| FB-QH:2844 | Land | Mountain | In progress | 0.94 | Near 20% threshold: Clear. Classification provisional. |
| FB-QH:2944 | Land | Hills | Verified | 0.98 |  |
| FB-QH:3044 | Mixed land/water | Clear | Verified | 0.98 |  |
| FB-QH:3144 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2043 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2243 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2343 | Mixed land/water | Clear | Verified | 0.98 |  |
| FB-QH:2443 | Land | Clear | Verified | 0.98 |  |
| FB-QH:2543 | Land | Hills | Verified | 0.98 |  |
| FB-QH:2643 | Land | Hills | Verified | 0.98 |  |
| FB-QH:2743 | Land | Mountain | Verified | 0.98 |  |
| FB-QH:2843 | Land | Mountain | Verified | 0.98 |  |
| FB-QH:2943 | Land | Clear | Verified | 0.98 |  |
| FB-QH:3043 | Mixed land/water | Clear | Verified | 0.98 |  |
| FB-QH:2142 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2342 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2442 | Mixed land/water | Clear | Verified | 0.98 |  |
| FB-QH:2542 | Land | Clear | Verified | 0.98 |  |
| FB-QH:2642 | Land | Hills | Verified | 0.98 |  |
| FB-QH:2742 | Mixed land/water | Hills | Verified | 0.98 |  |
| FB-QH:2842 | Land | Hills | Verified | 0.98 |  |
| FB-QH:2942 | Land | Hills | Verified | 0.98 |  |
| FB-QH:3042 | Land | Clear | Verified | 0.98 |  |
| FB-QH:3142 | Mixed land/water | Clear | Verified | 0.98 |  |
| FB-QH:1841 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2041 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2241 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2341 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2441 | Mixed land/water | Clear | Verified | 0.98 |  |
| FB-QH:2541 | Mixed land/water | Clear | In progress | 0.94 | Near 20% threshold: Clear. Classification provisional. |
| FB-QH:2641 | Mixed land/water | Hills | Verified | 0.98 |  |
| FB-QH:2741 | Mixed land/water | Hills | Verified | 0.98 |  |
| FB-QH:2841 | Land | Hills | Verified | 0.98 |  |
| FB-QH:2941 | Land | Clear | Verified | 0.98 |  |
| FB-QH:3041 | Land | Clear | Verified | 0.98 |  |
| FB-QH:2540 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2640 | Mixed land/water | Clear | Verified | 0.98 |  |
| FB-QH:2740 | Mixed land/water | Clear | In progress | 0.94 | Near 20% threshold: Swamp. Classification provisional. |
| FB-QH:2840 | Mixed land/water | Hills | In progress | 0.94 | Near 20% threshold: Hills. Classification provisional. |
| FB-QH:2940 | Mixed land/water | Hills | Verified | 0.98 |  |
| FB-QH:3040 | Land | Clear, Swamp | In progress | 0.94 | Near 20% threshold: Swamp. Classification provisional. |
| FB-QH:3140 | Land | Clear | In progress | 0.94 | Near 20% threshold: Swamp. Classification provisional. |
| FB-QH:2239 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2339 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2439 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2539 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2639 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2739 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2839 | Mixed land/water | Clear | Verified | 0.98 |  |
| FB-QH:2939 | Land | Clear | Verified | 0.98 |  |
| FB-QH:3039 | Land | Clear | Verified | 0.98 |  |
| FB-QH:2138 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2338 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2438 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2538 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2638 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2738 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2838 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2938 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex.; Near 20% threshold: Clear. Classification provisional. |
| FB-QH:3038 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2137 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2637 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2737 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2937 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:3037 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2136 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2336 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2436 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2536 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2736 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2836 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2936 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:3036 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2235 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2335 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2435 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2535 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2735 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2835 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2935 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2234 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2334 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2534 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2634 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:1833 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:1933 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2033 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2233 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2333 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2433 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2533 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2733 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2833 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2933 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:1932 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2032 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2132 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2332 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2432 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2532 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2932 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:3032 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:1831 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2031 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2131 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2331 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2431 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2531 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2631 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2731 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2831 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2931 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:3031 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:1930 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2030 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2130 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2330 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2430 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2530 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2630 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:2730 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2830 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2930 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:3030 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:3130 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-QH:1829 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:1929 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2029 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2729 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2829 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2929 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2228 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:3128 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex.; Near 20% threshold: Clear. Classification provisional. |
| FB-QH:1827 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:1927 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2027 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2727 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2827 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:1926 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2026 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2126 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2726 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2826 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:3126 | Mixed land/water | Clear | Verified | 0.98 |  |
| FB-QH:1825 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2025 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2125 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2625 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2725 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:3025 | Mixed land/water | Clear | Verified | 0.98 |  |
| FB-QH:1924 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2024 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2124 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2324 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2424 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2524 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2724 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:3124 | Land | Clear | Verified | 0.98 |  |
| FB-QH:2023 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2223 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2323 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2423 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2523 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2222 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2322 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2522 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-QH:2622 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0250 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0350 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0450 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0650 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0850 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0950 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1150 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1350 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1650 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0149 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-RH:0549 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0849 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0949 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1549 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0248 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0348 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0448 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0748 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0848 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0948 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1148 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1248 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1548 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1648 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:3048 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0147 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0247 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0347 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0447 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0647 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0747 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0847 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1047 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1147 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1247 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1547 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1647 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:3047 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0246 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0446 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1046 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1146 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1346 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1946 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0145 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0245 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0345 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0645 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0745 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0845 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1045 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1145 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1245 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1345 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1545 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1645 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1745 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0244 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0344 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0644 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0744 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0844 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0944 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1144 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1244 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1344 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1644 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1744 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1844 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0143 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-RH:0243 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-RH:0343 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-RH:0443 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-RH:0543 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0643 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0843 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1443 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1743 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1843 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0242 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-RH:0342 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-RH:0442 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0542 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-RH:0642 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0742 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0842 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0942 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1142 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1242 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1342 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1542 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1742 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1842 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:2042 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0141 | Land | Clear | Verified | 0.98 |  |
| FB-RH:0241 | Mixed land/water | Clear | Verified | 0.98 |  |
| FB-RH:0341 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-RH:0441 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0541 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-RH:0641 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0741 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0841 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1041 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1141 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1241 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1341 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1541 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1741 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1941 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:2041 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0240 | Land | Clear, Swamp | Verified | 0.98 |  |
| FB-RH:0340 | Land | Clear | Verified | 0.98 |  |
| FB-RH:0440 | Mixed land/water | Clear | Verified | 0.98 |  |
| FB-RH:0540 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex.; Near 20% threshold: Clear. Classification provisional. |
| FB-RH:0640 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-RH:1040 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1140 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1340 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1440 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1940 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:2040 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0139 | Mixed land/water | Clear | Verified | 0.98 |  |
| FB-RH:0239 | Mixed land/water | Clear | In progress | 0.94 | Near 20% threshold: Swamp. Classification provisional. |
| FB-RH:0339 | Mixed land/water | Clear | Verified | 0.98 |  |
| FB-RH:0439 | Mixed land/water | Clear | Verified | 0.98 |  |
| FB-RH:0539 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-RH:0639 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1039 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1139 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1239 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1339 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1939 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:2039 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:2139 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:2539 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:2639 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0438 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0638 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:2538 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:2638 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0836 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0936 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1035 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1135 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:1134 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0133 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0932 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0131 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-RH:0831 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0230 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0330 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0430 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0630 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0730 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0830 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-RH:0129 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-RH:0229 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex.; Near 20% threshold: Clear. Classification provisional. |
| FB-RH:0329 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-RH:0729 | Mixed land/water | Clear | Verified | 0.98 |  |
| FB-RH:0228 | Mixed land/water | Clear | Verified | 0.98 |  |
| FB-RH:0328 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex.; Near 20% threshold: Clear. Classification provisional. |
| FB-RH:0428 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-RH:0127 | Land | Clear, Swamp | In progress | 0.94 | Near 20% threshold: Swamp. Classification provisional. |
| FB-RH:0227 | Mixed land/water | Clear, Swamp | In progress | 0.94 | Near 20% threshold: Swamp. Classification provisional. |
| FB-RH:0327 | Mixed land/water | None | In progress | 0.94 | Small land area: no individual land type confidently exceeds 20% of whole hex. |
| FB-RH:0226 | Mixed land/water | Clear | Verified | 0.98 |  |
| FB-RH:0326 | Mixed land/water | Clear | Verified | 0.98 |  |
| FB-RH:0123 | Land | Clear | Verified | 0.98 |  |
| FB-SH:0547 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0146 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0246 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:1146 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0145 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0345 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0445 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0344 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0444 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0543 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0642 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0541 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0741 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0840 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0838 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0637 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0836 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0936 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0735 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0835 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0734 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0834 | Water | Lake/Sea | Verified | 0.98 |  |
| FB-SH:0733 | Water | Lake/Sea | Verified | 0.98 |  |
