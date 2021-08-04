const url = "http://flip1.engr.oregonstate.edu:4949/"

function fetchData(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        buildTable(JSON.parse(this.responseText));
        }
    };
    xhttp.open("GET", url, true);
    xhttp.send();
}

function buildTable(data){
    var table = document.getElementById('resultTable');
    table.innerHTML = '';
    console.log(data);
    table.appendChild(buildTh(['Name','Reps','Weight','Date','Unit','Edit Button','Delete Button']));
    data.data.forEach(d =>{
        table.appendChild(buildTd(d));
    });

    var editBtns = document.getElementsByClassName("Edit");

    for (var i = 0; i < editBtns.length; i++) {
        editBtns[i].addEventListener('click', function(e){
            var data = getUpdateData(e.target);
            updateData(data);
        });
    }

    var deleteBtns = document.getElementsByClassName("Delete");

    for (var i = 0; i < deleteBtns.length; i++) {
        deleteBtns[i].addEventListener('click', function(e){
            var data = getUpdateData(e.target);
            deleteData(data);
        });
    }
}

function buildTh(data){
    var tr = document.createElement("tr");
    data.forEach(e =>{
        let th = document.createElement("th");
        th.innerText = e;
        tr.appendChild(th);
    });
    return tr;
}

function buildTd(data){
    var tr = document.createElement("tr");
    
    Object.entries(data).forEach(entry => {
        const [keys,values] = entry;
        if(keys == 'name'){
            tr.appendChild(buildInput(values,keys,'text'));
        }else if(keys == 'reps' || keys == 'weight'){
            tr.appendChild(buildInput(values,keys,'number'));
        }else if(keys == 'date'){
            tr.appendChild(buildInput(values,keys,'date'));
        }else if(keys == 'lbs'){
            tr.appendChild(buildRadio(values,keys, data.id));
        }else if(keys == 'id'){
            tr.appendChild(buildInput(values,keys,'hidden'));
        }
    })

    tr.appendChild(buildButton('Edit'));
    tr.appendChild(buildButton('Delete'));
    
    return tr;
}

function buildButton(text){
    var td = document.createElement("td");
    var button = document.createElement('button');
    button.innerText = text;
    button.setAttribute('class',text);
    button.setAttribute('type','button');
    td.appendChild(button);
    return td;
}

function buildInput(data,key,type){
    if(type != 'hidden'){
        var td = document.createElement("td");
        var input = document.createElement('input');
        input.setAttribute('type',type);
        input.setAttribute('class',key);
        if(key == 'date'){
            let returnDate = getFormattedDate(data);
            input.value = returnDate;
        }else{
            input.value = data;
        }
        
        td.appendChild(input);
        return td;
    }else{
        var input = document.createElement('input');
        input.setAttribute('type',type);
        input.setAttribute('class',key);
        input.value = data;
        return input;
    }
}

function buildRadio(value,keys,id){
    var td = document.createElement("td");
    var input = document.createElement('input');
    input.setAttribute('type','radio');
    input.setAttribute('class','unit');
    input.setAttribute('name','unit'+id);
    input.setAttribute('value','lbs');
    if(value == 1){
        input.setAttribute('checked',true);
    }
    td.appendChild(input);

    var label = document.createElement('label');
    label.innerText = 'lbs';
    td.appendChild(label);

    var input = document.createElement('input');
    input.setAttribute('type','radio');
    input.setAttribute('class','unit');
    input.setAttribute('value','kg');
    input.setAttribute('name','unit'+id);
    if(value == 0){
        input.setAttribute('checked',true);
    }
    td.appendChild(input);


    var label = document.createElement('label');
    label.innerText = 'kg';
    td.appendChild(label);
    return td;
}

function getFormattedDate(date) {
    var newdate = date.substr(0, date.indexOf('T')); 
    return newdate;
}

function getNewData(target){
    let result = {};
    result.name = target.parentNode.querySelector('.name').value;
    result.reps = target.parentNode.querySelector('.reps').value;
    result.weight = target.parentNode.querySelector('.weight').value;
    result.date = target.parentNode.querySelector('.date').value;
    units = target.parentNode.getElementsByClassName('unit');
    for(var i=0; i< units.length; i++){
        if(units[i].checked){
            result.unit = units[i].value;
        }
    }
    return result;
}

function getUpdateData(target){
    let result = {};
    result.name = target.parentNode.parentNode.querySelector('.name').value;
    result.reps = target.parentNode.parentNode.querySelector('.reps').value;
    result.weight = target.parentNode.parentNode.querySelector('.weight').value;
    result.date = target.parentNode.parentNode.querySelector('.date').value;
    result.id = target.parentNode.parentNode.querySelector('.id').value;
    units = target.parentNode.parentNode.getElementsByClassName('unit');
    for(var i=0; i< units.length; i++){
        if(units[i].checked){
            result.unit = units[i].value;
        }
    }
    return result;
}

function insertData(data){
    var xhttp = new XMLHttpRequest();
    var params = {name: data.name,
        reps: data.reps,
        weight: data.weight,
        date: data.date,
        unit: (data.unit == 'lbs' ? '1' : '0')
    };
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        buildTable(JSON.parse(this.responseText));
        }
    };
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.send(JSON.stringify(params));
}

function updateData(data){
    var xhttp = new XMLHttpRequest();
    var params = {name: data.name,
        reps: data.reps,
        weight: data.weight,
        date: data.date,
        unit: (data.unit == 'lbs' ? '1' : '0'),
        id: data.id
    };
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        buildTable(JSON.parse(this.responseText));
        }
    };
    xhttp.open("PUT", url, true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.send(JSON.stringify(params));
}

function deleteData(data){
    var xhttp = new XMLHttpRequest();
    var params = {
        id: data.id
    };
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        buildTable(JSON.parse(this.responseText));
        }
    };
    xhttp.open("DELETE", url, true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.send(JSON.stringify(params));
}

document.getElementById('addBtn').addEventListener('click',function(e){
    var data = getNewData(e.target);
    insertData(data);
});

fetchData();
