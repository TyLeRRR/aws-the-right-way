var stockSymbols = ["APPL", "ADBE", "AMZN", "GOOGL", "MSFT", "TSLA"];

function saveSymbol() {
    stockSymbols.push(document.getElementById("symbol_id").value);
    document.getElementById("symbol_id").value = "";
}

function showRandomStock() {
    var curr = stockSymbols[Math.floor(Math.random() * stockSymbols.length)];
    document.write(curr);
}