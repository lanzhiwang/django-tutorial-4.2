from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.name} the place"


class Restaurant(models.Model):
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return "%s the restaurant" % self.place.name


class Waiter(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return "%s the waiter at %s" % (self.name, self.restaurant)

"""
CREATE TABLE "myapp_place" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(50) NOT NULL,
    "address" varchar(80) NOT NULL
)

CREATE TABLE "myapp_restaurant" (
    "place_id" bigint NOT NULL PRIMARY KEY REFERENCES "myapp_place" ("id") DEFERRABLE INITIALLY DEFERRED,
    "serves_hot_dogs" bool NOT NULL,
    "serves_pizza" bool NOT NULL
)

CREATE TABLE "myapp_waiter" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(50) NOT NULL,
    "restaurant_id" bigint NOT NULL REFERENCES "myapp_restaurant" ("place_id") DEFERRABLE INITIALLY DEFERRED
)
"""
