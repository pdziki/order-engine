from collections import namedtuple
import OrderBook

# Do not modify this tuple.
TradeRequest = namedtuple('TradeRequest', ['OrderId', 'Quantity', 'Price', 'Symbol', 'TraderName']);

class OrderMatchingEngine(object):

    global orderBook
    orderBook = OrderBook.OrderBook()

    def __init__(self):
        
        pass

    def clearOrders(self, orderBook):
        orderBook.buyMap.clear()
        orderBook.sellMap.clear()
        orderBook.buyOrders.clear()
        orderBook.sellOrders.clear()
        orderBook.buyTickers.clear()
        orderBook.sellTickers.clear()

    def NewTradeRequest(self, tradeRequest):
        if tradeRequest[1] > 0:
            orderBook.newBuyOrder(tradeRequest)
        elif tradeRequest[1] < 0:
            orderBook.newSellOrder(tradeRequest)


    def testNoMatch(self):
        orderBook1 = OrderBook.OrderBook()
        print("incoming orders: ")
        self.NewTradeRequest(TradeRequest(1, 10, 1.00, 'A', 'TLH'))
        self.NewTradeRequest(TradeRequest(3, -10, 1.05, 'A', 'FORR'))
        orderBook1.populateMap()
        orderBook1.prettyPrintOrders()
        orderBook1.executeOrders()
        orderBook1.prettyPrintOrders()
        self.clearOrders(orderBook1)
        print("\n")

    def testSimpleMatch(self):
        orderBook2 = OrderBook.OrderBook()
        print("incoming orders: ")
        self.NewTradeRequest(TradeRequest(1, 10, 1.00, 'A', 'TLH'))
        self.NewTradeRequest(TradeRequest(3, -10, .99, 'A', 'FORR'))
        orderBook2.populateMap()
        orderBook2.prettyPrintOrders()
        orderBook2.executeOrders()
        orderBook2.prettyPrintOrders()
        self.clearOrders(orderBook2)
        print("\n")

    def testPriceImprovement(self):
        orderBook3 = OrderBook.OrderBook()
        print("incoming orders: ")
        self.NewTradeRequest(TradeRequest(1, 10, 1.00, 'A', 'TLH'))
        self.NewTradeRequest(TradeRequest(5, 10, .99, 'A', 'YZH'))
        self.NewTradeRequest(TradeRequest(3, -10, .99, 'A', 'FORR'))
        orderBook3.populateMap()
        orderBook3.prettyPrintOrders()
        orderBook3.executeOrders()
        orderBook3.prettyPrintOrders()
        self.clearOrders(orderBook3)
        print("\n")

    def testFullFillMultOrders(self):
        orderBook4 = OrderBook.OrderBook()
        print("incoming orders: ")
        self.NewTradeRequest(TradeRequest(1, 10, 1.00, 'A', 'TLH'))
        self.NewTradeRequest(TradeRequest(5, 10, .99, 'A', 'YZH'))
        self.NewTradeRequest(TradeRequest(3, -20, .99, 'A', 'FORR'))
        orderBook4.populateMap()
        orderBook4.prettyPrintOrders()
        orderBook4.executeOrders()
        orderBook4.prettyPrintOrders()
        self.clearOrders(orderBook4)
        print("\n")

    def testPartialFill(self):
        orderBook5 = OrderBook.OrderBook()
        print("incoming orders: ")
        self.NewTradeRequest(TradeRequest(1, -10, 1.00, 'A', 'TLH'))
        self.NewTradeRequest(TradeRequest(5, -10, 1.00, 'A', 'YZH'))
        self.NewTradeRequest(TradeRequest(4, -5, 1.00, 'B', 'LINZ'))
        self.NewTradeRequest(TradeRequest(3, 25, 1.00, 'A', 'FORR'))
        orderBook5.populateMap()
        orderBook5.prettyPrintOrders()
        orderBook5.executeOrders()
        orderBook5.prettyPrintOrders()
        self.clearOrders(orderBook5)
        print("\n")

    def runTests(self):
        self.testNoMatch()
        self.testSimpleMatch()
        self.testPriceImprovement()
        self.testFullFillMultOrders()
        self.testPartialFill()

test = OrderMatchingEngine()
test.runTests()

