/**
 * register.js for valid register form and get response from google api.
 */
/**
 * register.js for valid register form.
 */
if (window.initCaptcha) {
    initCaptcha('id_register_form');
}
$("#id_register_form").submit(function(event){
    event.preventDefault();
    var form = this;
    if (!$(form).valid()) {
        return false;
    }
    if (showCaptchaWindow()) {
        return false;
    }
    showWaiting();
    form.submit();
}).validate({
    ignore: [],
    errorElement: "div",
    errorClass: "alert alert-danger",
    rules: {
        email: {required: true, email:true}
    },
    errorPlacement: function(error,element) {
        error.appendTo(element.parent());
    }
});
/**
 * valid set password form.
 */
$("#id_set_password_form").submit(function(event){
    event.preventDefault();
    var form = this;
    if (!$(form).valid()) {
        return false;
    }
    showWaiting();
    form.submit()
}).validate({
    ignore: [],
    errorElement: "div",
    errorClass: "alert alert-danger",
    rules: {
        password: {required: true, minlength:6, maxlength:16, password:true},
        repassword: {required: true, minlength: 6, maxlength:16, equalTo:"#id_password", password:true},
    },
    errorPlacement: function(error,element) {
        error.appendTo(element.parent());
    }
});
