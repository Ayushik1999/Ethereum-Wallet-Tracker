from requests import get
from matplotlib import pyplot as plt
from datetime import datetime
base_url="https://api.etherscan.io/api"
API_KEY= "13KDWQNC62THVSD99G1AF3RMTTBU1UDGK2"
address="0x73bceb1cd57c711feac4224d062b0f6ff338501e"
ether_value=10**18
def api_url(module,action,address,**kwargs):
   URL=base_url+f"?module={module}&action={action}&address={address}&apikey={API_KEY}"
   for key, value in kwargs.items():
      URL+=f"&{key}={value}"
   return URL 
def balance(address):
   balance_url=api_url("account", "balance", address, tag="latest")
   response = get(balance_url)
   data = response.json()
   value = int(data["result"]) / ether_value
   return value
def transactions(address):
   value=balance(address)
   tx_url=api_url("account","txlist",address,startblock=0,endblock=99999999,page=1,offset=10,sort="asc")
   res=get(tx_url)
   dat=res.json()['result']

   internal_tx_url = api_url("account", "txlistinternal", address, startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
   response2 = get(internal_tx_url)
   data2 = response2.json()["result"]

   dat.extend(data2)
   dat.sort(key=lambda x: int(x['timeStamp']))
   current_bal=0
   balances=[]
   times=[]
   for tx in dat:
      to = tx["to"]
      from_addr = tx["from"]
      value = int(tx["value"]) / ether_value

      if "gasPrice" in tx:
         gas = int(tx["gasUsed"]) * int(tx["gasPrice"]) / ether_value
      else:
         gas = int(tx["gasUsed"]) / ether_value

      time = datetime.fromtimestamp(int(tx['timeStamp']))
      money_in = to.lower() == address.lower()

      if money_in:
         current_bal += value
      else:
         current_bal -= value + gas

      balances.append(current_bal)
      times.append(time)

   plt.plot(times, balances)
   plt.show()
transactions(address)