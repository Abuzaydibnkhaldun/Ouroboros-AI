import json
import urllib.request

GlassRatio = 0.55 # Default fallback proxy
WallRatio = 0.45
VisionStatus = "Idle. Set 'RunVision' to True."

if RunVision:
    if not ApiKey:
        VisionStatus = "Warning: No API Key provided. Using default material ratios."
    else:
        try:
            base_url = "https://api.fortyguard.com/v1"
            headers = {"api-key": ApiKey, "Content-Type": "application/json"}
            
            # Payload for FortyGuard Satellite/Street View Segmentation
            vision_payload = {
                "latitude": float(Lat) if Lat else 40.7128,
                "longitude": float(Lon) if Lon else -74.0060,
                "analysis_type": "material_segmentation"
            }
            
            data = json.dumps(vision_payload).encode('utf-8')
            req = urllib.request.Request(f"{base_url}/satellite", data=data, headers=headers, method='POST')
            
            with urllib.request.urlopen(req, timeout=30) as resp:
                res_json = json.loads(resp.read().decode('utf-8'))
                result_data = res_json.get("data", {}).get("segmentation", {})
                
                # Extract quantified material ratios from FortyGuard's vision model
                GlassRatio = float(result_data.get("glass_ratio", 0.55))
                WallRatio = float(result_data.get("wall_ratio", 0.45))
                
                VisionStatus = "Success: FortyGuard vision segmentation loaded."
                
        except Exception as e:
            VisionStatus = f"Vision API Fallback Active: {str(e)}"