import inputimeout, qrcode, requests, websockets
import log
from settings import Settings

_scopes = " ".join(["channel:bot",
		  "user:write:chat",
		  "channel:read:ads"
])

def _GetInput(prompt: str, timeout: float) -> str:
	try:
		return inputimeout.inputimeout(prompt, timeout)
	except inputimeout.TimeoutOccurred:
		log.LogWarning("Input timed out, exiting...", True)

class Twitch:
	settings: Settings
	
	accessToken: str
	refreshToken: str
	token_type: str
	
	def __init__(self) -> None:
		self.settings = Settings.Load()
		self._GetToken()
	
	def _GetToken(self) -> None:
		response: dict
		status_code: int
		
		log.LogMessage("Getting token...")
		response, status_code = self._Post("https://id.twitch.tv/oauth2/device",
											{
												"client_id": self.settings.clientID,
												"scopes": _scopes
											})
		# display qr code for auth
		qr = qrcode.QRCode()
		qr.add_data(response["verification_uri"])
		qr.print_ascii()
		log.LogMessage("Waiting for auth...")
		
		# Wait for thirty seconds or api timeout, whichever is shorter
		_GetInput(f"Go to {response["verification_uri"]} and enter code [{response["user_code"]}], press <ENTER> when complete...",
				min(response["expires_in"], 30))
		
		response, status_code = self._Post("https://id.twitch.tv/oauth2/token",
											{
												"client_id": self.settings.clientID,
												"scopes": _scopes,
												"device_code": response["device_code"],
												"grant_type": "urn:ietf:params:oauth:grant-type:device_code"
											})
		
		if status_code != 200:
			log.LogError(f"Device authentication error: {response["message"]}", True)
		else:
			self.accessToken = response["access_token"]
			self.refreshToken = response["refresh_token"]
			self.token_type = response["token_type"]
	
	def _RefreshToken(self) -> None:
		response: dict
		status_code: int
		
		response, status_code = self._Post("https://id.twitch.tv/oauth2/token",
											{
												"client_id": self.settings.clientID,
												"client_secret": self.settings.clientSecret,
												"grant_type": "refresh_token",
												"refresh_token": self.refreshToken
											})
		if status_code != 200:
			log.LogError(f"An error occured while refreshing token: {response["message"]}", True)
		else:
			self.accessToken = response["access_token"]
			self.refreshToken = response["refresh_token"]
			self.token_type = response["token_type"]
	
	# Send POST data, return response JSON and HTTP status code
	def _Post(self, endpoint: str, data: dict) -> tuple(dict, int):
		try:
			response = requests.post(endpoint, data=data)
			return response.json(), response.status_code
		except requests.RequestsException as e:
			log.LogError(f"A connection error occured: {e}", True)
	
	# Establish websocket connection, then start event loop
	def RunEventLoop(self):
		pass
