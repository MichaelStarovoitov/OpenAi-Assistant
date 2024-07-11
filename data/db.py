from components.loadData import load_data
from fuzzywuzzy import fuzz

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
        return self.sortProduct

    def search_json_with_similarity(self, query, threshold=70):
        results = []
        for entry in self.products:
            for key, value in entry.items():
                if isinstance(value, str) and fuzz.partial_ratio(query.lower(), value.lower()) > threshold:
                    results.append(entry)
                    break
        if len(results) > 5:
            self.sortProduct = results[0:10]
        else:
            self.sortProduct = results