from django.http import HttpResponse
from django.core import serializers
from http import HTTPStatus
from .forms import UploadImageForm
from .models import Restaurant, Dish
from django.contrib.auth import authenticate, login, logout
import json

UTF8 = 'utf-8'
JSON = 'json'
USERNAME = 'username'
PASSWORD = 'password'
NAME = 'name'
ADDRESS = 'address'
TAGS = 'tags'
IMAGE = 'image'
DESCRIPTION = 'description'
PRICE = 'price'
INVALID_CREDENTIALS = 'Credentials are invalid'
INVALID_IMAGE = 'Image is invalid'
USER_MUST_LOG_IN = 'User must log in'
METHOD_NOT_SUPPORTED = 'Method is not supported'
METHOD_ALLOWED_FOR_OWNER_ONLY = 'Method is allowed for the owner of the object only'
RESTAURANT_NOT_FOUND = 'Cannot find restaurant'
DISH_NOT_FOUND = 'Cannot find dish'
GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'

"""
method for logging user in
"""
def user_login(request):

    # get request body
    body = json.loads(request.body.decode(UTF8))

    # authenticate user
    user = authenticate(request, username=body.get(
        USERNAME), password=body.get(PASSWORD))

    # if user can be authenticated, log user in
    if user is not None:
        login(request, user)

        # return 200 response
        return HttpResponse()
    else:

        # return 401 error if user can not be authenticated
        return HttpResponse(status=HTTPStatus.UNAUTHORIZED, reason=INVALID_CREDENTIALS)

"""
method for logging user out
"""
def user_logout(request):

    # log user out
    logout(request)

"""
method for returning all restaurants or creating new restaurant
"""
def restaurant_list(request):

    # GET
    if request.method == GET:

        # return 200 response and all restaurants
        return HttpResponse(serializers.serialize(JSON, Restaurant.objects.all()))

    # POST
    elif request.method == POST:

        # authenticate user
        if not request.user.is_authenticated:
            return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=USER_MUST_LOG_IN)

        # get body of request
        body = json.loads(request.body.decode(UTF8))

        # create new restaurant
        new_restaurant = Restaurant(owner=request.user, name=body.get(NAME), address=body.get(ADDRESS), tags=body.get(TAGS))
        new_restaurant.save()
    else:

        # return 405 error if method is not supported
        return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=METHOD_NOT_SUPPORTED)

"""
method for retrieving, updating or deleting a restaurant by id
"""
def restaurant_detail(request, restaurant_id):

    # GET
    if request.method == GET:

        # get restaurant by id
        try:
            query_set = Restaurant.objects.filter(pk=restaurant_id)
        except Restaurant.DoesNotExist:

            # return 404 error if restaurant is not found
            return HttpResponse(status=HTTPStatus.NOT_FOUND, reason=RESTAURANT_NOT_FOUND)

        # return 200 response and the found restaurant
        return HttpResponse(serializers.serialize(JSON, query_set))

    # PUT
    elif request.method == PUT:

        # authenticate user
        if not request.user.is_authenticated:

            # return 405 if user can not be authenticated
            return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=USER_MUST_LOG_IN)

        # get body of request
        body = json.loads(request.body.decode(UTF8))

        # get restaurant by id
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:

            # return 404 error if restaurant is not found
            return HttpResponse(status=HTTPStatus.NOT_FOUND, reason=RESTAURANT_NOT_FOUND)

        # check if user is the owner of restaurant
        if not restaurant.owner == request.user:

            # return 405 error if user is not the owner of restaurant
            return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=METHOD_ALLOWED_FOR_OWNER_ONLY)

        # update the found restaurant
        restaurant.name = body.get(NAME)
        restaurant.address = body.get(ADDRESS)
        restaurant.tags = body.get(TAGS)
        restaurant.save()

        # return 200 response
        return HttpResponse()

    # DELETE
    elif request.method == DELETE:

        # authenticate user
        if not request.user.is_authenticated:

            # return 405 if user can not be authenticated
            return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=USER_MUST_LOG_IN)

        # get restaurant by id
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:

            # return 404 error if restaurant is not found
            return HttpResponse(status=HTTPStatus.NOT_FOUND, reason=RESTAURANT_NOT_FOUND)

        # check if user is the owner of restaurant
        if not restaurant.owner == request.user:

            # return 405 error if user is not the owner of restaurant
            return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=METHOD_ALLOWED_FOR_OWNER_ONLY)

        # delete restaurant
        restaurant.delete()

        # return 200 response
        return HttpResponse()
    else:

        # return 405 error if method is not supported
        return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=METHOD_NOT_SUPPORTED)

