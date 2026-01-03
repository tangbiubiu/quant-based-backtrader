# QMT交易模块使用说明

## 快速开始

### 1. 安装依赖
```bash
pip install xtquant
```

### 2. 配置环境
编辑项目根目录的 `.env` 文件，确保包含：
```bash
MINIQMT_PATH=你的miniqmt路径
MINIQMT_ACCOUNT=你的资金账号
MINIQMT_ACCOUNT_TYPE=STOCK
```

### 3. 运行测试
```bash
# 从项目根目录运行
python qmt_trading/test_connection.py

# 或者使用模块方式（从项目根目录）
python -m qmt_trading.test_connection
```

## 使用示例

### 基本连接
```python
from qmt_trading.connection import QMTConnection

# 方式1：手动管理
conn = QMTConnection()
try:
    conn.connect()
    asset = conn.query_asset()
    positions = conn.query_positions()
finally:
    conn.disconnect()

# 方式2：上下文管理器
with QMTConnection() as conn:
    asset = conn.query_asset()
    positions = conn.query_positions()
```

### 配置验证
```python
from qmt_trading.config import QMTConfig

config = QMTConfig()
print(f"路径: {config.path}")
print(f"账号: {config.account}")
print(f"类型: {config.account_type}")
```

## 功能列表

- ✅ QMT连接管理
- ✅ 账户资产查询
- ✅ 持仓信息查询
- ✅ 交易回调处理
- ✅ 环境变量配置
- ✅ 错误处理
- ✅ 测试验证

## 注意事项

1. 确保QMT客户端已安装并运行
2. 确保有权限访问miniqmt接口
3. 所有敏感信息通过.env文件配置
4. 运行前请验证配置正确性