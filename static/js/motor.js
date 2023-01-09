const toggleSwitch = document.querySelector(".toggleSwitch");

toggleSwitch.onclick = () => {
  toggleSwitch.classList.toggle("active");
  fetch("/led/" + (toggleSwitch.classList.contains("active") ? "on" : "off"))
    .then((response) => response.text())
    .then((data) => {
      console.log(data);
      let result = document.querySelector("#result");
      if (data == "on") {
        result.innerHTML = "<h1>LED is " + (toggleSwitch.classList.contains("active") ? "running" : "stopping") + "</h1>";
      } else {
        result.innerHTML = "<h1>LED is off</h1>";
      }
    });
};
