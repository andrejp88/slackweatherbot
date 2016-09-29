import pyowm
from slackclient import SlackClient as sc

print("This will overwrite the old config. Press Enter to configure, or Ctrl-C to cancel.")
input()

file = open('config.xml', 'w')

file.write("""<?xml version="1.0" encoding="UTF-8" ?>\n""")
file.write("""<config>\n""")

owm_token = input("Please enter the OWM token: ")
print("Trying the owm token...")
try:
    print("Opening the OWM client...")
    owm_client = pyowm.OWM(owm_token)
    print("Fetching observation...")
    observation = owm_client.weather_at_place('Vancouver,BC')
    print("Getting weather...")
    weather = observation.get_weather()

except:
    print("Could not confirm the OWM token. Please check it and try again.")
    exit(1)

print("OWM connection successful.")
file.write("""\t<owm-token>""" + owm_token + """</owm-token>\n""")

botname = input("\n\nPlease enter the bot's name: ")

slack_token = input("Please enter the slack token: ")
print("Trying the slack token...")
bot_id = None
try:
    print("Opening the slack client...")
    slack_client = sc(slack_token)
    print("Checking the api connection...")
    slack_client.api_call('api.test')
    print("Getting the bot id...")
    bot_id = slack_client.api_call('auth.test')['user_id']
except:
    print("Could not confirm the slack token. Please check it and try again.")
    exit(1)
print("Success.\n\n")
file.write("""\t<slack-token>""" + slack_token + """</slack-token>\n""")
file.write("""\t<slack-id>""" + bot_id + """</slack-id>\n""")

debug = eval(input("Would you like to use debug mode? Enter True or False. ").capitalize())
while type(debug).__name__ != 'bool':
    print("Response not recognized. Enter True or False.")
    debug = eval(input().capitalize())

print()
file.write("""\t<debug>""" + str(debug) + """</debug>\n""")
file.write("""</config>\n""")
file.close()

print("Configuration complete.")
