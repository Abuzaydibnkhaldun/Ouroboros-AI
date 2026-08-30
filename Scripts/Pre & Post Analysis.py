import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

# 1. Input Safety & Null Handling
safe_base_temp = BaseTemp if BaseTemp is not None else 35.0
safe_solar_ghi = SolarGHI if SolarGHI is not None else 850.0
safe_ped_area = PedestrianArea if PedestrianArea is not None else 450.0
safe_veh_area = VehicularArea if VehicularArea is not None else 800.0
safe_ped_density = PedestrianDensity if PedestrianDensity is not None else 1.5
safe_green_ratio = GreeneryRatio if GreeneryRatio is not None else 0.0
safe_paver_ratio = CoolPaverRatio if CoolPaverRatio is not None else 0.0

# 2. Extract Geometry Data (Separating Commercial vs. Residential)
total_tower_volume = 0.0
total_facade_area = 0.0
total_res_volume = 0.0

if TowerBreps:
    for brep in TowerBreps:
        if brep:
            total_tower_volume += brep.GetVolume()
            total_facade_area += brep.GetArea()

if ResidentialBreps:
    for brep in ResidentialBreps:
        if brep:
            total_res_volume += brep.GetVolume()

# 3. BASELINE CALCULATIONS (BEFORE)
# Commercial offices have high HVAC rejection (0.0001); Residential is much lower (0.00002)
raw_hvac = (total_tower_volume * 0.0001) + (total_res_volume * 0.00002)
# Replace the raw glare penalty calculation in Component B with this:
safe_glass_ratio = GlassRatio if GlassRatio is not None else 0.55

# Specular reflection is now dynamically driven by FortyGuard's actual facade vision data
raw_glare = (total_facade_area * safe_glass_ratio) * (safe_solar_ghi * 0.00002)
glare_penalty = min(raw_glare, 5.0)

hvac_penalty = min(raw_hvac, 6.0)
glare_penalty = min(raw_glare, 4.0)

BeforeTemp = safe_base_temp + hvac_penalty + glare_penalty
BeforePTSI = BeforeTemp * safe_ped_density

# 4. GENERATIVE INTERVENTIONS (AFTER)
safe_tree_dist = AvgTreeDist if AvgTreeDist is not None else 50.0

# SPATIAL INTELLIGENCE: Trees closer to hot glass towers multiply their cooling effect (Max 2x bonus)
spatial_multiplier = min(2.0, max(1.0, 30.0 / max(safe_tree_dist, 1.0)))

tree_cooling = (safe_green_ratio * 0.5) * 1.5 * spatial_multiplier       
shrub_cooling = (safe_green_ratio * 0.3) * 0.8      
groundcover_cooling = (safe_green_ratio * 0.2) * 0.5 
delta_t_green = tree_cooling + shrub_cooling + groundcover_cooling

total_hardscape = safe_ped_area + safe_veh_area
ped_weight = safe_ped_area / total_hardscape if total_hardscape > 0 else 0.5
veh_weight = safe_veh_area / total_hardscape if total_hardscape > 0 else 0.5

ped_material_cooling = (safe_paver_ratio * ped_weight) * 2.2 
veh_material_cooling = (safe_paver_ratio * veh_weight) * 1.1 
delta_t_materials = ped_material_cooling + veh_material_cooling

louver_mitigation = 0.0
if glare_penalty > 1.5 and safe_green_ratio > 0.4:
    louver_mitigation = glare_penalty * 0.7 

AfterTemp = BeforeTemp - (delta_t_green + delta_t_materials + louver_mitigation)
AfterPTSI = AfterTemp * safe_ped_density

# 5. EVOLUTIONARY FITNESS SCORE
w1, w2, w3, w4 = 0.4, 0.4, 0.1, 0.1
FitnessScore = (w1 * AfterTemp) + (w2 * AfterPTSI) - (w3 * (safe_green_ratio * 100)) + (w4 * (glare_penalty - louver_mitigation))

# 6. HUD OUTPUT METRICS
TempDelta = BeforeTemp - AfterTemp
PTSIDropPercent = ((BeforePTSI - AfterPTSI) / BeforePTSI) * 100 if BeforePTSI > 0 else 0.0
AsphaltRetrofitted = safe_ped_area * safe_paver_ratio

HUD_Text = "OUROBOROS: IMPACT REPORT\n"
HUD_Text += "----------------------------------\n"
HUD_Text += "Pre-Intervention Ambient: {:.2f} °C\n".format(BeforeTemp)
HUD_Text += "Post-Intervention Ambient: {:.2f} °C\n".format(AfterTemp)
HUD_Text += "Net Temperature Delta: -{:.2f} °C\n".format(TempDelta)
HUD_Text += "Pedestrian Thermal Stress Reduction: -{:.1f} %\n".format(PTSIDropPercent)
HUD_Text += "Total Pedestrian Asphalt Retrofitted: {:.0f} m²".format(AsphaltRetrofitted)