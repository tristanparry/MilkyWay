# IMPORT STATEMENTS
import discord
from discord.ext import commands
from aiohttp import request
import random
import os

####################################################################################################

# INITIALIZE DISCORD BOT CLIENT + SET THE BOT PREFIX AS '<'
client = commands.Bot(command_prefix = '<')

####################################################################################################

# VARIABLE INITIALIZATIONS
TOKEN = os.getenv("MILKYWAY_TOKEN")
NASA_API_KEY = os.getenv("NASA_APIKEY")
NASA_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/NASA_logo.svg/200px-NASA_logo.svg.png"

####################################################################################################
# BOT EVENTS
@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game("Exploring the cosmos"))





@client.command()
async def status(context):
    await context.send("MilkyWay is **Online** - Developed by **Tristan Parry** (2021)")





@client.command()
async def apod(context):
    URL = ("https://api.nasa.gov/planetary/apod?api_key=" + NASA_API_KEY)

    async with request("GET", URL) as response:
        if response.status == 200:
            api_page = await response.json()
            api_description = api_page["title"] + " - *" + api_page["date"].replace('-', '/') + "*"
            api_image = api_page["url"]
        else:
            await context.send("")
    
    apod_embed = discord.Embed(title = "NASA Astronomy Picture of the Day (APOD)", description = api_description, colour = discord.Colour.blue())
    apod_embed.set_image(url = api_image)
    apod_embed.set_thumbnail(url = NASA_LOGO)
    await context.send(embed = apod_embed)





@client.command()
async def epic(context):
    URL = ("https://api.nasa.gov/EPIC/api/natural/images?api_key=" + NASA_API_KEY)

    async with request("GET", URL) as response:
        if response.status == 200:
            api_page = await response.json()
            random_number = random.randint(0, (len(api_page)-1))
            api_description = api_page[random_number]["caption"] + " - *" + api_page[random_number]["date"].replace('-', '/') + "*"
            api_image = "https://epic.gsfc.nasa.gov/epic-archive/jpg/" + api_page[random_number]["image"] + ".jpg"
            api_coordinates = "*Latitude:* " + str(api_page[random_number]["centroid_coordinates"]["lat"]) + "\n" + "*Longitude:* " + str(api_page[random_number]["centroid_coordinates"]["lon"])
        else:
            await context.send("")
    
    epic_embed = discord.Embed(title = "NASA Earth Polychromatic Imaging Camera (EPIC)", description = api_description, colour = discord.Colour.greyple())
    epic_embed.set_image(url = api_image)
    epic_embed.add_field(name = "Camera Coordinates", value = api_coordinates)
    epic_embed.set_thumbnail(url = NASA_LOGO)
    await context.send(embed = epic_embed)





@client.command()
async def insight(context):
    URL = ("https://api.nasa.gov/insight_weather/?api_key=" + NASA_API_KEY + "&feedtype=json&ver=1.0")

    async with request("GET", URL) as response:
        if response.status == 200:
            api_page = await response.json()
            sol = api_page["sol_keys"][0]
            api_time = "*First Time:* " + api_page[sol]["First_UTC"] + "\n" + "*Last Time:* " + api_page[sol]["Last_UTC"]
            api_season = "*Northern:* " + api_page[sol]["Northern_season"] + "\n" + "*Southern:* " + api_page[sol]["Southern_season"]
            api_pressure = "*Average:* " + str(api_page[sol]["PRE"]["av"]) + " Pa\n" + "*Minimum:* " + str(api_page[sol]["PRE"]["mn"]) + " Pa\n" + "*Maximum:* " + str(api_page[sol]["PRE"]["mx"]) + " Pa"
        else:
            await context.send("")
    
    insight_embed = discord.Embed(title = "NASA InSight: Mars Weather Service", description = "This data is from NASA's InSight Mars lander", colour = discord.Colour.orange())
    insight_embed.set_image(url = "https://wallpaperaccess.com/full/1608.jpg")
    insight_embed.add_field(name = "Sol", value = sol)
    insight_embed.add_field(name = "Time", value = api_time, inline = False)
    insight_embed.add_field(name = "Season", value = api_season, inline = False)
    insight_embed.add_field(name = "Atmospheric Pressure", value = api_pressure, inline = False)
    insight_embed.set_thumbnail(url = NASA_LOGO)
    await context.send(embed = insight_embed)





