const selectBtn = document.querySelector(".select-btn"), 
        items = document.querySelectorAll(".item"), 
        addBtn = document.querySelector(".add-from-list-btn"),
        addTmpBtn = document.querySelectorAll(".add-from-template-btn");

selectBtn.addEventListener("click", () => {
    selectBtn.classList.toggle("open");
});

let list = []

items.forEach(item => {
    item.addEventListener("click", () => {
        item.classList.toggle("checked");
        let checked = document.querySelectorAll(".checked"),
            btnText = document.querySelector(".curr-btn");

        if(item.classList.contains("checked")) {
            list.push(item.innerText)
        } else {
            for(let i = 0; i < list.length; i++){
                if(list[i] == item.innerText){
                    list.splice(i, i+1);
                }
            }
        }

        if(list.length == 0) {
            btnText.innerText = "Select";
        }else {
            btnText.innerText = list;
        }
    })
})

addBtn.addEventListener('click', function(event) {
    event.preventDefault();

    let form = document.createElement("form");
    let element1 = document.createElement("input");

    form.method = "POST";
    form.action = "/create-curr-pdf";  

    element1.value = list;
    
    element1.name = "currencies";
    form.appendChild(element1);

    document.body.appendChild(form);

    form.submit();
});

addTmpBtn.forEach(btn => {
    btn.addEventListener('click', function(event) {
        event.preventDefault();
    
        let form = document.createElement("form");
        let element1 = document.createElement("input");
    
        form.method = "POST";
        form.action = "/create-curr-pdf";  

        element1.value = btn.innerText;
        
        element1.name = "currencies";
        form.appendChild(element1);
    
        document.body.appendChild(form);
    
        form.submit();
    })
})