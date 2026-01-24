from abc import ABCMeta, abstractmethod

import backtrader as bt


class ABCMetaStrategy(ABCMeta):
    pass


class TradeStrategy(bt.Strategy, metaclass=ABCMetaStrategy):
    strategy_name: str | None = None  # 用于标识策略名称(可选)

    def __init__(self, **params) -> None:
        """
        在这里初始化信号和策略参数。
        """
        super().__init__()

    @abstractmethod
    def next(self) -> None:
        """
        在这里实现策略的逻辑。

        步骤：
        1. 获取必要数据（-1表示前一交易日）。例：
            prev_close = self.data.close[-1]
            prev_sma = self.sma[-1]
            prev_diff = self.diff[-1]
        2. 计算信号。例：
            # 开仓信号
            condition1 = prev_close < prev_sma
            condition2 = prev_volume > prev_volume_avg
            long_signal = all([condition1, condition2])
            # 平仓信号
            exit_condition1 = prev_close > prev_sma
            exit_condition2 = prev_volume < prev_volume_avg
            exit_signal = all([exit_condition1, exit_condition2])
        3. 执行交易。例：
            if not self.position:
                if long_signal and self.order is None:
                    self.order = self.buy()  # 默认使用全部可用资金
            else:
                if exit_signal and self.order is None:
                    self.order = self.close()  # 平仓
        """
        pass

    def notify_order(self, order) -> None:
        """
        获取订单状态，这个函数一般无须重写。
        """
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f"BUY EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm {order.executed.comm:.2f}"
                )
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(
                    f"SELL EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm {order.executed.comm:.2f}"
                )
                self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled / Margin / Rejected")
        self.order = None

    def notify_trade(self, trade) -> None:
        """
        追踪每笔交易的状态，这个函数一般无须重写。
        """
        if not trade.isclosed:
            return
        self.log(f"OPERATION PROFIT, GROSS {trade.pnl:.2f}, NET {trade.pnlcomm:.2f}")

    def log(self, txt, dt=None, doprint=False) -> None:
        """
        保存日志
        """
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f"{dt.isoformat()}, {txt}")
