from datetime import date
from django.http import Http404
from portfolioviz.models import (
  Asset,
  Portfolio,
  PortfolioValue,
  Price,
  Weight,
  Quantity,
  Share
)
from portfolioviz.constants import INITIAL_DATE
from portfolioviz.utils import Singleton


class MarketInformationSelector(metaclass=Singleton):
  
  def asset_get(self, **kwgs):
    return Asset.objects.get(**kwgs)
  
  def assets_list(self):
    return Asset.objects.all()
  
  def price_get(self, asset, date):
    return Price.objects.get(asset=asset, date=date)
  
  def fetch_initial_operating_date(self) -> date:
    ## TODO: Make with price query
    return INITIAL_DATE


class PortfolioSelector(metaclass=Singleton):
  
  def __init__(self, market_selector: MarketInformationSelector) -> None:
    self.market_selector = market_selector
  
  def portfolio_get(self, **kwgs):
    try:
      return Portfolio.objects.get(**kwgs)
    except Portfolio.DoesNotExist:
      raise Http404(f"No such portfolio: {str(kwgs)}")

  def portfolios_list(self):
    return Portfolio.objects.all()
  
  def share_get(self, portfolio, asset, date):
    return Share.objects.get(
      portfolio=portfolio,
      asset=asset,
      date=date)

  def quantity_get(self, portfolio, asset, date):
    return Quantity.objects.get(
      portfolio=portfolio,
      asset=asset,
      date=date)
  
  def portfolio_value_get(self, portfolio: Portfolio, date):
    return PortfolioValue.objects.get(
      portfolio=portfolio, date=date)
  
  def portfolio_value_list(
      self,
      portfolio_id: str, 
      date_from: date,
      date_to: date):
    portfolio = self.portfolio_get(id=portfolio_id)
    return PortfolioValue.objects.filter(
      date__range=PortfolioSelector.date_range(date_from, date_to),
      portfolio=portfolio)
  
  def weight_list(
      self,
      portfolio_id: str,
      date_from: date,
      date_to: date):
    portfolio = self.portfolio_get(id=portfolio_id)
    return list(Weight.objects.filter(
      date__range=PortfolioSelector.date_range(date_from, date_to),
      portfolio=portfolio))
  
  @staticmethod
  def date_range(date_from, date_to):
    return [
      date_from if date_from is not None else INITIAL_DATE,
      date_to if date_to is not None else date.today()
    ]


marketSelector = MarketInformationSelector()

portfolioSelector = PortfolioSelector(marketSelector)