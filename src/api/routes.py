from flask import jsonify, make_response, Blueprint, request
from src.services.sales_analysis.SalesAnalysis import SalesAnalysis

sales_analytics = SalesAnalysis()
api = Blueprint('api', __name__)

@api.route('/sales_analysis', methods=['POST'])
def sales_analysis():
    data = request.get_json()
    data_type = data.get("data_type", "all")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    region = data.get("region")
    country = data.get("country")
    ship_mode = data.get("ship_mode")
    segment = data.get("segment")
    category = data.get("category")
    sub_category = data.get("sub_category")
    state = data.get("state")
    city = data.get("city")

    if data_type == "all":
        sales_and_profit_sum = sales_analytics.sales_and_profit_sum(start_date, end_date, ship_mode, country, city, state, region, category, sub_category, segment)
        profit_margins_over_time = sales_analytics.profit_margins_over_time(start_date, end_date, ship_mode, country, city, state, region, category, sub_category, segment)
        sales_profit_profit_margin_per_year = sales_analytics.sales_profit_profit_margin_per_year(ship_mode, country, city, state, region, category, sub_category, segment)
        sales_profit_profit_margin_year_on_year_growth = sales_analytics.sales_profit_profit_margin_year_on_year_growth(ship_mode, country, city, state, region, category, sub_category, segment)
        sales_profit_profit_margin_per_region = sales_analytics.sales_profit_profit_margin_per_region(start_date, end_date, ship_mode, country, state, region, category, sub_category, segment)
        sales_profit_profit_margin_per_region_per_year = sales_analytics.sales_profit_profit_margin_per_region_per_year(ship_mode, country, city, state, category, sub_category, segment)
        sales_profit_profit_margin_per_category = sales_analytics.sales_profit_profit_margin_per_category(start_date, end_date, ship_mode, country, city, state, region, segment)
        sales_profit_profit_margin_per_category_per_year = sales_analytics.sales_profit_profit_margin_per_category_per_year(ship_mode, country, city, state, region, segment)
        profit_per_unit_product = sales_analytics.profit_per_unit_product_in_category(start_date, end_date, ship_mode, country, city, state, region, segment)

        response = {
            "sales_and_profit_sum": sales_and_profit_sum,
            "profit_margins_over_time": profit_margins_over_time,
            "sales_profit_profit_margin_per_year": sales_profit_profit_margin_per_year,
            "sales_profit_profit_margin_year_on_year_growth": sales_profit_profit_margin_year_on_year_growth,
            "sales_profit_profit_margin_per_region": sales_profit_profit_margin_per_region,
            "sales_profit_profit_margin_per_region_per_year": sales_profit_profit_margin_per_region_per_year,
            "sales_profit_profit_margin_per_category": sales_profit_profit_margin_per_category,
            "sales_profit_profit_margin_per_category_per_year": sales_profit_profit_margin_per_category_per_year,
            "profit_per_unit_product": profit_per_unit_product
        }

        return make_response(jsonify(response), 200)

    elif data_type == "sales_and_profit_sum":
        sales_and_profit_sum = sales_analytics.sales_and_profit_sum(start_date, end_date, ship_mode, country, city, state, region, category, sub_category, segment)
        response = {
            "sales_and_profit_sum": sales_and_profit_sum
        }
        return make_response(jsonify(response), 200)

    elif data_type == "profit_margins_over_time":
        profit_margins_over_time = sales_analytics.profit_margins_over_time(start_date, end_date, ship_mode, country, city, state, region, category, sub_category, segment)
        response = {
            "profit_margins_over_time": profit_margins_over_time
        }
        return make_response(jsonify(response), 200)

    elif data_type == "sales_profit_profit_margin_per_year":
        sales_profit_profit_margin_per_year = sales_analytics.sales_profit_profit_margin_per_year(ship_mode, country, city, state, region, category, sub_category, segment)
        response = {
            "sales_profit_profit_margin_per_year": sales_profit_profit_margin_per_year
        }
        return make_response(jsonify(response), 200)

    elif data_type == "sales_profit_profit_margin_year_on_year_growth":
        sales_profit_profit_margin_year_on_year_growth = sales_analytics.sales_profit_profit_margin_year_on_year_growth(ship_mode, country, city, state, region, category, sub_category, segment)
        response = {
            "sales_profit_profit_margin_year_on_year_growth": sales_profit_profit_margin_year_on_year_growth
        }
        return make_response(jsonify(response), 200)

    elif data_type == "sales_profit_profit_margin_per_region":
        sales_profit_profit_margin_per_region = sales_analytics.sales_profit_profit_margin_per_region(start_date, end_date, ship_mode, country, city, state, region, category, sub_category, segment)
        response = {
            "sales_profit_profit_margin_per_region": sales_profit_profit_margin_per_region
        }
        return make_response(jsonify(response), 200)

    elif data_type == "sales_profit_profit_margin_per_region_per_year":
        sales_profit_profit_margin_per_region_per_year = sales_analytics.sales_profit_profit_margin_per_region_per_year(ship_mode, country, city, state, region, category, sub_category, segment)
        response = {
            "sales_profit_profit_margin_per_region_per_year": sales_profit_profit_margin_per_region_per_year
        }
        return make_response(jsonify(response), 200)

    elif data_type == "sales_profit_profit_margin_per_category":
        sales_profit_profit_margin_per_category = sales_analytics.sales_profit_profit_margin_per_category(start_date, end_date, ship_mode, country, city, state, region, category, sub_category, segment)
        response = {
            "sales_profit_profit_margin_per_category": sales_profit_profit_margin_per_category
        }
        return make_response(jsonify(response), 200)

    elif data_type == "sales_profit_profit_margin_per_category_per_year":
        sales_profit_profit_margin_per_category_per_year = sales_analytics.sales_profit_profit_margin_per_category_per_year(ship_mode, country, city, state, region, category, sub_category, segment)
        response = {
            "sales_profit_profit_margin_per_category_per_year": sales_profit_profit_margin_per_category_per_year
        }
        return make_response(jsonify(response), 200)

    elif data_type == "profit_per_unit_product":
        profit_per_unit_product = sales_analytics.profit_per_unit_product_in_category(start_date, end_date, ship_mode, country, city, state, region, segment)
        response = {
            "profit_per_unit_product": profit_per_unit_product
        }
        return make_response(jsonify(response), 200)

    else:
        response = {
            "error": "Invalid data_type. Please specify a valid data_type."
        }
        return make_response(jsonify(response), 400)


