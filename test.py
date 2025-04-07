from src.utils import helpers
from src.utils.helpers import HelperFunctions
# prods = helpers.get_products_in_list(product_ids = [39, 40, 41])
service = HelperFunctions()
prods = service.fetch_trending_products(country=237, sort_by="")

print(prods)