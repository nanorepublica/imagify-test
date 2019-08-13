import logging
from datetime import datetime, timedelta

from .exceptions import WebsiteAllowanceExceededException, WebsiteDoesNotExist

logger = logging.getLogger(__name__)


class Plan:
    """
    Class representing a Pricing Plan
    """

    def __init__(self, name: str, price: float, website_allowance: int) -> None:
        self.name = name
        self.price = price
        self.website_allowance = website_allowance
        self.unlimited_websites = website_allowance == 0

    def __str__(self):
        s = '' if self.website_allowance == 1 else 's'
        website_count = self.website_allowance if self.website_allowance != 0 else 'unlimited'
        return f'{self.name}, {website_count} website{s} @ ${self.price}'

    def __eq__(self, other):
        if self.price == other.price and self.website_allowance == other.website_allowance:
            return True
        return False

    def can_website_be_created(self, current_website_count: int):
        if self.unlimited_websites:
            return True
        if current_website_count < self.website_allowance:
            return True
        return False


class Customer:
    "Class representing a customer"
    def __init__(self, name: str, password: str, email: str, subscription: Plan) -> None:
        self.name = name
        self.password = password
        self.email = email
        self.subscription = subscription
        self.update_renewal_date()
        self._websites = []

    def __str__(self):
        return f'{self.name} ({self.email})'

    def update_renewal_date(self):
        self.subscription_renewal_date = datetime.now() + timedelta(days=365)

    @property
    def websites(self):
        return self._websites

    def add_website(self, website):
        if self.subscription.can_website_be_created(len(self._websites)):
            self._websites.append(website)
        else:
            raise WebsiteAllowanceExceededException()

    def remove_website(self, website):
        try:
            self._websites.remove(website)
            del website
        except ValueError:
            raise WebsiteDoesNotExist(website)

    def update_website(self, website, new_url):
        website_idx = self._websites.index(website)
        site = self._websites[website_idx]
        site.url = new_url

    def update_plan(self, new_plan):
        if self.subscription != new_plan:
            self.subscription = new_plan
            self.update_renewal_date()
        else:
            logger.info('Already on this plan')


class Website:
    "Class representing a website"

    def __init__(self, url: str, customer: Customer) -> None:
        self._url = url
        self.customer = customer
        customer.add_website(self)

    def __str__(self):
        return self.url

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
