import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class TradingConfig:
    """Configuration for the trading ecosystem"""
    # Exchange Configuration
    EXCHANGE_ID: str = "binance"
    EXCHANGE_API_KEY: Optional[str] = os.getenv("EXCHANGE_API_KEY")
    EXCHANGE_SECRET: Optional[str] = os.getenv("EXCHANGE_SECRET")
    
    # Trading Parameters
    SYMBOL: str = "BTC/USDT"
    TIMEFRAME: str = "1h"
    INITIAL_BALANCE: float = 10000.0
    MAX_POSITION_SIZE: float = 0.1  # 10% of portfolio
    TRANSACTION_FEE: float = 0.001  # 0.1%
    
    # Neuroevolution Parameters
    POPULATION_SIZE: int = 50
    GENERATIONS: int = 100
    MUTATION_RATE: float = 0.1
    ELITISM_COUNT: int = 5
    
    # Model Architecture
    INPUT_FEATURES: int = 20
    HIDDEN_LAYERS: tuple = (32, 16, 8)
    OUTPUT_ACTIONS: int = 3  # Buy, Sell, Hold
    
    # Firebase Configuration
    FIREBASE_CREDENTIALS_PATH: Optional[str] = os.getenv("FIREBASE_CREDENTIALS_PATH")
    FIREBASE_DATABASE_URL: Optional[str] = os.getenv("FIREBASE_DATABASE_URL")
    
    # Telegram Alerts
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID: Optional[str] = os.getenv("TELEGRAM_CHAT_ID")
    
    # Risk Management
    MAX_DRAWDOWN: float = 0.2  # 20%
    STOP_LOSS_PERCENT: float = 0.02  # 2%
    TAKE_PROFIT_PERCENT: float = 0.05  # 5%
    
    def validate(self) -> bool:
        """Validate configuration"""
        if not self.EXCHANGE_API_KEY or not self.EXCHANGE_SECRET:
            raise ValueError("Exchange credentials not configured")
        if not self.FIREBASE_CREDENTIALS_PATH:
            raise ValueError("Firebase credentials path not configured")
        if self.INITIAL_BALANCE <= 0:
            raise ValueError("Initial balance must be positive")
        return True