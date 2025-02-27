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
                    <img src="/img/${item.img}" alt="${item.txt}">
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
}