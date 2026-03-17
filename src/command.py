import re
from enum import Enum, auto
from log import LogErrorAndExit

class CommandTypes(Enum):
	BASIC_MESSAGE = auto()

class Command:
	
	# The chat message to match
	# This is a compiled regex object
	match: re.Pattern
	
	# The message to respond with in chat
	message: str
	
	def __init__(self: Command, command: dict) -> None:
		try:
			self.commandType = CommandTypes[command["command_type"]]
		except KeyError:
			LogErrorAndExit(f"Invalid command type: {command["type"]}")
		
		try:
			match self.commandType:
				# Parameters for BASIC_MESSAGE commands
				case CommandTypes.BASIC_MESSAGE:
					pass
				
				# Common parameters
				case _:
					self.match = re.compile(command["match"])
		except Exception as e:
			LogErrorAndExit(f"Error parsing command: {e}")
	
	
