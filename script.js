const chat_btn = document.querySelector(".chat-btn");
const close_chat = document.querySelector(".close-chat");
const chatbot_card = document.querySelector(".chatbot-card");
const user_input = document.querySelector(".search");
const query_form = document.querySelector(".query-form");
const card_content = document.querySelector(".card-content");
const btns = document.querySelectorAll(".btns button");
const loading = document.querySelector(".loading");
const send_query = document.querySelector(".send-query");

chat_btn.addEventListener("click", ()=>{
    chat_btn.style.display = "none";
    chatbot_card.style.display = "block";
});

close_chat.addEventListener("click", ()=>{
    chatbot_card.style.display = "none"; 
    chat_btn.style.display = "block";
});

query_form.addEventListener("submit", async (event)=>{
    event.preventDefault();
    const input_val = user_input.value;
    user_input.value = "";
    user_input.style.backgroundColor = "rgba(0,0,0,0.1)";
    user_input.disabled = true;
    send_query.disabled = true;
    btns.forEach(btn=>{
        btn.disabled = true;
    })
    let div = document.createElement("div");
    let p = document.createElement("p");
    div.classList.add("user-chat");
    p.textContent = input_val;
    div.appendChild(p);
    card_content.appendChild(div);
    await don(input_val);
    user_input.disabled = false;
    user_input.style.backgroundColor = "white";
    send_query.disabled = false;
    btns.forEach(btn=>{
        btn.disabled = false;
    })
    
});

btns.forEach(button =>{
    button.addEventListener("click", (event)=>{
        // user_input.value = "";
        user_input.style.backgroundColor = "rgba(0,0,0,0.1)";
        user_input.disabled = true;
        send_query.disabled = true;
        button.disabled = true;
        let div = document.createElement("div");
        let p = document.createElement("p");
        div.classList.add("user-chat");
        p.textContent = event.target.textContent;
        div.appendChild(p);
        card_content.appendChild(div);
        don(event.target.textContent);
        user_input.disabled = false;
        user_input.style.backgroundColor = "white";
        send_query.disabled = false;
        button.disabled = false;
    })
})

async function don(input){
    const formData = new FormData();

    card_content.appendChild(loading);
    loading.style.display = "flex";
    loading.scrollIntoView({behavior: "smooth"});

    let my_div = document.createElement("div");
    let my_p = document.createElement("p");
    my_div.classList.add("bot-chat");
    formData.append("query", input);
    const res = await fetch("http://127.0.0.1:8000/chatbot", {
        method: "POST",
        body: formData
    });
    const res_data = await res.json();
    
    my_p.textContent = res_data.response;
    my_div.appendChild(my_p);
    loading.style.display = "none";
    card_content.appendChild(my_div);

    if(res_data.link){
        let new_div = document.createElement("div");
        let a = document.createElement("a");
        new_div.classList.add("bot-link");
        a.href = res_data.link;
        a.textContent = res_data.intent;
        new_div.appendChild(a);
        card_content.appendChild(new_div);
        new_div.scrollIntoView({behavior: "smooth"});

    } else{
        my_div.scrollIntoView({behavior: "smooth"});

    }
}