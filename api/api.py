from flask import Flask, request, jsonify
from notion.client import NotionClient
from .utils import IGNORE_ATTRS

app = Flask(__name__)


@app.route('/page/<pid>', methods=['GET'], strict_slashes=False)
def page(pid):
    token = request.headers.get('Authorization').split()[-1]
    page_url = f"https://notion.so/{pid}?v={request.args['v']}"

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

    result = page.build_query(sort=sort_params, filter=filter_params).execute()

    # handle reponse
    response = []
    for r in result:
        data = {}
        for attr in dir(r):
            if not attr.startswith('_') and attr not in IGNORE_ATTRS:
                data[attr] = getattr(r, attr)

        response.append(data)

    if 'limit' in request.args:
        response = response[:int(request.args['limit'])]

    return jsonify(response)


@app.route('/post', methods=['POST'], strict_slashes=False)
def post():
    token = request.headers.get('Authorization').split()[-1]
    page_url = request.headers.get('Notion-Page-Url')

    # initialize notion db page
    client = NotionClient(token_v2=token)
    page = client.get_collection_view(page_url)

    # add new empty row to page
    record = page.collection.add_row()

    error_fields = []
    for field in request.json:
        # match int or single-tag field to schema
        if getattr(record, field) is None and isinstance(request.json[field], int) or isinstance(request.json[field], str):
            continue
        # check if datatype matches schema
        elif type(getattr(record, field)) != type(request.json[field]):
            error_fields.append(field)

    response = {}

    if not error_fields:
        # update added empty row as per request
        for field in request.json:
            setattr(record, field, request.json[field])
        response['success'] = True
        response['message'] = "Added data to table successfully."
    else:
        response['success'] = False
        response['message'] = "Unable to add data to table. One or more of the POSTed data doesn't match schema."
        response['error_fields'] = error_fields

    return jsonify(response)
