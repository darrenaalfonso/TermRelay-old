from django.db import models
from django.contrib.auth.models import User
from .utilities import ChoiceEnum
from django.core.validators import MinValueValidator


class Company(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    row_stamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_index=True)
    level = models.CharField(max_length=255, db_index=True)
    row_stamp = models.DateTimeField(auto_now=True)


class Inquiry(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_index=True)
    inquirer_email = models.CharField(max_length=255, db_index=True)
    inquirer = models.ForeignKey(User, null=True, blank=True, on_delete=models.ObjectDoesNotExist, db_index=True)
    is_anonymous = models.BooleanField(default=True)
    inquiry_date = models.DateTimeField(auto_now=True)
    row_stamp = models.DateTimeField(auto_now=True)


class ProposalTemplate(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_index=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    creation_date = models.DateTimeField(db_index=True)
    row_stamp = models.DateTimeField(auto_now=True)


class Proposal(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, db_index=True)
    inquiry = models.ForeignKey(Inquiry, on_delete=models.DO_NOTHING, null=True, blank=True, db_index=True)
    template = models.ForeignKey(ProposalTemplate, on_delete=models.DO_NOTHING, db_index=True)
    users = models.ManyToManyField(User, db_index=True)
    round = models.IntegerField(validators=[MinValueValidator(1)])
    date = models.DateTimeField(db_index=True)
    row_stamp = models.DateTimeField(auto_now=True)


class ProductType(ChoiceEnum):
    product = 0
    service = 1
    virtual = 2


class Product(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    company = models.ForeignKey(Company, related_name='company', on_delete=models.CASCADE, db_index=True)
    image = models.TextField(null=True, blank=True)
    description = models.TextField(db_index=True)
    product_type = models.CharField(choices=ProductType.choices(), max_length=255)
    unit_description = models.CharField(max_length=255)
    price_per_unit = models.DecimalField(decimal_places=2, max_digits=20)
    row_stamp = models.DateTimeField(auto_now=True)


class ProductQuestion(models.Model):
    product = models.ForeignKey(Product, related_name='product_questions', on_delete=models.CASCADE, db_index=True)
    question = models.TextField(db_index=True)
    row_stamp = models.DateTimeField(auto_now=True)


class ProductQuestionChoice(models.Model):
    product_question = models.ForeignKey(ProductQuestion, related_name='choices', on_delete=models.CASCADE,
                                         db_index=True)
    text_answer = models.TextField(null=True, blank=True)
    numerical_answer = models.DecimalField(decimal_places=4, max_digits=20, null=True, blank=True)
    numerical_answer_units = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField
    notes = models.TextField(null=True, blank=True)
    row_stamp = models.DateTimeField(auto_now=True)


class ProductRow(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    inquiry = models.ForeignKey(Inquiry, related_name='product_rows', on_delete=models.CASCADE, null=True, blank=True,
                                db_index=True)
    proposal = models.ForeignKey(Proposal, related_name='product_rows', on_delete=models.CASCADE, null=True, blank=True,
                                 db_index=True)
    proposal_template = models.ForeignKey(ProposalTemplate, on_delete=models.CASCADE, null=True, blank=True,
                                          db_index=True)
    quantity = models.IntegerField
    price = models.DecimalField(decimal_places=2, max_digits=20)


class ProductQuestionResponse(models.Model):
    product_row = models.ForeignKey(ProductRow, on_delete=models.CASCADE, db_index=True)
    question = models.ForeignKey(ProductQuestion, on_delete=models.CASCADE, db_index=True)
    response = models.ForeignKey(ProductQuestionChoice, on_delete=models.CASCADE)
