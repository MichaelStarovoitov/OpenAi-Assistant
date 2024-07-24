from components.loadData import load_data
from fuzzywuzzy import fuzz, process
from components.textTools import text_translator

class Data:
    def __init__(self, path):
        self.allData = load_data(path)
        self.products = self.allData['products']
        self.contacts = self.allData["contact_info"]
        self.delivAndPay = self.allData["delivery_payment_info"]
        self.sortProduct = []

    def getProduccts(self):
        return self.products
    def getContacts(self):
        return self.contacts
    def getDelivAndPay(self):
        return self.delivAndPay
    def getSortProduct(self):
        result = self.sortProduct[0:10]
        for el in result:
            el['name'] = text_translator(el['name'])
            el['description'] = text_translator(el['description'])
        return result
    
    def search_json_with_similarity(self,query, threshold=70):
        query = text_translator(query,"uk", "ru")
        print(query)
        matches = []
        for obj in self.products:
            name_similarity = fuzz.partial_ratio(query.lower(), obj['name'].lower())
            description_similarity = fuzz.partial_ratio(query.lower(), obj['description'].lower())
            
            if name_similarity > threshold or description_similarity > threshold:
                matches.append({
                    'object': obj,
                    'name_similarity': name_similarity,
                    'description_similarity': description_similarity
                })
        matches.sort(key=lambda x: max(x['name_similarity'], x['description_similarity']), reverse=True)
        self.sortProduct = [match['object'] for match in matches]