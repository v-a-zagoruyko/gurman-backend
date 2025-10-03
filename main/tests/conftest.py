import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from unittest.mock import patch
from .factories import AuthTokenFactory

@pytest.fixture
def api_client():
	return APIClient()

@pytest.fixture
def auth_client(db):
    auth_token = AuthTokenFactory()
    user = User.objects.create_user(username="dummy_user")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {auth_token.token}")
    client.handler._force_user = user
    return client
