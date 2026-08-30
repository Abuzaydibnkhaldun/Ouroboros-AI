================================================================================
                                OUROBOROS AI
================================================================================
Generative Urban Microclimate Optimization Engine
Built for Rhino 8 & Grasshopper (CPython 3)
Powered by FortyGuard Enterprise API & OpenStreetMap

--------------------------------------------------------------------------------
1. EXECUTIVE SUMMARY & CORE VALUE PROPOSITION
--------------------------------------------------------------------------------
Current urban microclimate tools are either static 2D heat map viewers that show
what is hot without explaining why, or slow, physics-heavy simulation engines
that take hours to run. 

Ouroboros AI bridges FortyGuard's Large Temperature Models (LTMs) directly into 
an interactive, computational CAD environment inside Rhino/Grasshopper. By fusing 
baseline thermal data with OpenStreetMap (OSM) typologies, material reflectance 
matrices, and native ecological databases, the platform:

  • Diagnoses Root Causes: Pinpoints specular glare from glass facades, HVAC 
    anthropogenic heat rejection, and high-albedo ground absorption.
  • Generates Targeted Interventions: Recommends native flora, bio-swales, 
    and movement-weighted street coatings.
  • Optimizes Automatically: Uses closed-loop evolutionary solvers (Galapagos) 
    driven by spatial attractor logic to find the optimal spatial layout.
  • Quantifies Impact: Delivers a clear, validated "Before vs. After" 
    microclimate delta (ΔT°C and PTSI score drop %).

--------------------------------------------------------------------------------
2. SYSTEM ARCHITECTURE & DATA FLOW
--------------------------------------------------------------------------------
[ DATA INGESTION LAYER ]
  ├─ FortyGuard Enterprise API: POST /v1/env_params, POST /v1/satellite
  ├─ OpenStreetMap (OSM) / GIS: Building Footprints, Height, Road Hierarchy
  └─ Botanical & Material DB: Native Species Matrix, Albedo Coefficients

         │
         ▼

[ RHINO / GRASSHOPPER GENERATIVE ENGINE (PYTHON 3) ]
  1. Context Generation: Auto-extrude OSM footprints & classify building types.
  2. Baseline Diagnostics: Calculate PTSI, Facade Glare Rays, & HVAC Penalties.
  3. Generative Interventions: Multi-tiered greenery & movement-weighted pavers.
  4. Evolutionary Loop (Galapagos): Mutate genome -> Shift Attractor -> Converge.

         │
         ▼

[ "BEFORE & AFTER" HUD OUTPUT LAYER ]
  ├─ 3D Rhino Viewport Color-Coded Mesh (Pre-Intervention Red -> Post Green)
  └─ Real-time HUD Panel: Temp Delta (-Δ°C), PTSI Drop %, & Area Retrofitted

--------------------------------------------------------------------------------
3. FEATURE SPECIFICATION
--------------------------------------------------------------------------------
Feature 1: Location-Aware Native Greenery & Bio-Swale Generator
Identifies underutilized, high-heat ground zones and populates them with 
regionally accurate plant species across 3 canopy layers (Trees, Shrubs, 
Groundcover) while enforcing spatial exclusion rules on roads and footprints.

Feature 2: Movement-Weighted Surface & Material Retrofit Engine
Differentiates road surfaces based on human foot traffic versus vehicular 
traffic:
  • Pedestrian Paths (High PTSI): Replaces asphalt with high-albedo (0.65), 
    permeable cool pavers.
  • Vehicular Roads (Low PTSI): Applies high-durability solar-reflective 
    coatings (albedo 0.45).

Feature 3: Typology Profiling, Glare, & Anthropogenic Heat Load
Sources building footprints via OSM tags (office vs. residential) and applies 
energy rejection proxies. Calculates specular glare rays from high-rise glass 
facades and triggers automated shading louvers when reflection heat is severe.

Feature 4: Attractor-Driven Evolutionary Optimization (Galapagos)
Uses Grasshopper's Galapagos solver to iterate through spatial configurations.
Galapagos controls a 2D spatial attractor point that physically slides across 
the pedestrian network, "hunting" for the hot glass tower zones to cluster 
canopy placement where cooling impact is maximized.

Feature 5: Quantified "Before & After" Heads-Up Display (HUD)
A real-time viewport display panel providing instant feedback on baseline 
ambient temperatures, post-intervention microclimates, thermal stress drop %, 
and total retrofitted square meterage.

--------------------------------------------------------------------------------
4. REPOSITORY STRUCTURE
--------------------------------------------------------------------------------
  ├── ThermoSynthesize_AI_v1.0.gh   # Master Grasshopper canvas definition
  ├── Ouroboros_Sandbox.3dm          # Optional Rhino 8 sandbox setup file
  ├── scripts/
  │   ├── component_a_fortyguard.py # FortyGuard API connection & LTM fallback
  │   ├── component_b_engine.py     # Microclimate math, PTSI, & fitness engine
  │   ├── component_d_osm.py        # Overpass API parser & auto-extrusion
  │   └── component_e_vision.py     # Satellite vision material parser
  └── README.txt                    # Project documentation file

--------------------------------------------------------------------------------
5. QUICK START INSTRUCTIONS
--------------------------------------------------------------------------------
1. Open Rhino 8 and set document units to Meters.
2. Launch Grasshopper and open `ThermoSynthesize_AI_v1.0.gh`.
3. In Component D (OSM Ingestion), set your target latitude/longitude and toggle 
   `RunOSM` to True to build the 3D neighborhood context.
4. In Component A (FortyGuard API), paste your API Key and toggle `Run` to True.
5. Double-click the Galapagos component, navigate to the Solvers tab, and click 
   "Start Solver" to execute the spatial optimization loop.

================================================================================
                              END OF TRANSMISSION
================================================================================
