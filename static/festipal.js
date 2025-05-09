function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    if (!userInput.trim()) return;
    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<div class="user-message">${userInput}</div>`;
    fetch("/ask", {
      method: "POST",
      body: new URLSearchParams("userINPUT=" + userInput),
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        chatBox.innerHTML += `<div class="ai-message">${data.response}</div>`;
        document.getElementById("user-input").value = "";
        chatBox.scrollTop = chatBox.scrollHeight;
      });
  }