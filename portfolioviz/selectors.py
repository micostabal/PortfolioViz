from typing import List, Dict
from datetime import date
from portfolioviz.models import (
  Asset,
  Portfolio,
  PortfolioValue,
  Weight,
  Quantity
)
from portfolioviz.constants import INITIAL_DATE
from portfolioviz.utils import to_dict_mapper

def asset_get(asset_name):
  return Asset.objects.get(name=asset_name)

def assets_list():
  return Asset.objects.all()

def assets_list_response():
  return to_dict_mapper(list(assets_list()))

def market_operating_date_get():
  pass

def market_operating_date_create():
  pass

def portfolio_get(name):
  return Portfolio.objects.get(name=name)

def portfolios_list():
  return Portfolio.objects.all()

def portfolios_list_response():
  portfolios = portfolios_list()
  return to_dict_mapper(list(portfolios))

def weights_get_date_range(portfolio, asset, date_from, date_to):
  return list(Weight.objects.filter(
    date__range=[
      date_from if date_from is not None else INITIAL_DATE,
      date_to if date_to is not None else date.today()
    ],
    portfolio=portfolio,
    asset=asset))

def portfolio_value_list(
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
  return to_dict_mapper(list(values_raw))

def quantity_get(portfolio, asset):
  return Quantity.objects.get(
    portfolio=portfolio,
    asset=asset
  )

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


class PortfolioValuesService: pass

class WeightDistributionService: pass
