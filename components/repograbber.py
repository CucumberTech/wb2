import sys, json


def load_resource(resource_type, resource):
    if resource_type == "archetype":
        if resource == "standard":
            mainFolder = sys.argv[0][0:sys.argv[0].rfind("/")]
            with open(mainFolder + "/standard-archetype.json") as file:
                return json.loads(file.read())
