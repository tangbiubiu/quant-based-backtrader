#!/usr/bin/env python3
"""
QMT连接测试脚本
运行方式:
    python qmt_trading/test_connection.py
    或
    python -m qmt_trading.test_connection  # 从项目根目录运行
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_dependencies():
    """检查必要依赖"""
    try:
        import xtquant
        print(f"✅ xtquant已安装")
    except ImportError:
        print("❌ 未安装xtquant，请运行: pip install xtquant")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv已安装")
    except ImportError:
        print("❌ 未安装python-dotenv，请运行: pip install python-dotenv")
        return False
    
    return True

def main():
    """主测试函数"""
    print("🚀 开始QMT连接测试...")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        return False
    
    try:
        from qmt_trading.connection import QMTConnection
        
        # 测试配置加载
        print("📋 步骤1: 加载配置...")
        try:
            from qmt_trading.config import QMTConfig
            config = QMTConfig()
            print(f"✅ 配置加载成功")
            print(f"   路径: {config.path}")
            print(f"   账号: *** (已隐藏)")
            print(f"   类型: {config.account_type}")
        except ValueError as e:
            print(f"❌ 配置错误: {e}")
            print("\n💡 请在项目根目录的.env文件中添加以下配置:")
            print("   MINIQMT_PATH=你的miniqmt路径")
            print("   MINIQMT_ACCOUNT=你的资金账号")
            print("   MINIQMT_ACCOUNT_TYPE=STOCK")
            return False
        
        # 验证路径
        print("\n📋 步骤2: 验证路径...")
        if not os.path.exists(config.path):
            print(f"❌ 路径不存在: {config.path}")
            print("💡 请检查MINIQMT_PATH配置是否正确")
            return False
        print("✅ 路径验证通过")
        
        # 测试连接
        print("\n📋 步骤3: 测试连接...")
        conn = QMTConnection()
        
        try:
            conn.connect()
            print("✅ QMT连接成功！")
            
            # 查询账户信息
            print("\n📋 步骤4: 查询账户信息...")
            try:
                asset = conn.query_asset()
                print(f"💰 账户资产:")
                print(f"   总资产: {asset.total_asset}")
                print(f"   可用资金: {asset.cash}")
                print(f"   市值: {asset.market_value}")
            except Exception as e:
                print(f"⚠️ 资产查询失败: {e}")
            
            # 查询持仓
            print("\n📋 步骤5: 查询持仓...")
            try:
                positions = conn.query_positions()
                print(f"📊 持仓数量: {len(positions)}")
                if positions:
                    for pos in positions[:5]:  # 只显示前5条
                        print(f"   {pos.stock_code}: {pos.volume}股 市值:{pos.market_value}")
                    if len(positions) > 5:
                        print(f"   ... 还有{len(positions)-5}条持仓")
                else:
                    print("   当前无持仓")
            except Exception as e:
                print(f"⚠️ 持仓查询失败: {e}")
                
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            return False
        finally:
            try:
                conn.disconnect()
            except Exception as e:
                print(f"⚠️ 断开连接时出错: {e}")
        
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 50)
    print("🎉 QMT连接测试完成！")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)