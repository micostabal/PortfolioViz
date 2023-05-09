from django.db import models
from portfolioviz.settings import DATE_FORMAT


class PortfolioBaseModel(models.Model):
    
    class Meta:
        app_label = 'portfolioviz'
        abstract=True


class Portfolio(PortfolioBaseModel):
    name = models.CharField(max_length=30, unique=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name}


class Asset(PortfolioBaseModel):
    name = models.CharField(max_length=30, unique=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name}


class MarketOperatingDate(PortfolioBaseModel):
    date = models.DateField(unique=True)
    nextOperatingDate = models.OneToOneField(
        'self',
        null=True,
        blank=True,
        related_name="next",
        on_delete=models.SET_NULL)
    
    def to_dict(self):
        return {"date": self.id}
    
    def setNext(self, nextMarketOperatingDate):
        self.nextOperatingDate = nextMarketOperatingDate


class Share(PortfolioBaseModel):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=6, max_digits=40)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    marketOperatingDate = models.ForeignKey(
        MarketOperatingDate, on_delete=models.CASCADE)
    
    def to_dict(self):
        return {
            "id": self.id,
            "asset_name": self.asset.name,
            "amount": self.amount,
            "date": self.marketOperatingDate.date}


class Price(PortfolioBaseModel):
    amount = models.DecimalField(decimal_places=6, max_digits=40)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    marketOperatingDate = models.ForeignKey(MarketOperatingDate, on_delete=models.CASCADE)
    
    def to_dict(self):
        return {
            "amount": self.amount,
            "date": self.marketOperatingDate.date,
            "asset_name": self.asset.name}


class Quantity(PortfolioBaseModel):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    marketOperatingDate = models.ForeignKey(MarketOperatingDate, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=6, max_digits=40)
    
    def to_dict(self):
        return {"amount": self.amount}
    

class QuantityTransaction(PortfolioBaseModel):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    marketOperatingDate = models.ForeignKey(MarketOperatingDate, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=6, max_digits=40)
    
    def to_dict(self):
        return {
            "amount": self.amount,
            "date": self.marketOperatingDate.date.strftime(DATE_FORMAT)}


class Weight(PortfolioBaseModel):
    amount = models.DecimalField(decimal_places=6, max_digits=40)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    marketOperatingDate = models.ForeignKey(MarketOperatingDate, on_delete=models.CASCADE)

    def to_dict(self):
        return {
            "amount": self.amount,
            "date": self.marketOperatingDate.date.strftime(DATE_FORMAT),
            "asset_name": self.asset.name}


class PortfolioValue(PortfolioBaseModel):
    amount = models.DecimalField(decimal_places=6, max_digits=40)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    marketOperatingDate = models.ForeignKey(MarketOperatingDate, on_delete=models.CASCADE)
    
    def to_dict(self):
        return {
            "amount": self.amount,
            "date": self.marketOperatingDate.date.strftime(DATE_FORMAT)}