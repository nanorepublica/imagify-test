# Code Review

source: https://gist.github.com/jbma/3b7e26c595f2e4c05525b0d70f4b3605

## What do you think of that code?

This code is not particularly well written, it has a major logical error in syntax. This means the code would likely run, but not as expected. This means the `create` method would not run which would result in the ViewSet using the default `create` method and not the one in code. This is certainly code I would not want to see in production.

Please see below for more a detailed breakdown.

## Are there any issues you see?
* Unused import on line 1 & line 4
* star import on line 3, it is better to use explicit imports
* Serializer not imported on line 8
* Incorrect Indentation on line 11
* Custom Authentication (not leveraging DRF functionality) on line 12
* Not using the serializer `create` method on line 17
* `User` model not imported but is used.
* use of a `print` statement on line 24, logging ought to be used instead
* The responses on lines 13 and 25 does not return the correct HTTP status code
* The response on line 25 does not use the error messages from the serializer
* Line 15 could raise expections without catching them appropriately to return to the client which would result in HTTP code 500.

## Please describe your evaluation of this code.

If I saw this code in a PR, I would think that either the engineer is new to Python, Django & Django Rest Framework. I would not approve the PR and would take the time to coach them and point them in the direction of appropriate resources, specifically the DRF docs & http://www.cdrf.co for future reference.


## Would you write it differently? If so, please rewrite it to meet your standards and explain the reasoning behind any changes.

This code relies on the Serializer to handle more of the logic in terms of data so that is could be reused in multiple views if necessary or as a nested serializer. Also the permissions are handled by DRF using the `IsAuthenticated` class. We also do not hard code our user model by lean on the Django authentication framework to tell us the user model to use. The result is much less custom code, that is cleaner and easier to read as well as being more robust in functionality and maintainability.

```python
# serializers.py
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'password'
            'comment'
        )

# views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .serializers import UserSerializer

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated]
```
