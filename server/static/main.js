let btn = document.getElementById("register_form_submit");
btn.addEventListener('click', () => {
    let form = document.getElementById("register_form");
    let formData = new FormData(form);
    let params = new URLSearchParams(formData).toString();
   params = "register?" + params;
   console.log(params)

    $.post(
        params,
        {},
        function(data) {
          alert("Response: " + data);
        }
    );
});
