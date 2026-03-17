import asyncio, qrcode, requests

from log import LogMessage, LogError, LogErrorAndExit
from settings import Settings

def Clear() -> None:
	print("\x1b[H\x1b[2J")

settings: Settings

def ObtainAuthToken() -> dict:
	tokens = {}
	scopes = ["channel:bot",
			  "user:write:chat",
			  "channel:read:ads"
	]
	scopeString = " ".join(scopes)
	LogMessage(f"Scopes: {scopeString}")
	
	device_code_response: dict = requests.post("https://id.twitch.tv/oauth2/device",
		data={"client_id": settings.clientID,
			  "scopes": scopeString
		}).json()
	
	# display qr code for auth
	qr = qrcode.QRCode()
	qr.add_data(device_code_response["verification_uri"])
	qr.print_ascii()
	LogMessage("Waiting for auth.")
	input(f"Go to {device_code_response["verification_uri"]} and enter code [{device_code_response["user_code"]}], press <ENTER> when complete...")
	LogMessage("Checking with server...")
	
	token_response: dict = requests.post("https://id.twitch.tv/oauth2/token",
		data={"client_id": settings.clientID,
			  "scopes": "%20".join(scopes),
			  "device_code": device_code_response["device_code"],
			  "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
		}).json()
	
	# If we have a status code, something went wrong...
	if "status" in token_response:
		LogErrorAndExit(f"Device authentication error: {token_response["message"]}")
	# Else, success!
	else:
		tokens["access_token"] = token_response["access_token"]
		tokens["expires_in"] = token_response["expires_in"]
		tokens["refresh_token"] = token_response["refresh_token"]
		tokens["scope"] = token_response["scope"]
		tokens["token_type"] = token_response["token_type"]
	
	return tokens

async def main() -> None:
	# Clear the screen
	Clear()
	
	LogMessage("Starting app...")
	
	ObtainAuthToken()
	
	LogMessage("Successfully aquired user token!")

if __name__ == "__main__":
	settings = Settings.Load()
	
	asyncio.run(main())
