import pandas as pd
from typing import List
from dataclasses import dataclass
from portfolioviz.models import (
  Asset,
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


@dataclass
class RawPortfolioData:
	assets: List[str]
	portfolios: List[str]
	initial_weights: pd.DataFrame	
	prices: pd.DataFrame
	dates: List[pd.Timestamp]
	initial_date: pd.Timestamp
	initial_value: int


def quantity_create(portfolio, asset, weight, value, price):
  Quantity.objects.create(
    amount=weight * value / price,
    portfolio=portfolio,
    asset=asset)

def weight_create(portfolio, asset, date, share, value):
  Weight.objects.create(
    amount = share / value,
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


class DataExtractor:
    
    def extract_data(self) -> RawPortfolioData:
      df_initial_weights = pd.read_excel(DATA_PATH_NAME, sheet_name='weights')
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


class DataLoader:

  def load_data(self, raw_data : RawPortfolioData) -> None:
    self.portfolios_load(raw_data)
    self.assets_load(raw_data)
    self.quantities_load(raw_data)
    self.value_weight_price_load(raw_data)

  def portfolios_load(self, raw_data : RawPortfolioData):
    for portfolio_name in raw_data.portfolios:
      Portfolio.objects.create(name=portfolio_name)

  def assets_load(self, raw_data : RawPortfolioData):
    for asset in raw_data.assets:
      Asset.objects.create(name=asset)

  def quantities_load(self, raw_data : RawPortfolioData):
     for portfolio_name in raw_data.portfolios:
      portfolio = portfolio_get(portfolio_name)
      
      for asset in assets_list():
        weight = raw_data.initial_weights.loc[
          (raw_data.initial_date, asset.name)][portfolio_name]
        price = raw_data.prices.loc[
          raw_data.initial_date][asset.name]
        
        quantity_create(
          portfolio, asset, weight, raw_data.initial_value, price)
          
  def value_weight_price_load(self, raw_data: RawPortfolioData):
    for portfolio_name in raw_data.portfolios:
      portfolio = portfolio_get(portfolio_name)
      for tt_date in raw_data.dates:
        date = tt_date.date()
        x_asset = {}
        value = 0
        for asset_name in raw_data.assets:
          asset = asset_get(asset_name)
          
          quantity = quantity_get(portfolio,asset)
          
          raw_price = raw_data.prices.loc[tt_date][asset_name]
          
          price_create(raw_price, asset, date)
          
          x = raw_price * float(quantity.amount)
          x_asset[asset_name] = x
          value += x
        
        portfolio_value_create(
          portfolio, value, date)
        
        for asset_name in raw_data.assets:
            asset = asset_get(asset_name)
            weight_create(
              portfolio, asset, date, x_asset[asset_name], value)
