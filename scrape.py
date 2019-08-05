import json
import requests
from AdvancedHTMLParser import AdvancedHTMLParser
import re


LOCATION_URL = "https://sayt.wettercomassets.com/suggest/search/{}"
WEATHER_URL = "https://www.wetter.com/deutschland/{}.html"
WEATHER_TOMORROW_URL = "https://www.wetter.com/wetter_aktuell/wettervorhersage/morgen/deutschland/{}.html"

plz = "85540"
r = requests.get(LOCATION_URL.format(plz))
res = json.loads(r.content)
first_suggestion = res["suggest"]["location"][0]["options"][0]["_source"]
name = first_suggestion["name"]
loc_id = first_suggestion["originId"]
print("Result for {}".format(name))

r = requests.get(WEATHER_URL.format(loc_id))
dom = AdvancedHTMLParser()
dom.parseStr(r.content)
temperatures = dom.getElementsByClassName("hwg-col-temperature")
temperatures = sorted(temperatures, key=lambda x: int(x.attributes["data-num"]))
temperatures = list(map(lambda x: int(re.findall("\d+", x.innerText)[0]), temperatures))
print("Temperature forecast, hourly from now, °C")
print(temperatures)

rain = dom.getElementsByClassName("hwg-col-rain-text")
rain = sorted(rain, key=lambda x: int(x.attributes["data-num"]))
rain = list(map(lambda x: int(re.findall("\d+", x.innerText)[0]), rain))
print("Rain forecast, hourly from now, %")
print(rain)

wind = dom.getElementsByClassName("hwg-col-wind-text")
wind = sorted(wind, key=lambda x: int(x.attributes["data-num"]))
wind = list(map(lambda x: (re.findall("[NOSW]{1,2}", x.innerText)[0], int(re.findall("\d+", x.innerText)[0])), wind))
print("Wind forecast, hourly from now, Direction + speed km/h")
print(wind)

r = requests.get(WEATHER_TOMORROW_URL.format(loc_id))
dom = AdvancedHTMLParser()
dom.parseStr(r.content)
sun_hours = dom.getElementsByClassName("icon-sun_hours")[0].nextElementSibling
sun_hours = sun_hours.innerText
sun_hours = int(re.findall("\d+", sun_hours)[0])
print("Sun hours for the next day")
print(sun_hours)
