var forms = document.forms;

for (var i = 0; i < forms.length; i++) { 
    var form = forms[i];
    form.addEventListener('submit', function () {
        var allInputs = form.getElementsByClassName('form-control');
    
        for (var i = 0; i < allInputs.length; i++) {
            var input = allInputs[i];
    
            if (input.name && !input.value) {
                input.name = '';
            }
        }
    });
}