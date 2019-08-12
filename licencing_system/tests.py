import unittest
from datetime import datetime, timedelta

from .models import Customer, Plan, Website
from .exceptions import WebsiteDoesNotExist, WebsiteAllowanceExceededException


class PlanTests(unittest.TestCase):

    def test_normal_plan(self):
        """
        Test the website limit with a normal plan
        """
        plan = Plan('basic', 49, 1)
        self.assertTrue(plan.can_website_be_created(0))
        self.assertFalse(plan.can_website_be_created(1))
        self.assertFalse(plan.can_website_be_created(4))

    def test_unlimited_plan(self):
        """
        Test the website limit with an unlimited plan
        """
        plan = Plan('infinite', 249, 0)
        self.assertTrue(plan.can_website_be_created(0))
        self.assertTrue(plan.can_website_be_created(1))
        self.assertTrue(plan.can_website_be_created(4))
        self.assertTrue(plan.can_website_be_created(4000))

    def test__str__method(self):
        'test the rendering of the __str__ method'
        plan = Plan('basic', 49, 1)
        self.assertEqual(str(plan), 'basic, 1 website @ $49')
        plan = Plan('plus', 99, 3)
        self.assertEqual(str(plan), 'plus, 3 websites @ $99')
        plan = Plan('infinite', 249, 0)
        self.assertEqual(str(plan), 'infinite, unlimited websites @ $249')

    def test_comparing_plan(self):
        basic = Plan('basic', 49, 1)
        normal = Plan('normal', 49, 1)
        plus = Plan('plus', 99, 3)
        self.assertEqual(basic, normal)
        self.assertNotEqual(basic, plus)


class WebsiteTests(unittest.TestCase):

    def setUp(self):
        self.plan = Plan('basic', 49, 1)
        self.customer = Customer('Jane Doe', 'password', 'jane.doe@example.com', self.plan)

    def test__str__method(self):
        site = Website('https://akmiller.co.uk', self.customer)
        self.assertEqual(str(site), 'https://akmiller.co.uk')

    def test_url_update(self):
        site = Website('https://akmiller.co.uk', self.customer)
        self.assertEqual(site.url, 'https://akmiller.co.uk')
        site.url = 'https://google.com'
        self.assertEqual(site.url, 'https://google.com')


class CustomerTests(unittest.TestCase):

    def setUp(self):
        self.plan = Plan('basic', 49, 1)
        self.customer = Customer('Jane Doe', 'password', 'jane.doe@example.com', self.plan)

    def test__str__method(self):
        self.assertEqual(str(self.customer), 'Jane Doe (jane.doe@example.com)')

    def test_renewal_date(self):
        in_a_year = (datetime.now() + timedelta(days=365)).date()
        self.assertEqual(self.customer.subscription_renewal_date.date(), in_a_year)

    def test_add_website_success(self):
        customer = Customer('Jane Doe', 'password', 'jane.doe@example.com', self.plan)
        website = Website('https://akmiller.co.uk', customer)
        self.assertIn(website, customer.websites)

    def test_add_website_error(self):
        customer = Customer('Jane Doe', 'password', 'jane.doe@example.com', self.plan)
        website = Website('https://akmiller.co.uk', customer)
        with self.assertRaises(WebsiteAllowanceExceededException):
            website1 = Website('https://google.co.uk', customer)

    def test_remove_website(self):
        customer = Customer('Jane Doe', 'password', 'jane.doe@example.com', self.plan)
        website = Website('https://akmiller.co.uk', customer)
        self.assertIn(website, customer.websites)
        customer.remove_website(website)
        self.assertNotIn(website, customer.websites)

    def test_remove_website_error(self):
        plus = Plan('plus', 99, 3)
        customer = Customer('Jane Doe', 'password', 'jane.doe@example.com', plus)
        website = None
        website1 = Website('https://google.co.uk', customer)
        self.assertIn(website1, customer.websites)
        with self.assertRaises(WebsiteDoesNotExist):
            customer.remove_website(website)
        self.assertIn(website1, customer.websites)

    def test_update_website(self):
        customer = Customer('Jane Doe', 'password', 'jane.doe@example.com', self.plan)
        website = Website('https://akmiller.co.uk', customer)
        self.assertEqual(website.url, 'https://akmiller.co.uk')
        customer.update_website(website, 'https://google.com')
        self.assertEqual(website.url, 'https://google.com')

    def test_update_plan(self):
        customer = Customer('Jane Doe', 'password', 'jane.doe@example.com', self.plan)
        plus = Plan('plus', 99, 3)
        self.assertEqual(customer.subscription, self.plan)
        renewal_date = customer.subscription_renewal_date
        customer.update_plan(plus)
        self.assertEqual(customer.subscription, plus)
        self.assertNotEqual(customer.subscription_renewal_date, renewal_date)


if __name__ == '__main__':
    unittest.main()
