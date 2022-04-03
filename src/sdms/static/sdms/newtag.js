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
      var auxlabel = document.createElement("label");
      auxlabel.innerText = data.label;
      auxlabel.setAttribute('for', id_for_label);
      auxlabel.setAttribute('class', 'tag newly-added');
      auxlabel.style.color = data.text_color;
      auxlabel.style.backgroundColor = data.fill_color;
      auxlabel.style.borderColor = data.border_color;
      parent.appendChild(auxlabel);

      parent = document.getElementById("doctags");
      var input = document.createElement("input");
      input.setAttribute('class', 'cbtag newly-added');
      input.setAttribute('id', id_for_label);
      input.setAttribute('name', 'tags');
      input.setAttribute('type', 'checkbox');
      input.setAttribute('value', data.tag_id);
      input.setAttribute('checked', '');
      parent.appendChild(input);
      var label = document.createElement("label");
      label.innerText = data.label;
      label.setAttribute('for', id_for_label);
      label.setAttribute('class', 'tag newly-added');
      label.style.color = data.text_color;
      label.style.backgroundColor = data.fill_color;
      label.style.borderColor = data.border_color;
      parent.appendChild(label);

      /* avoid repeating the animation when the tag is hidden and shown later */
      setTimeout(() => {
        auxlabel.classList.remove("newly-added");
        label.classList.remove("newly-added");
      }, 1200);


    };
    request.open("POST", form.action);
    request.send(new FormData(form));
    form.reset();
    /* restyle_newtag is defined directly in a <script> tag, because it uses template values */
    restyle_newtag();
    return false;
  });

})();
