from astropy.coordinates import EarthLocation,SkyCoord
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import AltAz
from astropy.coordinates import ICRS, Galactic, FK4, FK5, TETE

import sys

class Ansi_font_styles:
    color_black = '\u001b[30m'
    color_red = '\u001b[31m'
    color_green = '\u001b[32m'
    color_yellow = '\u001b[33m'
    color_blue = '\u001b[34m'
    color_magenta = '\u001b[35m'
    color_cyan = '\u001b[36m'
    color_white = '\u001b[37m'
    end = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'



if(len(sys.argv) != 6 or " ".join(sys.argv).lower().find("-h") != -1):
    print(
        "please call the script like this: 'python3 scriptname.py target_ra_deg target_dec_deg observation_time_ymd observation_time_hms'\n"+
        "example: 'python3 scriptname.py 206.88515734206297 49.31326672942533 2022-02-25 04:28:00'"
    )
    sys.exit(0)

target_ra_deg = sys.argv[1] # for example 206.88515734206297(alkaid)
target_dec_deg = sys.argv[2] # for example  (alkaid)
observation_time_ymd = sys.argv[3] # for example '2022-02-25'
observation_time_hms = sys.argv[4] # for example '04:28:00'
sky_object_name = sys.argv[5] # for example 'm31'

print(sys.argv)
# alkaid_ra_deg = 206.88515734206297
# alkaid_dec_deg = 49.31326672942533
# 13 47 32.43776 +49 18 47.7602
# alkaid_ra = '13h47m32.43776s'
# alkaid_dec = '49d18m47.7602s'

# target_ra_deg = alkaid_ra_deg # test
# target_dec_deg = alkaid_dec_deg  # test


gorgergrat_observatory_code      = 'K29'
# gorgergrat_observatory_latitude  = '45:59:00' #45.983361 NORD
gorgergrat_observatory_latitude  = '45.9844' #45.983361 NORD
# gorgergrat_observatory_longitude = '7:47:06' # 7.78361 EAST oder -7.78361 oder 352.21639 WEST
gorgergrat_observatory_longitude = '-7.7858' # 7.78361 EAST oder -7.78361 oder 352.21639 WEST
gorgergrat_observatory_altitude  = 3135

observing_location = EarthLocation(
    lat=gorgergrat_observatory_latitude,
    lon=gorgergrat_observatory_longitude,
    height=gorgergrat_observatory_altitude*u.m
    )

# sky_object = SkyCoord.from_name(sky_object_name, frame=TETE) #frame = An equatorial coordinate or frame using the True Equator and True Equinox (TETE).
sky_object = SkyCoord.from_name(sky_object_name) #frame = An equatorial coordinate or frame using the True Equator and True Equinox (TETE).


# observing_time = Time('2022-02-25 04:28:00') #test
# observing_time = Time('2022-02-25 23:19:00') #test
# observing_time_now = Time.now()

utcoffset = +1*u.hour  # Eastern Daylight Time
observing_time = Time(observation_time_ymd + " " + observation_time_hms) - utcoffset
observing_time = Time(observation_time_ymd + " " + observation_time_hms)

aa = AltAz(
    location=observing_location,
    # obstime=observing_time_now
    obstime=observing_time
    )

# coord = SkyCoord(
#     # ra=alkaid_ra, 
#     # dec=alkaid_dec
#     ra=float(target_ra_deg) * u.degree, 
#     dec=float(target_dec_deg) * u.degree
#     # unit="deg"
# )
    

# print(coord)
# print(aa)
# az_alt = coord.transform_to(aa)

