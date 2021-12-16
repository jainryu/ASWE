let register_btn = document.getElementById("register_form_submit");
register_btn.addEventListener('click', () => {
    let form = document.getElementById("register_form");
    let formData = new FormData(form);
    let params = new URLSearchParams(formData).toString();
   params = "register?" + params;

   $.ajax({
    url: params,
    type: 'POST',
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
   params = "register?" + params;

   $.ajax({
    url: params,
    type: 'PUT',
    success: function(response) {
      console.log(response);
    }
    });
});
