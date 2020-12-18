from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.models import Entity, UserRights, Pays, MatierePremiere, Biocarburant, Depot, EntityDepot
from producers.models import ProductionSite, ProductionSiteInput, ProductionSiteOutput
from api.v3.admin.urls import urlpatterns


class SettingsAPITest(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user_email = 'testuser1@toto.com'
        self.user_password = 'totopouet'
        self.user1 = user_model.objects.create_user(email=self.user_email, name='Le Super Testeur 1', password=self.user_password)

        # a few entities
        self.entity1, _ = Entity.objects.update_or_create(name='Le Super Producteur 1', entity_type='Producteur')
        self.entity2, _ = Entity.objects.update_or_create(name='Le Super Operateur 1', entity_type='Opérateur')
        self.entity3, _ = Entity.objects.update_or_create(name='Le Super Trader 1', entity_type='Trader')

        # some rights
        UserRights.objects.update_or_create(user=self.user1, entity=self.entity1)
        UserRights.objects.update_or_create(user=self.user1, entity=self.entity2)         

        loggedin = self.client.login(username=self.user_email, password=self.user_password)
        self.assertTrue(loggedin)

    def test_get_settings(self):
        url = 'api-v3-settings-get'
        response = self.client.get(reverse(url))
        # api works
        self.assertEqual(response.status_code, 200)
        data = response.json()['data']
        self.assertIn('rights', data)
        self.assertIn('email', data)
        self.assertIn('requests', data)

    def test_mac_option(self):
        url_enable = 'api-v3-settings-enable-mac'
        url_disable = 'api-v3-settings-disable-mac'

        # wrongly formatted
        response = self.client.post(reverse(url_enable), {'entity_id':'blablabla'})
        self.assertEqual(response.status_code, 400)
        # no entity_id
        response = self.client.post(reverse(url_enable))
        self.assertEqual(response.status_code, 400)
        # entity I do not belong to
        response = self.client.post(reverse(url_enable), {'entity_id': self.entity3.id})
        self.assertEqual(response.status_code, 403)
        # should pass
        response = self.client.post(reverse(url_enable), {'entity_id': self.entity2.id})
        self.assertEqual(response.status_code, 200)
        entity = Entity.objects.get(id=self.entity2.id)
        self.assertEqual(entity.has_mac, True)

        # disable:
        # wrongly formatted
        response = self.client.post(reverse(url_disable), {'entity_id':'blablabla'})
        self.assertEqual(response.status_code, 400)
        # no entity_id
        response = self.client.post(reverse(url_disable))
        self.assertEqual(response.status_code, 400)
        # entity I do not belong to
        response = self.client.post(reverse(url_disable), {'entity_id': self.entity3.id})
        self.assertEqual(response.status_code, 403)
        # should pass
        response = self.client.post(reverse(url_disable), {'entity_id': self.entity2.id})
        self.assertEqual(response.status_code, 200)
        entity = Entity.objects.get(id=self.entity2.id)
        self.assertEqual(entity.has_mac, False)        

        # revert
        response = self.client.post(reverse(url_enable), {'entity_id': self.entity2.id})
        self.assertEqual(response.status_code, 200)
        entity = Entity.objects.get(id=self.entity2.id)
        self.assertEqual(entity.has_mac, True)

    def test_trading_option(self):
        url_enable = 'api-v3-settings-enable-trading'
        url_disable = 'api-v3-settings-disable-trading'

        # wrongly formatted
        response = self.client.post(reverse(url_enable), {'entity_id':'blablabla'})
        self.assertEqual(response.status_code, 400)
        # no entity_id
        response = self.client.post(reverse(url_enable))
        self.assertEqual(response.status_code, 400)
        # entity I do not belong to
        response = self.client.post(reverse(url_enable), {'entity_id': self.entity3.id})
        self.assertEqual(response.status_code, 403)
        # should pass
        response = self.client.post(reverse(url_enable), {'entity_id': self.entity1.id})
        self.assertEqual(response.status_code, 200)
        entity = Entity.objects.get(id=self.entity1.id)
        self.assertEqual(entity.has_trading, True)

        # disable:
        # wrongly formatted
        response = self.client.post(reverse(url_disable), {'entity_id':'blablabla'})
        self.assertEqual(response.status_code, 400)
        # no entity_id
        response = self.client.post(reverse(url_disable))
        self.assertEqual(response.status_code, 400)
        # entity I do not belong to
        response = self.client.post(reverse(url_disable), {'entity_id': self.entity3.id})
        self.assertEqual(response.status_code, 403)
        # should pass
        response = self.client.post(reverse(url_disable), {'entity_id': self.entity1.id})
        self.assertEqual(response.status_code, 200)
        entity = Entity.objects.get(id=self.entity1.id)
        self.assertEqual(entity.has_trading, False)        

        # revert
        response = self.client.post(reverse(url_enable), {'entity_id': self.entity1.id})
        self.assertEqual(response.status_code, 200)
        entity = Entity.objects.get(id=self.entity1.id)
        self.assertEqual(entity.has_trading, True)

        # should not work on Operator
        response = self.client.post(reverse(url_enable), {'entity_id': self.entity2.id})
        self.assertEqual(response.status_code, 400)

    def test_set_national_system_certificate(self):
        url = 'api-v3-settings-set-national-system-certificate'
        certificate_id = 'SV-BLABLABLA'

        # wrongly formatted arg
        response = self.client.post(reverse(url), {'entity_id': 'TOTO', 'national_system_certificate': certificate_id})
        self.assertEqual(response.status_code, 400)        
        # missing arguments
        response = self.client.post(reverse(url), {'entity_id': self.entity2.id})
        self.assertEqual(response.status_code, 400)
        response = self.client.post(reverse(url), {'national_system_certificate': certificate_id})
        self.assertEqual(response.status_code, 400)

        # reject if trader
        response = self.client.post(reverse(url), {'entity_id': self.entity3.id, 'national_system_certificate': certificate_id})
        self.assertEqual(response.status_code, 403)        

        # should pass
        response = self.client.post(reverse(url), {'entity_id': self.entity2.id, 'national_system_certificate': certificate_id})
        self.assertEqual(response.status_code, 200)
        # check
        entity = Entity.objects.get(id=self.entity2.id)
        self.assertEqual(entity.national_system_certificate, certificate_id)


    def test_production_sites_settings(self):
        url_get = 'api-v3-settings-get-production-sites'
        url_add = 'api-v3-settings-add-production-site'
        url_update = 'api-v3-settings-update-production-site'
        url_delete = 'api-v3-settings-delete-production-site'
        url_set_mps = 'api-v3-settings-set-production-site-matieres-premieres'
        url_set_bcs = 'api-v3-settings-set-production-site-biocarburants'

        # get - 0 sites
        response = self.client.get(reverse(url_get), {'entity_id': self.entity1.id})
        self.assertEqual(response.status_code, 200)
        data = response.json()['data']
        self.assertEqual(len(data), 0)
        # add 1
        france, _ = Pays.objects.update_or_create(code_pays='FR', name='France')
        psite = {'country_code':'FR', 'name':'Site prod 1', 
                 'date_mise_en_service': '2020-12-01', 'ges_option': 'ACTUAL', 
                 'entity_id': self.entity1.id, 'eligible_dc': 'true', 
                 'dc_reference': 'DC-FR-12-493', 'site_id': 'FR0001', 
                 'city':'Seynod', 'postal_code':'74600', 
                 'manager_name':'Gaston Gasoil', 'manager_phone': '0145247000', 
                 'manager_email':'g.gasoil@superpetrole.com'}
        response = self.client.post(reverse(url_add), psite)
        self.assertEqual(response.status_code, 200)        
        # check in db
        site = ProductionSite.objects.get(site_id='FR0001')
        # update 
        psite['postal_code'] = '75018'
        psite['production_site_id'] = site.id
        response = self.client.post(reverse(url_update), psite)
        self.assertEqual(response.status_code, 200)   
        site = ProductionSite.objects.get(site_id='FR0001')
        self.assertEqual(site.postal_code, '75018')
        # set mps/bcs
        MatierePremiere.objects.update_or_create(code='COLZA', name='Colza')
        MatierePremiere.objects.update_or_create(code='BEETROOT', name='Betterave')
        Biocarburant.objects.update_or_create(code='ETH', name='Ethanol')
        Biocarburant.objects.update_or_create(code='HVO', name='HVO')

        response = self.client.post(reverse(url_set_mps), {'production_site_id': site.id, 'matiere_premiere_codes': ['COLZA', 'BEETROOT']})
        self.assertEqual(response.status_code, 200)   
        response = self.client.post(reverse(url_set_bcs), {'production_site_id': site.id, 'biocarburant_codes': ['ETH', 'HVO']})
        self.assertEqual(response.status_code, 200)   
        # check
        inputs = ProductionSiteInput.objects.filter(production_site=site)
        outputs = ProductionSiteOutput.objects.filter(production_site=site)
        self.assertEqual(len(inputs), 2)
        self.assertEqual(len(outputs), 2)

        # delete
        response = self.client.post(reverse(url_delete), psite)
        self.assertEqual(response.status_code, 200)   
        # get - 0 sites
        response = self.client.get(reverse(url_get), {'entity_id': self.entity1.id})
        self.assertEqual(response.status_code, 200)
        data = response.json()['data']
        self.assertEqual(len(data), 0)

    def test_delivery_sites_settings(self):
        url_get = 'api-v3-settings-get-delivery-sites'
        url_add = 'api-v3-settings-add-delivery-site'
        url_delete = 'api-v3-settings-delete-delivery-site'
        # get 0
        response = self.client.get(reverse(url_get), {'entity_id': self.entity1.id})
        self.assertEqual(response.status_code, 200)
        data = response.json()['data']
        self.assertEqual(len(data), 0)
        # add
        france, _ = Pays.objects.update_or_create(code_pays='FR', name='France')
        depot, _ = Depot.objects.update_or_create(depot_id='TEST', name='toto', city='paris', country=france)
        postdata = {'entity_id': self.entity1.id, 'delivery_site_id': depot.depot_id, 'ownership_type': 'OWN'}
        response = self.client.post(reverse(url_add), postdata)
        self.assertEqual(response.status_code, 200)
        # get 1
        response = self.client.get(reverse(url_get), {'entity_id': self.entity1.id})
        self.assertEqual(response.status_code, 200)
        data = response.json()['data']
        self.assertEqual(len(data), 1)
        # delete
        response = self.client.post(reverse(url_delete), {'entity_id': self.entity1.id, 'delivery_site_id':depot.depot_id})
        self.assertEqual(response.status_code, 200)        
        # get 0
        response = self.client.get(reverse(url_get), {'entity_id': self.entity1.id})
        self.assertEqual(response.status_code, 200)
        data = response.json()['data']
        self.assertEqual(len(data), 0)

    def test_iscc_certificates(self):
        pass