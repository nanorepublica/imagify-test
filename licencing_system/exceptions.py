
class WebsiteAllowanceExceededException(BaseException):
    message = 'You have exceeded the number of websites for your current plan'


class WebsiteDoesNotExist(BaseException):

    def __init__(self, website):
        self.message = f'The website {website} does not exist or does not belong to you'
