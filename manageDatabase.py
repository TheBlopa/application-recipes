import json
import requests

class manageDatabase():
    """Class to create and use the database that will be using in the appliaction"""
    # url for your database, for example firebase
    url = ''

    def get(self):
        """Get data of databse on json format from the url
         Returns
         -------
         list of str
            all the information from the database
            """
        try:
            result = requests.get(self.url)
            return json.loads(result.content.decode())
        except:
            pass
        # Database to test the app
        # with open('1.json') as json_file:
        #     data = json.load(json_file)
        #     return data

    def patch(self, JSON, category):
        """Update existing data or add new data
        Parameters
        ----------
        JSON: list of str
        category: str"""
        try:
            to_database = json.loads(JSON)
            requests.patch(url = self.url[:-5] + '/' + category + '.json', json = to_database)
        except:
            pass

    def post(self, JSON):
        """Add data with unique key, not recomended
        Parameters
        ----------
        JSON: list of str"""
        try:
            to_database = json.loads(JSON)
            requests.post(url = self.url, json = to_database)
        except:
            pass

    def put(self, JSON):
        """Add data, but delete the rest of the data
        Parameters
        ----------
        JSON: list of str"""
        try:
            to_database = json.loads(JSON)
            requests.put(url = self.url, json = to_database)
        except:
            pass

    def delete(self, category, title):
        """Delete the specific child of the database
        Parameters
        ----------
        category: str
        title: str"""
        try:
            requests.delete(url = 'https://recetas-acfc9.firebaseio.com/1/%s/%s.json' %(category, title))    
        except:
            pass