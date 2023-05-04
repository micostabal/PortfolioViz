from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from portfolioviz.selectors import (
    portfolios_list,
    assets_list_response,
    portfolio_value_list,
    weight_list
)
from portfolioviz.utils import parse_request_date, parse_query_param

@require_http_methods(["GET"])
def pong(request):
    return HttpResponse("<p>Pong</p>")

@require_http_methods(["GET"])
@csrf_exempt
def get_assets(request):
    assets = assets_list_response()
    return JsonResponse({
        "instances": assets}, status=200)

@require_http_methods(["GET"])
@csrf_exempt
def get_portfolios(request):
    portfolios = portfolios_list()
    return JsonResponse({
        "instances": portfolios}, status=200)

@require_http_methods(["GET"])
@csrf_exempt
def get_portfolio_value(request, portfolio_id):
    values = portfolio_value_list(
        portfolio_id=portfolio_id,
        date_from=parse_request_date(
            parse_query_param(request, 'from')),
        date_to=parse_request_date(
            parse_query_param(request, 'to')))
    return JsonResponse({
        "portfolio_id": portfolio_id,
        "values": values}, status=200)

@require_http_methods(["GET"])
@csrf_exempt
def get_weights(request, portfolio_id):
    weights = weight_list(
        portfolio_id=portfolio_id,
        date_from=parse_request_date(
            parse_query_param(request, 'from')),
        date_to=parse_request_date(
            parse_query_param(request, 'to')))
    return JsonResponse({
        "portfolio_id": portfolio_id,
        "weights": weights}, status=200)