import re
from enum import Enum, auto
import log

class CommandTypes(Enum):
	BASIC_MESSAGE = auto()

class UserLevels(Enum):
	BROADCASTER = auto()
	MODERATOR = auto()
	USER = auto()

class Command:
	
	# The chat message to match
	# This is a compiled regex object
	match: re.Pattern
	
	# The type of command
	type: CommandTypes
	
	# The required user level
	userLevel: UserLevels
	
	# The message to respond with in chat
	message: str
	
	def __init__(self, name: str, command: dict) -> None:
		# Set command type
		try:
			self.commandType = CommandTypes[command["command_type"]]
		except KeyError:
			log.LogError(f"Invalid command type for {name}: {command["type"]}", True)
			
		# Set user level
		try:
			self.userLevel = UserLevels[command["user_level"]]
		except KeyError:
			log.LogError(f"Invalid user level for {name}: {command["user_level"]}", True)
		
		try:
			match self.commandType:
				# Parameters for BASIC_MESSAGE commands
				case CommandTypes.BASIC_MESSAGE:
					pass
				
				# Common parameters
				case _:
					self.match = re.compile(command["match"])
		except Exception as e:
			log.LogError(f"Error parsing command '{name}'': {e}", True)
	
	
