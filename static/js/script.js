var file = document.getElementById("output-image");

file.onchange = function () {
  if (file.files.length > 0) {
    document.getElementById('file-name').innerHTML = file.files[0].name;
  }
};

function preview_image(event) {
  var reader = new FileReader();
  reader.onload = function () {
    var output = document.getElementById('output-image')
    output.src = reader.result;
  }
  reader.readAsDataURL(event.target.files[0]);
}


