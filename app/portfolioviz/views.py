from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.http import Http404, HttpResponseBadRequest
from rest_framework.views import exception_handler
from rest_framework import exceptions
from portfolioviz.selectors import (
    marketSelector,
    portfolioSelector
)
from portfolioviz.exceptions import BadDateFormatException
from portfolioviz.utils import parse_request_date, parse_query_param, to_dict_mapper

@require_http_methods(["GET"])
def pong(request):
    return HttpResponse("<p>Pong</p>")

@require_http_methods(["GET"])
@csrf_exempt
def get_assets(request):
    assets = marketSelector.assets_list()
    return JsonResponse({
        "instances": to_dict_mapper(assets)}, status=200)

@require_http_methods(["GET"])
@csrf_exempt
def get_portfolios(request):
    portfolios = portfolioSelector.portfolios_list()
    return JsonResponse({
        "instances": to_dict_mapper(portfolios)}, status=200)

@require_http_methods(["GET"])
@csrf_exempt
def get_portfolio_value(request, portfolio_id):
    values = portfolioSelector.portfolio_value_list(
        portfolio_id=portfolio_id,
        date_from=parse_request_date(
            parse_query_param(request, 'from')),
        date_to=parse_request_date(
            parse_query_param(request, 'to')))
    return JsonResponse({
        "portfolio_id": portfolio_id,
        "values": to_dict_mapper(list(values))}, status=200)

@require_http_methods(["GET"])
@csrf_exempt
def get_weights(request, portfolio_id):
    weights = portfolioSelector.weight_list(
        portfolio_id=portfolio_id,
        date_from=parse_request_date(
            parse_query_param(request, 'from')),
        date_to=parse_request_date(
            parse_query_param(request, 'to')))
    weight_response_list = to_dict_mapper(weights)
    
    by_date_grouping = {}
    for weight_response in weight_response_list:
        date_str = weight_response["date"]
        if date_str not in by_date_grouping:
            by_date_grouping[date_str] = {"date": date_str}
        by_date_grouping[date_str][
        weight_response["asset_name"]] = float(weight_response["amount"])
    
    return JsonResponse({
        "portfolio_id": portfolio_id,
        "weights": list(by_date_grouping.values())}, status=200)


def portfolioviz_exception_handler(exc, ctx):
  print("-------------------------")
  if isinstance(exc, BadDateFormatException):
      exc = HttpResponseBadRequest()
  
  if isinstance(exc, Http404):
      exc = exceptions.NotFound()
  
  response = exception_handler(exc, ctx)
  
  return response