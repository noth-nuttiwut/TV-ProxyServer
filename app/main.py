from fastapi import FastAPI,  Body, Request, Header
import httpx
import uvicorn
from pprint import pprint
from os import environ
from enum import Enum
from datetime import datetime
from app.parse_message import OrderMesssage
from jwt import decode

TESTNET_DOMAIN = environ.get("TESTNET_DOMAIN", "localhost")
MAINNET_DOMAIN = environ.get("MAINNET_DOMAIN", "localhost")

TESTNET_PROTOCAL = environ.get("TESTNET_PROTOCAL", "http")
MAINNET_PROTOCAL = environ.get("MAINNET_PROTOCAL", "http")

TV_API_SECRET = environ.get("TV_API_SECRET", "")
TV_API_KEY = environ.get("TV_API_KEY", "")


class Side(Enum):
  Sell = "SELL"
  Buy = "BUY"
  
  def __str__(self) -> str:
    return self.value
    
class Action(Enum):
  OpenShort = "OS"
  OpenLong = "OL"
  CloseShort = "CS"
  CloseLong = "CL"
  
  def __str__(self) -> str:
    return self.value

class WebhookURL(Enum):
  testnet = f'{TESTNET_PROTOCAL}://{TESTNET_DOMAIN}/alert-hook'
  mainnet = f'{MAINNET_PROTOCAL}://{MAINNET_DOMAIN}/alert-hook'
  
  def __str__(self) -> str:
    return self.value
  
class Network(Enum):
  testnet = "TESTNET"
  mainnet= "MAINNET"
  both = "BOTH"
  
  def __str__(self) -> str:
    return self.value

HEADERS = {
  "Content-Type": "text/plain; charset=UTF-8",
  "jwt": f'{environ["jwt"]}'
}

app = FastAPI()


@app.get("/")
async def main(request: Request):
  user_ip = request.headers.get('CF-Connecting-IP', request.client.host)
  country = request.headers.get('CF-IPCountry', "nowhere")
  return {"message": f"Hello {user_ip} from {country}:: {datetime.now()}"}

@app.head("/")
async def head():
  return {"message": f"Still Alive :: {datetime.now()}"}

@app.get("/health")
async def health():
  return {"message": f"Still Alive :: {datetime.now()}"}

def verify_jwt(jwt_str, secret, api_key):
  try:
      result = decode(jwt_str, secret, algorithms=["HS256"])
      print(result)
      return api_key == result.get("apiKey", None)
  except Exception as e:
      return False

def send_message(body, order, url, network="TESTNET"):
  try:
    pprint(order.json)
    r = httpx.post(url, headers=HEADERS, data=body)
  except Exception as e:
    result = {"status": 500, "message": f"{e}"}
  else:
    result = r.json()
  finally:
    print(f"[INFO  ] [{network} ]RESULT : {result}")
    print("---"*10, datetime.now())
    print()
    return result

@app.post("/alert-hook")
async def alert_hook(body: str = Body(..., media_type='text/plain')):
    order = OrderMesssage(body)
    print()
    print("--------- ", order.message, " ---------")
    if not verify_jwt(order.jwt, TV_API_SECRET, TV_API_KEY):
      print("Authentication Error")
      print("--------- ", "Error", " ---------")
      return {"status": 403, "message" : "Authentication Error"} 
    
    network = order.network if order.network else Network.testnet.value
    
    if network == Network.both.value:
      send_message(body, order, url=f"{WebhookURL.mainnet}", network=f"{Network.mainnet}")
      return send_message(body, order, url=f"{WebhookURL.testnet}")
    elif network == Network.mainnet.value:
      return send_message(body, order, url=f"{WebhookURL.mainnet}", network=f"{Network.mainnet}")
    else:
      return send_message(body, order, url=f"{WebhookURL.testnet}")
    

if __name__ == "__main__":
  uvicorn.run(app, port=int(environ.get("PORT", 8080)), host="0.0.0.0")