// DRAW GOOGLE-CHART DIAGRAM
function Draw() {
    $.ajax({
        method: 'GET',
        url: '/draw_calendar_graphic/',
        dataType: 'json',
        data: {
            'start_date': $('#start_date').val(),
            'end_date': $('#end_date').val(),
            'iso': $('#iso').val(),
        },
        contentType: 'application/json; charset=utf-8',

        success: function (rates) {
            alert('success !!!');

            google.charts.load('current', {'packages': ['corechart']});
            google.charts.setOnLoadCallback(drawChart);

            function drawChart() {
                let iso_code = $('#iso').val();
                console.log(rates);
                let arr = [];
                var data = google.visualization.arrayToDataTable([
                    ['Date', 'ISO']
                ]);
                for (let i = 0; i < rates.length; i++) {
                    alert('i = ' + i);
                    alert('i = ' + rates[i]['USD']);
                    console.log('i = ' + rates[i]);
                    for (let key in rates[i]) {
                        alert(key + ' // ' + rates[i][key][iso_code]);
                        arr[key] = rates[key][iso_code];
                        data.push(arr);
                    }
                }
                console.log(data);

                let options = {
                    title: 'Company Performance',
                    curveType: 'function',
                    legend: {position: 'bottom'}
                };

                let chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

                chart.draw(data, options);

                let attr = document.createAttribute('style');
                attr.value = "width: 900px; height: 500px";
                document.getElementById('curve_chart').setAttributeNode(attr);
            }

        },
        errors: function (e) {
            alert(e);
        }
    })
}


// By_date_by_iso
function changeDate() {
    $.ajax({
        method: 'GET',
        url: '/by_date/',
        dataType: 'json',
        data: {'date': $('#date').val()},
        contentType: 'application/json; charset=utf-8',

        success: function (rates) {
            let response =
                '<table class="table thead-dark">' +
                '<tr class="thead-dark">' +
                '<th scope="col">ISO</th>' +
                '<th scope="col">Amount</th>' +
                '<th scope="col">Rate</th>' +
                '<th scope="col">Difference</th>' +
                '</tr>';
            for (let val in rates) {
                response += '<tr>';
                for (let item in rates[val]) {
                    response += '<td>' + rates[val][item] + '</td>';
                }
                response += '</tr>';
            }
            response += '</table>';

            let attr = document.createAttribute('class');
            attr.value = 'row';
            document.getElementById('response').setAttributeNode(attr);
            document.getElementById('response').innerHTML = response;
        },
        errors: function (e) {
            alert(e);
        }
    })
}