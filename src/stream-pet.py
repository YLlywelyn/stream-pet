import asyncio, logging, os, requests, sys, tomllib
from twitchAPI.twitch import Twitch

from settings import Settings

logger: logging.Logger
log_path: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), "stream-pet.log")

settings: Settings
default_settings: str = """# Settings for Stream Pet
client_id = "CLIENT_ID"
client_secret = "CLIENT_SECRET"
channel_name = "YOUR_TWITCH_NAME
"""

def LogErrorAndExit(message: str) -> None:
	logger.error(message)
	sys.exit(1)

# Set up the logger
def SetupLogger() -> None:
	global logger
	
	# Setup logger
	logging.basicConfig(handlers=[
							logging.StreamHandler(sys.stdout),
							logging.FileHandler(log_path)
						],
						encoding="utf-8",
						level=logging.DEBUG, # TODO: change log level for production
						format='[%(asctime)s] %(levelname)s: %(message)s',
						datefmt='%Y-%m-%d %I:%M:%S')
	# Disable logging from the urllib3 library
	logging.getLogger("urllib3").setLevel(logging.ERROR)
	
	logger = logging.getLogger("StreamPet")

# Load settings from file
def LoadSettings() -> None:
	global settings
	
	try:
		with open(settings_path, "rb") as f:
			settings = tomllib.load(f)
	except FileNotFoundError:
		# Settings file not found.  Create it, log error and quit
		with open(settings_path, "w") as f:
			f.write(default_settings)
		os.chmod(settings_path, 0o600)
		LogErrorAndExit("Settings file not found, default written.")
	except tomllib.TOMLDecodeError as e:
		# Settings file malformed.  Log error and quit
		LogErrorAndExit(f"Settings file has malformed TOML: {e}")
	
	# Rough sanity check
	if type(settings) is not dict:
		LogErrorAndExit("Settings failed to load.")
	if "api_settings" not in settings:
		LogErrorAndExit("API settings missing from file.")
		
def ObtainAccessToken() -> None:
	# Obtain access token
	token_response: dict = requests.post("https://id.twitch.tv/oauth2/token",
		data={"client_id": settings["api_settings"]["client_id"],
		   "client_secret": settings["api_settings"]["client_secret"],
		   "grant_type": "client_credentials"}).json()
	# If no token recieved, exit
	if "access_token" not in token_response:
		LogErrorAndExit("No token recieved, check client_id and client_secret.")
	# Else, store token and continue
	else:
		settings["api_token"] = token_response

async def main() -> None:
	twitch: Twitch = await Twitch(settings["api_settings"]["client_id"],
								  settings["api_settings"]["client_secret"])
	users: list = []
	async for user in twitch.get_users(logins=["ylva_the_voiceless", "nachochoco"]):
		users.append({"id": user.id, "name": user.display_name, "description": user.description})
	print(users)

if __name__ == "__main__":
	SetupLogger()
	LoadSettings()
	
	asyncio.run(main())
