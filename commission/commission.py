from backtrader import CommInfoBase


class MyStockCommissionScheme(CommInfoBase):
    """
    A股交易手续费计算类
    包含佣金(双向,最低5元)+印花税(卖出0.05%)+过户费(双向0.001%)
    """

    params = (
        ("commission", 0.0006),  # 佣金费率（双向）
        ("stamp_duty", 0.0005),  # 印花税率（卖出）
        ("transfer_fee", 0.00001),  # 过户费（双向）
        ("percabs", False),  # 是否按绝对值固定收费
    )

    def __init__(self, **params):
        super().__init__()
        for k, v in params.items():
            setattr(self.p, k, v)

    def _getcommission(self, size, price, pseudoexec):
        """
        计算交易费用核心逻辑
        Args:
            size: 正数为买入，负数为卖出
            price: 交易价格
            pseudoexec: 是否模拟执行
        Returns:
            float: 手续费总额(保留两位小数)
        """
        if size == 0:  # 零股交易不收费
            return 0.0

        # 计算成交金额绝对值
        trade_amount = abs(size) * price

        # 1. 计算佣金(双向)
        commission_fee = max(trade_amount * self.p.commission, 5.0)

        # 2. 计算过户费(双向)
        transfer_fee = trade_amount * self.p.transfer_fee

        # 3. 计算印花税(仅卖出)
        stamp_duty = 0.0
        if size < 0:  # 卖出操作
            stamp_duty = trade_amount * self.p.stamp_duty

        # 总手续费 = 佣金 + 过户费 + 印花税
        total_fee = commission_fee + transfer_fee + stamp_duty

        # 保留两位小数(四舍五入)
        return round(total_fee, 2)

    def getcommission(self, size, price):
        """Backtrader标准接口"""
        return self._getcommission(size, price, False)

    def getvaluesize(self, size, price):
        """返回交易金额(用于保证金计算)"""
        return abs(size) * price
