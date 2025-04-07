from flask import Flask, jsonify, make_response, Blueprint, request
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

    if data_type == "all":
        sales_and_profit_sum = sales_analytics.sales_and_profit_sum(start_date, end_date, ship_mode, country, state, region, category, sub_category, segment)

    return make_response(jsonify(sales_and_profit_sum), 200)


