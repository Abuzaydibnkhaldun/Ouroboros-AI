import json
import time
import urllib.request
import urllib.error

# 1. Initialize Default Fallback Outputs
BaseTemp = 35.0  
SolarGHI = 850.0 
StatusLog = "Idle. Set 'Run' to True to execute."

def is_within_us(lat, lon):
    """Checks if coordinates fall within the contiguous US bounding box."""
    return (24.396308 <= lat <= 49.384358) and (-125.000000 <= lon <= -66.934570)

def http_post(url, headers, payload):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))

def http_get(url, headers):
    req = urllib.request.Request(url, headers=headers, method='GET')
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))

if Run:
    if not ApiKey:
        StatusLog = "Warning: No API Key provided. Outputting baseline proxy values."
    else:
        try:
            base_url = "https://api.fortyguard.com/v1"
            headers = {"api-key": ApiKey, "Content-Type": "application/json"}
            
            # Safely handle null coordinate inputs
            lat = float(CenterLat) if CenterLat is not None else 40.7128
            lon = float(CenterLon) if CenterLon is not None else -74.0060
            
            if not is_within_us(lat, lon):
                StatusLog = f"Coords ({lat}, {lon}) outside US bound. Using LTM Proxy Mode."
            else:
                StatusLog = "Connecting to FortyGuard Enterprise API..."
                
                # Fetch maximum of 3 parameters to ensure API Basic plan compliance
                env_payload = {
                    "latitude": lat,
                    "longitude": lon,
                    "temperature": 32.5,
                    "date_time": {
                        "start_date": DateStr if DateStr else "2024-01-20",
                        "start_time": TimeStr if TimeStr else "16:00",
                        "filter_type": 1
                    },
                    "analysis": ["heat_index_celsius", "apparent_temperature_celsius", "solar_irradiance"]
                }
                
                env_res = http_post(f"{base_url}/env_params", headers, env_payload)
                act_id = env_res["data"]["activity_id"]
                StatusLog = f"Task Submitted (ID: {act_id}). Polling engine..."

                # Asynchronous Bounded Polling Loop (Max 60 seconds)
                completed = False
                for _ in range(20):
                    time.sleep(3)
                    st_res = http_get(f"{base_url}/status/{act_id}", headers)
                    st_data = st_res.get("data", {})
                    st_val = st_data.get("status", "").lower()
                    
                    if st_val in ("completed", "succeeded"):
                        result = st_data.get("result", {})
                        locs = result.get("locations", [{}])[0]
                        params = locs.get("parameters", {})
                        
                        # Safely extract dynamic JSON paths
                        hi_list = params.get("heat_index_celsius", [35.0])
                        BaseTemp = float(hi_list[0]) if (hi_list and hi_list[0] is not None) else 35.0
                        
                        solar_data = locs.get("solar_irradiance", {}).get("clear_sky", {})
                        SolarGHI = float(solar_data.get("ghi", 850.0))
                        
                        completed = True
                        StatusLog = "Success: FortyGuard Live Data loaded."
                        break
                    elif st_val in ("failed", "error"):
                        StatusLog = f"Task {act_id} failed. Outputting baseline proxy values."
                        break
                        
                if not completed:
                    StatusLog = "Polling timeout. Outputting baseline proxy values."

        except Exception as e:
            StatusLog = f"API Execution Error: {str(e)}. Defaulting to proxy values."