import logging, os, sys

__logger: logging.Logger

__log_path: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), "stream-pet.log")

def __SetupLogger() -> None:
	global __logger
	
	# Setup logger
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
	
	__logger = logging.getLogger("StreamPet")

def LogMessage(message: str) -> None:
	__logger.info(message)

def LogError(message: str) -> None:
	__logger.error(message)

def LogErrorAndExit(message: str) -> None:
	__logger.error(message)
	sys.exit(1)

try:
	LOG_IMPORTED
except NameError:
	LOG_IMPORTED = True
	__SetupLogger()
	LogMessage("Logger setup.")
