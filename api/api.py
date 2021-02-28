from flask import Flask, request, jsonify
from notion.client import NotionClient
import json
import pprint

app = Flask(__name__)


@app.route('/post', methods=['POST'])
def post():
    token = request.headers.get('Notion-Auth-Token')
    page_url = request.headers.get('Notion-Page-Url')

    # initialize notion db page
    client = NotionClient(token_v2=token)
    page = client.get_collection_view(page_url)

    # add new empty row to page
    record = page.collection.add_row()

    error_fields = []
    for field in request.json:
        # match int field to schema
        if getattr(record, field) is None and isinstance(request.json[field], int):
            continue
        # check if datatype matches schema
        elif type(getattr(record, field)) != type(request.json[field]):
            error_fields.append(field)

    if not error_fields:
        # update added empty row as per request
        for field in request.json:
            setattr(record, field, request.json[field])
        return "added data"
    else:
        print(error_fields)
        return "datatype mismatch"


@app.route('/get', methods=['GET'])
def get():
    token = request.headers.get('Notion-Auth-Token')
    page_url = request.headers.get('Notion-Page-Url')

    # initialize notion db page
    client = NotionClient(token_v2=token)
    page = client.get_collection_view(page_url)

    sort_params = []
    filter_params = {
        "filters": [],
        "operator": "and"
    }

    for arg in request.args.items():
        if arg[1] == 'asc' or 'desc':
            param = {
                "property": arg[0],
                "direction": f"{arg[1]}ending"
            }
            sort_params.append(param)
        else:
            # TODO: filter param inflator
            filter = {}

    result = page.build_query(sort=sort_params, filter=filter_params).execute()

    # handle reponse
    ignore_attrs = ['add_callback', 'alive', 'child_list_key', 'children', 'collection', 'color', 'convert_to_type', 'cover', 'get', 'get_all_properties', 'get_backlinks', 'get_browseable_url', 'get_property',
                    'icon', 'id', 'is_alias', 'is_template', 'locked', 'move_to', 'parent', 'refresh', 'remove', 'remove_callbacks', 'role', 'schema', 'set', 'set_property', 'space_info', 'title_plaintext', 'type']
    response = []
    for r in result:
        data = {}
        for attr in dir(r):
            if not attr.startswith('_') and attr not in ignore_attrs:
                data[attr] = getattr(r, attr)

        response.append(data)

    return jsonify(response)
