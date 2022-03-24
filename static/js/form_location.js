document.addEventListener('DOMContentLoaded', () => {
document.querySelector('#done').style.display = "none";

document.querySelector('#submit').onclick = () => {
var insert = [];
$('.get_value').each(function() {
if ($(this).is(":checked")) {
insert.push($(this).val() );
}
});

insert = insert.toString() ;
var insert_string = 'checkboxvalue='+insert;

var wizard = document.querySelector('.wizard').value;
var location_1 = document.querySelector('#location_1').value;
var location_2 = document.querySelector('#location_2').value;
var location_3 = document.querySelector('#location_3').value;

var facebook = document.querySelector('#facebook').value;
var instagram = document.querySelector('#instagram').value;
var twitter = document.querySelector('#twitter').value;
var youtube = document.querySelector('#youtube').value;


const request = new XMLHttpRequest();
request.open('POST','/locations_dit');
request.onload = () =>{
const response = JSON.parse(request.responseText);
if(response.success){

document.querySelector('#submit').style.display = "none";
document.querySelector('#done').style.display = "block";


const dataA = `${response.msgA}`
const dataB = `${response.msgB}`
const dataC = `${response.msgC}`
const dataD= `${response.msgD}`

document.querySelector('#done').innerHTML = dataD;
swal( dataA, dataB, dataC);

}
else{
 alert("not success");

}
}

const data = new FormData();
data.append('wizard',wizard);
data.append('location_1',location_1);
data.append('location_2',location_2);
data.append('location_3',location_3);
data.append('facebook',facebook);
data.append('instagram',instagram);
data.append('twitter',twitter);
data.append('youtube',youtube);

data.append('insert',insert);

request.send(data);

}
});