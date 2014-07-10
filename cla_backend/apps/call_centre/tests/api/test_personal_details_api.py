from core.tests.mommy_utils import make_recipe
from core.tests.test_base import CLAOperatorAuthBaseApiTestMixin
from django.core.urlresolvers import reverse
from legalaid.tests.views.mixins.resource import \
    NestedSimpleResourceCheckAPIMixin
from rest_framework import status
from rest_framework.test import APITestCase


class PersonalDetailsTestCase(CLAOperatorAuthBaseApiTestMixin,
                              NestedSimpleResourceCheckAPIMixin, APITestCase):

   CHECK_RECIPE = 'legalaid.personal_details'
   BASE_NAME = 'personaldetails'

   @property
   def check_keys(self):
       return \
           [
               'reference',
               'title',
               'full_name',
               'postcode',
               'street',
               'mobile_phone',
               'home_phone'
           ]

   def get_http_authorization(self):
        return 'Bearer %s' % self.token

   def _get_default_post_data(self):
       return {
           'title': 'MR',
           'full_name': 'John Doe',
           'postcode': 'SW1H 9AJ',
           'street': '102 Petty France',
           'mobile_phone': '0123456789',
           'home_phone': '9876543210',
       }

   def _create(self, data=None, url=None):
       if not url:
           self.check_case.personal_details = None
           self.check_case.save()
       return super(PersonalDetailsTestCase, self)._create(data=data, url=url)

   def _test_method_in_error(self, method, url):
       """
       Generic method called by 'create' and 'patch' to test against validation
       errors.
       """
       data={
           "title": '1'*21,
           "full_name": '1'*456,
           "postcode": '1'*13,
           "street": '1'*256,
           "mobile_phone": '1'*21,
           "home_phone": '1'*21,
           }

       method_callable = getattr(self.client, method)
       response = method_callable(url, data,
                                  format='json',
                                  HTTP_AUTHORIZATION='Bearer %s' % self.token)
       self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

       expected_errors = {
           'title': [u'Ensure this value has at most 20 characters (it has 21).'],
           'full_name': [u'Ensure this value has at most 400 characters (it has 456).'],
           'postcode': [u'Ensure this value has at most 12 characters (it has 13).'],
           'street': [u'Ensure this value has at most 255 characters (it has 256).'],
           'mobile_phone': [u'Ensure this value has at most 20 characters (it has 21).'],
           'home_phone': [u'Ensure this value has at most 20 characters (it has 21).'],
           }

       self.maxDiff = None
       errors = response.data
       self.assertItemsEqual(
           errors.keys(), expected_errors.keys()
       )
       self.assertItemsEqual(
           errors,
           expected_errors
       )

   def assertPersonalDetailsEqual(self, data, obj):
       if data is None or obj is None:
           self.assertEqual(data, obj)
       else:
           for prop in ['title', 'full_name', 'postcode', 'street', 'mobile_phone', 'home_phone']:
               self.assertEqual(unicode(getattr(obj, prop)), data[prop])

   def test_methods_not_allowed(self):
       """
       Ensure that we can't POST, PUT or DELETE
       """
       ### LIST
       if hasattr(self, 'list_url') and self.list_url:
           self._test_delete_not_allowed(self.list_url)

   def test_methods_in_error(self):
       self._test_method_in_error('patch', self.detail_url)
       self._test_method_in_error('put', self.detail_url)

       # CREATE

   def test_create_no_data(self):
       """
       CREATE should work, even with an empty POST
       """
       response = self._create()
       self.assertEqual(response.status_code, status.HTTP_201_CREATED)
       self.assertCheckResponseKeys(response)

   def test_create_with_data(self):
       data = self._get_default_post_data()
       check = make_recipe('legalaid.personal_details', **data)

       response = self._create(data=data)
       # check initial state is correct

       self.assertEqual(response.status_code, status.HTTP_201_CREATED)
       self.assertCheckResponseKeys(response)

       self.assertPersonalDetailsEqual(response.data, check)