from django.conf import settings

# Get the MongoDB books collection
db = settings.MONGO_DB
books_collection = db['books']