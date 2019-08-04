import json
import requests
from AdvancedHTMLParser import AdvancedHTMLParser
import re


LOCATION_URL = "https://sayt.wettercomassets.com/suggest/search/{}"
WEATHER_URL = "https://www.wetter.com/deutschland/{}.html"

plz = "85540"
r = requests.get(LOCATION_URL.format(plz))
res = json.loads(r.content)
first_suggestion = res["suggest"]["location"][0]["options"][0]["_source"]
name = first_suggestion["name"]
loc_id = first_suggestion["originId"]

r = requests.get(WEATHER_URL.format(loc_id))
dom = AdvancedHTMLParser()
dom.parseStr(r.content)
temperatures = dom.getElementsByClassName("hwg-col-temperature")
temperatures = sorted(temperatures, key=lambda x: int(x.attributes["data-num"]))
temperatures = list(map(lambda x: re.findall("\d+", x.innerText)[0], temperatures))
print(temperatures)

