from components.loadData import load_data
from fuzzywuzzy import fuzz, process
from components.textTools import text_translator
from difflib import SequenceMatcher

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from sentence_transformers import SentenceTransformer

class Data:
    def __init__(self, path):
        self.allData = load_data(path)
        self.products = self.allData['products']
        self.contacts = self.allData["contact_info"]
        self.delivAndPay = self.allData["delivery_payment_info"]
        self.sortProduct = []
        self.moreSortProduct = []
        self.isMore = False

    def getProduccts(self):
        return self.products
    def getContacts(self):
        return self.contacts
    def getDelivAndPay(self):
        return self.delivAndPay
    def getIsMore(self):
        return self.isMore

    def getSortProduct(self):
        result = self.sortProduct[0:5]
        for el in result:
            el['name'] = text_translator(el['name'])
            el['description'] = text_translator(el['description'])
        return result
    
    def search_similarity_with_more_products(self, query, text="больше товаров", threshold=0.7):
        documents = [text, query]
        vectorizer = TfidfVectorizer().fit_transform(documents)
        cosine_similarities = cosine_similarity(vectorizer[1], vectorizer[0]).flatten()
        print(cosine_similarities[0])
        return True if cosine_similarities[0] > threshold else False
    
    def search_json_with_similarityNew(self, query, max_results=10):
        query = text_translator(query,"uk", "ru")
        if self.search_similarity_with_more_products(query):
            self.moreSortProduct = self.sortProduct
            self.isMore = False
            print("yes")
            return
        # Объединяем все текстовые поля продукта для лучшего анализа
        product_descriptions = [
            f"{p['name']} {p['description']} {' '.join(p['categories'])} {p['price']} {p['delivery_payment_info']['delivery_methods']} {p['delivery_payment_info']['payment_methods']}"
            for p in self.products
        ]
        # Добавляем запрос пользователя как еще один "документ"
        documents = product_descriptions + [query]
        # Используем TF-IDF для векторизации текста
        vectorizer = TfidfVectorizer().fit_transform(documents)
        # Считаем косинусное сходство между запросом и продуктами
        cosine_similarities = cosine_similarity(vectorizer[-1], vectorizer[:-1]).flatten()
        # Сортируем продукты по степени сходства
        related_products_indices = cosine_similarities.argsort()[::-1]
        # Берем от 1 до 10 наиболее подходящих продуктов
        top_indices = related_products_indices[:max_results]
        second_indices = related_products_indices[max_results:max_results*2]
        # Вернем только продукты с ненулевым сходством
        self.sortProduct = [self.products[i] for i in top_indices if cosine_similarities[i] > 0] 
        self.moreSortProduct = [self.products[i] for i in second_indices if cosine_similarities[i] > 0] 
        self.isMore = True if len(self.moreSortProduct)>0 else False











#  def search_json_with_similarity(self, query, max_results=10):
#         query = text_translator(query,"uk", "ru")
#         def match_score(query, product):
#             product_text = f"{product['name']} {product['description']} {' '.join(product['categories'])}"
#             return SequenceMatcher(None, query, product_text).ratio()
#         sorted_products = sorted(self.products, key=lambda p: match_score(query, p), reverse=True)
#         self.sortProduct = sorted_products[:max_results]