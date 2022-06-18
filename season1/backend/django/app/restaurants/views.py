from django.http import HttpResponse
from django.core import serializers
from http import HTTPStatus
from .forms import RestaurantForm, DishForm, UploadImageForm
from .models import Restaurant, Dish
from django.views.decorators.csrf import csrf_exempt
import json

UTF8 = 'utf-8'
JSON = 'json'
NAME = 'name'
ADDRESS = 'address'
TAGS = 'tags'
IMAGE = 'image'
DESCRIPTION = 'description'
PRICE = 'price'
INVALID_IMAGE = 'Image is invalid'
INVALID_FORM = 'Form is invalid'
METHOD_NOT_SUPPORTED = 'Method is not supported'
RESTAURANT_NOT_FOUND = 'Cannot find restaurant'
DISH_NOT_FOUND = 'Cannot find dish'
GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'

"""
method for returning all restaurants or creating new restaurant
"""
@csrf_exempt
def restaurant_list(request):

    # GET
    if request.method == GET:

        # return 200 response and all restaurants
        return HttpResponse(serializers.serialize(JSON, Restaurant.objects.all()))

    # POST
    elif request.method == POST:

        # create form from request
        form = RestaurantForm(request.POST, request.FILES)

        # if form is valid
        if form.is_valid():

            # save form
            form.save()

            # return 201 response
            return HttpResponse(status=HTTPStatus.CREATED)
        else:

            # return 422 error if form is invalid
            return HttpResponse(status=HTTPStatus.UNPROCESSABLE_ENTITY, reason=INVALID_FORM)
    else:

        # return 405 error if method is not supported
        return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, reason=METHOD_NOT_SUPPORTED)

"""
method for retrieving, updating or deleting a restaurant by id
"""
@csrf_exempt
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

        # get body of request
        body = json.loads(request.body.decode(UTF8))

        # get restaurant by id
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:

            # return 404 error if restaurant is not found
            return HttpResponse(status=HTTPStatus.NOT_FOUND, reason=RESTAURANT_NOT_FOUND)

        # update the found restaurant
        restaurant.name = body.get(NAME)
        restaurant.address = body.get(ADDRESS)
        restaurant.tags = body.get(TAGS)
        restaurant.save()

        # return 200 response
        return HttpResponse()

    # DELETE
    elif request.method == DELETE:

        # get restaurant by id
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:

            # return 404 error if restaurant is not found
            return HttpResponse(status=HTTPStatus.NOT_FOUND, reason=RESTAURANT_NOT_FOUND)

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
@csrf_exempt
def restaurant_upload_image(request, restaurant_id):

    # POST
    if request.method == POST:

        # get restaurant by id
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:

            # return 404 error if restaurant is not found
            return HttpResponse(status=HTTPStatus.NOT_FOUND, reason=RESTAURANT_NOT_FOUND)

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
@csrf_exempt
def dish_list(request, restaurant_id):

    # GET
    if request.method == GET:

        # get restaurant by id
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:

            # return 404 error if restaurant is not found
            return HttpResponse(status=HTTPStatus.NOT_FOUND, reason=RESTAURANT_NOT_FOUND)

        # return 200 response and dishes of found restaurant
        return HttpResponse(serializers.serialize(JSON, restaurant.dish_set.all()))

    # POST
    elif request.method == POST:

        # create form from request
        form = DishForm(request.POST, request.FILES)

        # if form is valid
        if form.is_valid():

            # save form
            form.save()

            # return 201 response
            return HttpResponse(status=HTTPStatus.CREATED)
        else:

            # return 422 error if form is invalid
            return HttpResponse(status=HTTPStatus.UNPROCESSABLE_ENTITY, reason=INVALID_FORM)
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

        # get restaurant by id
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:

            # return 404 error if restaurant is not found
            return HttpResponse(status=HTTPStatus.NOT_FOUND, reason=RESTAURANT_NOT_FOUND)

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

        # get restaurant by id
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:

            # return 404 error if restaurant is not found
            return HttpResponse(status=HTTPStatus.NOT_FOUND, reason=RESTAURANT_NOT_FOUND)

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

        # get restaurant by id
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:

            # return 404 error if restaurant is not found
            return HttpResponse(status=HTTPStatus.NOT_FOUND, reason=RESTAURANT_NOT_FOUND)

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
