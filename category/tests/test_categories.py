from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
import pytest 
from model_bakery import baker

from category.models import Category

@pytest.fixture
def create_category(api_client):
    def do_create(category):
        return api_client.post(f"/api/categories/",category)
    return do_create 

@pytest.fixture
def update_category(api_client):
    def do_update(updated_category):
        category =baker.make(Category,title='title')
        return api_client.patch(f'/api/categories/{category.id}/',updated_category)
    return do_update

@pytest.fixture
def delete_category(api_client):
    def do_delete():
        category =baker.make(Category)
        return api_client.delete(f'/api/categories/{category.id}/')
    return do_delete
        



@pytest.mark.django_db
class TestCreateCategories:
    def test_if_user_anonymous_return_401(self,create_category):
        response = create_category({'title':"a"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED 

    def test_if_user_authenticated_return_403(self,api_client,
                                              create_category,
                                              authenticate):
        authenticate()
        response = create_category({'title':"a"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_admin_and_invalid_data_return_400(self,api_client,
                                                       create_category,
                                                       authenticate):
        authenticate(is_staff=True)
        response = create_category({'title':""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_user_admin_and_valid_data_return_201(self,api_client,
                                                     create_category,
                                                     authenticate):
        
        authenticate(is_staff=True)
        response = create_category({'title':"a"})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

@pytest.mark.django_db
class TestRetriveCategory:
    def test_if_category_exists_retuen_200(self,api_client):
        category = baker.make(Category) 

        response = api_client.get(f'/api/categories/{category.id}/')

        assert response.status_code == status.HTTP_200_OK 
        assert response.data == {
            'id':category.id,
            'title' :category.title,
            'description': category.description,
            'product_count':0
        }


@pytest.mark.django_db
class TestUpdateCategory:
    def test_if_anonyous_user_update_return_401(self,update_category):
        response = update_category({'title':'updated title'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticated_user_update_return_403(self,update_category,authenticate):
        authenticate()
        response = update_category({'title':'updated title'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_admin_user_update_wit_valid_data_return_200(self,update_category,authenticate):
        authenticate(is_staff=True)
        updated_category = {'title':'updated title'}
        response = update_category(updated_category)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'updated title' 

    def test_if_admin_user_update_wit_invalid_data_return_200(self,update_category,authenticate):
        authenticate(is_staff=True)
        updated_category = {'title':''}
        response = update_category(updated_category)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestDeleteCategory: 
    def test_if_anonyous_user_Delete_return_401(self,delete_category):
        response = delete_category()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_autenticated_user_Delete_return_403(self,authenticate,delete_category):
        authenticate()
        response = delete_category()

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_admin_user_Delete_return_(self,authenticate,delete_category):
        authenticate(is_staff=True)
        response = delete_category()

        assert response.status_code == status.HTTP_204_NO_CONTENT
