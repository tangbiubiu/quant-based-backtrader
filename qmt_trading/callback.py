from xtquant.xttype import XtOrder, XtTrade, XtPosition, XtAsset
from xtquant.xttrader import XtQuantTraderCallback

class QMTCallback(XtQuantTraderCallback):
    """QMT交易回调处理类"""
    
    def on_disconnected(self):
        """连接断开回调"""
        print("⚠️ QMT连接断开")
        
    def on_stock_order(self, order: XtOrder):
        """委托回报回调"""
        print(f"📋 委托回报: {order.stock_code} 数量:{order.order_volume} 价格:{order.price} 状态:{order.order_status}")
        
    def on_stock_trade(self, trade: XtTrade):
        """成交回报回调"""
        print(f"💰 成交回报: {trade.stock_code} 数量:{trade.traded_volume} 价格:{trade.traded_price}")
        
    def on_stock_position(self, position: XtPosition):
        """持仓变动回调"""
        print(f"📊 持仓变动: {position.stock_code} 数量:{position.volume} 市值:{position.market_value}")
        
    def on_stock_asset(self, asset: XtAsset):
        """资金变动回调"""
        print(f"💵 资金变动: 总资产:{asset.total_asset} 可用资金:{asset.cash}")