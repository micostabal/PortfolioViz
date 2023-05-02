import pandas as pd
from typing import List
from dataclasses import dataclass
from portfolioviz.models import Asset, MyModel, \
  Portfolio, PortfolioValue, Quantity, Weight, Price
from portfolioviz.settings import DATA_PATH_NAME


@dataclass
class RawPortfolioData:
	assets: List[str]
	portfolios: List[str]
	initial_weights: pd.DataFrame	
	prices: pd.DataFrame
	dates: List[pd.Timestamp]
	initial_date: pd.Timestamp
	initial_value: int


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
      V0 = 1_000_000_000
      
      return RawPortfolioData(
        assets,
        portfolios,
        df_initial_weights,
        df_prices,
        dates,
        initial_date,
        V0)


class DataLoader:
    
  def load_data(self, raw_data : RawPortfolioData) -> None:
    MyModel.objects.create(
      name='Instance 1', description='Description 1')
    MyModel.objects.create(
      name='Instance 2', description='Description 2')
    
    for portfolio_name in raw_data.portfolios:
      Portfolio.objects.create(name=portfolio_name)
    
    for asset in raw_data.assets:
      Asset.objects.create(name=asset)
        
    for portfolio_name in raw_data.portfolios:
      portfolio = Portfolio.objects.get(name=portfolio_name)
      for asset_name in raw_data.assets:
          asset = Asset.objects.get(name=asset_name)
          weight = raw_data.initial_weights.loc[
             (raw_data.initial_date, asset_name)][portfolio_name]
          price = raw_data.prices.loc[
             raw_data.initial_date][asset_name]
          
          Quantity.objects.create(
            amount=weight * raw_data.initial_value / price,
            portfolio=portfolio,
            asset=asset)
    

    for portfolio_name in raw_data.portfolios:
      portfolio = Portfolio.objects.get(name=portfolio_name)
      for tt_date in raw_data.dates:
        date = tt_date.date()
        x_asset = {}
        value = 0
        for asset_name in raw_data.assets:
            asset = Asset.objects.get(name=asset_name)
            
            quantity = Quantity.objects.get(
               portfolio=portfolio,
               asset=asset
            )

            raw_price = raw_data.prices.loc[tt_date][asset_name]

            Price.objects.create(
              amount=raw_price,
              asset=asset,
              date=date
            )
            x = raw_price * float(quantity.amount)
            x_asset[asset_name] = x
            value += x
        
        PortfolioValue.objects.create(
          amount=value,
          portfolio=portfolio,
          date=date
        )
        
        for asset_name in raw_data.assets:
            Weight.objects.create(
              amount = x_asset[asset_name] / value,
              portfolio=portfolio,
              asset=asset,
              date=date
            )
         
