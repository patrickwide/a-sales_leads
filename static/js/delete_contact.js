document.addEventListener('DOMContentLoaded', () => {

    var name = document.querySelector('#id').value;

    document.querySelector("#delete").onclick = () => {



    swal({
    title: "Are you sure you want to delete this CONTACT?",
    text: "Once deleted, you will not be able to recover this CONTACT!",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  })
  .then((willDelete) => {
    if (willDelete) {


    var name = document.querySelector('#id').value;
    var email = document.querySelector('#user').value;



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


      swal("Contact deleted successfully!", {
        icon: "success",
      });
    } else {
      swal("The TEACHER is not deleted!");
    }
});


    }

});
