from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from portfolioviz.selectors import (
    portfolios_list,
    assets_list_response,
    portfolio_value_list,
    weight_list
)
from portfolioviz.utils import parse_request_date

def pong(request):
    return HttpResponse("<p>Pong</p>")

@csrf_exempt
def get_assets(request):
    assets = assets_list_response()
    return JsonResponse({
        "instances": assets}, status=200)

@csrf_exempt
def get_portfolios(request):
    portfolios = portfolios_list()
    return JsonResponse({
        "instances": portfolios}, status=200)

@csrf_exempt
def get_portfolio_value(request, portfolio_id):
    from_str = request.GET.get('from', None)
    to_str = request.GET.get('to', None)
    values = portfolio_value_list(
        portfolio_id=portfolio_id,
        date_from=parse_request_date(from_str),
        date_to=parse_request_date(to_str))
    return JsonResponse({
        "portfolio_id": portfolio_id,
        "values": values}, status=200)

@csrf_exempt
def get_weights(request, portfolio_id):
    from_str = request.GET.get('from', None)
    to_str = request.GET.get('to', None)
    weights = weight_list(
        portfolio_id=portfolio_id,
        date_from=parse_request_date(from_str),
        date_to=parse_request_date(to_str))
    return JsonResponse({
        "portfolio_id": portfolio_id,
        "weights": weights}, status=200)