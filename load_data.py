from mongoengine import connect, Document, StringField, DateTimeField, ReferenceField, ListField
from datetime import datetime
import json

uri = "mongodb+srv://Nazar:NazarCanon09@wb8.3wglwy9.mongodb.net/?retryWrites=true&w=majority"
connect(host=uri)

class Author(Document):
    fullname = StringField(required=True)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()


if not Author.objects:
    with open("authors.json", "r", encoding="utf-8") as file:
        authors_data = json.load(file)

    for author_data in authors_data:
        born_date = datetime.strptime(author_data["born_date"], "%B %d, %Y")
        Author(
            fullname=author_data["fullname"],
            born_date=born_date,
            born_location=author_data["born_location"],
            description=author_data["description"]
        ).save()

if not Quote.objects:
    with open("quotes.json", "r", encoding="utf-8") as file:
        quotes_data = json.load(file)

    for quote_data in quotes_data:
        author = Author.objects(fullname=quote_data["author"]).first()
        Quote(
            tags=quote_data["tags"],
            author=author,
            quote=quote_data["quote"]
        ).save()

