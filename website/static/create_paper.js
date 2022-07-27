function set_today() {
  var today = new Date().toISOString().slice(0, 16);
  document.getElementsByName("start_time")[0].min = today;
}

function calc_marks() {
  var marks = 0;
  for (let i = 1; i < q_no; i++) {
    let form = document.getElementById("f" + i);
    let m = parseInt(form['marks'].value);
    console.log(m === m);
    if (m === m)
      marks = marks + m;
  }
  document.getElementById("total_marks").value = marks;
}

function isEmpty(element) {
  if (element == null || element == "") return true;
  return false;
}

function send_form(form, i) {
  const req = new XMLHttpRequest();
  const fd = new FormData(form);
  req.open("POST", "{{url_for('add_question')}}", false);
  fd.append("q_no", i)
  req.send(fd);
}

function validate() {
  if (q_no == 1) {
    alert('Add at least one question');
  }
  else {
    let flag = 0;
    for (let i = 1; i < q_no; i++) {
      let form = document.getElementById("f" + i);
      var q = form["q"].value;
      var A = form["A"].value;
      var B = form["B"].value;
      var C = form["C"].value;
      var D = form["D"].value;
      var ca = form["c_ans"].value;
      var marks = form["marks"].value;
      // var err = form["error"].innerHTML;
      var err_fieldRequired = document.createElement("p");
      err_fieldRequired.innerHTML = "Fill all required fields";
      err_fieldRequired.setAttribute('name', "empty error");
      err_fieldRequired.style.color = "red";

      var err_cAns = document.createElement("p");
      err_cAns.innerHTML = "correct ans should be from A,B,C,D";
      err_cAns.setAttribute('name', "correct ans error");
      err_cAns.style.color = "red";

      var err_mark = document.createElement("p");
      err_mark.innerHTML = "marks should be +ve number";
      err_mark.setAttribute('name', "marks error");
      err_mark.style.color = "red";

      if (!isEmpty(q) && !isEmpty(A) && !isEmpty(B) && !isEmpty(C) && !isEmpty(D)) {
        if ((ca == 'A' || ca == 'B' || ca == 'C' || ca == 'D') && marks > 0) {
          send_form(form, i);

        }
        else {
          if (marks <= 0 && form.children["marks error"] == null) form.appendChild(err_mark);
          else if (form.children["correct ans error"] == null) form.appendChild(err_cAns);
          flag = 1;
        }
      }
      else {
        flag = 1;
        if (form.children["empty error"] == null) form.appendChild(err_fieldRequired);
      }
    }

    if (flag == 0) {
      document.getElementById('0')['total_marks'].removeAttribute("disabled");
      console.log(document.getElementById('0'));
      document.getElementById('0').submit();
    }
  }


}

var q_no = 1;
function addQ() {
  const f = document.createElement("form");
  f.id = "f" + q_no;
  f.name = "form" + q_no;

  const q = document.createElement("textarea");
  q.id = "q" + q_no;
  q.name = "q";
  q.placeholder = "Type your question here";
  q.rows = "5";
  q.cols = "40";

  const lq = document.createElement("label");
  lq.for = "q" + q_no;
  lq.innerHTML = "Q" + q_no + ". ";

  const a = document.createElement("textarea")
  a.id = "A" + q_no;
  a.name = "A";
  a.placeholder = "Option 1";
  a.rows = "2";
  a.cols = "20";

  const la = document.createElement("label");
  la.htmlFor = "A" + q_no;
  la.innerHTML = "A. "

  const b = document.createElement("textarea")
  b.id = "B" + q_no;
  b.name = "B";
  b.placeholder = "Option 2";
  b.rows = "2";
  b.cols = "20";

  const lb = document.createElement("label");
  lb.htmlFor = "B" + q_no;
  lb.innerHTML = "B. "

  const c = document.createElement("textarea")
  c.id = "C" + q_no;
  c.name = "C";
  c.placeholder = "Option 3";
  c.rows = "2";
  c.cols = "20";

  const lc = document.createElement("label");
  lc.htmlFor = "C" + q_no;
  lc.innerHTML = "C. "

  const d = document.createElement("textarea")
  d.id = "D" + q_no;
  d.name = "D";
  d.placeholder = "Option 4";
  d.rows = "2";
  d.cols = "20";

  const ld = document.createElement("label");
  ld.htmlFor = "D" + q_no;
  ld.innerHTML = "D. "

  const correct_ans = document.createElement("input")
  correct_ans.type = "text";
  correct_ans.id = "correct_ans" + q_no;
  correct_ans.name = "c_ans";
  correct_ans.placeholder = "A,B,C,D";

  const lca = document.createElement("label");
  lca.htmlFor = "correct_ans" + q_no;
  lca.innerHTML = "Correct Ans. "

  const marks = document.createElement("input")
  marks.type = "number";
  marks.id = "marks" + q_no;
  marks.name = "marks";
  marks.placeholder = "marks";
  marks.defaultValue = 0;
  marks.onchange = calc_marks;

  const lm = document.createElement("label");
  lm.htmlFor = "marks" + q_no;
  lm.innerHTML = "Marks. ";

  const p = document.createElement("p");
  p.name = "p";


  // p.appendChild(err);

  q_no++;

  const br = document.createElement('br');

  f.appendChild(lq);
  f.appendChild(q);
  f.appendChild(br.cloneNode());

  f.appendChild(la);
  f.appendChild(a);
  f.appendChild(br.cloneNode());

  f.appendChild(lb);
  f.appendChild(b);
  f.appendChild(br.cloneNode());

  f.appendChild(lc);
  f.appendChild(c);
  f.appendChild(br.cloneNode());

  f.appendChild(ld);
  f.appendChild(d);
  f.appendChild(br.cloneNode());

  f.appendChild(lca);
  f.appendChild(correct_ans);
  f.appendChild(br.cloneNode());

  f.appendChild(lm);
  f.appendChild(marks);
  f.appendChild(br.cloneNode());

  f.appendChild(p.cloneNode());

  document.getElementById('questions').appendChild(f);

  var nodes = f.childNodes;
  for (var i = 0; i < nodes.length; i++) {
    nodes[i].setAttribute('class', 'form-control');
  }
}

function removeQ() {
  if (q_no == 1) return;
  q_no--;
  document.getElementById("f" + q_no).remove();
}