# print('bf39fcaf-375e-4391-ac7c-31a90f5eb540-JSON:'+
#     f"""
#         {{
#             {Ansi_font_styles.color_cyan}"az"{Ansi_font_styles.end}: {az_alt.az.to_string()},  
#             {Ansi_font_styles.color_cyan}"az_deg"{Ansi_font_styles.end}: {az_alt.az.degree},
#             {Ansi_font_styles.color_cyan}"alt"{Ansi_font_styles.end}: {az_alt.alt.to_string()},  
#             {Ansi_font_styles.color_cyan}"alt_deg"{Ansi_font_styles.end}: {az_alt.alt.degree},  
#         }}
#     """
# )

sky_object_apparent = sky_object.transform_to(FK4(equinox='J2022.183'))

print(sky_object_apparent.ra.hms)
print(sky_object_apparent.dec)


az_alt = sky_object_apparent.transform_to(aa)

print('bf39fcaf-375e-4391-ac7c-31a90f5eb540-JSON:'+
    f"""
        {{
            {Ansi_font_styles.color_cyan}"az"{Ansi_font_styles.end}: {az_alt.az.to_string()},  
            {Ansi_font_styles.color_cyan}"az_deg"{Ansi_font_styles.end}: {az_alt.az.degree},
            {Ansi_font_styles.color_cyan}"alt"{Ansi_font_styles.end}: {az_alt.alt.to_string()},  
            {Ansi_font_styles.color_cyan}"alt_deg"{Ansi_font_styles.end}: {az_alt.alt.degree},  
        }}
    """
)

sky_object_apparent = sky_object.transform_to(FK5(equinox='J2022.183'))

print(sky_object_apparent.ra.hms)
print(sky_object_apparent.dec)


az_alt = sky_object_apparent.transform_to(aa)

print('bf39fcaf-375e-4391-ac7c-31a90f5eb540-JSON:'+
    f"""
        {{
            {Ansi_font_styles.color_cyan}"az"{Ansi_font_styles.end}: {az_alt.az.to_string()},  
            {Ansi_font_styles.color_cyan}"az_deg"{Ansi_font_styles.end}: {az_alt.az.degree},
            {Ansi_font_styles.color_cyan}"alt"{Ansi_font_styles.end}: {az_alt.alt.to_string()},  
            {Ansi_font_styles.color_cyan}"alt_deg"{Ansi_font_styles.end}: {az_alt.alt.degree},  
        }}
    """
)

sky_object_apparent = sky_object.transform_to(TETE)

print(sky_object_apparent.ra.hms)
print(sky_object_apparent.dec)


az_alt = sky_object_apparent.transform_to(aa)

print('bf39fcaf-375e-4391-ac7c-31a90f5eb540-JSON:'+
    f"""
        {{
            {Ansi_font_styles.color_cyan}"az"{Ansi_font_styles.end}: {az_alt.az.to_string()},  
            {Ansi_font_styles.color_cyan}"az_deg"{Ansi_font_styles.end}: {az_alt.az.degree},
            {Ansi_font_styles.color_cyan}"alt"{Ansi_font_styles.end}: {az_alt.alt.to_string()},  
            {Ansi_font_styles.color_cyan}"alt_deg"{Ansi_font_styles.end}: {az_alt.alt.degree},  
        }}
    """
)

coord = SkyCoord('9h57m43.72s', '69d34m23.3s')
print(coord.ra.degree)
print(coord.dec.degree)

az_alt = coord.transform_to(aa)

print('bf39fcaf-375e-4391-ac7c-31a90f5eb540-JSON:'+
    f"""
        {{
            {Ansi_font_styles.color_cyan}"az"{Ansi_font_styles.end}: {az_alt.az.to_string()},  
            {Ansi_font_styles.color_cyan}"az_deg"{Ansi_font_styles.end}: {az_alt.az.degree},
            {Ansi_font_styles.color_cyan}"alt"{Ansi_font_styles.end}: {az_alt.alt.to_string()},  
            {Ansi_font_styles.color_cyan}"alt_deg"{Ansi_font_styles.end}: {az_alt.alt.degree},  
        }}
    """
)
sys.exit()

# print(az_alt.az.degree)
# print(az_alt.az)


