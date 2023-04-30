from django.db import models


class PortfolioModelEntity(models.Model):

    class Meta:
        app_label = 'portfolioviz'



class MyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description
        }
    
    class Meta:
        app_label = 'portfolioviz'


class Asset(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def to_dict(self):
        return {"name": self.name}
    

class Price(models.Model):
    amount = models.DecimalField(decimal_places=6, max_digits=40)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()
    
    def to_dict(self):
        return {"amount": self.amount}
    
    class Meta:
        app_label = 'portfolioviz'


class Portfolio(models.Model):
    name = models.CharField(max_length=30, unique=True)
    
    def to_dict(self):
        return {"name": self.name}
    
    class Meta:
        app_label = 'portfolioviz'


class Quantity(models.Model):
    amount = models.DecimalField(decimal_places=6, max_digits=40)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    def to_dict(self):
        return {"amount": self.amount}
    
    class Meta:
        app_label = 'portfolioviz'


class Weight(models.Model):
    amount = models.DecimalField(decimal_places=6, max_digits=40)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        app_label = 'portfolioviz'