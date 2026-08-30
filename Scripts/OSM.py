import json
import urllib.request
import Rhino.Geometry as rg
import math

# Initialize outputs
OfficeBreps = []
ResidentialBreps = []
PedestrianPaths = []
VehicularRoads = []
Status = "Waiting for RunOSM toggle."

def latlon_to_xy(lat, lon, center_lat, center_lon):
    """Converts Lat/Lon to local Cartesian XY in meters."""
    r = 6371000 # Earth radius in meters
    x = math.radians(lon - center_lon) * r * math.cos(math.radians(center_lat))
    y = math.radians(lat - center_lat) * r
    return rg.Point3d(x, y, 0)

if RunOSM:
    Status = "Querying Overpass API..."
    
    # Overpass QL query targeting buildings and roads
    query = f"""
    [out:json];
    (
      way["building"](around:{Radius},{Lat},{Lon});
      way["highway"](around:{Radius},{Lat},{Lon});
    );
    out body;
    >;
    out skel qt;
    """
    
    url = "http://overpass-api.de/api/interpreter"
    data = query.encode('utf-8')
    
    # Headers to satisfy API security rules and prevent 406 Error
    headers = {
        "User-Agent": "ThermoSynthesizeAI-Hackathon/1.0",
        "Accept": "application/json"
    }
    
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            osm_data = json.loads(response.read().decode('utf-8'))
            
            # Map node IDs to coordinates
            nodes = {node['id']: (node['lat'], node['lon']) for node in osm_data['elements'] if node['type'] == 'node'}
            
            for element in osm_data['elements']:
                if element['type'] == 'way' and 'nodes' in element:
                    pts = []
                    for nid in element['nodes']:
                        if nid in nodes:
                            n_lat, n_lon = nodes[nid]
                            pts.append(latlon_to_xy(n_lat, n_lon, Lat, Lon))
                    
                    if len(pts) < 2:
                        continue
                        
                    tags = element.get('tags', {})
                    
                    # Process Buildings
                    if 'building' in tags:
                        # Close the polygon loop if open
                        if pts[0].DistanceTo(pts[-1]) > 0.1:
                            pts.append(pts[0]) 
                        
                        curve = rg.PolylineCurve(pts)
                        
                        # Correct flipped Z-axis extrusions by checking curve orientation
                        if curve.ClosedCurveOrientation(rg.Plane.WorldXY) == rg.CurveOrientation.Clockwise:
                            curve.Reverse()
                        
                        # Extrude based on building levels (defaulting to 3 if tag is missing)
                        levels = float(tags.get('building:levels', 3))
                        height = levels * 3.5 
                        
                        extrusion = rg.Extrusion.Create(curve, height, True)
                        if extrusion:
                            brep = extrusion.ToBrep()
                            # Sort building typologies
                            if tags.get('building') in ['commercial', 'office', 'retail']:
                                OfficeBreps.append(brep)
                            else:
                                ResidentialBreps.append(brep)
                                
                    # Process Roads
                    elif 'highway' in tags:
                        curve = rg.PolylineCurve(pts)
                        # Sort road types for targeted material mitigation
                        if tags.get('highway') in ['pedestrian', 'footway', 'path', 'steps']:
                            PedestrianPaths.append(curve)
                        else:
                            VehicularRoads.append(curve)
                            
        Status = f"Success: Loaded {len(OfficeBreps)} office, {len(ResidentialBreps)} residential buildings, {len(PedestrianPaths)} paths, and {len(VehicularRoads)} roads."
    except Exception as e:
        Status = f"OSM Error: {str(e)}"