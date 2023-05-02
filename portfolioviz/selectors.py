from datetime import date
from portfolioviz.models import Asset, Portfolio, PortfolioValue, Weight
from portfolioviz.constants import INITIAL_DATE

def assets_get():
    assets = Asset.objects.all()
    return list(map(lambda x: x.to_dict(), list(assets)))

def portfolios_get():
    portfolios = Portfolio.objects.all()
    return list(map(lambda x: x.to_dict(), list(portfolios)))

def portfolio_value_get(
        portfolio_id: str, 
        date_from: date,
        date_to: date):
    portfolio = Portfolio.objects.get(id=portfolio_id)
    values_raw =PortfolioValue.objects.filter(
      date__range=[
          date_from if date_from is not None else INITIAL_DATE,
          date_to if date_to is not None else date.today()
      ],
      portfolio=portfolio)
    return list(map(lambda x: x.to_dict(), list(values_raw)))

def weight_get(
        portfolio_id: str,
        date_from: date,
        date_to: date):
    portfolio = Portfolio.objects.get(id=portfolio_id)
    all_weights = []
    for asset in Asset.objects.all():
      weights_raw = list(Weight.objects.filter(
        date__range=[
            date_from if date_from is not None else INITIAL_DATE,
            date_to if date_to is not None else date.today()
        ],
        portfolio=portfolio,
        asset=asset))
      all_weights += list(map(lambda x: x.to_dict(), list(weights_raw)))
    ## TODO: Group by date
    return all_weights