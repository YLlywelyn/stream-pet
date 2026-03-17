import os, tomllib
from command import Command
from log import LogErrorAndExit

settings_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "settings.toml")
default_settings: str = """# Settings for Stream Pet

client_id = "CLIENT_ID"
# client_secret = "CLIENT_SECRET"
channel_name = "CHANNEL_NAME"

[commands.test]
match = "!test"
command_type = "BASIC_MESSAGE"
message = "Hello from Stream Pet!"
"""

# Holds the app settings
class Settings:
	# The client ID for this app
	clientID: str
	
	# The client secret for this app
	clientSecret: str
	
	# The channel to connect to
	channelName: str
	
	# The commands for this instance
	commands: dict(Command)
	
	def __init__(self, clientID: str, clientSecret: str, channel_name: str, commands: dict(Command)):
		self.clientID = clientID
		self.clientSecret = clientSecret
		self.channel_name = channel_name
		self.commands = dict()
			
	# Load settings from a toml file at <filename>
	def Load() -> Settings:
		tomlSettings: dict
		try:
			with open(settings_path, "rb") as f:
				tomlSettings = tomllib.load(f)
		except FileNotFoundError:
			# Settings file not found.  Create it, log error and quit
			with open(settings_path, "w") as f:
				f.write(default_settings)
			os.chmod(settings_path, 0o600)
			LogErrorAndExit("Settings file not found, default written.")
		except tomllib.TOMLDecodeError as e:
			# Settings file malformed.  Log error and quit
			LogErrorAndExit(f"Settings file has malformed TOML: {e}")
		
		try:
			# Parse commands from file
			commands: dict(Command) = {}
			for key, data in tomlSettings["commands"].items():
				commands[key] = Command(data)
			
			# Create settings object
			settings: Settings = Settings(clientID = tomlSettings["client_id"],
										  clientSecret = tomlSettings["client_secret"],
										  channel_name = tomlSettings["channel_name"],
										  commands = commands)
		except Exception as e:
			LogErrorAndExit(f"Settings failed to load: {e}")
		
		return settings