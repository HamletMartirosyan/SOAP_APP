from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime, timedelta
from .models import Exchange
from zeep import Client
import json


def get_rates_by_date(date):
    client = Client('http://api.cba.am/exchangerates.asmx?wsdl')
    return client.service.ExchangeRatesByDate(date)


def get_rates_by_date_by_iso(date, iso):
    client = Client('http://api.cba.am/exchangerates.asmx?wsdl')
    return client.service.ExchangeRatesByDateByISO(date, iso)


def get_rates_latest():
    date = datetime.now().strftime('%Y-%m-%d')
    client = Client('http://api.cba.am/exchangerates.asmx?wsdl')
    return client.service.ExchangeRatesLatest(date)


def get_rates_latest_by_iso(iso):
    client = Client('http://api.cba.am/exchangerates.asmx?wsdl')
    return client.service.ExchangeRatesLatestByISO(iso)


def get_iso_codes():
    client = Client('http://api.cba.am/exchangerates.asmx?wsdl')
    return client.service.ISOCodes()


def index(request):
    return render(request, 'index.html', {})


def exchange_rates_by_date_by_iso(request):
    iso_code = ''
    iso = get_iso_codes()
    date = datetime.now().strftime('%Y-%m-%d')
    count = ''
    convert_value = ''

    post = request.POST
    if post:
        date = datetime.strptime(post.get('date'), "%Y-%m-%d")  # post.get('date')
        count = post.get('count')
        iso_code = post.get('iso')

        rates = get_rates_by_date_by_iso(date, iso_code).Rates.ExchangeRate[0]
        amount = rates.Amount
        rate = rates.Rate

        date = post.get('date')

        convert_value = convert_by_date_by_iso(
            float(count),
            float(rate),
            float(amount))

    context = {
        'iso': iso,
        'date': date,
        'count': count,
        'iso_code': iso_code,
        'convert_value': convert_value,
    }
    return render(request, 'by_date_by_iso.html', context)


def exchange_rates_by_date(request):
    date = datetime.strptime(request.GET.get('date'), "%Y-%m-%d")  # request.GET['date']
    data = get_rates_by_date(date).Rates.ExchangeRate
    iso = get_iso_codes()

    rates = {}
    for i, item in enumerate(data):
        rates[iso[i]] = {
            'ISO': item.ISO,
            'Amount': item.Amount,
            'Rate': item.Rate,
            'Difference': item.Difference,
        }

    return JsonResponse(rates)


def view_calendar_graphic(request):
    iso = get_iso_codes()
    start_date = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
    end_date = datetime.now().strftime("%Y-%m-%d")
    rates = {}
    ctx = {}

    if request.POST:
        start_date = datetime.strptime(request.POST.get('date1'), "%Y-%m-%d")  # request.POST['date']
        end_date = datetime.strptime(request.POST.get('date2'), "%Y-%m-%d")  # request.POST['date']

        if start_date != '' and end_date != '':
            delta = end_date - start_date

            dates = []
            for i in range(delta.days + 1):
                dates.append(start_date + timedelta(days=i))
                print(dates[i])

            data = {}
            for i, date in enumerate(dates):
                data[i] = get_rates_by_date(date).Rates.ExchangeRate

            iso = get_iso_codes()

            r = {}

            for i, d in enumerate(data):
                for j, item in enumerate(d):
                    r[iso[j]] = {
                        'ISO': item.ISO,
                        'Amount': item.Amount,
                        'Rate': item.Rate,
                        'Difference': item.Difference,
                    }
                rates[dates[i]] = r[iso[i]]
            print(f'rates => {rates}')
    ctx = {
        'iso': iso,
        'start_date': start_date,
        'end_date': end_date,
        'rates': rates,
    }
    return render(request, 'calendar_graphic.html', ctx)


def exchange_rates_latest(request):
    pass


def exchange_rates_latest_by_iso(request):
    pass


def exchange_rates_iso_codes(request):
    pass


def convert_by_date_by_iso(count, rate, amount):
    num = count * rate / amount
    return round(num, 3)


def str_to_dict(string):
    result = {}
    string = str(string.replace('{', '').replace("'", "")).split(', ')
    for item in string:
        key = str(item).split(': ')[0]
        val = str(item).split(': ')[1]
        result[key] = val
    return result


def convert_two_rates_by_date(value, rate1, amount1, rate2, amount2):
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
