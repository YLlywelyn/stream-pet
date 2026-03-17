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

def LogMessage(message: str, exit: bool = False) -> None:
	__logger.info(message)
	if exit:
		sys.exit(1)

def LogWarning(message: str, exit: bool = False) -> None:
	__logger.warning(message)
	if exit:
		sys.exit(1)

def LogError(message: str, exit: bool = False) -> None:
	__logger.error(message)
	if exit:
		sys.exit(1)

try:
	LOG_IMPORTED
except NameError:
	LOG_IMPORTED = True
	__SetupLogger()
	LogMessage("Logger setup.")
