document.addEventListener('DOMContentLoaded', () => {


    document.querySelector('#student').onsubmit = () => {

    var s_a_num = document.querySelector('#s_a_num').value;
    var s_f_name = document.querySelector('#s_f_name').value;
    var S_l_name = document.querySelector('#S_l_name').value;
    var s_grade = document.querySelector('#s_grade').value;
    var p_name = document.querySelector('#p_name').value;
    var p_phone = document.querySelector('#p_phone').value;
    var p_email = document.querySelector('#p_email').value;

    if(s_a_num == "" || s_f_name == "") {
    document.querySelector('#demo').innerHTML = "am blank";
    return false;

    }
     else {


    const request = new XMLHttpRequest();
    request.open('POST','/add_student');
    request.onload = () =>{
    const response = JSON.parse(request.responseText);

    if(response.success){
    const data = `${response.msg}`
    const datav = `${response.types}`

    //using custom CSS
    // .ajs-message.ajs-custom { color: #31708f;  background-color: #d9edf7;  border-color: #31708f; }
    alertify.set('notifier','position', 'top-right');
    alertify.notify(data, datav, 2, function(){console.log('dismissed');}).dismissOthers();

    document.querySelector('#s_a_num').value = "";
    document.querySelector('#s_f_name').value = "";
    document.querySelector('#S_l_name').value = "";
    document.querySelector('#s_grade').value = "";
    document.querySelector('#p_name').value = "";
    document.querySelector('#p_phone').value = "";
    document.querySelector('#p_email').value = "";

    }
    else{
        msg = "there was a problem"
        //using custom CSS
        // .ajs-message.ajs-custom { color: #31708f;  background-color: #d9edf7;  border-color: #31708f; }
        alertify.set('notifier','position', 'top-right');
        alertify.notify(msg, error, 2, function(){console.log('dismissed');}).dismissOthers();

    }
    }
    const data = new FormData();
    data.append('s_a_num',s_a_num);
    data.append('s_f_name',s_f_name);
    data.append('S_l_name',S_l_name);
    data.append('s_grade',s_grade);
    data.append('p_name',p_name);
    data.append('p_phone',p_phone);
    data.append('p_email',p_email);

    request.send(data);

    return false;

    }
    return false;

    }



document.querySelector('#delete_student').onclick = () => {
swal({
    title: "Are you sure you want to delete this STUDENT?",
    text: "Once deleted, you will not be able to recover this STUDENT!",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  })
  .then((willDelete) => {
    if (willDelete) {
      swal("The STUDENT has been deleted successfully!", {
        icon: "success",
      });
    } else {
      swal("The STUDENT is not deleted!");
    }
});
}






});