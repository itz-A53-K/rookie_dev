let loginURL

window.onload = function() {
    loginURL = "/login/"
    let currentURL = window.location.href;
    if (currentURL.includes("doct")){
        $("#signpForm").hide();
        $("#loginForm a").hide();
        $("#loginForm>h2").text("Doctor Login");
        document.title = "Doctor Login";
        loginURL="/doct/login/"
    }
    if(currentURL.includes("manager")) {
        $("#signpForm").hide();
        $("#loginForm a").hide();
        $("#loginForm>h2").text("Manager Login");
        document.title = "Manager Login";
        loginURL = "/manager/login/"
    }
};
$("#form_login").submit((e) =>{
    e.preventDefault()
    let form = $(e.target)
    let data = form.serialize()

    $.ajax({
        url: loginURL,  
        type: "POST",
        data: data,
        success: function(response){
            if(response.status == 200){
                window.location.href = response.redirectLink;
                alert_show("success", 'Login successful!');
            }
            else{
                alert_show("error", response.error)
            }
            //reset form
            form[0].reset()
        },
    })               
})

$("#form_register").submit((e) =>{
    e.preventDefault()
    let form = $(e.target)
    let data = form.serialize()

    $.ajax({
        url: "/register/",  
        type: "POST",
        data: data,
        success: function(response){
            if(response.status == 200){
                msg = 'Registration successful! Please login.';
                $('#signupForm').hide()
                $('#loginForm').show();
                alert_show("success", msg);
            }
            else if(response.status == 409){
                msg = response?.msg;
                $('#signupForm').hide()
                $('#loginForm').show();
                alert_show("error", msg);
            }
            else{
                msg = 'Registration failed. Please try again.';
                alert_show("error", msg);
            }

            form[0].reset()
        },
    })               
})





function toggleForms() {
    document.getElementById("loginForm").classList.toggle("hidden");
    document.getElementById("signupForm").classList.toggle("hidden");
}

// Check URL for "doct" or "manager" and hide sign-up form
