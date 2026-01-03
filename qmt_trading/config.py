import os
from dotenv import load_dotenv

class QMTConfig:
    """QMT配置类 - 严格环境变量验证，无默认值"""
    
    def __init__(self):
        load_dotenv()
        
        # 必要配置验证（无默认值）
        self.path = self._require_env('MINIQMT_PATH')
        self.account = self._require_env('MINIQMT_ACCOUNT')
        self.account_type = self._require_env('MINIQMT_ACCOUNT_TYPE')
    
    def _require_env(self, key: str) -> str:
        """获取必要环境变量，缺失立即报错"""
        value = os.getenv(key)
        if not value or value.strip() == '':
            raise ValueError(f"环境变量 {key} 必须配置，请在.env文件中设置")
        return value.strip()
    
    def __repr__(self):
        return f"QMTConfig(path='{self.path}', account='***', account_type='{self.account_type}')"