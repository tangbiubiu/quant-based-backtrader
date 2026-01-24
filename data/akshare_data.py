import akshare as ak
import pandas as pd


def get_stock_data(symbol: str, adjust: str) -> pd.DataFrame:
    # 利用 AKShare 获取股票的后复权数据，这里只获取前 7 列
    stock_hfq_df = ak.stock_zh_a_hist(symbol=symbol, adjust=adjust).iloc[:, :7]
    # 删除 `股票代码` 列
    if "股票代码" in stock_hfq_df.columns:
        stock_hfq_df = stock_hfq_df.drop(columns=["股票代码"])
    # 处理字段命名，以符合 Backtrader 的要求
    stock_hfq_df.columns = [
        "date",
        "open",
        "close",
        "high",
        "low",
        "volume",
    ]
    # 把 date 作为日期索引，以符合 Backtrader 的要求
    stock_hfq_df["date"] = pd.to_datetime(stock_hfq_df["date"])
    stock_hfq_df = stock_hfq_df.set_index("date")
    return stock_hfq_df


if __name__ == "__main__":
    # --- 使用示例 ---
    symbol = "000063"  # 示例股票代码
    adjust = "qfq"  # 前复权
    df = get_stock_data(symbol, adjust)
    print(df.head())
    print(df.info())
    print(df.describe())
