# 项目目标
即使`backtrader`在易用性上已经非常牛逼了，但它毕竟要考虑丰富的交易种类和各种交易需求。对散户来说未免还是没那么好用。
这个项目将专注于**A股市场的散户策略**，做到让使用者**专注于策略本身，而不是复杂的工程实现上**。（以后最好能拿这个卖钱😏）
> 八八八八，咔咔就发😜

# 项目结构
```
.
├── commission/                 # 佣金模块
├── config/                     # 配置化目录
│   ├── config.toml
│   └── strategy_config.toml
├── data/                       # 数据处理模块
│   ├── db_based_tushare.py     # 从数据源获取数据，存放到数据库
│   └── db_reader.py            # 从数据库读取数据，并转为bt适用的格式
├── main.py                     # 主逻辑入口
└── strategy/                   # 策略模块
    ├── config_loader.py        # 策略注册，用来实现工厂模式
    └── macd_strategy.py        # 一个具体的策略实现
```
这个项目在 backtrader 基本使用方法的基础上，做了以下两件事：
* 模块化。把`data`、`strategy`和`commssion`三个部分从主逻辑中分离出来。方便定制化拓展。
* 配置化。方便调试策略。

# 部署
1. Python解释器**必须**使用3.11。
2. 安装依赖:
    ```bash
    pip install -r requirements.txt
    ```

# 使用方法
## 首次使用
1. 在`./config/`新建`.env`文件，并写入`TUSHARE_TOKEN= <Your Token>`
2. 执行`python main.py inin_db`，从`Tushare`获取数据。
## 进行回测
进行回测时数据库会自动更新。
1. 修改`config/config.toml`和`config/strategy_config.toml`
2. 执行:
```python
python main.py run
```
## 只想更新数据库
执行:
```python
python main.py update
```

# 贡献代码
请参照`CONTRIBUTING.md`

# 进度
- [x] 架构构思和搭建
- [x] 回测流程跑通
- [x] MCAD策略实现
- [ ] 接入券商api，实现交易
