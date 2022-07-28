function set_today() {
  var today = new Date().toISOString().slice(0, 16);
  document.getElementsByName("start_time")[0].min = today;
}

function calcMarks() {
  var marks = 0;
  for (let i = 1; i < q_no; i++) {
    let node = document.getElementById("marks" + i);
    let val = parseInt(node.value);
    if (val)
      marks += val;
  }
  document.getElementById("total_marks").value = marks;
}

function send_form(form, i) {
  const req = new XMLHttpRequest();
  const fd = new FormData(form);
  req.open("POST", "{{url_for('add_question')}}", false);
  fd.append("q_no", i)
  req.send(fd);
}

var q_no = 1;
function addQuestion() {
  const defaultQ = document.getElementById("defaultQ");
  const newQ = defaultQ.cloneNode(true);
  newQ.classList.remove("d-none");
  newQ.id = q_no;
  newQ.firstElementChild.firstElementChild.textContent += q_no;

  let tags = newQ.getElementsByTagName("label");
  for (let label of tags) {
    label.setAttribute("for", label.getAttribute("for") + q_no);
  }

  tags = newQ.getElementsByTagName("textarea");
  for (let textarea of tags) {
    textarea.id = textarea.id + q_no;
    textarea.name = textarea.id;
    textarea.setAttribute("required", "");
  }

  tags = newQ.getElementsByTagName("input");
  for (let input of tags) {
    input.id = input.id + q_no;
    input.name = input.id;
    input.setAttribute("required", "");
  }
  select = newQ.getElementsByTagName("select")[0];
  select.id += q_no;
  select.name = select.id;
  select.setAttribute("required", "");

  q_no++;
  document.getElementById("questions").appendChild(newQ);
}

function removeQuestion() {
  if (q_no == 2) return;
  q_no--;
  document.getElementById(q_no).remove();
}

window.onload = function () {
  addQuestion();
};