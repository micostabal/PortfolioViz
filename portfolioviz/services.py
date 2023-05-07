import pandas as pd
from typing import List
import logging
from dataclasses import dataclass
from portfolioviz.models import (
  Asset,
  MarketOperatingDate,
  Portfolio,
  PortfolioValue,
  Quantity,
  Weight,
  Price
)
from portfolioviz.selectors import (
  asset_get,
  assets_list,
  portfolio_get,
  quantity_get
)
from portfolioviz.settings import DATA_PATH_NAME
from portfolioviz.constants import INITIAL_VALUE

logger = logging.getLogger(__name__)


@dataclass
class RawPortfolioData:
	assets: List[str]
	portfolios: List[str]
	initial_weights: pd.DataFrame	
	prices: pd.DataFrame
	dates: List[pd.Timestamp]
	initial_date: pd.Timestamp
	initial_value: int
        

def quantity_create(portfolio, asset, amount):
  Quantity.objects.create(
    amount=amount,
    portfolio=portfolio,
    asset=asset)

def weight_create(portfolio, asset, date, raw_weight):
  Weight.objects.create(
    amount=raw_weight,
    portfolio=portfolio,
    asset=asset,
    date=date
  )

def portfolio_value_create(portfolio, value, date):
  PortfolioValue.objects.create(
    amount=value,
    portfolio=portfolio,
    date=date
  )

def price_create(amount, asset, date):
  Price.objects.create(
    amount=amount,
    asset=asset,
    date=date
  )


class EntityRelations:

  @staticmethod
  def weight_from_share_value(share, value):
    return share/value
  
  @staticmethod
  def quantity_from_weight_value_price(weight, value, price):
    return weight * value / price
  
  @staticmethod
  def share_from_price_quantity(price, quantity):
    return price * quantity


class EntityLoader:
  
  def load_data(self, raw_data : RawPortfolioData) -> None:
    logger.debug("This might take a while...")
    self.portfolios_load(raw_data)
    self.assets_load(raw_data)
    self.market_operating_dates_load(raw_data)
    self.quantities_load(raw_data)

  
  def portfolios_load(self, raw_data : RawPortfolioData) -> None:
    logger.debug("Loading portfolios")
    for portfolio_name in raw_data.portfolios:
      Portfolio.objects.create(name=portfolio_name)

  def assets_load(self, raw_data : RawPortfolioData):
    logger.debug("Loading assets")
    for asset in raw_data.assets:
      Asset.objects.create(name=asset)

  def market_operating_dates_load(self, raw_data : RawPortfolioData) -> None:
    logger.debug("Loading market operating dates")
    created_dates = []
    for date_ts in raw_data.dates:
      created_dates.append(MarketOperatingDate(
        date=date_ts.date()
      ))
    for element, succesor in zip(created_dates, created_dates[:1]):
      element.setNext(succesor)
    for element in created_dates:
      element.save()
    
  def prices_load(self, raw_data : RawPortfolioData) -> None:
    logger.debug("Loading market prices")
    for tt_date in raw_data.dates:
      date = tt_date.date()
      for asset_name in raw_data.assets:
        asset = asset_get(asset_name)
        raw_price = raw_data.prices.loc[tt_date][asset_name]
        
        price_create(raw_price, asset, date)

  def weights_initial_load(self, raw_data : RawPortfolioData) -> None:
    logger.debug("Loading initial weights")
    for portfolio_name in raw_data.portfolios:
      portfolio = portfolio_get(portfolio_name)
      for asset in assets_list():
        raw_weight = raw_data.initial_weights.loc[
          (raw_data.initial_date, asset.name)][portfolio_name]
        weight_create(
          portfolio,
          asset,
          raw_data.initial_date.date(),
          raw_weight)
  
  def quantities_load(self, raw_data : RawPortfolioData) -> None:
    logger.debug("Calculating and loading quantities")
    for portfolio_name in raw_data.portfolios:
      portfolio = portfolio_get(portfolio_name)
      
      for asset in assets_list():
        weight = raw_data.initial_weights.loc[
          (raw_data.initial_date, asset.name)][portfolio_name]
        price = raw_data.prices.loc[
          raw_data.initial_date][asset.name]
        
        quantity_create(
          portfolio,
          asset,
          EntityRelations.quantity_from_weight_value_price(
            weight, raw_data.initial_value, price))
          
  # def value_weight_load(self, raw_data: RawPortfolioData) -> None:
  #   logger.debug("Calculating and loading portfolio values and asset weights")
  #   for portfolio_name in raw_data.portfolios:
  #     portfolio = portfolio_get(portfolio_name)
  #     for tt_date in raw_data.dates:
  #       date = tt_date.date()
  #       x_asset = {}
  #       value = 0
  #       for asset_name in raw_data.assets:
  #         asset = asset_get(asset_name)
          
  #         quantity = quantity_get(portfolio,asset)
          
  #         raw_price = raw_data.prices.loc[tt_date][asset_name]
          
  #         x = raw_price * float(quantity.amount)
  #         x_asset[asset_name] = x
  #         value += x
        
  #       portfolio_value_create(
  #         portfolio, value, date)
        
  #       for asset_name in raw_data.assets:
  #           asset = asset_get(asset_name)
  #           weight_create(
  #             portfolio,
  #             asset,
  #             date,
  #             EntityRelations.weight_from_share_value(x_asset[asset_name], value))
