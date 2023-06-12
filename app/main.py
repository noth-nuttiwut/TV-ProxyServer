from fastapi import FastAPI,  Body
import httpx
import uvicorn
from pprint import pprint
from os import environ
from enum import Enum
from datetime import datetime
from app.parse_message import OrderMesssage


class Side(Enum):
    Sell = "SELL"
    Buy = "BUY"
    
class Action(Enum):
    OpenShort = "OS"
    OpenLong = "OL"
    CloseShort = "CS"
    CloseLong = "CL"

HEADERS = {
  "Content-Type": "text/plain; charset=UTF-8",
  "jwt": f'{environ["jwt"]}'
}

app = FastAPI()


@app.get("/")
async def main():
  return {"message": f"Still Alive :: {datetime.now()}"}

@app.head("/")
async def head():
  return {"message": f"Still Alive :: {datetime.now()}"}

@app.get("/health")
async def health():
  return {"message": f"Still Alive :: {datetime.now()}"}


@app.post("/alert-hook")
async def alert_hook(body: str = Body(..., media_type='text/plain')):
    order = OrderMesssage(body)
    print()
    print("--------- ", order.message, " ---------")
    try:
      pprint(order.json)
      r = httpx.post('http://nsheadquarters.3bbddns.com:40480/alert-hook', headers=HEADERS, data=body)
    except Exception as e:
      result = {"status": 500, "message": f"{e}"}
    else:
      result = r.json()
    finally:
      print("---"*10, datetime.now())
      print()
      return result


if __name__ == "__main__":
  uvicorn.run(app, port = 8080, host = "0.0.0.0")