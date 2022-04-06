const form = document.forms[0];

form.addEventListener("submit", function(event) {
  event.preventDefault();

  buildJSON(this);
});

function buildJSON(form) {
  const data = new FormData(form);
  const entries = data.entries();
  const obj = Object.fromEntries(entries);
  const json = JSON.stringify(obj);
  const dataURL = `data:application/json,${json}`;

  const anchor = document.querySelector("a");
  anchor.setAttribute("download", "Your_data.txt");
  anchor.setAttribute("href", dataURL);
}