from bcv import get_dolar_rate, get_euro_rate
from binance import get_binance_buy_rate, get_binance_sell_rate
from discord_webhook import send_to_discord

class PriceMonitor:
  def __init__(self):
    self.bcv_usd = None
    self.bcv_eur = None
    self.binance_buy = None
    self.binance_sell = None

  def fetch_data(self):
    self.bcv_usd = get_dolar_rate()
    self.bcv_eur = get_euro_rate()
    self.binance_buy = get_binance_buy_rate()
    self.binance_sell = get_binance_sell_rate()

  def compare_buy(self):
    return round(((self.binance_buy - self.bcv_usd) / self.bcv_usd) * 100, 2)
  
  def compare_sell(self):
    return round(((self.binance_sell - self.bcv_usd) / self.bcv_usd) * 100, 2)
  
  def report(self):
    print("=== Tasas BCV ===")
    print(f"Dólar BCV: {self.bcv_usd} VES")
    print(f"Euro BCV:  {self.bcv_eur} VES\n")

    print("=== Binance P2P ===")
    print(f"Compra USDT: {self.binance_buy} VES")
    print(f"Venta USDT:  {self.binance_sell} VES\n")

    print("=== Comparación con BCV ===")
    print(f"Diferencia compra: {self.compare_buy()}%")
    print(f"Diferencia venta:  {self.compare_sell()}%")

  def discord_report(self):
      msg = (
          f"💵 **Reporte del dólar en Venezuela**\n"
          f"🇻🇪 **BCV:** {self.bcv_usd} VES\n"
          f"💶 **Euro BCV:** {self.bcv_eur} VES\n\n"
          f"🟢 **Binance Compra:** {self.binance_buy} VES\n"
          f"🔵 **Binance Venta:** {self.binance_sell} VES\n\n"
          f"📊 Diferencia compra: {self.compare_buy()}%\n"
          f"📊 Diferencia venta: {self.compare_sell()}%\n"
      )

      send_to_discord(msg)

def main():
  monitor = PriceMonitor()
  monitor.fetch_data()
#  monitor.report()
  monitor.discord_report()

if __name__ == "__main__":
  main()