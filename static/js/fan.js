const toggleSwitch = document.querySelector(".toggleSwitch");

toggleSwitch.onclick = () => {
  toggleSwitch.classList.toggle("active");
  fetch("/fan/" + (toggleSwitch.classList.contains("active") ? "on" : "off"))
    .then((response) => response.text())
    .then((data) => {
      console.log(data);
      let result = document.querySelector("#result");
      if (data == "on") {
        result.innerHTML = "<h2>fan is " + (toggleSwitch.classList.contains("active") ? "running" : "stopping") + "</h2>";
      } else {
        result.innerHTML = "<h2>fan is off</h2>";
      }
    });
};