@client.command()
async def mars(context):
    URL = ("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos?api_key=" + NASA_API_KEY)

    async with request("GET", URL) as response:
        if response.status == 200:
            api_page = await response.json()
            random_number = random.randint(0, (len(api_page["latest_photos"])-1))
            api_rover = api_page["latest_photos"][random_number]["camera"]["rover_id"]
            api_camera = api_page["latest_photos"][random_number]["camera"]["full_name"]
            api_image = api_page["latest_photos"][random_number]["img_src"]
            api_date = "*" + api_page["latest_photos"][random_number]["earth_date"].replace('-', '/') + "*"
            api_status = api_page["latest_photos"][random_number]["rover"]["status"]
        else:
            await context.send("")
    
    mars_embed = discord.Embed(title = "NASA Mars Rover Photos", description = "This data is from NASA's Mars Rover Archives", colour = discord.Colour.orange())
    mars_embed.set_image(url = api_image)
    mars_embed.add_field(name = "Date", value = api_date)
    mars_embed.add_field(name = "Rover Camera", value = api_camera, inline = False)
    mars_embed.add_field(name = "Rover Id + Status", value = "Rover " + str(api_rover) + ", " + api_status, inline = False)
    mars_embed.set_thumbnail(url = NASA_LOGO)
    await context.send(embed = mars_embed)





@client.command()
async def astronauts(context):
    URL = ("http://api.open-notify.org/astros.json")

    async with request("GET", URL) as response:
        if response.status == 200:
            api_page = await response.json()
            api_number = "*" + str(api_page["number"]) + "* astronauts"
            api_names = ""
            for i in range(0, (len(api_page["people"]))):
                api_names += (api_page["people"][i]["name"] + ", ")
        else:
            await context.send("")
    
    astronauts_embed = discord.Embed(title = "Astronauts Currently in Space", description = "All ISS Astronauts currently in outer space", colour = discord.Colour.purple())
    astronauts_embed.add_field(name = "Total", value = api_number)
    astronauts_embed.add_field(name = "Names", value = api_names[0 : -2], inline = False)
    astronauts_embed.set_thumbnail(url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/ISS_emblem.png/1200px-ISS_emblem.png")
    await context.send(embed = astronauts_embed)





@client.command()
async def iss(context):
    URL = ("http://api.open-notify.org/iss-now.json")

    async with request("GET", URL) as response:
        if response.status == 200:
            api_page = await response.json()
            api_latitude = "*" + str(api_page["iss_position"]["latitude"]) + "*"
            api_longitude = "*" + str(api_page["iss_position"]["longitude"]) + "*"
        else:
            await context.send("")
    
    iss_embed = discord.Embed(title = "Current ISS Location", description = "Realtime location of the International Space Station", colour = discord.Colour.purple())
    iss_embed.set_image(url = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/International_Space_Station_after_undocking_of_STS-132.jpg/1200px-International_Space_Station_after_undocking_of_STS-132.jpg")
    iss_embed.add_field(name = "Latitude", value = api_latitude)
    iss_embed.add_field(name = "Longitude", value = api_longitude, inline = True)
    iss_embed.set_thumbnail(url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/ISS_emblem.png/1200px-ISS_emblem.png")
    await context.send(embed = iss_embed)





@client.command()
async def commands(context):    
    commands_embed = discord.Embed(title = "MilkyWay Commands", description = "List of updated commands for the MilkyWay bot", colour = discord.Colour.red())
    commands_embed.add_field(name = "<status", value = "Informs user if MilkyWay is online", inline = False)
    commands_embed.add_field(name = "<apod", value = "Returns NASA's Astronomy Picture of the Day (APOD)", inline = False)
    commands_embed.add_field(name = "<epic", value = "Returns current data from NASA's Earth Polychromatic Imaging Camera (EPIC)", inline = False)
    commands_embed.add_field(name = "<insight", value = "Returns current data from NASA's InSight: Mars Weather Service", inline = False)
    commands_embed.add_field(name = "<mars", value = "Returns a current mars rover photograph/metadata", inline = False)
    commands_embed.add_field(name = "<astronauts", value = "Returns the amount of astronauts currently in space, as well as their names", inline = False)
    commands_embed.add_field(name = "<iss", value = "Returns the current position of the International Space Station (latitude/longitude)", inline = False)
    commands_embed.add_field(name = "<commands", value = "Returns list of MilkyWay commands", inline = False)
    await context.send(embed = commands_embed)

####################################################################################################

# RUN BOT CLIENT FROM PREDETERMINED DISCORD TOKEN
client.run(TOKEN)