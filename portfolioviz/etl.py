import pandas as pd
from typing import List
from dataclasses import dataclass
from portfolioviz.models import MyModel
from portfolioviz.settings import DATA_PATH_NAME


@dataclass
class RawPortfolioData:
	assets: List[str]
	portfolios: List[str]
	prices: pd.DataFrame
	quantities: pd.DataFrame
	values: pd.DataFrame
	weights: pd.DataFrame


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
      
      df_quantity = pd.DataFrame(
        index=pd.MultiIndex.from_product(
          [portfolios, assets], 
          names=["portfolio", "asset"]
        ),
        columns=['amount'])
      df_values = pd.DataFrame(
        index=pd.MultiIndex.from_product(
          [portfolios, dates],
          names=["portfolio", "date"]),
        columns=['amount'])
      df_weights = pd.DataFrame(
        index=pd.MultiIndex.from_product(
          [portfolios, dates, assets],
          names=["portfolio", "date", "asset"]),
        columns=['weight'])
      
      for index, row in df_quantity.iterrows():
        portfolio, asset = index
        weight = df_initial_weights.loc[(initial_date, asset)][portfolio]
        price = df_prices.loc[initial_date][asset]
        
        quantity = weight * V0 / price
        
        df_quantity.loc[(portfolio, asset)]['amount'] = quantity
      
      for index, row in df_values.iterrows():
        portfolio, date = index
        
        x_asset = {}
        value = 0
        for asset in assets:
          x = df_prices.loc[date][asset]*\
          df_quantity.loc[(portfolio, asset)]['amount']
          x_asset[asset] = x
          value += x
        
        df_values.loc[(portfolio, date)] = value
        
        for asset in assets:
            df_weights.loc[(portfolio, date, asset)]['weight'] =\
              x_asset[asset] / value
      
      return RawPortfolioData(
        assets,
        portfolios,
        df_prices,
        df_quantity,
        df_values,
        df_weights)


class DataLoader:
    
  def load_data(self, raw_data : RawPortfolioData) -> None:
    MyModel.objects.create(
      name='Instance 1', description='Description 1')
    MyModel.objects.create(
      name='Instance 2', description='Description 2')
    
		



