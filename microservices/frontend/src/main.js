function createStock() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            alert(this.responseText);
        }
    };
    xhttp.open("POST", "http://localhost:8080/api/v1.0/stocks", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    var stock_name = document.getElementsByName("stock")[0].value;
    var stock = {
        "name": stock_name
    };
    xhttp.send(JSON.stringify(stock));
}

function getRandomStock() {
    var request = new XMLHttpRequest();
    request.open('GET', 'http://localhost:8080/api/v1.0/stocks', true);
    request.onload = function () {
        var data = JSON.parse(this.response);

        if (request.status >= 200 && request.status < 400) {
            document.getElementById("stockSymbol").innerHTML = data.stock.name;
        } else {
            console.log('error')
        }
    };
    request.send()
}