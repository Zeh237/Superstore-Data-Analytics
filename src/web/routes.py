from flask import Blueprint, request, render_template
from src.services.sales_analysis.SalesAnalysis import SalesAnalysis
from src.utils.Utils import Utils

sales_analytics = SalesAnalysis()
utils = Utils()
web = Blueprint('web', __name__)

@web.route('/')
@web.route('/home')
def home():
    return render_template('web/sales_analytics.html')

@web.route('/sales_analysis', methods=['GET'])
def sales_analysis():
    data_type = request.args.get("data_type", "all")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    region = request.args.get("region")
    country = request.args.get("country")
    ship_mode = request.args.get("ship_mode")
    segment = request.args.get("segment")
    category = request.args.get("category")
    sub_category = request.args.get("sub_category")
    state = request.args.get("state")
    city = request.args.get("city")

    if data_type == "all":
        sales_and_profit_sum = sales_analytics.sales_and_profit_sum(start_date, end_date, ship_mode, country, city,
                                                                    state, region, category, sub_category, segment)
        profit_margins_over_time = sales_analytics.profit_margins_over_time(start_date, end_date, ship_mode, country,
                                                                            city, state, region, category, sub_category,
                                                                            segment)
        sales_profit_profit_margin_per_year = sales_analytics.sales_profit_profit_margin_per_year(ship_mode, country,
                                                                                                  city, state, region,
                                                                                                  category,
                                                                                                  sub_category, segment)
        sales_profit_profit_margin_year_on_year_growth = sales_analytics.sales_profit_profit_margin_year_on_year_growth(
            ship_mode, country, city, state, region, category, sub_category, segment)
        sales_profit_profit_margin_per_region = sales_analytics.sales_profit_profit_margin_per_region(start_date,
                                                                                                      end_date,
                                                                                                      ship_mode,
                                                                                                      country, state,
                                                                                                      region, category,
                                                                                                      sub_category,
                                                                                                      segment)
        sales_profit_profit_margin_per_region_per_year = sales_analytics.sales_profit_profit_margin_per_region_per_year(
            ship_mode, country, city, state, category, sub_category, segment)
        sales_profit_profit_margin_per_category = sales_analytics.sales_profit_profit_margin_per_category(start_date,
                                                                                                          end_date,
                                                                                                          ship_mode,
                                                                                                          country, city,
                                                                                                          state, region,
                                                                                                          segment)
        sales_profit_profit_margin_per_category_per_year = sales_analytics.sales_profit_profit_margin_per_category_per_year(
            ship_mode, country, city, state, region, segment)
        profit_per_unit_product = sales_analytics.profit_per_unit_product_in_category(start_date, end_date, ship_mode,
                                                                                      country, city, state, region,
                                                                                      segment)

        return render_template(
            "sales_analytics.html",
            sales_and_profit_sum=sales_and_profit_sum,
            profit_margins_over_time=profit_margins_over_time,
            sales_profit_profit_margin_per_year=sales_profit_profit_margin_per_year,
            sales_profit_profit_margin_year_on_year_growth=sales_profit_profit_margin_year_on_year_growth,
            sales_profit_profit_margin_per_region=sales_profit_profit_margin_per_region,
            sales_profit_profit_margin_per_region_per_year=sales_profit_profit_margin_per_region_per_year,
            sales_profit_profit_margin_per_category=sales_profit_profit_margin_per_category,
            sales_profit_profit_margin_per_category_per_year=sales_profit_profit_margin_per_category_per_year,
            profit_per_unit_product=profit_per_unit_product
        )

    elif data_type == "sales_and_profit_sum":
        sales_and_profit_sum = sales_analytics.sales_and_profit_sum(start_date, end_date, ship_mode, country, city,
                                                                    state, region, category, sub_category, segment)
        return render_template("sales_analytics.html", sales_and_profit_sum=sales_and_profit_sum)

    elif data_type == "profit_margins_over_time":
        profit_margins_over_time = sales_analytics.profit_margins_over_time(start_date, end_date, ship_mode, country,
                                                                            city, state, region, category, sub_category,
                                                                            segment)
        return render_template("sales_analytics.html", profit_margins_over_time=profit_margins_over_time)

    elif data_type == "sales_profit_profit_margin_per_year":
        sales_profit_profit_margin_per_year = sales_analytics.sales_profit_profit_margin_per_year(ship_mode, country,
                                                                                                  city, state, region,
                                                                                                  category,
                                                                                                  sub_category, segment)
        return render_template("sales_analytics.html",
                               sales_profit_profit_margin_per_year=sales_profit_profit_margin_per_year)

    elif data_type == "sales_profit_profit_margin_year_on_year_growth":
        sales_profit_profit_margin_year_on_year_growth = sales_analytics.sales_profit_profit_margin_year_on_year_growth(
            ship_mode, country, city, state, region, category, sub_category, segment)
        return render_template("sales_analytics.html",
                               sales_profit_profit_margin_year_on_year_growth=sales_profit_profit_margin_year_on_year_growth)

    elif data_type == "sales_profit_profit_margin_per_region":
        sales_profit_profit_margin_per_region = sales_analytics.sales_profit_profit_margin_per_region(start_date, end_date,
                                                        ship_mode, country, city, state, category, sub_category, segment)
        return render_template("sales_analytics.html",
                               sales_profit_profit_margin_per_region=sales_profit_profit_margin_per_region)

    elif data_type == "sales_profit_profit_margin_per_region_per_year":
        sales_profit_profit_margin_per_region_per_year = sales_analytics.sales_profit_profit_margin_per_region_per_year(ship_mode,
                                                                            country, city, state, category, sub_category, segment)
        return render_template("sales_analytics.html",
                               sales_profit_profit_margin_per_region_per_year=sales_profit_profit_margin_per_region_per_year)

    elif data_type == "sales_profit_profit_margin_per_category":
        sales_profit_profit_margin_per_category = sales_analytics.sales_profit_profit_margin_per_category(start_date,
                                                            end_date, ship_mode, country, city, state, region, segment)
        return render_template("sales_analytics.html",
                               sales_profit_profit_margin_per_category=sales_profit_profit_margin_per_category)

    elif data_type == "sales_profit_profit_margin_per_category_per_year":
        sales_profit_profit_margin_per_category_per_year = sales_analytics.sales_profit_profit_margin_per_category_per_year(
            ship_mode, country, city, state, region, segment)
        return render_template("sales_analytics.html",
                               sales_profit_profit_margin_per_category_per_year=sales_profit_profit_margin_per_category_per_year)

    elif data_type == "profit_per_unit_product":
        profit_per_unit_product = sales_analytics.profit_per_unit_product_in_category(start_date, end_date, ship_mode,
                                                                                      country, city, state, region,
                                                                                      segment)
        return render_template("sales_analytics.html", profit_per_unit_product=profit_per_unit_product)

    else:
        return render_template("sales_analytics.html", error="Invalid data_type. Please specify a valid data_type.")

@web.route("/homepage")
def homepage():
    states = utils.get_state()
    ship_modes = utils.get_ship_mode()
    cities = utils.get_city()
    regions = utils.get_region()
    countries = utils.get_country()
    categories = utils.get_category()
    segments = utils.get_segment()
    return render_template("web/sales_analytics.html", states=states, ship_modes=ship_modes, cities=cities, regions=regions,
                           countries=countries, categories=categories, segments=segments)