"""
method for uploading image for a restaurant by id
"""
def restaurant_upload_image(request, restaurant_id):

    # POST
    if request.method == POST:

        # authenticate user
        if not request.user.is_authenticated:

            # return 405 if user can not be authenticated
            return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=USER_MUST_LOG_IN)

        # get restaurant by id
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:

            # return 404 error if restaurant is not found
            return HttpResponse(status=HTTPStatus.NOT_FOUND, reason=RESTAURANT_NOT_FOUND)

        # check if user is the owner of restaurant
        if not restaurant.owner == request.user:

            # return 405 error if user is not the owner of restaurant
            return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=METHOD_ALLOWED_FOR_OWNER_ONLY)

        # get form
        form = UploadImageForm(request.POST, request.FILES)

        # if form is valid
        if form.is_valid():

            # save restaurant image
            restaurant.image = request.FILES[IMAGE]
            restaurant.save()

            # return 200 response
            return HttpResponse()
        else:

            # return 422 error if image is invalid
            return HttpResponse(status=HTTPStatus.UNPROCESSABLE_ENTITY, reason=INVALID_IMAGE)
    else:

        # return 405 error if method is not supported
        return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=METHOD_NOT_SUPPORTED)

"""
method for retrieving all dishes of a restaurant by id
"""
def dish_list(request, restaurant_id):

    # GET
    if request.method == GET:

        # get restaurant by id
        try:
            restaurant = Restaurant.objects.get(restaurant_id)
        except Restaurant.DoesNotExist:

            # return 404 error if restaurant is not found
            return HttpResponse(status=HTTPStatus.NOT_FOUND, reason=RESTAURANT_NOT_FOUND)

        # return 200 response and dishes of found restaurant
        return HttpResponse(serializers.serialize(JSON, restaurant.dish_set.all()))

    # POST
    elif request.method == POST:

        # authenticate user
        if not request.user.is_authenticated:

            # return 405 if user can not be authenticated
            return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=USER_MUST_LOG_IN)

        # get body of request
        body = json.loads(request.body.decode(UTF8))

        # get restaurant by id
        try:
            restaurant = Restaurant.objects.get(restaurant_id)
        except Restaurant.DoesNotExist:

            # return 404 error if restaurant is not found
            return HttpResponse(status=HTTPStatus.NOT_FOUND, reason=RESTAURANT_NOT_FOUND)

        # create new dish
        new_dish = Dish(name=body.get(NAME), description=body.get(DESCRIPTION),
                        price=body.get(PRICE), restaurant=restaurant)
        new_dish.save()

        # return 201 response
        return HttpResponse(status=HTTPStatus.CREATED)
    else:

        # return 405 error if method is not supported
        return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=METHOD_NOT_SUPPORTED)

