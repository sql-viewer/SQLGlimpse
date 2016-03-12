from django.core.cache import cache
from sqlviewer.glimpse.models import Model, Table, Column, ForeignKey, Diagram, ConnectionElement, LayerElement, \
    TableElement, Version
from django.db.transaction import atomic
from django.conf import settings

__author__ = 'Stefan Martinov <stefan.martinov@gmail.com>'


def get_diagram_data(diagram: Diagram) -> dict:
    """
    Get diagram data method for retrieval of diagram dictionary (json data)
    Is cached to increase performance
    :param Diagram diagram:
    :return dict: diagram hierarchy with embedded json data
    """
    data = cache.get(diagram.id)
    if not data:
        data = diagram.to_json()
        cache.set(diagram.id, data)
    return data


def version_search(version: Version, query: str, offset: int = 0, size: int = None) -> list:
    """
    Searches the specified version with the specified query
    :param Version version: version to search
    :param str query: query to search
    :param int offset: for result paging
    :param int size: for result paging
    :return list of dict: search results for this query
    """
    size = size or settings.VERSION_SEARCH_CONFIG['search_limit']
    excluded_layers = settings.VERSION_SEARCH_CONFIG['exclude_layers'] or []
    search_results = []

    table_elements = TableElement.objects.filter(table__name__contains=query) \
                         .filter(table__model_version=version) \
                         .exclude(layer_element__name__in=excluded_layers) \
                         .prefetch_related('table') \
                         .prefetch_related('layer_element') \
                         .prefetch_related('layer_element__diagram') \
                         .all()[offset: size]

    for te in table_elements:
        result = {'type': 'table',
                  'id': te.extid,
                  'name': te.table.name,
                  'diagram': {
                      "id": te.layer_element.diagram.id,
                      "name": te.layer_element.diagram.name
                  },
                  'layer': {
                      "id": str(te.layer_element.extid),
                      "name": te.layer_element.name,
                      "color": te.layer_element.color
                  }}
        search_results.append(result)

    return search_results


@atomic
def save_imported_model(model: dict) -> None:
    """
    Model imported from one of our importers
    :param dict model: imported model
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
