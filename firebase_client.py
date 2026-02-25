import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

try:
    import firebase_admin
    from firebase_admin import credentials, firestore, initialize_app
    from google.cloud.firestore_v1 import Client as FirestoreClient
except ImportError as e:
    logging.error(f"Firebase admin not installed: {e}")
    raise

class FirebaseClient:
    """Firebase client for state persistence and real-time data streaming"""
    
    def __init__(self, config):
        self.config = config
        self._client: Optional[FirestoreClient] = None
        self._initialized = False
        
    def initialize(self) -> bool:
        """Initialize Firebase connection with error handling"""
        try:
            if not firebase_admin._apps:
                cred_path = self.config.FIREBASE_CREDENTIALS_PATH
                if not cred_path:
                    raise ValueError("Firebase credentials path not provided")
                    
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': self.config.FIREBASE_DATABASE_URL
                })
            
            self._client = firestore.client()
            self._initialized = True
            logging.info("Firebase initialized successfully")
            return True
            
        except Exception as e:
            logging.error(f"Firebase initialization failed: {e}")
            self._initialized = False
            return False
    
    def save_agent_state(self, agent_id: str, state: Dict[str, Any]) -> bool:
        """Save agent state to Firestore"""
        if not self._initialized or not self._client:
            logging.error("Firebase not initialized")
            return False
            
        try:
            state['updated_at'] = datetime.utcnow()
            doc_ref = self._client.collection('trading_agents').document(agent_id)
            doc_ref.set(state, merge=True)
            logging.debug(f"Saved state for agent {agent_id}")
            return True
        except Exception as e:
            logging.error(f"Failed to save agent state: {e}")
            return False
    
    def load_agent_state(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Load agent state from Firestore"""
        if not self._initialized or not self._client:
            logging.error("Firebase not initialized")
            return None
            
        try:
            doc_ref = self._client.collection('trading_agents').document(agent_id)
            doc = doc_ref.get()
            return doc.to_dict() if doc.exists else None
        except Exception as e:
            logging.error(f"Failed to load agent state: {e}")
            return None
    
    def save_population_state(self, generation: int, population_data: List[Dict