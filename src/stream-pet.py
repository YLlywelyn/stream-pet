import logging, tomllib, os

__settings_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "settings.toml")
__log_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "stream-pet.log")
__default_settings = """# Settings for Stream Pet

[api_settings]
client_id = "CLIENT_ID"
client_secret = "CLIENT_SECRET"
"""

def main():
	# Create the logger to log output
	logger = logging.getLogger("Stream Pet")
	
	# Set filename for logger
	logging.basicConfig(filename=__log_path,
						encoding="utf-8",
						level=logging.DEBUG, # TODO: change log level for production
						format='[%(asctime)s] %(levelname)s: %(message)s',
						datefmt='%Y-%m-%d %I:%M:%S')
	
	# Log startt of program
	logger.info("Stream Pet started.")
	
	# Load settings
	try:
		with open(__settings_path, "rb") as f:
			settings = tomllib.load(f)
	except FileNotFoundError:
		# Settings file not found, create it
		with open(__settings_path, "w") as f:
			f.write(__default_settings)
		os.chmod(__settings_path, 0o600)
		settings = tomllib.loads(__default_settings)
	
	# 

if __name__ == "__main__":
	main()