import pytest
from config.config_validator import ConfigValidator

def test_valid_config():
    config = {
        "gmail_api": {
            "client_id": "test-client-id",
            "client_secret": "test-secret",
            "project_id": "test-project",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost:8080/oauth2callback"]
        }
    }
    
    validator = ConfigValidator(config)
    assert validator.validate()
    assert len(validator.get_errors()) == 0

def test_missing_required_field():
    config = {
        "gmail_api": {
            "client_id": "test-client-id",
            # Missing client_secret
            "project_id": "test-project",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost:8080/oauth2callback"]
        }
    }
    
    validator = ConfigValidator(config)
    assert not validator.validate()
    assert "Missing required field: gmail_api.client_secret" in validator.get_errors()

def test_invalid_uri():
    config = {
        "gmail_api": {
            "client_id": "test-client-id",
            "client_secret": "test-secret",
            "project_id": "test-project",
            "auth_uri": "invalid-uri",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost:8080/oauth2callback"]
        }
    }
    
    validator = ConfigValidator(config)
    assert not validator.validate()
    assert "Invalid URI format in gmail_api.auth_uri" in validator.get_errors()
