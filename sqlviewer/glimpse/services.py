from sqlviewer.glimpse.models import Model, Table, Column, ForeignKey, Diagram, ConnectionElement, LayerElement, \
    TableElement, Version
from django.db.transaction import atomic

__author__ = 'Stefan Martinov <stefan.martinov@gmail.com>'


@atomic
def save_imported_model(model):
    """
    Model imported from one of our importers
    :type model: dict
    :return:
    """

    dbmodel = Model.objects.filter(extid=model['id']).first()
    if not dbmodel:
        dbmodel = Model.objects.create(
            extid=model['id'],
            name=model['name']
        )

    dbversion = Version.objects.create(
        label=model['version'],
        model=dbmodel,
    )

    dbtables = {}
    dbcolumns = {}
    dbfks = {}
    dbdiagrams = {}
    dblayers = {}
    dbconnections = {}
    dbtable_elements = {}

    for table in model['data']['tables']:
        dbtable = Table.objects.create(
            extid=table['id'],
            name=table['name'],
            comment=table['comment'],
            model_version=dbversion
        )
        dbtables[str(dbtable.extid).lower()] = dbtable

        for col in table['columns']:
            dbcol = Column.objects.create(
                extid=col['id'],
                name=col['name'],
                comment=col['comment'],
                table=dbtable,
                is_key=col['flags']['key'],
                is_auto_increment=col['flags']['autoIncrement'],
                is_nullable=col['flags']['nullable'],
                is_reference=col['flags']['reference'],
                is_hidden=col['flags']['hidden'],
            )
            dbcolumns[str(dbcol.extid).lower()] = dbcol

    for fk in model['data']['foreignKeys']:
        dbfk = ForeignKey.objects.create(
            extid=fk['id'],
            type=fk['type'],
            target_table=dbtables[str(fk['target']['tableId']).lower()],
            target_column=dbcolumns[str(fk['target']['columnId']).lower()],
            source_table=dbtables[str(fk['source']['tableId']).lower()],
            source_column=dbcolumns[str(fk['source']['columnId']).lower()],
            model_version=dbversion
        )
        dbfks[str(dbfk.extid).lower()] = dbfk

    for dia in model['diagrams']:
        dbdiagram = Diagram.objects.create(
            extid=dia['id'],
            name=dia['name'],
            model_version=dbversion
        )
        dbdiagrams[str(dbdiagram.extid).lower()] = dbdiagram

        for con in dia['connections']:
            dbconn = ConnectionElement.objects.create(
                extid=con['id'],
                draw=con['element']['draw'],
                foreignKey=dbfks[str(con['foreignKeyId']).lower()],
                diagram=dbdiagram
            )
            dbconnections[str(dbconn.extid)] = dbconn

        for layer in dia['layers']:
            dblayer = LayerElement.objects.create(
                extid=layer['id'],
                name=layer['name'],
                description=layer['description'],
                pos_x=layer['element']['x'],
                pos_y=layer['element']['y'],
                height=layer['element']['height'],
                width=layer['element']['width'],
                color=layer['element']['color'],
                diagram=dbdiagram
            )
            dblayers[str(dblayer.extid)] = dblayer

            for table in layer['tables']:
                dbtable_element = TableElement.objects.create(
                    extid=table['id'],
                    table=dbtables[str(table['tableId']).lower()],
                    pos_x=table['element']['x'],
                    pos_y=table['element']['y'],
                    height=table['element']['height'],
                    width=table['element']['width'],
                    color=table['element']['color'],
                    collapsed=table['element']['collapsed'],
                    layer_element=dblayer
                )
                dbtable_elements[str(dbtable_element.extid)] = dbtable_element
