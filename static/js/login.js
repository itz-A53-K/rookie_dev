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
                msg = 'Login successful!';
                window.location.href = response.redirectLink;
            }
            else{
                msg = 'Login failed. Please try again.';
            }
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
            }
            else{
                msg = 'Registration failed. Please try again.';
            }
        },
    })               
})





function toggleForms() {
    document.getElementById("loginForm").classList.toggle("hidden");
    document.getElementById("signupForm").classList.toggle("hidden");
}

// Check URL for "doct" or "manager" and hide sign-up form
