from rest_framework import status
import pytest
from model_bakery import baker

from product.models import Product

@pytest.fixture
def create_product(api_client):
    def do_create(product):
        return api_client.post(f"/api/products/",product)
    return do_create 

@pytest.fixture
def update_product(api_client):
    def do_update(updated_product):
        product =baker.make(Product,title='title')
        return api_client.patch(f'/api/products/{product.id}/',updated_product)
    return do_update

@pytest.fixture
def delete_product(api_client):
    def do_delete():
        category =baker.make(Product)
        return api_client.delete(f'/api/products/{category.id}/')
    return do_delete
        



@pytest.mark.django_db
class TestCreateProducts:
    def test_if_user_anonymous_return_401(self,create_product):
        response = create_product({"title": "aa",
                                    "description": "ad",
                                    "price": 55.0,
                                    "inventory": 4,
                                    "category": "a"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED 

    def test_if_user_authenticated_return_403(self,
                                              create_product,
                                              authenticate):
        authenticate()
        response = create_product({"title": "aa",
                                    "description": "ad",
                                    "price": 55.0,
                                    "inventory": 4,
                                    "category": "a"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_admin_and_invalid_data_return_400(self,
                                                       create_product,
                                                       authenticate):
        authenticate(is_staff=True)
        response = create_product({"title": "",
                                    "description": "ad",
                                    "price": 55.0,
                                    "inventory": 4,
                                    "category": "a"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_user_admin_and_valid_data_return_201(self,
                                                     create_product,
                                                     authenticate):
        
        authenticate(is_staff=True)
        response = create_product({"title": "aa",
                                    "description": "ad",
                                    "price": 55.0,
                                    "inventory": 4,
                                    "category": "a"})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

@pytest.mark.django_db
class TestRetriveProducts:
    def test_if_category_exists_retuen_200(self,api_client):
        product = baker.make(Product) 

        response = api_client.get(f'/api/products/{product.id}/')

        assert response.status_code == status.HTTP_200_OK 
        


@pytest.mark.django_db
class TestUpdateProducts:
    def test_if_anonyous_user_update_return_401(self,update_product):
        response = update_product({'title':'updated title'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticated_user_update_return_403(self,update_product,authenticate):
        authenticate()
        response = update_product({'title':'updated title'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_admin_user_update_wit_valid_data_return_200(self,update_product,authenticate):
        authenticate(is_staff=True)
        updated_product = {'title':'updated title'}
        response = update_product(updated_product)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'updated title' 

    def test_if_admin_user_update_wit_invalid_data_return_200(self,update_product,authenticate):
        authenticate(is_staff=True)
        updated_product = {'title':''}
        response = update_product(updated_product)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestDeleteProducts: 
    def test_if_anonyous_user_Delete_return_401(self,delete_product):
        response = delete_product()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_autenticated_user_Delete_return_403(self,authenticate,delete_product):
        authenticate()
        response = delete_product()

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_admin_user_Delete_return_(self,authenticate,delete_product):
        authenticate(is_staff=True)
        response = delete_product()

        assert response.status_code == status.HTTP_204_NO_CONTENT
