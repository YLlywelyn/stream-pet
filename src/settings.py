from command import Command

# Holds the app settings
class Settings:
	# The client ID for this app
	clientID: str
	
	# The client secret for this app
	clientSecret: str
	
	# The commands for this instance
	commands: dict(Command)
	
	def __init__(self, clientID: str, clientSecret: str):
		self.clientID = clientID
		self.clientSecret = clientSecret
		self.commands = dict()
			
	# Load settings from a toml file at <filename>
	def LoadFromFile(filename: str) -> Settings:
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
		
		# Rough sanity check
		if type(tomlSettings) is not dict:
			LogErrorAndExit("Settings failed to load.")
		
		settings: Settings = Settings(clientID = tomlSettings["client_id"],
									  clientSecret = tomlSettings["client_secret"])
		
		return settings