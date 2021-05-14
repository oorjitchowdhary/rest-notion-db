# rest-notion-db
A RESTful way to use your Notion tables as a database.

### UPDATE
As of May 11, 2021, the [official Notion API](https://developers.notion.com/) is available in its public beta version. I'd recommend you to use that.

## Use-cases
Form submissions or frontend websites, use one database that is understood by everyone at your workplace for all your needs.

## Usage
In order to use the API, you need to provide your Notion `token_v2` cookie and the Notion database page URL.
You can obtain your `token_v2` using Chrome DevTools or the like for other browsers.

### GET data
Endpoint: `/page/<PAGE_ID>`<br>
The `PAGE_ID` includes the ID of the page along with the default `?v` URL parameter.

Simply replace the `notion.so` to `rest-notion-db.herokuapp.com` on your database page to access the table data as a JSON response.

In case of an auth-secured page, send your `token_v2` cookie as a Authorization Bearer Token header in the request.

**Queries**<br>
Currently, you can sort and limit the data using request parameters.

For example:<br/>
`?name=asc`: sorts all the names in alphabetical order as per the default Notion intent.<br/>
`?limit=5`: limits the number of results in the response to 5.

You can add multiple query parameters to sort the data as per your use-cases.

**Demo**<br/>
Database: [User Research Template](https://www.notion.so/1d595a4c3f9a4254b332587507e87267?v=43045489a1a44683b04154a85a562898)

Request: `https://rest-notion-db.herokuapp.com/page/1d595a4c3f9a4254b332587507e87267?v=43045489a1a44683b04154a85a562898&name=desc&limit=2`<br/>
Response:
```json
[{
    "completion_time": 20,
    "email": "",
    "name": "Kyle Miller",
    "rsvp": true,
    "status": "Cancelled",
    "task": ["Profile Editing"],
    "title": "Kyle Miller"
}, {
    "completion_time": 30,
    "email": "",
    "name": "Emily Cohen",
    "rsvp": false,
    "status": "Contacted",
    "task": ["Offline Mode", "Profile Editing"],
    "title": "Emily Cohen"
}]
```

### POST data
Endpoint: `/post`

Send the Notion Page URL and the `token_v2` cookie, in case of a private page, as request headers along with the JSON POST data.

In order to successfully POST, the request data keys should match the schema names and the values should match the schema datatypes.

**Demo**<br/>
Database: [User Research Template](https://www.notion.so/1d595a4c3f9a4254b332587507e87267?v=43045489a1a44683b04154a85a562898)

Request:<br/>
Headers
```json
{
    "Authorization": "Bearer <TOKEN_V2>",
    "Notion-Page-Url": "<DB_PAGE_URL>",
    "Content-Type": "application/json"
}
```
Body
```json
{
    "name": "Ivan Zhao",
    "task": ["Offline Mode", "Profile Editing"],
    "status": "Scheduled",
    "completion_time": 42,
    "rsvp": true
}
```
Response:
```json
{
    "message": "Added data to table successfully.",
    "success": true
}
```

## Credits
[notion-py](https://github.com/jamalex/notion-py) for the unofficial Notion client wrapper.

## Problems?
File an issue or [contact](https://t.me/oorjitchowdhary) me.
