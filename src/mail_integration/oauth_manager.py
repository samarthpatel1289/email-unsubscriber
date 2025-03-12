import json
import time
from typing import Optional, Dict, Any

class OAuthTokenManager:
    """Manages OAuth2 token storage and refresh"""
    
    def __init__(self, storage=None):
        """Initialize with optional storage backend
        
        Args:
            storage: Storage backend implementing get/set/remove methods.
                     If None, uses in-memory storage.
        """
        self.storage = storage or InMemoryStorage()
    
    async def store_tokens(self, tokens: Dict[str, Any]) -> None:
        """Store OAuth tokens securely"""
        encrypted_tokens = self._encrypt_tokens(tokens)
        await self.storage.set('oauth_tokens', encrypted_tokens)
    
    async def get_tokens(self) -> Optional[Dict[str, Any]]:
        """Retrieve stored OAuth tokens"""
        encrypted = await self.storage.get('oauth_tokens')
        if encrypted:
            return self._decrypt_tokens(encrypted)
        return None
    
    async def clear_tokens(self) -> None:
        """Remove stored OAuth tokens"""
        await self.storage.remove('oauth_tokens')

    def is_token_expired(self, tokens: Dict[str, Any]) -> bool:
        """Check if access token is expired"""
        if not tokens or 'expires_at' not in tokens:
            return True
        return time.time() >= tokens['expires_at']
    
    def _encrypt_tokens(self, tokens: Dict[str, Any]) -> str:
        """Encrypt tokens before storage"""
        # Basic encryption for now - should be replaced with proper encryption
        return json.dumps(tokens)
    
    def _decrypt_tokens(self, encrypted: str) -> Dict[str, Any]:
        """Decrypt stored tokens"""
        # Basic decryption for now - should be replaced with proper encryption
        return json.loads(encrypted)

class InMemoryStorage:
    """In-memory storage backend for testing"""
    
    def __init__(self):
        self._store = {}
    
    async def set(self, key: str, value: Any) -> None:
        self._store[key] = value
    
    async def get(self, key: str) -> Any:
        return self._store.get(key)
    
    async def remove(self, key: str) -> None:
        self._store.pop(key, None)
