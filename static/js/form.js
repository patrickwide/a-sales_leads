

--------------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#try').onclick = () => {


    var name = "PATO"
    var email = "PATO"

    if(name == "" || email == "") {
    document.querySelector('#demo').innerHTML = "am blank";

    return false;
    } else {


    const request = new XMLHttpRequest();
    request.open('POST','/take');
    request.onload = () =>{
    const response = JSON.parse(request.responseText);
    if(response.success){
    const data = `i love ${response.email} ,${response.name}.`


    }
    else{
    document.querySelector('#demo').innerHTML = "there was a problem";

    }
    }
    const data = new FormData();
    data.append('name',name);
    data.append('email',email);
    request.send(data);
    return false;
    }

    }
});
---------------------------------------------------


    const request = new XMLHttpRequest();
    request.open('POST','/take');
    request.onload = () =>{
    const response = JSON.parse(request.responseText);
    if(response.success){
    const data = `i love ${response.email} ,${response.name}.`
    }
    else{
    alert("error")
    }

    }
    const data = new FormData();
    data.append('name',name);
    data.append('email',email);
    request.send(data);

    }
