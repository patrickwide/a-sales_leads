document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#create_assessment').onsubmit = () => {

    var new_assessment = document.querySelector('#new_assessment').value;

    if(new_assessment == "") {
    document.querySelector('#demo').innerHTML = "am blank";

    return false;
    } else {

    const request = new XMLHttpRequest();
    request.open('POST','/new_assessment');
    request.onload = () =>{
    const response = JSON.parse(request.responseText);
    if(response.success){

    const data = `${response.msg}`
    const datav = `${response.types}`

    //using custom CSS
    // .ajs-message.ajs-custom { color: #31708f;  background-color: #d9edf7;  border-color: #31708f; }
    alertify.set('notifier','position', 'top-right');
    alertify.notify(data, datav, 2, function(){console.log('dismissed');}).dismissOthers();

    document.querySelector('#new_assessment').value = "";
    var dit = document.querySelector('#exampleModal');
    }
    else{
    const msg = "there was a problem"
    const datav = "error"

    //using custom CSS
    // .ajs-message.ajs-custom { color: #31708f;  background-color: #d9edf7;  border-color: #31708f; }
    alertify.set('notifier','position', 'top-right');
    alertify.notify(msg, datav, 2, function(){console.log('dismissed');}).dismissOthers();

    }
    }
    const data = new FormData();
    data.append('new_assessment',new_assessment);

    request.send(data);
    return false;

    return false;

    }

    }
});