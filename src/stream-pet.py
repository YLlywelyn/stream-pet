import log
from twitch import Twitch

twitch: Twitch

# Clears the screen.
def Clear() -> None:
	print("\x1b[H\x1b[2J")

def main() -> None:
	# Clear the screen

if __name__ == "__main__":
	Clear()
	
	log.LogMessage("Starting app...")
	
	twitch = Twitch()
	
	log.LogMessage("Starting main loop...")
	
	try:
		twitch.RunEventLoop()
	except KeyboardInterupt:
		log.LogMessage("CTRL-C pressed, terminating...")
