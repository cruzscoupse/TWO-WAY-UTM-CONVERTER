from utm_converter import latlon_to_utm, utm_to_latlon

# Test the example 36 N, 30 E
easting, northing, zone, hemisphere = latlon_to_utm(36, 30)
assert zone == 36 and hemisphere == "N"
lat, lon = utm_to_latlon(easting, northing, zone, hemisphere)
assert abs(lat - 36) < 1e-7
assert abs(lon - 30) < 1e-7

print("All basic conversion tests passed.")
print(f"Easting: {easting:.3f} m")
print(f"Northing: {northing:.3f} m")
