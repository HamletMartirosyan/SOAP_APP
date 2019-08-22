from django.shortcuts import render
from datetime import datetime
from zeep import Client
from .models import Exchange


def str_to_dict(string):
    result = {}
    string = str(string.replace('{', '').replace("'", "")).split(', ')
    for item in string:
        key = str(item).split(': ')[0]
        val = str(item).split(': ')[1]
        result[key] = val
    return result


def convert_money(value, rate1, amount1, rate2, amount2):
    value = float(value)
    rate1 = float(rate1)
    amount1 = float(amount1)
    rate2 = float(rate2)
    amount2 = float(amount2)

    r1 = rate1 / amount1
    r2 = rate2 / amount2
    if r2 != 0:
        return value * r1 / r2
    else:
        return "Rate_2 is 0.0000"


# get data from SOAP
def exchange_rates_by_date(request):
    date = datetime.now().strftime('%Y-%m-%d')
    iso = []
    amount = {}
    data = {}
    rate = {}
    difference = {}
    convert_value = ''

    if request.GET:
        data = Exchange.objects.last()
        iso = data.iso
        amount = data.amount
        rate = data.rate
        difference = data.differnce

    elif request.POST:
        if request.POST.get('date'):
            date = datetime.strptime(request.POST.get('date'), "%Y-%m-%d")
            client = Client('http://api.cba.am/exchangerates.asmx?wsdl')
            result = client.service.ExchangeRatesByDate(date)

            list_rates = list(result.Rates.ExchangeRate)

            for i, val in enumerate(list_rates, 1):
                data[i] = val

            for val in data.values():
                iso.append(val.ISO)
            for val in data.values():
                amount[val.ISO] = val.Amount
            for val in data.values():
                rate[val.ISO] = val.Rate
            for val in data.values():
                difference[val.ISO] = val.Difference

            d = Exchange(iso=iso, amount=amount, rate=rate, difference=difference, date=date)
            d.save()
        elif request.POST.get('number'):
            post = request.POST
            print("========================================== START =================================================")
            query = Exchange.objects.last()

            date = query.date

            iso = str(query.iso[1:-1]).replace("'", "").split(', ')
            amount = str_to_dict(query.amount)
            rate = str_to_dict(query.rate)
            difference = str_to_dict(query.difference)

            # print(f'iso ===> {iso}')
            # print(f'amount ===> {amount}')
            # print(f'rate ===> {rate}')
            # print(f'difference ===> {difference}')

            iso_from = post.get('select_from')
            iso_to = post.get('select_to')

            amount_from = amount.get(iso_from)
            amount_to = amount.get(iso_to)
            rate_from = rate.get(iso_from)
            rate_to = rate.get(iso_to)

            number = post.get('number')
            print(f'num = {number}')

            print(f'iso_from = {iso_from}')
            print(f'iso_to = {iso_to}')
            print(f'amount_from = {amount_from}')
            print(f'amount_to = {amount_to}')
            print(f'rate_from = {rate_from}')
            print(f'rate_to = {rate_to}')
            convert_value = convert_money(number, rate_from, amount_from, rate_to, amount_to)

            print(
                "================================================= END =================================================")

    context = {
        'date': date,
        'data': data,
        'iso': iso,
        'amount': amount,
        'rate': rate,
        'difference': difference,
        'convert_value': convert_value,
    }

    return render(request, 'soap.html', context)


def exchange_rates(request):
    context = {}
    post = request.POST
    print("=============================================== START =================================================")
    query = Exchange.objects.last()

    convert_value = ''
    date = query.date
    iso = query.iso
    amount = query.amount
    rate = query.rate
    difference = query.difference

    iso_from = post.get('select_from')
    iso_to = post.get('select_to')

    amount_from = amount.get(iso_from)
    amount_to = amount.get(iso_to)
    rate_from = rate.get(iso_from)
    rate_to = rate.get(iso_to)

    number = post.get('number')
    print(f'num = {number}')

    print(f'iso_from = {iso_from}')
    print(f'iso_to = {iso_to}')
    print(f'amount_from = {amount_from}')
    print(f'amount_to = {amount_to}')
    print(f'rate_from = {rate_from}')
    print(f'rate_to = {rate_to}')
    convert_value = convert_money(number, rate_from, amount_from, rate_to, amount_to)

    print("================================================= END =================================================")

    context = {
        # 'date': date,
        'difference': difference,
        'iso': iso,
        'amount': amount,
        'rate': rate,
        'convert_value': convert_value,
    }
    return render(request, 'soap.html', context)


"""

from django.shortcuts import render
from datetime import datetime
from zeep import Client


def convert_rate(value: float, rate1: float, amount1: int, rate2: float, amount2: int):
    r1 = rate1 / amount1
    r2 = rate2 / amount2
    if r2 != 0:
        return value * r1 / r2
    else:
        return "Rate_2 is 0.0000"


def exchange_rates_by_date(request):
    context = {}

    if request.POST:
        date = request.POST.get('date')
        if date != '':
            print("============================================================================================")

            client = Client('http://api.cba.am/exchangerates.asmx?wsdl')
            datetime_object = datetime.strptime(date, '%Y-%m-%d')

            result = client.service.ExchangeRatesByDate(datetime_object)
            list_rate = list(result.Rates.ExchangeRate)
            rates = {}
            for i, r in enumerate(list_rate, 1):
                rates[i] = r

            iso = []
            for val in rates.values():
                iso.append(val.ISO)

            amount = {}
            for val in rates.values():
                amount[val.ISO] = val.Amount

            rate = {}
            for val in rates.values():
                rate[val.ISO] = val.Rate

            '''    
            select_from = request.POST.get('select_from')
            select_to = request.POST.get('select_to')
            
            
            iso_from = request.POST.get('select_from')
            print(f'iso_from = {iso_from}')
            '''
            convert_value = "convert_value"

            print("============================================================================================")

            context = {
                'result': result,
                'rates': rates,
                'iso': iso,
                'amount': amount,
                'rate': rate,
                'convert_value': convert_value,
            }
    # elif request.GET:
    #     date = request.POST.get['date']
    #     context['date'] = date

    return render(request, 'soap.html', context)
"""
