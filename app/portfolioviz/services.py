import pandas as pd
from datetime import date
from typing import List
import logging
from dataclasses import dataclass
from portfolioviz.models import (
  Asset,
  Portfolio,
  PortfolioValue,
  Price,
  Quantity,
  Weight,
  Share
)
from portfolioviz.selectors import (
  marketSelector,
  portfolioSelector
)
from portfolioviz.settings import DATA_PATH_NAME
from portfolioviz.constants import INITIAL_VALUE, INITIAL_DATE
from portfolioviz.utils import Singleton

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

class MarketService(metaclass=Singleton):
  
  def asset_create(self, name):
    Asset.objects.create(name=name)

class PortfolioService(metaclass=Singleton):
  
  def quantity_create(self, portfolio, asset, amount, date):
    Quantity.objects.create(
      amount=amount,
      portfolio=portfolio,
      asset=asset,
      date = date)
  
  def weight_create(self, portfolio, asset, date, raw_weight):
    Weight.objects.create(
      amount=raw_weight,
      portfolio=portfolio,
      asset=asset,
      date=date)
    
  def portfolio_create(self, name) -> None:
    Portfolio.objects.create(name=name)

  def portfolio_value_create(self, portfolio, date, amount):
    PortfolioValue.objects.create(
      amount=amount,
      portfolio=portfolio,
      date=date)

  def price_create(self, amount, asset, date):
    Price.objects.create(
      amount=amount,
      asset=asset,
      date=date)
    
  def share_create(self, portfolio, asset, date, amount):
    Share.objects.create(
      portfolio=portfolio,
      asset=asset,
      amount=amount,
      date=date)


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


class DataExtractor(metaclass=Singleton):
    
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

  def __init__(self,
      market_selector,
      portfolio_selector,
      market_service,
      portfolio_service) -> None:
    self.market_selector = market_selector
    self.market_service= market_service
    self.portfolio_selector = portfolio_selector
    self.portfolio_service = portfolio_service
  
  def populate_db(self, raw_data: RawPortfolioData) -> None:
    logger.debug("This might take a while...")
    self.portfolios_load(raw_data)
    self.assets_load(raw_data)
    self.prices_load(raw_data)
    self.quantities_initial_load(raw_data)
    self.quantities_load_all_periods(raw_data)
    self.share_load_all_periods(raw_data)
    self.portfolio_values_load_all_periods(raw_data)
    self.weights_load_all_periods(raw_data)

  def all_dates(self, raw_data: RawPortfolioData):
    return list(map(lambda x: x.date(), raw_data.dates))
  
  def portfolios_load(self, raw_data: RawPortfolioData) -> None:
    logger.debug("Loading portfolios")
    for portfolio_name in raw_data.portfolios:
      self.portfolio_service.portfolio_create(portfolio_name)
  
  def assets_load(self, raw_data: RawPortfolioData):
    logger.debug("Loading assets")
    for asset in raw_data.assets:
      self.market_service.asset_create(asset)
      
  def prices_load(self, raw_data: RawPortfolioData) -> None:
    logger.debug("Loading market prices")
    for tt_date in raw_data.dates:
      for asset_name in raw_data.assets:
        asset = self.market_selector.asset_get(name=asset_name)
        raw_price = raw_data.prices.loc[tt_date][asset_name]
        self.portfolio_service.price_create(raw_price, asset, tt_date.date())
    
  def quantities_initial_load(self, raw_data: RawPortfolioData) -> None:
    logger.debug("Calculating and loading initial quantities")
    for portfolio_name in raw_data.portfolios:
      portfolio = self.portfolio_selector.portfolio_get(name=portfolio_name)
      for asset in self.market_selector.assets_list():
        weight = raw_data.initial_weights.loc[
          (raw_data.initial_date, asset.name)][portfolio_name]
        price = raw_data.prices.loc[
          raw_data.initial_date][asset.name]
        amount = EntityRelations.quantity_from_weight_value_price(
            weight, raw_data.initial_value, price)
        initial_operating_date = INITIAL_DATE
        
        self.portfolio_service.quantity_create(
          portfolio,
          asset,
          amount,
          initial_operating_date)
        
  def quantities_load_all_periods(self, raw_data: RawPortfolioData) -> None:
    logger.debug("Calculating and loading remaining quantities")
    initial_market_date = INITIAL_DATE
    
    for portfolio in self.portfolio_selector.portfolios_list():
      for asset in self.market_selector.assets_list():
        previous_date = initial_market_date
        for dt_date in self.all_dates(raw_data):
          if dt_date==initial_market_date:
            continue
          
          previous_quantity = self.portfolio_selector.quantity_get(
            portfolio, asset, previous_date)
          
          ## TODO : complete
          previous_transactions_amount = 0
          
          self.portfolio_service.quantity_create(
            portfolio,
            asset,
            previous_quantity.amount + previous_transactions_amount,
            dt_date)
          previous_date = dt_date
          
  def share_load_all_periods(self, raw_data: RawPortfolioData):
    logger.debug("Loading shares")
    for portfolio in self.portfolio_selector.portfolios_list():
      for dt_date in self.all_dates(raw_data):
        for asset in self.market_selector.assets_list():
          price = self.market_selector.price_get(asset, dt_date)
          quantity = self.portfolio_selector.quantity_get(portfolio, asset, dt_date)
          self.portfolio_service.share_create(
            portfolio,
            asset,
            dt_date,
            EntityRelations.share_from_price_quantity(
              price.amount, quantity.amount))
  
  def portfolio_values_load_all_periods(self, raw_data: RawPortfolioData):
    logger.debug("Loading portfolio values")
    for portfolio in self.portfolio_selector.portfolios_list():
      for dt_date in self.all_dates(raw_data):
        value_amount = 0
        for asset in self.market_selector.assets_list():
          share = self.portfolio_selector.share_get(portfolio, asset, dt_date)
          value_amount += share.amount
        self.portfolio_service.portfolio_value_create(
          portfolio, dt_date, value_amount)
  
  def weights_load_all_periods(self, raw_data: RawPortfolioData) -> None:
    logger.debug("Loading asset weights")
    for portfolio in self.portfolio_selector.portfolios_list():
      for dt_date in self.all_dates(raw_data):
        value = self.portfolio_selector.portfolio_value_get(portfolio, dt_date)
        for asset in self.market_selector.assets_list():
          share = self.portfolio_selector.share_get(portfolio, asset, dt_date)
          self.portfolio_service.weight_create(
            portfolio,
            asset,
            dt_date,
            EntityRelations.weight_from_share_value(
              share.amount, value.amount))


dataExtractor = DataExtractor()

marketService = MarketService()

portfolioService = PortfolioService()

entityLoader = EntityLoader(
  marketSelector,
  portfolioSelector,
  marketService,
  portfolioService
)