"""
QMT交易接口模块
提供miniqmt连接和交易功能
"""

__version__ = "1.0.0"
__author__ = "Trading System"

from .config import QMTConfig
from .connection import QMTConnection
from .callback import QMTCallback

__all__ = ["QMTConfig", "QMTConnection", "QMTCallback"]