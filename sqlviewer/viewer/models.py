import uuid
from django.db import models


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Model(UUIDModel):
    name = models.CharField(max_length=128, blank=False, null=False)
    version = models.CharField(max_length=128, blank=False, null=False)

    def diagrams(self):
        return Diagram.objects.filter(model=self)


class Diagram(UUIDModel):
    name = models.CharField(max_length=128, blank=False, null=False)
    model = models.ForeignKey(Model)


class Table(UUIDModel):
    name = models.CharField(max_length=128, blank=False, null=False)
    comment = models.TextField(blank=True, null=True)
    model = models.ForeignKey(Model)

    def columns(self):
        return Column.objects.filter(table=self)


class Column(UUIDModel):
    name = models.CharField(max_length=128, blank=False, null=False)
    comment = models.TextField(blank=True, null=True)
    table = models.ForeignKey(Table)
    is_key = models.BooleanField(default=False)
    is_auto_increment = models.BooleanField(default=False)
    is_nullable = models.BooleanField(default=False)
    is_reference = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)


class ForeignKey(UUIDModel):
    TYPE_COLUMN = 'column'
    TYPE_TABLE = 'table'
    TYPE_CHOICES = (
        (TYPE_COLUMN, 'column'),
        (TYPE_TABLE, 'table')
    )

    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=TYPE_COLUMN)
    target_table = models.ForeignKey(Table, related_name='target_table')
    target_column = models.ForeignKey(Column, null=True, related_name='target_column')
    source_table = models.ForeignKey(Table, related_name='source_table')
    source_column = models.ForeignKey(Column, null=True, related_name='source_column')
    model = models.ForeignKey(Model)


class AbstractElement(UUIDModel):
    pos_x = models.IntegerField()
    pos_y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    color = models.CharField(max_length=7)

    class Meta:
        abstract = True


class LayerElement(AbstractElement):
    name = models.CharField(max_length=128, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    diagram = models.ForeignKey(Diagram)


class TableElement(AbstractElement):
    table = models.ForeignKey(Table)
    layer_element = models.ForeignKey(LayerElement)
    collapsed = models.BooleanField(default=False)


class ConnectionElement(UUIDModel):
    DRAW_SPLIT = "split"
    DRAW_FULL = "full"
    DRAW_HIDDEN = "hidden"
    DRAW_CHOICES = (
        (DRAW_SPLIT, "split"),
        (DRAW_FULL, "full"),
        (DRAW_HIDDEN, "hidden")
    )
    diagram = models.ForeignKey(Diagram)
    foreignKey = models.ForeignKey(ForeignKey)
    draw = models.CharField(max_length=10, choices=DRAW_CHOICES, default=DRAW_FULL)
