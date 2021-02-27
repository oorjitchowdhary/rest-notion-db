from flask import Flask, request
from notion.client import NotionClient

app = Flask(__name__)

@app.route('/post', methods=['POST'])
def post():
    token = request.headers.get('Notion-Auth-Token')
    page_url = request.headers.get('Notion-Page-Url')

    # initialize notion db page
    client = NotionClient(token_v2=token)
    page = client.get_collection_view(page_url)

    record = page.collection.add_row()

    error_fields = []
    for field in request.json:
        # match int field to schema
        if getattr(record, field) is None and isinstance(request.json[field], int):
            continue
        # check if datatype match schema
        elif type(getattr(record, field)) != type(request.json[field]):
            error_fields.append(field)

    if not error_fields:
        # update added record as per request
        for field in request.json:
            setattr(record, field, request.json[field])
        return "added data"
    else:
        print(error_fields)
        return "datatype mismatch"