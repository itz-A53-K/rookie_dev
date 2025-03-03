data = [
    {
        "img":"urology.png",
        "txt":"Urology",
    },
    {
        "img":"neurology.png",
        "txt":"Neurology",
    },
    {
        "img":"orthopedic.png",
        "txt":"Orthopedic",
    },
    {
        "img":"cardiologist.png",
        "txt":"Cardiologist",
    },
    {
        "img":"dentist.png",
        "txt":"Dentist",
    },

]

html=""
data.forEach((item)=>{
    html +=` <div class="specialty-box">
               <div>
                    <img src="/media/img/${item.img}" alt="${item.txt}">
                    <h3>${item.txt}</h3>
                   
                </div></div>`
})

document.getElementById("specialties_container").innerHTML = html;

//chat-bot
function openChat() {
    document.getElementById("chatPopup").style.display = "flex";
}
function closeChat() {
    document.getElementById("chatPopup").style.display = "none";
    $("#chatBody").html("")
}


$("#chat").submit(function(e) {
    e.preventDefault()
    let form = $(e.target)
    let data = form.serialize()
    msg = $("#chat .msg").val()

    if (msg != ""){
        $("#chatBody").append(`<p>
        <strong>You:</strong> ${msg}
        </p>`)
        form[0].reset()
        //disable form
        $("#chat").prop("disabled", true)
        
        $.ajax({
            url: "/chat/",
            type: "POST",
            data: data,
            success: function(resp) {
                console.log(resp);
                if (resp.status == 200) {
                    $("#chatBody").append(`<p>
                        <strong>Bot:</strong> ${resp.msg.response}
                        </p>`)
                        $("#chat").prop("disabled", false)
                }
            }
        });
    }
});