
const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgeruuid = get(".msger-uuid");
const msgerChat = get(".msger-chat");

async function postData(uuid,query) {
  console.log("Posting data...");
  var data = new FormData();
  data.append('uuid', uuid);
  data.append('query', query);

      const response = await axios.post('http://127.0.0.1:8000/api/get_responce', data, {
          timeout: 30000,
      });
      console.log('Response:', response.data);
  // alert(response.data.response)
  appendMessage(response.data.name,response.data.profile_url,'left',response.data.response)
}

msgerForm.addEventListener("submit", event => {
  event.preventDefault();

  const msgText = msgerInput.value;
  const msguuid = msgeruuid.value;
  if (!msgText) return;
  appendMessage("User", "https://www.clipartmax.com/png/middle/47-470043_icons8-flat-businessman-person-icon-png.png", "right", msgText);
  
  console.log(msgText,msguuid)
  postData(msguuid,msgText)
  msgerInput.value = "";
});

function appendMessage(name, img, side, text) {
  //   Simple solution for small apps
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}



// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

