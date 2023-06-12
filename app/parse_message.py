
class OrderMesssage:
  """_summary_
  Example
  symbol = {{tikcer}}, exchange = {{exchange}}, side = {{strategy.order.action}}, message = {{strategy.order.comment}}, size = {{strategy.position_size}}, ID = {{strategy.order.id}}, price = {{strategy.order.price}}
  """

  def __init__(self, message):
    self.raw_message = message
    self.__dict = self.parse()

  def parse(self):
    result = {}
    key_values = self.raw_message.split(", ")
    for kv in key_values:
      k, v = kv.split(" = ")
      if not k and not v:
        continue
        
      if "." not in v:
        result[k] = v.upper()  
      else:
        try:
          result[k] = float(v)
        except Exception as e:
          result[k] = v.upper()
      
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
    return self.__dict.get("message", None)

  @property
  def id(self):
    return self.__dict.get("ID", None)

  @property
  def price(self):
    return self.__dict.get("price", None)


if __name__ == "__main__":
  order = OrderMesssage("symbol = ARBUSDT, exchange = Binance, side = sell, message = Short-Entry, size = -4000.0")
  print(order.symbol, order.exchange, order.side)
  print(order.json)
  