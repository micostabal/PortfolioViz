import pandas as pd
from datetime import date
from typing import List
import logging
from dataclasses import dataclass
from portfolioviz.models import (
  Asset,
  MarketOperatingDate,
  Portfolio,
  PortfolioValue,
  Price,
  Quantity,
  Weight,
  Share
)
from portfolioviz.selectors import (
  asset_get,
  assets_list,
  portfolio_get,
  portfolios_list,
  price_get,
  quantity_get,
  market_operating_date_list,
  market_operating_date_get,
  share_get,
  portfolio_value_get,
  portfoliovizSelector
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
        

def quantity_create(portfolio, asset, amount, marketOperatingDate):
  Quantity.objects.create(
    amount=amount,
    portfolio=portfolio,
    asset=asset,
    marketOperatingDate = marketOperatingDate)

def weight_create(portfolio, asset, market_date, raw_weight):
  Weight.objects.create(
    amount=raw_weight,
    portfolio=portfolio,
    asset=asset,
    marketOperatingDate=market_date)

def portfolio_value_create(portfolio, market_date, amount):
  PortfolioValue.objects.create(
    amount=amount,
    portfolio=portfolio,
    marketOperatingDate=market_date)

def price_create(amount, asset, market_date):
  Price.objects.create(
    amount=amount,
    asset=asset,
    marketOperatingDate=market_date)
  
def share_create(portfolio, asset, market_operating_date, amount):
  Share.objects.create(
    portfolio=portfolio,
    asset=asset,
    amount=amount,
    marketOperatingDate=market_operating_date)


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


class DataExtractor:
    
    def extract_data(self) -> RawPortfolioData:
      df_initial_weights = pd.read_excel(
        DATA_PATH_NAME,
        sheet_name='weights'
      )
      df_initial_weights.set_index(['Fecha', 'activos'], inplace=True)
      
      df_prices=pd.read_excel(DATA_PATH_NAME, sheet_name='Precios')
      df_prices.set_index('Dates', inplace=True)
      assets = df_prices.columns.tolist()
      dates = df_prices.index.tolist()
      initial_date = dates[0]
      portfolios = df_initial_weights.columns.tolist()
      
      return RawPortfolioData(
        assets,
        portfolios,
        df_initial_weights,
        df_prices,
        dates,
        initial_date,
        INITIAL_VALUE)


class EntityLoader:
  
  def populate_db(self, raw_data: RawPortfolioData) -> None:
    logger.debug("This might take a while...")
    self.portfolios_load(raw_data)
    self.assets_load(raw_data)
    self.market_operating_dates_load(raw_data)
    self.prices_load(raw_data)
    self.quantities_initial_load(raw_data)
    self.quantities_load_all_periods()
    self.share_load_all_periods()
    self.portfolio_values_load_all_periods()
    self.weights_load_all_periods()
  
  def portfolios_load(self, raw_data: RawPortfolioData) -> None:
    logger.debug("Loading portfolios")
    for portfolio_name in raw_data.portfolios:
      Portfolio.objects.create(name=portfolio_name)
  
  def assets_load(self, raw_data: RawPortfolioData):
    logger.debug("Loading assets")
    for asset in raw_data.assets:
      Asset.objects.create(name=asset)
  
  def market_operating_dates_load(self, raw_data: RawPortfolioData) -> None:
    logger.debug("Loading market operating dates")
    created_dates = []
    for date_ts in raw_data.dates:
      current = MarketOperatingDate(
        date=date_ts.date()
      )
      current.save()
      created_dates.append(current)
    for element, succesor in zip(created_dates, created_dates[:1]):
      element.setNext(succesor)
    
  def prices_load(self, raw_data: RawPortfolioData) -> None:
    logger.debug("Loading market prices")
    for tt_date in raw_data.dates:
      marketOperatingDate = market_operating_date_get(tt_date.date())
      for asset_name in raw_data.assets:
        asset = asset_get(asset_name)
        raw_price = raw_data.prices.loc[tt_date][asset_name]
        price_create(raw_price, asset, marketOperatingDate)
    
  def quantities_initial_load(self, raw_data: RawPortfolioData) -> None:
    logger.debug("Calculating and loading initial quantities")
    for portfolio_name in raw_data.portfolios:
      portfolio = portfolio_get(portfolio_name)
      
      for asset in assets_list():
        weight = raw_data.initial_weights.loc[
          (raw_data.initial_date, asset.name)][portfolio_name]
        price = raw_data.prices.loc[
          raw_data.initial_date][asset.name]
        amount = EntityRelations.quantity_from_weight_value_price(
            weight, raw_data.initial_value, price)
        initial_operating_date = portfoliovizSelector.market_selector.fetch_initial_operating_date()
        
        quantity_create(
          portfolio,
          asset,
          amount,
          initial_operating_date)
        
  def quantities_load_all_periods(self) -> None:
    logger.debug("Calculating and loading remaining quantities")
    initial_market_date = portfoliovizSelector.market_selector.fetch_initial_operating_date()
    
    for portfolio in portfolios_list():
      for asset in assets_list():
        previous_date = initial_market_date
        for market_date in market_operating_date_list():
          if market_date.date==initial_market_date.date:
            continue
          
          previous_quantity = quantity_get(portfolio, asset, previous_date)
          
          ## TODO : complete
          previous_transactions_amount = 0
          
          quantity_create(
            portfolio,
            asset,
            previous_quantity.amount + previous_transactions_amount,
            market_date)
          previous_date = market_date
          
  def share_load_all_periods(self):
    logger.debug("Loading shares")
    for portfolio in portfolios_list():
      for market_date in market_operating_date_list():
        for asset in assets_list():
          price = price_get(asset, market_date)
          quantity = quantity_get(portfolio, asset, market_date)
          share_create(
            portfolio,
            asset,
            market_date,
            EntityRelations.share_from_price_quantity(
              price.amount, quantity.amount))
  
  def portfolio_values_load_all_periods(self):
    logger.debug("Loading portfolio values")
    for portfolio in portfolios_list():
      for market_date in market_operating_date_list():
        value_amount = 0
        for asset in assets_list():
          share = share_get(portfolio, asset, market_date)
          value_amount += share.amount
        portfolio_value_create(portfolio, market_date, value_amount)
  
  def weights_load_all_periods(self) -> None:
    logger.debug("Loading asset weights")
    for portfolio in portfolios_list():
      for market_date in market_operating_date_list():
        value_amount = portfolio_value_get(portfolio, market_date).amount
        for asset in assets_list():
          share = share_get(portfolio, asset, market_date)
          weight_create(
            portfolio,
            asset,
            market_date,
            EntityRelations.weight_from_share_value(
              share.amount, value_amount))