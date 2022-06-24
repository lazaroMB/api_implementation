import math


def format_number(n):
    return math.floor(n*100)/100


class DataService:

    def __init__(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def get_category_statistics(self, category):
        spent = 0.0
        for stat in self.get_data():
            tmp_category = stat.get('category')
            if tmp_category != category:
                continue
            spent += self.get_state_price(stat)
        return {category: format_number(spent)}

    def get_categories_statistics(self):
        categories = set()
        results = {}
        for stat in self.get_data():
            category = stat.get('category')
            if category in categories:
                continue
            categories.add(category)
            statistics = self.get_category_statistics(category)
            results.update(statistics)
        return results

    def get_state_price(self, stat):
        spended = stat.get('price')
        discount = stat.get('percentage_discount')
        if discount != 0:
            spended -= spended * (discount / 100)
        return spended
