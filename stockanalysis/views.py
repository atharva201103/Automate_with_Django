from django.shortcuts import render,redirect,get_object_or_404
from dal import autocomplete
from .models import Stock,Stockdata
from .forms import StockForm
from .utils import scrape_stock_data
from django.contrib import messages

# Create your views here.
def stock_view(request):
    if request.method=='POST':
        form=StockForm(request.POST)
        if form.is_valid():
            stock_id=request.POST.get('stock')
            stock=Stock.objects.get(pk=stock_id)
            symbol=stock.symbol
            exchange=stock.exchange
            stock_response=scrape_stock_data(symbol,exchange)
            if stock_response:
                try:
                    stock_data=Stockdata.objects.get(stock=stock)
                except Stockdata.DoesNotExist:
                    stock_data=Stockdata(stock=stock)

                stock_data.current_price=stock_response['current_price']
                stock_data.previous_close=stock_response['previous_close']
                stock_data.percentage_changed=stock_response['percentage_changed']
                stock_data.week_52_high=stock_response['week_52_high']
                stock_data.week_52_low=stock_response['week_52_low']
                stock_data.volume=stock_response['volume']
                stock_data.market_cap=stock_response['market_cap']
                stock_data.pe_ratio=stock_response['pe_ratio']
                stock_data.dividend_yield=stock_response['dividend_yield']
                stock_data.save()
                print('Data Updated!')
                return redirect('stock-detail', pk=stock_data.pk)
            else:
                messages.error(request,f"Could not retrieve stock data. for stock {symbol}")
                return redirect('stock')

            # Do something with the selected stock
    form=StockForm()
    context={
        'form':form,
    }
    
    return render(request,'stockanalysis/stock.html',context)

class StockAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor 
        qs = Stock.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
    
def stock_detail_view(request,pk):
    stock_data=get_object_or_404(Stockdata,pk=pk)
    context={
        'stock_data':stock_data,
    }
    return render(request,'stockanalysis/stock_detail.html',context)
