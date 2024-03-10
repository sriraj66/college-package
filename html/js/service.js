localStorage.setItem("message", "false");

    function getToggle() {
      return JSON.parse(localStorage.getItem("message"));
    }

    function toggleMessage() {
      var toggleValue = getToggle();
      var messageElement = document.getElementById('msger');

      if (toggleValue) {
        messageElement.classList.add("--hide");
      } else {
        messageElement.classList.remove("--hide");
      }

      localStorage.setItem("message", !toggleValue);
    }
