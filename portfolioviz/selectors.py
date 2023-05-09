from datetime import date
from django.db.models import Min
from portfolioviz.models import (
  Asset,
  MarketOperatingDate,
  Portfolio,
  PortfolioValue,
  Price,
  Weight,
  Quantity,
  Share
)
from portfolioviz.constants import INITIAL_DATE
from portfolioviz.utils import to_dict_mapper, singleton

def asset_get(asset_name):
  return Asset.objects.get(name=asset_name)

def assets_list():
  return Asset.objects.all()

def assets_list_response():
  return to_dict_mapper(list(assets_list()))

def market_operating_date_get(date_dt: date):
  return MarketOperatingDate.objects.get(date=date_dt)

def market_operating_date_list():
  return MarketOperatingDate.objects.all()

def market_dates_from_range(date_from, date_to):
  return MarketOperatingDate.objects.filter(
    date__range=[
      date_from if date_from is not None else INITIAL_DATE,
      date_to if date_to is not None else date.today()
    ])

def portfolio_get(name):
  return Portfolio.objects.get(name=name)

def portfolios_list():
  return Portfolio.objects.all()

def portfolios_list_response():
  portfolios = portfolios_list()
  return to_dict_mapper(list(portfolios))

def price_get(asset, market_date):
  return Price.objects.get(asset=asset, marketOperatingDate=market_date)

def weights_get_date_range(portfolio, asset, date_from, date_to):
  market_dates=market_dates_from_range(date_from, date_to)
  return list(Weight.objects.filter(
    marketOperatingDate__in=market_dates,
    portfolio=portfolio,
    asset=asset))

def portfolio_value_get(portfolio: Portfolio, market_date):
  return PortfolioValue.objects.get(
    portfolio=portfolio, marketOperatingDate=market_date)

def portfolio_value_list(
    portfolio_id: str, 
    date_from: date,
    date_to: date):
  portfolio=Portfolio.objects.get(id=portfolio_id)
  market_dates=market_dates_from_range(date_from, date_to)
  values_raw = PortfolioValue.objects.filter(
    marketOperatingDate__in=market_dates,
    portfolio=portfolio
  )

  return to_dict_mapper(list(values_raw))

def share_get(portfolio, asset, market_operating_date):
  return Share.objects.get(
    portfolio=portfolio,
    asset=asset,
    marketOperatingDate=market_operating_date)

def quantity_get(portfolio, asset, market_operating_date):
  return Quantity.objects.get(
    portfolio=portfolio,
    asset=asset,
    marketOperatingDate=market_operating_date)

def weight_list(
    portfolio_id: str,
    date_from: date,
    date_to: date):
  portfolio = Portfolio.objects.get(id=portfolio_id)
  all_weights = []
  for asset in assets_list():
    weights_raw = weights_get_date_range(portfolio, asset, date_from, date_to)
    all_weights += to_dict_mapper(list(weights_raw))
  
  by_date_grouping = {}
  for weight_response in all_weights:
    date_str = weight_response["date"]
    if date_str not in by_date_grouping:
      by_date_grouping[date_str] = {"date": date_str}
    by_date_grouping[date_str][
      weight_response["asset_name"]] = float(weight_response["amount"])
  return list(by_date_grouping.values())


@singleton
class PortfolioSelector: pass


@singleton
class WeightDistributionSelector: pass


@singleton
class MarketInformationSelector:
  
  def say_hi(self):
    print("holakease")

  def fetch_initial_operating_date(self) -> date:
    min_date = MarketOperatingDate.objects.aggregate(
      Min('date'))['date__min']
    return MarketOperatingDate.objects.get(date=min_date)
  
  def assets_list(self): pass


@singleton
class PortfoliovizSelector:
  
  def __init__(self) -> None:
    self.market_selector = MarketInformationSelector()
    self.portfolio_selector = PortfolioSelector()
    self.weight_selector = WeightDistributionSelector()


portfoliovizSelector = PortfoliovizSelector()