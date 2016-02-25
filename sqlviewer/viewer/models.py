import uuid
from django.db import models


class Model(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, blank=False, null=False)
    version = models.CharField(max_length=128, blank=False, null=False)


class Diagram(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    model = models.ForeignKey(Model)


class Table(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, blank=False, null=False)
    comment = models.TextField(blank=True, null=True)
    model = models.ForeignKey(Model)

    def columns(self):
        return Column.objects.filter(table=self)


class Column(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, blank=False, null=False)
    comment = models.TextField(blank=True, null=True)
    table = models.ForeignKey(Table)
    is_key = models.BooleanField(default=False)
    is_auto_increment = models.BooleanField(default=False)
    is_nullable = models.BooleanField(default=False)
    is_reference = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)


class ForeignKey(models.Model):
    TYPE_COLUMN = 'column'
    TYPE_TABLE = 'table'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=1, choices=(TYPE_COLUMN, TYPE_TABLE), default=TYPE_COLUMN)
    target_table = models.ForeignKey(Table)
    target_column = models.ForeignKey(Column, null=True)
    source_table = models.ForeignKey(Table)
    source_column = models.ForeignKey(Column, null=True)
