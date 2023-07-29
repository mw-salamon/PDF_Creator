const selectBtn = document.querySelectorAll(".select-btn"),
        exchanges = document.querySelectorAll(".exchange"),
        currencies = document.querySelectorAll(".currency");

selectBtn.forEach(btn => {
    btn.addEventListener("click", () => {
        btn.classList.toggle("open");
    });
})

let exchangeList = []

exchanges.forEach(item => {
    item.addEventListener("click", () => {
        item.classList.toggle("checked");

        if(item.classList.contains("checked")) {
            exchangeList.push(item.innerText)
        } else {
            for(let i = 0; i < exchangeList.length; i++){
                if(exchangeList[i] == item.innerText){
                    lexchangeListist.splice(i, i+1);
                }
            }
        }
    })
})

let currList = []

currencies.forEach(item => {
    item.addEventListener("click", () => {
        item.classList.toggle("checked");

        if(item.classList.contains("checked")) {
            currList.push(item.innerText)
        } else {
            for(let i = 0; i < currList.length; i++){
                if(currList[i] == item.innerText){
                    currList.splice(i, i+1);
                }
            }
        }
    })
})

const form = document.querySelector(".form");

form.addEventListener("submit", (event) => {
    event.preventDefault();
    
    const selectedExchangesField = document.getElementById("selected_exchanges");
    const selectedCurrenciesField = document.getElementById("selected_currencies");
    selectedExchangesField.value = JSON.stringify(exchangeList);
    selectedCurrenciesField.value = JSON.stringify(currList);

    fetch("/add-to-exchange", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            selected_exchanges: exchangeList,
            selected_currencies: currList,
        }),
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        window.location.href = "/curr-opt";
    })
    .catch((error) => {
        console.error(error);
    });
});