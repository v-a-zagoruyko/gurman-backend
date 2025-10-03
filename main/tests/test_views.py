import pytest
from django.urls import reverse
from rest_framework import status
from .factories import MenuFactory, ProductFactory


@pytest.mark.django_db
def test_menu_by_slug_not_found(auth_client):
    url = reverse("menu-by-slug", kwargs={"slug": "fake-slug"})
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert "error" in data
    assert "Меню не найдено" in data["error"]


@pytest.mark.django_db
def test_menu_by_slug_success(auth_client):
    product1 = ProductFactory()
    product2 = ProductFactory()
    menu = MenuFactory(products=[product1, product2])

    url = reverse("menu-by-slug", kwargs={"slug": menu.slug})
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == menu.name
    assert data["slug"] == menu.slug
    assert len(data["products"]) == 2
    product_ids = [p["id"] for p in data["products"]]
    assert product1.id in product_ids
    assert product2.id in product_ids