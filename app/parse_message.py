
class OrderMesssage:
  """_summary_
  Example
  symbol = {{tikcer}}, exchange = {{exchange}}, side = {{strategy.order.action}}, message = {{strategy.order.comment}}, size = {{strategy.position_size}}, ID = {{strategy.order.id}}, price = {{strategy.order.price}}, network = main
  """

  def __init__(self, message):
    self.raw_message = message
    self.__dict = self.parse()

  def parse(self, ignore_uppercase_key=["JWT"]):
    result = {}
    key_values = self.raw_message.split(", ")
    for kv in key_values:
      k, v = kv.split(" = ")
      if not k and not v:
        continue
        
      if "." not in v:
        result[k] = v if k in ignore_uppercase_key else v.upper()  
      else:
        try:
          result[k] = float(v)
        except Exception as e:
          result[k] = v if k in ignore_uppercase_key else v.upper() 
      
    return result

  @property
  def json(self):
    return self.__dict
  
  @property
  def symbol(self):
    return self.__dict.get("symbol", None).replace(".P", "")

  @property
  def exchange(self):
    return self.__dict.get("exchange", None)
  
  @property
  def size(self):
    return self.__dict.get("size", None)

  @property
  def side(self):
    return self.__dict.get("side", None)

  @property
  def message(self):
    msg = self.__dict.get("message", None)
    if not msg:
      return msg
    
    order_splitted = msg.split(" - ")
    return order_splitted[0]

  @property
  def id(self):
    return self.__dict.get("ID", None)

  @property
  def price(self):
    return self.__dict.get("price", None)
  
  @property
  def jwt(self):
    return self.__dict.get("JWT", None)
  
  @property
  def balance(self):
    return self.__dict.get("balance", None)
  
  @property
  def network(self):
    return self.__dict.get("network", None)
  
  @property
  def tp(self):
    return self.__dict.get("tp", None)
  
  @property
  def sl(self):
    return self.__dict.get("sl", None)


if __name__ == "__main__":
  order = OrderMesssage("symbol = ARBUSDT, exchange = Binance, side = sell, message = Short-Entry, size = -4000.0, network = MAINNET")
  print(order.symbol, order.exchange, order.side)
  print(order.json)
  