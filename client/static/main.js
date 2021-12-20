let register_btn = document.getElementById("register_form_submit");
register_btn.addEventListener('click', () => {
    let form = document.getElementById("register_form");
    let formData = new FormData(form);
    let params = new URLSearchParams(formData).toString();

   $.ajax({
    url: "https://tp-leads-app.herokuapp.com/register?" + params,
    type: 'POST',
    crossDomain: true,
    success: function(response) {
      console.log(response);
    }
 });
});

let edit_btn = document.getElementById("edit_form_submit");
edit_btn.addEventListener('click', () => {
    let form = document.getElementById("edit_form");
    let formData = new FormData(form);
    let params = new URLSearchParams(formData).toString();


   $.ajax({
    url: "https://tp-leads-app.herokuapp.com/register?" + params,
    type: 'PUT',
    success: function(response) {
      console.log(response);
    }
    });
});