"""
method for retrieving, updating and deleting a dish by id of a restaurant by id
"""
def dish_detail(request, restaurant_id, dish_id):

    # GET
    if request.method == GET:

        # get dish by id
        try:
            query_set = Dish.objects.filter(pk=dish_id)
        except Dish.DoesNotExist:

            # return 404 error if dish is not found
            return HttpResponse(status=HTTPStatus.NOT_FOUND, reason=DISH_NOT_FOUND)

        # return 200 response and the found dish
        return HttpResponse(serializers.serialize(JSON, query_set))

    # PUT
    elif request.method == PUT:

        # authenticate user
        if not request.user.is_authenticated:

            # return 405 if user can not be authenticated
            return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=USER_MUST_LOG_IN)

        # get restaurant by id
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:

            # return 404 error if restaurant is not found
            return HttpResponse(status=HTTPStatus.NOT_FOUND, reason=RESTAURANT_NOT_FOUND)

        # check if user is the owner of restaurant
        if not restaurant.owner == request.user:

            # return 405 error if user is not the owner of restaurant
            return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=METHOD_ALLOWED_FOR_OWNER_ONLY)

        # get body of request
        body = json.loads(request.body.decode(UTF8))

        # get dish by id
        try:
            dish = Dish.objects.get(pk=dish_id)
        except Dish.DoesNotExist:

            # return 404 error if dish is not found
            return HttpResponse(status=HTTPStatus.NOT_FOUND, reason=DISH_NOT_FOUND)

        # update the found dish
        dish.name = body.get(NAME)
        dish.description = body.get(DESCRIPTION)
        dish.price = body.get(PRICE)
        dish.save()

        # return 200 response
        return HttpResponse()

    # DELETE
    elif request.method == DELETE:

        # authenticate user
        if not request.user.is_authenticated:

            # return 405 if user can not be authenticated
            return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=USER_MUST_LOG_IN)

        # get restaurant by id
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:

            # return 404 error if restaurant is not found
            return HttpResponse(status=HTTPStatus.NOT_FOUND, reason=RESTAURANT_NOT_FOUND)

        # check if user is the owner of restaurant
        if not restaurant.owner == request.user:

            # return 405 error if user is not the owner of restaurant
            return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=METHOD_ALLOWED_FOR_OWNER_ONLY)

        # get dish by id
        try:
            dish = Dish.objects.get(pk=dish_id)
        except Dish.DoesNotExist:

            # return 404 error if dish is not found
            return HttpResponse(status=HTTPStatus.NOT_FOUND, reason=DISH_NOT_FOUND)

        # delete dish
        dish.delete()

        # return 200 response
        return HttpResponse()
    else:

        # return 405 error if method is not supported
        return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=METHOD_NOT_SUPPORTED)

"""
method for uploading image for a dish by id of a restaurant by id
"""
def dish_upload_image(request, restaurant_id, dish_id):
    if request.method == POST:

        # authenticate user
        if not request.user.is_authenticated:

            # return 405 if user can not be authenticated
            return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=USER_MUST_LOG_IN)

        # get restaurant by id
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:

            # return 404 error if restaurant is not found
            return HttpResponse(status=HTTPStatus.NOT_FOUND, reason=RESTAURANT_NOT_FOUND)

        # check if user is the owner of restaurant
        if not restaurant.owner == request.user:

            # return 405 error if user is not the owner of restaurant
            return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=METHOD_ALLOWED_FOR_OWNER_ONLY)

        # get dish by id
        try:
            dish = Dish.objects.get(pk=dish_id)
        except Dish.DoesNotExist:

            # return 404 error if dish is not found
            return HttpResponse(status=HTTPStatus.NOT_FOUND, reason=DISH_NOT_FOUND)

        # get form
        form = UploadImageForm(request.POST, request.FILES)

        # if form is valid
        if form.is_valid():

            # save dish image
            dish.image = request.FILES[IMAGE]
            dish.save()

            # return 200 response
            return HttpResponse()
        else:

            # return 422 error if image is invalid
            return HttpResponse(status=HTTPStatus.UNPROCESSABLE_ENTITY, reason=INVALID_IMAGE)
    else:

        # return 405 error if method is not supported
        return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=METHOD_NOT_SUPPORTED)
