const chat_btn = document.querySelector(".chat-btn");
const close_chat = document.querySelector(".close-chat");
const chatbot_card = document.querySelector(".chatbot-card");
const user_input = document.querySelector(".search");
const query_form = document.querySelector(".query-form");
const card_content = document.querySelector(".card-content");

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
    let div = document.createElement("div");
    let p = document.createElement("p");
    div.classList.add("user-chat");
    p.textContent = input_val;
    div.appendChild(p);
    card_content.appendChild(div);
    const formData = new FormData();
    formData.append("query", input_val);
    const res = await fetch("http://127.0.0.1:8000/chatbot", {
        method: "POST",
        body: formData
    });
    const res_data = await res.json();

    if(res_data.link){
        let my_div = document.createElement("div");
        let p = document.createElement("p");
        my_div.classList.add("bot-chat");
        p.textContent = res_data.response;
        my_div.appendChild(p);
        card_content.appendChild(my_div);

        let new_div = document.createElement("div");
        let a = document.createElement("a");
        new_div.classList.add("bot-link");
        a.href = res_data.link;
        a.textContent = res_data.intent;
        new_div.appendChild(a);
        card_content.appendChild(new_div);
        console.log(res_data);

    }else{
        let my_div = document.createElement("div");
        let p = document.createElement("p");
        my_div.classList.add("bot-chat");
        p.textContent = res_data.response;
        my_div.appendChild(p);
        card_content.appendChild(my_div);
        console.log("dsdfd");
    }

})