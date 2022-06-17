from queue import PriorityQueue
from collections import namedtuple
# organize orderbook based on tickers and their open orders
# use a priority queue to sort orders based on time they were sent, and prioritized by best price
#hashmap of priority queue -> if key (ticker) exists, add to queue/execute, if not, new order
# if buy price > or = sell price, execute trade
TradeRequest = namedtuple('TradeRequest', ['OrderId', 'Quantity', 'Price', 'Symbol', 'TraderName']);
class OrderBook(object):

    global buyMap
    buyMap = {}
    global sellMap
    sellMap = {}
    global buyOrders
    buyOrders = {}
    global sellOrders
    sellOrders = {}
    global buyTickers
    buyTickers = set()
    global sellTickers
    sellTickers = set()

    def __init__(self):
        self.buyMap = buyMap
        self.sellMap = sellMap
        self.buyOrders = buyOrders
        self.sellOrders = sellOrders
        self.buyTickers = buyTickers
        self.sellTickers = sellTickers

    def newBuyOrder(self, tradeRequest):
        buyTickers.add(tradeRequest.Symbol)
        if tradeRequest.Symbol in buyOrders:
            buyOrders[tradeRequest.Symbol].put((tradeRequest.Price, tradeRequest))
        else:
            tickerQueue = PriorityQueue()
            tickerQueue.put((tradeRequest.Price, tradeRequest))
            buyOrders[tradeRequest.Symbol] = tickerQueue
        pass

    def newSellOrder(self, tradeRequest):
        sellTickers.add(tradeRequest.Symbol)
        if tradeRequest.Symbol in sellOrders:
            sellOrders[tradeRequest.Symbol].put((tradeRequest.Price, tradeRequest))
        else:
            tickerQueue = PriorityQueue()
            tickerQueue.put((tradeRequest.Price, tradeRequest))
            sellOrders[tradeRequest.Symbol] = tickerQueue
        pass

    def populateMap(self):

        for ticker in buyTickers:
            buyMap[ticker] = buyOrders[ticker]
        for ticker in sellTickers:
            sellMap[ticker] = sellOrders[ticker]

    def prettyPrintOrders(self):
        for ticker in buyTickers:
            i = 0
            while i < len(buyOrders[ticker].queue):
                printable = buyOrders[ticker].queue[i][1]
                print(printable)
                i = i + 1
        for ticker in sellTickers:
            j = 0
            while j < len(sellOrders[ticker].queue):
                printable = sellOrders[ticker].queue[j][1]
                print(printable)
                j = j + 1

    def prettyPrintMap(self):
        print(buyMap)
        print(sellMap)

    def existingOrders(self):

        for ticker in buyMap:
            if ticker in sellMap:
                i = 0
                while i < len(buyOrders[ticker].queue):
                    i+=1
                    try:
                        buyPrice = buyOrders[ticker].queue[0][1].Price
                        sellPrice = sellOrders[ticker].queue[0][1].Price
                    except:
                        continue
                    buyer = buyOrders[ticker].queue[0][1].TraderName
                    seller = sellOrders[ticker].queue[0][1].TraderName
                    if buyer == seller:
                        continue
                    if buyPrice >= sellPrice:
                        return True
                    else:
                        return False

    def executeOrders(self):
        print("executing orders...")
        del_keys = []
        while self.existingOrders() == True:

            for ticker in buyMap:
                if ticker in sellMap:
                    i = 0
                    while i < len(buyOrders[ticker].queue):
                        i+=1
                        try:
                            buyPrice = buyOrders[ticker].queue[0][1].Price
                            sellPrice = sellOrders[ticker].queue[0][1].Price
                        except:
                            continue
                        buyer = buyOrders[ticker].queue[0][1].TraderName
                        seller = sellOrders[ticker].queue[0][1].TraderName
                        if buyer == seller:
                            continue
                        if buyPrice >= sellPrice:
                            buyQty = buyOrders[ticker].queue[0][1].Quantity
                            sellQty = -sellOrders[ticker].queue[0][1].Quantity
                            print("Price: ", sellOrders[ticker].queue[0][1].Price, " Quantity: ",
                                  sellQty, " BuyID: ", buyOrders[ticker].queue[0][1].OrderId,  " SellID: ",
                                  sellOrders[ticker].queue[0][1].OrderId)
                            if buyQty == sellQty:
                                buyOrders[ticker].get()
                                sellOrders[ticker].get()
                                del_keys.append(ticker)
                            elif buyQty > sellQty:
                                diff = buyQty - sellQty
                                orderID = buyOrders[ticker].queue[0][1].OrderId
                                traderName = buyOrders[ticker].queue[0][1].TraderName
                                sellOrders[ticker].get()
                                buyOrders[ticker].get()
                                self.newBuyOrder(TradeRequest(orderID, diff, buyPrice, ticker, traderName))
                            elif sellQty > buyQty:
                                diff = sellQty - buyQty
                                orderID = sellOrders[ticker].queue[0][1].OrderId
                                traderName = sellOrders[ticker].queue[0][1].TraderName
                                sellOrders[ticker].get()
                                buyOrders[ticker].get()
                                self.newSellOrder(TradeRequest(orderID, -diff, sellPrice, ticker, traderName))
            for ticker in del_keys:
                buyMap.pop(ticker)
                sellMap.pop(ticker)
        print("remaining orders: ")
