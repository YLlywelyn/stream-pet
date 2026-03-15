import logging, tomllib

__default_settings = """# Settings for Stream Pet

"""

def main():
	# Create the logger to log output
	logger = logging.getLogger("Stream Pet")
	
	# Set filename for logger
	logging.basicConfig(filename="stream-pet.log",
						encoding="utf-8",
						level=logging.DEBUG, # TODO: change log level for production
						format='[%(asctime)s] %(levelname)s: %(message)s',
						datefmt='%Y-%m-%d %I:%M:%S')
	
	logger.info("Stream Pet started.")
	
	try:
		with open("./settings.toml", "rb") as f:
			settings = tomllib.load(f)
	except FileNotFoundError:
		
		with open("./settings.toml", "w") as f:
			f.write(__default_settings)
		settings = tomllib.loads(__default_settings)
	
	print(f"{settings=}")

if __name__ == "__main__":
	main()