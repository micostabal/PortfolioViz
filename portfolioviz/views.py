from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from portfolioviz.models import MyModel
from portfolioviz.selectors import portfolios_get, assets_get, portfolio_value_get, weight_get
from portfolioviz.utils import parse_request_date

def hello(request):  
    return HttpResponse("<h2>Hello, Welcome to Django!</h2>")

@csrf_exempt
def my_view(request):
    instances = MyModel.objects.all()
    context = {'instances': list(map(lambda x: x.to_dict(), list(instances)))}
    return JsonResponse(context, status=200)

@csrf_exempt
def get_assets(request):
    assets = assets_get()
    return JsonResponse({
        "instances": assets}, status=200)

@csrf_exempt
def get_portfolios(request):
    portfolios = portfolios_get()
    return JsonResponse({
        "instances": portfolios}, status=200)

@csrf_exempt
def get_portfolio_value(request, portfolio_id):
    from_str = request.GET.get('from', None)
    to_str = request.GET.get('to', None)
    values = portfolio_value_get(
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
    weights = weight_get(
        portfolio_id=portfolio_id,
        date_from=parse_request_date(from_str),
        date_to=parse_request_date(to_str))
    return JsonResponse({
        "portfolio_id": portfolio_id,
        "weights": weights}, status=200)