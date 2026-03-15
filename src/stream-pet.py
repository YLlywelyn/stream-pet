import logging, tomllib, os, sys, requests

__settings_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "settings.toml")
__log_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "stream-pet.log")
__default_settings = """# Settings for Stream Pet

[api_settings]
client_id = "CLIENT_ID"
client_secret = "CLIENT_SECRET"
"""

def main():
	# Create the logger to log output
	logger = logging.getLogger("StreamPet")
	
	# Set filename for logger
	logging.basicConfig(handlers=[
							logging.StreamHandler(sys.stdout),
							logging.FileHandler(__log_path)
						],
						encoding="utf-8",
						level=logging.DEBUG, # TODO: change log level for production
						format='[%(asctime)s] %(levelname)s: %(message)s',
						datefmt='%Y-%m-%d %I:%M:%S')
	
	# Disable logging from the urllib3 library
	logging.getLogger("urllib3").setLevel(logging.ERROR)
	
	# Log startt of program
	logger.info("Stream Pet started.")
	
	# Load settings
	try:
		with open(__settings_path, "rb") as f:
			settings = tomllib.load(f)
	except FileNotFoundError:
		# Settings file not found, create it
		logger.warning("Settings file not found, default written.")
		with open(__settings_path, "w") as f:
			f.write(__default_settings)
		os.chmod(__settings_path, 0o600)
		settings = tomllib.loads(__default_settings)
	
	# Obtain access token
	token_response = requests.post("https://id.twitch.tv/oauth2/token",
		data={"client_id": settings["api_settings"]["client_id"],
		   "client_secret": settings["api_settings"]["client_secret"],
		   "grant_type": "client_credentials"}).json()
	# If no token recieved, exit
	if "access_token" not in token_response:
		logger.critical("No token recieved, check client_id and client_secret.")
		os._exit(1)
	# Else, store token and continue
	else:
		settings["api_settings"]["access_token"] = token_response["access_token"]

if __name__ == "__main__":
	main()