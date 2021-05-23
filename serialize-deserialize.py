from marshmallow import Schema, fields, post_load, pre_load, post_load, post_dump
import json


# --------------- Marshmallow Info ---------------

# Define the User Model
class User:
    def __init__(self, id_: int, name: str):
        self.id_ = id_
        self.name = name


# 1. Define the Schema
class UserSchema(Schema):
    id_ = fields.Int()
    name = fields.Str()

    # Post load invokes after deserializing (loading) an object
    # Have to add **kwargs to pre/post decorated methods if you're not using the "many" argument
    @post_load
    def load_user(self, data, **kwargs):
        """ Create the user object """
        return User(**data)


# 2. Create the schema object
user_schema = UserSchema()

# 3. Define data that matches the schema
user = {
    "id_": 1,
    "name": "mike"
}

# "dumps" serializes the data as a JSON-encoded string
serialize_object_into_json_string = user_schema.dumps(user)

# "dump" serializes objects into dictionaries
serialize_object_into_dict = user_schema.dump(user)

# "load" deserializes the user dictionary into a user object
# In other words, the user_schema loaded the user dictionary and converted it into a user object
# If the post_load wasn't their, it would return a user dictionary
deserialize_dict_into_object = user_schema.load(user)  # Converts Dict to User Object

# "loads" converts JSON encoded string to a user object
# If the post_load wasn't their, it would deserialize the JSON string into a user dictionary
deserialize_json_string_into_object = user_schema.loads(
    serialize_object_into_json_string)  # Converts JSON encoded string to a user object

# --------------- JSON Info ---------------

# Json "loads" deserializes the JSON encoded string into a dictionary
deserialize_json_str_into_dict = json.loads(serialize_object_into_json_string)

# Json "load" deserializes a JSON file into a dictionary
with open('./data.json') as f:
    deserialize_json_file_into_dict = json.load(f)

# Json "dumps" serializes an object (dictionary) into a JSON-encoded string
user_object = User(1, 'mike')
user_dict = {"id_": 1, "name": "mike"}

# Both these return the same JSON encoded string
serialize_object_into_json_str = json.dumps(user_object.__dict__)
serialize_dict_into_json_str = json.dumps(user_dict)

# Json "dump" serializes an object (dictionary) as a JSON formatted stream that can be saved to a file
with open('./user.json', 'w') as f:
    serialize_dict_into_json_stream = json.dump(user_dict, f)

print()