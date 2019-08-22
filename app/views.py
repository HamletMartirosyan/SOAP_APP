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


# get data from SOAP
def exchange_rates_by_date(request):
    date = datetime.now().strftime('%Y-%m-%d')
    iso = []
    amount = {}
    data = {}
    rate = {}
    difference = {}
    convert_value = ''

    # data = Exchange.objects.last()
    # iso = data.iso
    # print('ISO =', iso)
    # print('Exchange_rates_by_date_by_iso',exchange_rates_by_date_by_iso(date, 'USD'))

    if request.POST:
        if request.POST.get('date'):
            date = request.POST.get('date') #datetime.strptime(request.POST.get('date'), "%Y-%m-%d")
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

            exchange = Exchange(iso=iso, amount=amount, rate=rate, difference=difference, date=date)
            exchange.save()

        elif request.POST.get('number'):
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
            number = request.POST.get('number')

            convert_value = convert_money(number, rate_from, amount_from, rate_to, amount_to)

            print("=========================================== START =================================================")
            print(f'number = {number}')
            print(f'iso_from = {iso_from}')
            print(f'iso_to = {iso_to}')
            print(f'amount_from = {amount_from}')
            print(f'amount_to = {amount_to}')
            print(f'rate_from = {rate_from}')
            print(f'rate_to = {rate_to}')
            print("================================================ END ==============================================")

    print('date=', date)
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


def exchange_rates_by_date_by_iso(date, iso):
    client = Client('http://api.cba.am/exchangerates.asmx?wsdl')
    result = client.service.ExchangeRatesByDateByISO(date, iso)
    return result
