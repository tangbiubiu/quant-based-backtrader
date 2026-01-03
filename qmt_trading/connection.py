import os
import time
from xtquant.xttrader import XtQuantTrader
from xtquant.xttype import StockAccount
from qmt_trading.config import QMTConfig
from qmt_trading.callback import QMTCallback

class QMTConnection:
    """QMT连接管理类"""
    
    def __init__(self):
        self.config = QMTConfig()
        self.trader = None
        self.account = None
        self.callback = None
        
    def connect(self) -> bool:
        """建立QMT连接
        
        Returns:
            bool: 连接成功返回True
            
        Raises:
            FileNotFoundError: QMT路径不存在
            ConnectionError: 连接失败
            RuntimeError: 账户订阅失败
        """
        # 验证路径存在
        if not os.path.exists(self.config.path):
            raise FileNotFoundError(f"QMT路径不存在: {self.config.path}")
        
        # 创建连接
        session_id = int(time.time())
        self.trader = XtQuantTrader(self.config.path, session_id)
        self.account = StockAccount(self.config.account, self.config.account_type)
        
        # 注册回调
        self.callback = QMTCallback()
        self.trader.register_callback(self.callback)
        
        # 启动连接
        self.trader.start()
        result = self.trader.connect()
        
        if result != 0:
            raise ConnectionError(f"QMT连接失败，错误码: {result}")
        
        # 订阅账户
        subscribe_result = self.trader.subscribe(self.account)
        if subscribe_result != 0:
            raise RuntimeError(f"账户订阅失败，错误码: {subscribe_result}")
            
        return True
    
    def disconnect(self):
        """断开QMT连接"""
        if self.trader:
            try:
                self.trader.stop()
                print("✅ QMT连接已断开")
            except Exception as e:
                print(f"⚠️ 断开连接时出错: {e}")
    
    def query_asset(self):
        """查询账户资产"""
        if not self.trader or not self.account:
            raise RuntimeError("未建立连接")
        return self.trader.query_stock_asset(self.account)
    
    def query_positions(self):
        """查询持仓"""
        if not self.trader or not self.account:
            raise RuntimeError("未建立连接")
        return self.trader.query_stock_positions(self.account)
    
    def __enter__(self):
        """上下文管理器入口"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.disconnect()