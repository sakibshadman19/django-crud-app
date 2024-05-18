from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Parent, Child

class ParentViewSetTests(APITestCase):

    def setUp(self):
        self.parent_data = {
            'first_name': 'Shadman',
            'last_name': 'Sakib',
            'street': 'Khilgaon',
            'city': 'Dhaka',
            'state': 'Sabujbagh',
            'zip_code': '1214'
        }
        self.parent = Parent.objects.create(**self.parent_data)

    def test_create_parent(self):
        url = reverse('parent-list')
        response = self.client.post(url, self.parent_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Parent.objects.count(), 2)
        self.assertEqual(Parent.objects.get(id=response.data['id']).first_name, 'Shadman')

    def test_create_parent_missing_fields(self):
        url = reverse('parent-list')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Missing required fields', response.data['error'])

    def test_retrieve_parent(self):
        url = reverse('parent-detail', kwargs={'pk': self.parent.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.parent.first_name)

    def test_update_parent(self):
        url = reverse('parent-detail', kwargs={'pk': self.parent.pk})
        updated_data = {'first_name': 'Jane'}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.parent.refresh_from_db()
        self.assertEqual(self.parent.first_name, 'Jane')

    def test_update_parent_not_exist(self):
        url = reverse('parent-detail', kwargs={'pk': 999})
        updated_data = {'first_name': 'Jane'}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Parent not found. Please create the parent first.', response.data['error'])

    def test_delete_parent_with_children(self):
        child = Child.objects.create(first_name='Johnny', last_name='Sakib', parent=self.parent)
        url = reverse('parent-detail', kwargs={'pk': self.parent.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Cannot delete parent with existing children', response.data['error'])

    def test_delete_parent_without_children(self):
        url = reverse('parent-detail', kwargs={'pk': self.parent.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Parent.objects.count(), 0)

    def test_delete_parent_not_exist(self):
        url = reverse('parent-detail', kwargs={'pk': 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Parent not found.', response.data['error'])


class ChildViewSetTests(APITestCase):

    def setUp(self):
        self.parent = Parent.objects.create(
            first_name='Shadman',
            last_name='Sakib',
            street='Khilgaon',
            city='Dhaka',
            state='Sabujbagh',
            zip_code='1214'
        )
        self.child_data = {
            'first_name': 'Johnny',
            'last_name': 'Sakib',
            'parent': self.parent.id
        }
        self.child = Child.objects.create(
            first_name='Johnny',
            last_name='Sakib',
            parent=self.parent
        )

    def test_create_child(self):
        url = reverse('child-list')
        response = self.client.post(url, self.child_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Child.objects.count(), 2)
        self.assertEqual(Child.objects.get(id=response.data['id']).first_name, 'Johnny')

    def test_create_child_missing_fields(self):
        url = reverse('child-list')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Missing required fields', response.data['error'])

    def test_retrieve_child(self):
        url = reverse('child-detail', kwargs={'pk': self.child.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.child.first_name)

    def test_update_child(self):
        url = reverse('child-detail', kwargs={'pk': self.child.pk})
        updated_data = {'first_name': 'Janet'}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.child.refresh_from_db()
        self.assertEqual(self.child.first_name, 'Janet')
        
    def test_update_child_not_exist(self):
        url = reverse('child-detail', kwargs={'pk': 999})
        updated_data = {'first_name': 'Janet'}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Child not found.', response.data['error'])

    def test_delete_child(self):
        url = reverse('child-detail', kwargs={'pk': self.child.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Child.objects.count(), 0)

    def test_delete_child_not_exist(self):
        url = reverse('child-detail', kwargs={'pk': 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Child not found.', response.data['error'])
