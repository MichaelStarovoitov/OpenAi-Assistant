from components.loadData import load_data
from fuzzywuzzy import fuzz, process

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
        if len(self.sortProduct) > 10:
           return self.sortProduct[0:10]
        else:
            return self.sortProduct

    # Tmp function
    # def search_json_with_similarity(self, query, fields=None, threshold=70, max_results=10):
    #     results = []
    #     product_strings = []
    #     for entry in self.products:
    #         for key, value in entry.items():
    #             if fields and key not in fields:
    #                 continue
    #             if isinstance(value, str) and fuzz.partial_ratio(query.lower(), value.lower()) > threshold:
    #                 results.append(entry)
    #                 product_strings.append(value)
    #                 break
    #     extracted = process.extract(query, product_strings, scorer=fuzz.partial_ratio, limit=max_results)
    #     indices = [product_strings.index(item[0]) for item in extracted]
    #     self.sortProduct = [results[idx] for idx in indices]

    def search_json_with_similarity(self,query, threshold=70):
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