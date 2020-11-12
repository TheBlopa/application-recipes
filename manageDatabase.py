import json
import requests

# Class for create and use the database that will be using in the appliaction

class manageDatabase():
    url = 'https://recetas-acfc9.firebaseio.com/1.json'

    def get(self):
        result = requests.get(self.url)
        return json.loads(result.content.decode())
        # with open('1.json') as json_file:
        #     data = json.load(json_file)
        #     return data

    # Update existing data or add new data
    def patch(self, JSON, categoria):
        to_database = json.loads(JSON)
        requests.patch(url = self.url[:-5] + '/' + categoria + '.json', json = to_database)

    # Add data with a unique key, not recomended
    def post(self, JSON):
        to_database = json.loads(JSON)
        requests.post(url = self.url, json = to_database)

    # Add data, but delete the rest of the data
    def put(self, JSON):
        to_database = json.loads(JSON)
        requests.put(url = self.url, json = to_database)

    # Delete the specific child
    def delete(self, category, title):
        requests.delete(url = 'https://recetas-acfc9.firebaseio.com/1/%s/%s.json' %(category, title))

    