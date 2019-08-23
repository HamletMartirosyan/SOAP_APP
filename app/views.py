from django.shortcuts import render
from datetime import datetime
from .models import Exchange
from zeep import Client


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

    num1 = rate1 / amount1
    num2 = rate2 / amount2
    if num2 != 0:
        return round(value * num1 / num2, 4)
    else:
        return "Rate_2 is 0.0000"


def money_converter(count, rate, amount):
    count = float(count)
    rate = float(rate)
    amount = float(amount)
    print(f'\n\ncount ={count}\n\nRate = {rate}, Amount = {amount} \n\n')

    num = rate / amount
    result = round(count * num, 2)

    return result


def exchange_rates_by_date(request):  #
    date = datetime.now().strftime('%Y-%m-%d')
    iso = []
    amount = {}
    data = {}
    rate = {}
    difference = {}
    convert_value = ''
    count = ''

    # data = Exchange.objects.last()
    # iso = data.iso
    # print('ISO =', iso)
    # print('Exchange_rates_by_date_by_iso',exchange_rates_by_date_by_iso(date, 'USD'))

    if request.POST:
        if request.POST.get('date'):
            fdate = datetime.strptime(request.POST.get('date'), "%Y-%m-%d")
            client = Client('http://api.cba.am/exchangerates.asmx?wsdl')
            result = client.service.ExchangeRatesByDate(fdate)
            date = request.POST.get('date')

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

            exchange = Exchange(iso=iso, amount=amount, rate=rate, difference=difference, date=date)
            exchange.save()

        elif request.POST.get('count'):
            query = Exchange.objects.last()

            iso = str(query.iso[1:-1]).replace("'", "").split(', ')
            amount = str_to_dict(query.amount)
            rate = str_to_dict(query.rate)
            difference = str_to_dict(query.difference)

            iso_from = request.POST.get('select_from')
            iso_to = request.POST.get('select_to')
            amount_from = amount.get(iso_from)
            amount_to = amount.get(iso_to)
            rate_from = rate.get(iso_from)
            rate_to = rate.get(iso_to)
            count = request.POST.get('count')

            convert_value = convert_money(count, rate_from, amount_from, rate_to, amount_to)

            print("============================================= START ===============================================")
            print(f'count = {count}')
            print(f'iso_from = {iso_from}')
            print(f'iso_to = {iso_to}')
            print(f'amount_from = {amount_from}')
            print(f'amount_to = {amount_to}')
            print(f'rate_from = {rate_from}')
            print(f'rate_to = {rate_to}')
            print("============================================== END ================================================")

    context = {
        'date': date,
        'data': data,
        'iso': iso,
        'amount': amount,
        'rate': rate,
        'count': count,
        'difference': difference,
        'convert_value': convert_value,
    }

    return render(request, 'soap.html', context)


def exchange_rates_by_date_by_iso(date, iso):
    client = Client('http://api.cba.am/exchangerates.asmx?wsdl')
    result = client.service.ExchangeRatesByDateByISO(date, iso)
    return result


def exchange_rate(request):
    obj = Exchange.objects.last()

    date = datetime.now().strftime('%Y-%m-%d')
    iso = str(obj.iso[1:-1]).replace("'", "").split(', ')
    count = 1
    result = ''

    if request.POST:
        date = datetime.strptime(request.POST.get('date'), "%Y-%m-%d")
        iso = request.POST.get('iso', '')
        count = request.POST.get('count', '')

        data = exchange_rates_by_date_by_iso(date, iso)

        rate = data.Rates.ExchangeRate[0]['Rate']
        amount = data.Rates.ExchangeRate[0]['Amount']

        result = money_converter(count, rate, amount)

        iso = str(obj.iso[1:-1]).replace("'", "").split(', ')
        date = request.POST.get('date')

    context = {
        'date': date,
        'iso': iso,
        'count': count,
        'result': result,
    }

    return render(request, 'by_date_by_iso.html', context)
