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
        return self.sortProduct

    def search_json_with_similarity(self, query, fields=None, threshold=70, max_results=10):
        """
        Search for products with fields similar to the query string.

        Args:
            query (str): The query string to search for.
            fields (list of str, optional): Specific fields to search within each product. If None, search all string fields.
            threshold (int, optional): The similarity threshold (0-100) to consider a match. Default is 70.
            max_results (int, optional): The maximum number of results to return. Default is 10.

        Returns:
            list: List of products matching the query.
        """
        results = []
        product_strings = []

        for entry in self.products:
            for key, value in entry.items():
                if fields and key not in fields:
                    continue
                if isinstance(value, str) and fuzz.partial_ratio(query.lower(), value.lower()) > threshold:
                    results.append(entry)
                    product_strings.append(value)
                    break
        
        # Process and sort results by similarity score
        extracted = process.extract(query, product_strings, scorer=fuzz.partial_ratio, limit=max_results)
        indices = [product_strings.index(item[0]) for item in extracted]
       
        self.sortProduct = [results[idx] for idx in indices]
        if len(self.sortProduct) > 5:
            self.sortProduct = self.sortProduct[0:10]
        else:
            self.sortProduct = self.sortProduct
