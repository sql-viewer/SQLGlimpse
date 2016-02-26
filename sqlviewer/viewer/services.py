from sqlviewer.viewer.models import Model, Table, Column, ForeignKey, Diagram, ConnectionElement, LayerElement, \
    TableElement

__author__ = 'Stefan Martinov <stefan.martinov@gmail.com>'


def save_imported_model(model):
    """
    Model imported from one of our importers
    :type model: dict
    :return:
    """
    dbmodel = Model.objects.create(
        id=model['id'],
        name=model['name'],
        version=model['version']
    )

    dbtables = {}
    dbcolumns = {}
    dbfks = {}
    dbdiagrams = {}

    for table in model['data']['tables']:
        dbtable = Table.objects.create(
            id=table['id'],
            name=table['name'],
            comment=table['comment'],
            model=dbmodel
        )
        dbtables[str(dbtable.id).lower()] = dbtable

        for col in table['columns']:
            dbcol = Column.objects.create(
                id=col['id'],
                name=col['name'],
                comment=col['comment'],
                table=dbtable,
                is_key=col['flags']['key'],
                is_auto_increment=col['flags']['autoIncrement'],
                is_nullable=col['flags']['nullable'],
                is_reference=col['flags']['reference'],
                is_hidden=col['flags']['hidden'],
            )
            dbcolumns[str(dbcol.id).lower()] = dbcol

    for fk in model['data']['foreignKeys']:
        dbfk = ForeignKey.objects.create(
            id=fk['id'],
            type=fk['type'],
            target_table=dbtables[str(fk['target']['tableId']).lower()],
            target_column=dbcolumns[str(fk['target']['columnId']).lower()],
            source_table=dbtables[str(fk['source']['tableId']).lower()],
            source_column=dbcolumns[str(fk['source']['columnId']).lower()],
            model=dbmodel
        )
        dbfks[str(dbfk.id).lower()] = dbfk

    for dia in model['diagrams']:
        dbdiagram = Diagram.objects.create(
            id=dia['id'],
            name=dia['name'],
            model=dbmodel
        )
        dbdiagrams[str(dbdiagram.id).lower()] = dbdiagram

        for con in dia['connections']:
            ConnectionElement.objects.create(
                id=con['id'],
                draw=con['element']['draw'],
                foreignKey=dbfks[str(con['foreignKeyId']).lower()],
                diagram=dbdiagram
            )

        for layer in dia['layers']:
            dblayer = LayerElement.objects.create(
                id=layer['id'],
                name=layer['name'],
                description=layer['description'],
                pos_x=layer['element']['x'],
                pos_y=layer['element']['y'],
                height=layer['element']['height'],
                width=layer['element']['width'],
                color=layer['element']['color'],
                diagram=dbdiagram
            )

            for table in layer['tables']:
                TableElement.objects.create(
                    id=table['id'],
                    table=dbtables[str(table['tableId']).lower()],
                    pos_x=table['element']['x'],
                    pos_y=table['element']['y'],
                    height=table['element']['height'],
                    width=table['element']['width'],
                    color=table['element']['color'],
                    collapsed=table['element']['collapsed'],
                    layer_element=dblayer
                )
