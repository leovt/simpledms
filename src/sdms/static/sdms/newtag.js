/*jshint esversion: 6 */

(() => {
  var form = document.getElementById("newtagform");
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    var request = new XMLHttpRequest();
    request.onload = () => {
      var parent = document.getElementById("availabletags");
      var data = JSON.parse(request.responseText);
      var id_for_label = "cb" + data.tag_id;
      var label = document.createElement("label");
      label.innerText = data.label;
      label.setAttribute('for', id_for_label);
      label.setAttribute('class', 'tag newly-added');
      label.style.color = data.text_color;
      label.backgroundColor = data.fill_color;
      label.borderColor = data.border_color;
      parent.appendChild(label);
    };
    request.open("POST", form.action);
    request.send(new FormData(form));
    form.reset();
    return false;
  });

})();