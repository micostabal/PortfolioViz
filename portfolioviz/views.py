from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from portfolioviz.models import MyModel, Portfolio
  
def hello(request):  
    return HttpResponse("<h2>Hello, Welcome to Django!</h2>")

@csrf_exempt
def my_view(request):
    instances = MyModel.objects.all()
    context = {'instances': list(map(lambda x: x.to_dict(), list(instances)))}
    return JsonResponse(context, status=200)

@csrf_exempt
def get_portfolios(request):
    portfolios = Portfolio.objects.all()
    return JsonResponse({
        'instances': list(map(lambda x: x.to_dict(), list(portfolios)))
    }, status=200)