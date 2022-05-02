import datetime
from suntime import Sun, SunTimeException
from astral import LocationInfo
from astral.sun import sun
import json
from pytz import all_timezones

gorgergrat_observatory_latitude  = 45.983361 #45.983361 NORD
gorgergrat_observatory_longitude = 7.78361 # 7.78361 EAST oder -7.78361 WEST oder 352.21639 WEST

o_date = datetime.date(2022, 2,  24)

def suntime_example(): 
      # latitude = 51.21
      # longitude = 21.01



      sun = Sun(
            gorgergrat_observatory_latitude,
            gorgergrat_observatory_longitude
            )

      # # Get today's sunrise and sunset in UTC
      # today_sr = sun.get_sunrise_time()
      # today_ss = sun.get_sunset_time()
      # print('Today at Warsaw the sun raised at {} and get down at {} UTC'.
      #       format(today_sr.strftime('%H:%M'), today_ss.strftime('%H:%M')))

      # On a special date in your machine's local time zone
      
      abd_sr = sun.get_local_sunrise_time(o_date)
      abd_ss = sun.get_local_sunset_time(o_date)

      print(abd_sr)
      print(abd_ss)
      # # Error handling (no sunset or sunrise on given location)
      # latitude = 87.55
      # longitude = 0.1
      # sun = Sun(latitude, longitude)
      # try:
      #     abd_sr = sun.get_local_sunrise_time(abd)
      #     abd_ss = sun.get_local_sunset_time(abd)
      #     print('On {} at somewhere in the north the sun raised at {} and get down at {}.'.
      #           format(abd, abd_sr.strftime('%H:%M'), abd_ss.strftime('%H:%M')))
      # except SunTimeException as e:
      #     print("Error: {0}.".format(e))



def astral_example():

      # from docs https://astral.readthedocs.io/en/latest/package.html
      # solar_depression
      # The number of degrees the sun must be below the horizon for the dawn/dusk calculation.
      # Can either be set as a number of degrees below the horizon or as one of the following strings
      # String	Degrees
      # civil	6.0
      # nautical	12.0
      # astronomical	18.0
      o_dusk_degrees_by_name = {
            "civil": 6.0,
            "nautical": 12.0,
            "astronomical": 18.0
      }
      # print(all_timezones)
      # exit()
      # o_suntimes = {
      #       ""
      # }

      city = LocationInfo("Gornergrat", "Switzerland", "Europe/Zurich", gorgergrat_observatory_latitude, gorgergrat_observatory_longitude)
      # print((
      # f"Information for {city.name}/{city.region}\n"
      # f"Timezone: {city.timezone}\n"
      # f"Latitude: {city.latitude:.02f}; Longitude: {city.longitude:.02f}\n"
      # ))

      s_civil = sun(
            city.observer,
            date=o_date, 
            dawn_dusk_depression=o_dusk_degrees_by_name["civil"], 
            tzinfo="Europe/Zurich"
            )
      s_nautical = sun(
            city.observer,
            date=o_date, 
            dawn_dusk_depression=o_dusk_degrees_by_name["nautical"], 
            tzinfo="Europe/Zurich"
            )
      s_astronomical = sun(
            city.observer,
            date=o_date, 
            dawn_dusk_depression=o_dusk_degrees_by_name["astronomical"], 
            tzinfo="Europe/Zurich"
      )

      # print(s_civil["dawn"].timestamp())
      # print((
      # f"civil\n"
      # f"---\n"
      # f'Dawn:    {s_civil["dawn"]}\n'
      # f'Sunrise: {s_civil["sunrise"]}\n'
      # f'Noon:    {s_civil["noon"]}\n'
      # f'Sunset:  {s_civil["sunset"]}\n'
      # f'Dusk:    {s_civil["dusk"]}\n'
      # f"---\n"
      # f"nautical\n"
      # f"---\n"
      # f'Dawn:    {s_nautical["dawn"]}\n'
      # f'Sunrise: {s_nautical["sunrise"]}\n'
      # f'Noon:    {s_nautical["noon"]}\n'
      # f'Sunset:  {s_nautical["sunset"]}\n'
      # f'Dusk:    {s_nautical["dusk"]}\n'  
      # f"---\n"
      # f"astronomical\n"
      # f"---\n"
      # f'Dawn:    {s_astronomical["dawn"]}\n'
      # f'Sunrise: {s_astronomical["sunrise"]}\n'
      # f'Noon:    {s_astronomical["noon"]}\n'
      # f'Sunset:  {s_astronomical["sunset"]}\n'
      # f'Dusk:    {s_astronomical["dusk"]}\n'
      # f"---\n"
      # ))

      o_sun = {
            "location": city, 
            "dawn" : {
                  "dawn_is_before_sun_rises": "yes indeed", 
                  "civil": {
                        "unix_ts": s_astronomical["dawn"].timestamp(), 
                        "python_date": s_astronomical["dawn"], 
                  }, 
                  "nautical": {
                        "unix_ts": s_nautical["dawn"].timestamp(), 
                        "python_date": s_nautical["dawn"], 
                  }, 
                  "astronomical": {
                        "unix_ts": s_astronomical["dawn"].timestamp(), 
                        "python_date": s_astronomical["dawn"], 
                  }
            },
            "rise": {
                        "unix_ts": s_civil["sunrise"].timestamp(), 
                        "python_date": s_civil["sunrise"], 
            }, 
            "noon": {
                        "unix_ts": s_civil["noon"].timestamp(), 
                        "python_date": s_civil["noon"], 
            },
            "set": {
                        "unix_ts": s_civil["sunset"].timestamp(), 
                        "python_date": s_civil["sunset"], 
            }, 
            "dusk" : {
                  "dusk_is_before_sun_sets": "yes indeed", 
                  "civil": {
                        "unix_ts": s_astronomical["dusk"].timestamp(), 
                        "python_date": s_astronomical["dusk"], 
                  }, 
                  "nautical": {
                        "unix_ts": s_nautical["dusk"].timestamp(), 
                        "python_date": s_nautical["dusk"], 
                  }, 
                  "astronomical": {
                        "unix_ts": s_astronomical["dusk"].timestamp(), 
                        "python_date": s_astronomical["dusk"], 
                  }
            }
      }
      print("bf39fcaf-375e-4391-ac7c-31a90f5eb540-JSON:"+json.dumps(o_sun, indent=4, sort_keys=False, default=str))
      exit()



# suntime_example()
astral_example()