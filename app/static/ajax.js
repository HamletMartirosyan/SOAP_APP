$(document).ready(function () {
    $("#date").change(
        function changeDate(event) {
            event.preventDefault();
            {
                #alert('changeDate()');

            }
            $.ajax({
                method: 'GET',
                url: '/by_date/',
                dataType: 'json',
                data: {'date': $('#date').val()},
                contentType: 'application/json; charset=utf-8',

                success: function (rates) {


                    /*var response =
                        '<table class="table thead-dark">' +
                        '<tr class="thead-dark">' +
                        '<th scope="col">ISO</th>' +
                        '<th scope="col">Amount</th>' +
                        '<th scope="col">Rate</th>' +
                        '<th scope="col">Difference</th>' +
                        '</tr>';
                    for (var val in rates) {
                        response += '<tr>';
                        for (var item in rates[val]) {
                            response += '<td>' + rates[val][item] + '</td>';
                        }
                        response += '</tr>';
                    }
                    response += '</table>';

                    var attr = document.createAttribute('class');
                    attr.value = 'row';
                    document.getElementById('response').setAttributeNode(attr);
                    document.getElementById('response').innerHTML = response;*/
                },
                errors: function (e) {
                    alert(e);
                }
            })
        })
});


// By_date_by_iso
$(document).ready(function () {
    $("#date").change(
        function changeDate(event) {
            event.preventDefault();
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
        })
});
// By_date_by_iso
