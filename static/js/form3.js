document.addEventListener('DOMContentLoaded', () => {


    document.querySelector('#add-class-first').onsubmit = () => {

    var grade = document.querySelector('#grade').value;
    var grade_name = document.querySelector('#grade_name').value;

    if(grade == "" || grade_name == "") {
    document.querySelector('#demo').innerHTML = "am blank";

    return false;
    } else {


    const request = new XMLHttpRequest();
    request.open('POST','/add_class_first');
    request.onload = () =>{
    const response = JSON.parse(request.responseText);
    if(response.success){
    const data = `${response.msg}`
    const datav = `${response.types}`

    //using custom CSS
    // .ajs-message.ajs-custom { color: #31708f;  background-color: #d9edf7;  border-color: #31708f; }
    alertify.set('notifier','position', 'top-right');
    alertify.notify(data, datav, 2, function(){console.log('dismissed');}).dismissOthers();

    document.querySelector('#grade_name').value = "";

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
    data.append('grade',grade);
    data.append('grade_name',grade_name);

    request.send(data);
    return false;
    }
    return false;

    }
document.querySelector('#delete_class').onclick = () => {
swal({
    title: "Are you sure you want to delete this CLASS?",
    text: "Once deleted, you will not be able to recover this CLASS!",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  })
  .then((willDelete) => {
    if (willDelete) {
      swal("The CLASS has been deleted successfully!", {
        icon: "success",
      });
    } else {
      swal("The CLASS is not deleted!");
    }
});
}



});