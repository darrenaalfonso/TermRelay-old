from django.db import models
from django.contrib.auth.models import User
from .utilities import ChoiceEnum


class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    row_stamp = models.DateTimeField(auto_now=True)


class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    level = models.CharField(max_length=255)
    row_stamp = models.DateTimeField(auto_now=True)


class ProductType(ChoiceEnum):
    product = 0
    service = 1
    virtual = 2


class Product(models.Model):
    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    description = models.TextField
    product_type = models.CharField(choices=ProductType.choices(), max_length=255)
    unit_description = models.CharField(max_length=255)
    price_per_unit = models.DecimalField(decimal_places=2)
    row_stamp = models.DateTimeField(auto_now=True)


class ProductQuestion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    question = models.TextField
    row_stamp = models.DateTimeField(auto_now=True)


class ProductQuestionChoice(models.Model):
    product_question = models.ForeignKey(ProductQuestion, on_delete=models.CASCADE)
    description = models.TextField
    row_stamp = models.DateTimeField(auto_now=True)


class ProductRow(models.Model):
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField
    price = models.DecimalField(decimal_places=2)


class Inquiry(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    inquirer_email = models.CharField(max_length=255)
    inquirer = models.ForeignKey(User, null=True, blank=True, on_delete=models.ObjectDoesNotExist)
    is_anonymous = models.BooleanField
    row_stamp = models.DateTimeField(auto_now=True)


class ProductQuestionResponse(models.Model):
    product_row = models.ForeignKey(ProductRow, on_delete=models.CASCADE)
    question = models.ForeignKey(ProductQuestion, on_delete=models.CASCADE)
    response = models.ForeignKey(ProductQuestionChoice, on_delete=models.CASCADE)

