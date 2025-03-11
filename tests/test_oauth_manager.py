import pytest
import time
from unittest.mock import AsyncMock, MagicMock
from src.mail_integration.oauth_manager import OAuthTokenManager

@pytest.fixture
def oauth_manager():
    return OAuthTokenManager()

@pytest.mark.asyncio
async def test_store_tokens(oauth_manager):
    tokens = {
        'access_token': 'test-access',
        'refresh_token': 'test-refresh',
        'expires_in': 3600
    }
    
    await oauth_manager.store_tokens(tokens)
    stored = await oauth_manager.get_tokens()
    assert stored == tokens

@pytest.mark.asyncio
async def test_get_tokens(oauth_manager):
    test_tokens = {
        'access_token': 'test-access',
        'refresh_token': 'test-refresh',
        'expires_in': 3600
    }
    
    await oauth_manager.store_tokens(test_tokens)
    tokens = await oauth_manager.get_tokens()
    assert tokens == test_tokens

@pytest.mark.asyncio
async def test_clear_tokens(oauth_manager):
    await oauth_manager.store_tokens({'test': 'data'})
    await oauth_manager.clear_tokens()
    assert await oauth_manager.get_tokens() is None

def test_is_token_expired(oauth_manager):
    expired_tokens = {
        'expires_at': time.time() - 100
    }
    assert oauth_manager.is_token_expired(expired_tokens)
    
    valid_tokens = {
        'expires_at': time.time() + 3600
    }
    assert not oauth_manager.is_token_expired(valid_tokens)
