import sys
from datetime import datetime
import calendar
import tomllib
import pandas as pd
import matplotlib.pyplot as plt
from backtrader import bt
import akshare as ak
from pprint import pprint as pp

from strategy.config_loader import StrategyConfig
from commission.commission import MyStockCommissionScheme
# from data.akshare_data import get_stock_data
from data.db_reader import StockDBReader
from data.db_based_tushare import TushareDownloader


def main(update_db: bool = True):
    with open("config/config.toml", "rb") as f: 
        config = tomllib.load(f)

    config_info = f"""
配置参数:
       初始资金: {config["cash"]}
       股票代码: {config["stock"]["symbol"]}
       复权方式: {config["stock"]["adjust"]}
       回测区间: {config["date"]["start_year"]}-{config["date"]["start_month"]} ~ {config["date"]["end_year"]}-{config["date"]["end_month"]}
       策略名称: {config["strategy"]["name"]}
       佣金费率: {config["broker"]["commission"]}
       印花税率: {config["broker"]["stamp_duty"]}
    """

    pp(config_info)

    platform = sys.platform.lower()
    if platform.startswith("win"):
        plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS"]
    elif platform.startswith("linux"):
        plt.rcParams["font.sans-serif"] = ["SimHei", "WenQuanYi Zen Hei", "Noto Sans CJK SC"]
    else:
        plt.rcParams["font.sans-serif"] = ["Hiragino Sans GB", "Arial Unicode MS", "SimHei"]
    plt.rcParams["axes.unicode_minus"] = False

    end_month_last_day = calendar.monthrange(config["date"]["end_year"], config["date"]["end_month"])[1]
    start_date, end_date = (
        datetime(config["date"]["start_year"], config["date"]["start_month"], 1),
        datetime(config["date"]["end_year"], config["date"]["end_month"], end_month_last_day),
    )

    # raw_data = get_stock_data(
    #     symbol=config["stock"]["symbol"][0],
    #     adjust=config["stock"]["adjust"]
    # )
    
    # 更新数据库
    if update_db:
        data_downloader = TushareDownloader()
        data_downloader.update()
    # 读取数据库
    db_reader = StockDBReader()
    raw_data = db_reader.get_daily_price(
        ts_code=config["stock"]["symbol"][0],
        start_date=start_date.strftime('%Y%m%d'),
        end_date=end_date.strftime('%Y%m%d'),
        adj_type=config["stock"]["adjust"]
    )

    strategy_cfg = StrategyConfig()
    strategy_class, strategy_params = strategy_cfg.get_strategy(
        name=config["strategy"]["name"]
    )

    comminfo = MyStockCommissionScheme(**config["broker"])

    cerebro = bt.Cerebro()
    data = bt.feeds.PandasData(
        dataname=raw_data,
        fromdate=start_date,
        todate=end_date
    )
    cerebro.adddata(data)
    cerebro.addstrategy(strategy_class, **strategy_params)
    cerebro.broker.setcash(config["cash"])
    # 使用自定义佣金信息
    cerebro.broker.addcommissioninfo(comminfo)
    cerebro.run()

    port_value = cerebro.broker.getvalue()  # 获取回测结束后的总资金
    pnl = port_value - config["cash"]  # 盈亏统计

    result_info = f"""
回测结果:
       初始资金: {config["cash"]}
       回测期间: {start_date.strftime('%Y%m%d')} ~ {end_date.strftime('%Y%m%d')}
       总资金: {round(port_value, 2)}
       净收益: {round(pnl, 2)}
    """
    pp(result_info)

    cerebro.plot(style='candlestick')

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='quantitative trading with Backtrader')
    parser.add_argument('task', metavar='t', type=str, default='run',
                   help='''run: update database & run backtest; 
                   update: ONLY update database; 
                   init_db: initialize database, two date parameters required''')
    parser.add_argument('start_date', metavar='s', type=str, nargs='?', default=None,
                   help='start date for backtest in YYYYMMDD format')
    parser.add_argument('end_date', metavar='e', type=str, nargs='?', default=None,
                   help='end date for backtest in YYYYMMDD format')
    args = parser.parse_args()

    if args.task == 'run':
        main(update_db=True)
    elif args.task == 'update':
        data_downloader = TushareDownloader()
        data_downloader.update()
    elif args.task == 'init_db':
        data_downloader = TushareDownloader()
        data_downloader.frist_download(start_date=args.start_date, end_date=args.end_date)
    else:
        print("无效的任务参数，请使用 'run', 'update' 或 'init_db'。")