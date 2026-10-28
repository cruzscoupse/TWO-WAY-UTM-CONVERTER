"""
Two-Way UTM Coordinate Converter
Project: Latitude/Longitude and UTM Coordinate Conversion
Datum: WGS 84

Features:
1. Geographic latitude/longitude to UTM easting/northing.
2. UTM easting/northing to geographic latitude/longitude.
3. Conversion from one UTM zone/hemisphere to another.

Install dependency:
    pip install pyproj
"""

from pyproj import CRS, Transformer


def get_utm_crs(zone, hemisphere):
    """Return the WGS 84 UTM CRS for a zone (1-60) and hemisphere (N/S)."""
    if not 1 <= zone <= 60:
        raise ValueError("UTM zone must be between 1 and 60.")

    hemisphere = hemisphere.strip().upper()
    if hemisphere not in ("N", "S"):
        raise ValueError("Hemisphere must be N or S.")

    epsg_code = (32600 if hemisphere == "N" else 32700) + zone
    return CRS.from_epsg(epsg_code)


def latlon_to_utm(latitude, longitude, zone=None):
    """Convert decimal-degree WGS 84 latitude/longitude to UTM."""
    if not -80 <= latitude <= 84:
        raise ValueError("Standard UTM is normally valid from 80°S to 84°N.")
    if not -180 <= longitude <= 180:
        raise ValueError("Longitude must be between -180 and 180 degrees.")

    if zone is None:
        zone = min(60, int((longitude + 180) // 6) + 1)

    hemisphere = "N" if latitude >= 0 else "S"
    utm_crs = get_utm_crs(zone, hemisphere)
    transformer = Transformer.from_crs(
        CRS.from_epsg(4326), utm_crs, always_xy=True
    )
    easting, northing = transformer.transform(longitude, latitude)
    return easting, northing, zone, hemisphere


def utm_to_latlon(easting, northing, zone, hemisphere):
    """Convert WGS 84 UTM coordinates to decimal-degree latitude/longitude."""
    if easting < 100000 or easting > 900000:
        raise ValueError("Easting is outside the usual UTM range (100,000-900,000 m).")
    if northing < 0 or northing > 10000000:
        raise ValueError("Northing must be between 0 and 10,000,000 m.")

    utm_crs = get_utm_crs(zone, hemisphere)
    transformer = Transformer.from_crs(
        utm_crs, CRS.from_epsg(4326), always_xy=True
    )
    longitude, latitude = transformer.transform(easting, northing)
    return latitude, longitude


def utm_to_utm(easting, northing, source_zone, source_hemi,
               target_zone, target_hemi):
    """Convert UTM coordinates to another UTM zone/hemisphere."""
    latitude, longitude = utm_to_latlon(
        easting, northing, source_zone, source_hemi
    )
    target_crs = get_utm_crs(target_zone, target_hemi)
    transformer = Transformer.from_crs(
        CRS.from_epsg(4326), target_crs, always_xy=True
    )
    new_easting, new_northing = transformer.transform(longitude, latitude)
    return new_easting, new_northing, latitude, longitude


def main():
    while True:
        print("\n===== TWO-WAY UTM COORDINATE CONVERTER =====")
        print("1. Latitude/Longitude to UTM")
        print("2. UTM to Latitude/Longitude")
        print("3. Convert UTM to another zone/hemisphere")
        print("4. Exit")
        choice = input("Choose 1, 2, 3, or 4: ").strip()

        try:
            if choice == "1":
                lat = float(input("Enter latitude in decimal degrees: "))
                lon = float(input("Enter longitude in decimal degrees: "))
                zone_text = input("Enter UTM zone (Enter for automatic): ").strip()
                zone = int(zone_text) if zone_text else None
                easting, northing, zone, hemisphere = latlon_to_utm(lat, lon, zone)
                print("\n--- UTM RESULT ---")
                print(f"UTM zone: {zone}{hemisphere}")
                print(f"Easting:  {easting:.3f} m")
                print(f"Northing: {northing:.3f} m")

            elif choice == "2":
                easting = float(input("Enter UTM easting (m): "))
                northing = float(input("Enter UTM northing (m): "))
                zone = int(input("Enter UTM zone (1-60): "))
                hemisphere = input("Enter hemisphere (N/S): ").strip().upper()
                lat, lon = utm_to_latlon(easting, northing, zone, hemisphere)
                print("\n--- GEOGRAPHIC RESULT ---")
                print(f"Latitude:  {lat:.8f} degrees")
                print(f"Longitude: {lon:.8f} degrees")

            elif choice == "3":
                easting = float(input("Enter source UTM easting (m): "))
                northing = float(input("Enter source UTM northing (m): "))
                source_zone = int(input("Enter source UTM zone: "))
                source_hemi = input("Enter source hemisphere (N/S): ").strip().upper()
                target_zone = int(input("Enter target UTM zone: "))
                target_hemi = input("Enter target hemisphere (N/S): ").strip().upper()
                new_e, new_n, lat, lon = utm_to_utm(
                    easting, northing, source_zone, source_hemi,
                    target_zone, target_hemi
                )
                print("\n--- CONVERTED UTM RESULT ---")
                print(f"Target UTM: Zone {target_zone}{target_hemi.upper()}")
                print(f"Easting:  {new_e:.3f} m")
                print(f"Northing: {new_n:.3f} m")
                print(f"Geographic latitude:  {lat:.8f} degrees")
                print(f"Geographic longitude: {lon:.8f} degrees")

            elif choice == "4":
                print("Thank you for using the converter.")
                break
            else:
                print("Invalid choice. Select 1, 2, 3, or 4.")

        except (ValueError, TypeError) as error:
            print("Input error:", error)


if __name__ == "__main__":
    main()
