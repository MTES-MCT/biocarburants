from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.models import Entity, UserRights
from api.v3.admin.urls import urlpatterns


class AdminAPITest(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.admin_email = 'superadmin@carbure.beta.gouv.fr'
        self.admin_password = 'toto'
        self.fake_admin_email = 'fakeadmin@carbure.beta.gouv.fr'
        self.fake_admin_password = 'toto'

        self.admin_user = user_model.objects.create_user(email=self.admin_email, name='Super Admin', password=self.admin_password, is_staff=True)
        self.fake_admin_user = user_model.objects.create_user(email=self.fake_admin_email, name='Super Admin', password=self.fake_admin_password)

        # let's create a few users
        self.user1 = user_model.objects.create_user(email='testuser1@toto.com', name='Le Super Testeur 1', password=self.fake_admin_password)
        self.user2 = user_model.objects.create_user(email='testuser2@toto.com', name='Le Super Testeur 2', password=self.fake_admin_password)
        self.user3 = user_model.objects.create_user(email='testuser3@toto.com', name='Testeur 3', password=self.fake_admin_password)

        # a few entities
        self.entity1, _ = Entity.objects.update_or_create(name='Le Super Producteur 1', entity_type='Producteur')
        self.entity2, _ = Entity.objects.update_or_create(name='Le Super Producteur 2', entity_type='Producteur')
        self.entity3, _ = Entity.objects.update_or_create(name='Le Super Administrateur 1', entity_type='Administrateur')
        self.entity4, _ = Entity.objects.update_or_create(name='Le Super Operateur 1', entity_type='Opérateur')
        self.entity5, _ = Entity.objects.update_or_create(name='Le Super Trader 1', entity_type='Trader')        

        # some rights
        UserRights.objects.update_or_create(user=self.user1, entity=self.entity1)
        UserRights.objects.update_or_create(user=self.user1, entity=self.entity2)
        UserRights.objects.update_or_create(user=self.user1, entity=self.entity3)
        UserRights.objects.update_or_create(user=self.user2, entity=self.entity2)
        UserRights.objects.update_or_create(user=self.user3, entity=self.entity4)

    def test_accessrights(self):
        loggedin = self.client.login(username=self.fake_admin_email, password=self.fake_admin_password)
        self.assertTrue(loggedin)
        for url in urlpatterns:
            response = self.client.get(reverse(url.name))
            self.assertEqual(response.status_code, 403)
        loggedin = self.client.login(username=self.admin_email, password=self.admin_password)
        self.assertTrue(loggedin)
        for url in urlpatterns:
            response = self.client.get(reverse(url.name))
            self.assertNotEqual(response.status_code, 403)
            

    def test_get_users(self):
        # login as an admin
        loggedin = self.client.login(username=self.admin_email, password=self.admin_password)
        self.assertTrue(loggedin)

        response = self.client.get(reverse('api-v3-admin-get-users'))
        # api works
        self.assertEqual(response.status_code, 200)
        # and returns at least 3 users
        self.assertGreaterEqual(len(response.json()['data']), 3)
        # check if querying works
        response = self.client.get(reverse('api-v3-admin-get-users') + '?q=super')
        # works
        self.assertEqual(response.status_code, 200)
        # and returns at least 2 users
        data = response.json()['data']
        self.assertGreaterEqual(len(data), 2)
        # check if the content is correct
        random_user = data[0]
        self.assertIn('email', random_user)
        self.assertIn('name', random_user)


    def test_get_entities(self):
        # login as an admin
        loggedin = self.client.login(username=self.admin_email, password=self.admin_password)
        self.assertTrue(loggedin)

        response = self.client.get(reverse('api-v3-admin-get-entities'))
        # api works
        self.assertEqual(response.status_code, 200)
        # and returns at least 5 entities
        self.assertGreaterEqual(len(response.json()['data']), 5)
        # check if querying works
        response = self.client.get(reverse('api-v3-admin-get-entities') + '?q=prod')
        # works
        self.assertEqual(response.status_code, 200)
        # and returns at least 2 entities
        data = response.json()['data']
        self.assertGreaterEqual(len(data), 2)
        # check if the content is correct
        random_entity = data[0]
        self.assertIn('entity_type', random_entity)
        self.assertIn('name', random_entity)


    def test_get_rights(self):
        # login as an admin
        loggedin = self.client.login(username=self.admin_email, password=self.admin_password)
        self.assertTrue(loggedin)

        response = self.client.get(reverse('api-v3-admin-get-rights'))
        # api works
        self.assertEqual(response.status_code, 200)
        # and returns at least 5 rights
        lenallrights = len(response.json()['data'])
        self.assertGreaterEqual(lenallrights, 5)
        # check if querying works
        response = self.client.get(reverse('api-v3-admin-get-rights') + '?q=prod')
        # works
        self.assertEqual(response.status_code, 200)
        # and returns less rights than before
        filtered_rights = response.json()['data']
        lenfilteredrights = len(filtered_rights)
        self.assertGreater(lenallrights, lenfilteredrights)
        # check if the content is correct
        random_right = filtered_rights[0]
        self.assertIn('entity_type', random_right)
        self.assertIn('entity', random_right)
        self.assertIn('name', random_right)
        self.assertIn('email', random_right)


    def test_create_user(self):
        loggedin = self.client.login(username=self.admin_email, password=self.admin_password)
        self.assertTrue(loggedin)
        response = self.client.post(reverse('api-v3-admin-add-user'), {'name': 'Jean-Claude Test', 'email': 'jc.test@pouet.net'})
        self.assertEquals(response.status_code, 200)

        # check if user actually exists
        response = self.client.get(reverse('api-v3-admin-get-users') + '?q=jc.test@pouet.net')
        self.assertEqual(response.status_code, 200)
        # and returns 1 user
        jc = response.json()['data'][0]
        self.assertEqual(jc['email'], 'jc.test@pouet.net')

        # try to enter incorrect data
        response = self.client.post(reverse('api-v3-admin-add-user'))
        self.assertEqual(response.status_code, 400)
        response = self.client.post(reverse('api-v3-admin-add-user'), {'email': 'jc.test@pouet.net'})
        self.assertEqual(response.status_code, 400)
        response = self.client.post(reverse('api-v3-admin-add-user'), {'name': 'Jean-Claude Test'})
        self.assertEqual(response.status_code, 400)



    def test_create_entity(self):
        loggedin = self.client.login(username=self.admin_email, password=self.admin_password)
        self.assertTrue(loggedin)
        response = self.client.post(reverse('api-v3-admin-add-entity'), {'name': 'Société Test', 'category': 'Producteur'})
        self.assertEquals(response.status_code, 200)
        # check if user actually exists
        response = self.client.get(reverse('api-v3-admin-get-users') + '?q=jc.test@pouet.net')
        self.assertEqual(response.status_code, 200)
        # and returns 1 user
        jc = response.json()['data'][0]
        self.assertEqual(jc['email'], 'jc.test@pouet.net')

        # make sure all categories are supported
        response = self.client.post(reverse('api-v3-admin-add-entity'), {'name': 'Opérateur Test', 'category': 'Opérateur'})
        obj = Entity.objects.get(name='Opérateur Test')
        self.assertEquals(obj.entity_type, 'Opérateur')
        response = self.client.post(reverse('api-v3-admin-add-entity'), {'name': 'Trader Test', 'category': 'Trader'})
        obj = Entity.objects.get(name='Trader Test')
        self.assertEquals(obj.entity_type, 'Trader')        
        response = self.client.post(reverse('api-v3-admin-add-entity'), {'name': 'Admin Test', 'category': 'Administrateur'})
        obj = Entity.objects.get(name='Admin Test')
        self.assertEquals(obj.entity_type, 'Administrateur')


        # try to enter incorrect data
        response = self.client.post(reverse('api-v3-admin-add-user'))
        self.assertEqual(response.status_code, 400)
        response = self.client.post(reverse('api-v3-admin-add-user'), {'email': 'jc.test@pouet.net'})
        self.assertEqual(response.status_code, 400)
        response = self.client.post(reverse('api-v3-admin-add-user'), {'name': 'Jean-Claude Test'})
        self.assertEqual(response.status_code, 400)


    def test_create_right(self):
        loggedin = self.client.login(username=self.admin_email, password=self.admin_password)
        self.assertTrue(loggedin)

        # first RO call to api:
        response = self.client.get(reverse('api-v3-admin-get-rights'))
        self.assertEqual(response.status_code, 200)        
        prev_len = len(response.json()['data'])

        # create right
        response = self.client.post(reverse('api-v3-admin-add-rights'), {'user_id': self.user3.id, 'entity_id': self.entity5.id})
        self.assertEquals(response.status_code, 200)

        # check if right has been created
        obj = UserRights.objects.get(user=self.user3, entity=self.entity5)
        self.assertEquals(obj.user.id, self.user3.id)
        self.assertEquals(obj.entity.id, self.entity5.id)

        # check than api get-rights len has increased
        response = self.client.get(reverse('api-v3-admin-get-rights'))
        self.assertEqual(response.status_code, 200)
        new_len = len(response.json()['data'])
        self.assertGreater(new_len, prev_len)

        # check if search function works
        response = self.client.get(reverse('api-v3-admin-get-rights') + '?q=Admin%20Test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), 1)

        # try to enter incorrect data
        response = self.client.post(reverse('api-v3-admin-add-rights'), {'user_id': "pouet pouet", 'entity_id': self.entity5.id})
        self.assertEqual(response.status_code, 400)
        response = self.client.post(reverse('api-v3-admin-add-rights'), {'user_id': self.user3.id, 'entity_id': "pouet pouet"})
        self.assertEqual(response.status_code, 400)
        response = self.client.post(reverse('api-v3-admin-add-rights'), {'user_id': self.user3.id})
        self.assertEqual(response.status_code, 400)
        response = self.client.post(reverse('api-v3-admin-add-rights'), {'entity_id': self.entity5.id})
        self.assertEqual(response.status_code, 400)


    def test_delete_user(self):
        loggedin = self.client.login(username=self.admin_email, password=self.admin_password)
        self.assertTrue(loggedin)

        response = self.client.post(reverse('api-v3-admin-add-user'), {'name': 'Jean-Claude Test', 'email': 'jc.test@pouet.net'})
        self.assertEquals(response.status_code, 200)

        # check if user is created
        response = self.client.get(reverse('api-v3-admin-get-users') + '?q=jc.test@pouet.net')
        self.assertEqual(response.status_code, 200)
        user_id = response.json()['data'][0]['id']

        # delete user
        response = self.client.post(reverse('api-v3-admin-delete-users'), {'user_id': user_id})
        self.assertEqual(response.status_code, 200)        

        # check if user is deleted
        response = self.client.get(reverse('api-v3-admin-get-users') + '?q=jc.test@pouet.net')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), 0)


    def test_delete_entity(self):
        pass
    
    def test_delete_right(self):
        pass

    def test_reset_password(self):
        pass