var sample = [
  "### Instructions",
  "Enter text in the area on the left. For more info, click the ? (help) icon in the menu."
];

var simplemde = new SimpleMDE({element: document.getElementById("smde"), toolbar: ["bold", "italic", "heading", "|", "quote", "unordered-list", "ordered-list", "|", "link", "|", "guide"]});

$(document).ready(function() {
  writeSample();
  simplemde.codemirror.on("change", function(){
      var renderedHTML = simplemde.options.previewRender(simplemde.value());
      $("#write_here").html(renderedHTML);
      $("#write_here").css("height", $(".row").height() + "px");
  });
});

function writeSample() {
  var s = getSample();
  simplemde.value(s);
  var renderedHTML = simplemde.options.previewRender(simplemde.value());
  $("#write_here").html(renderedHTML);
  $("#write_here").css("height", $(".row").height() + "px");
}

function getSample() {
  var s = "";
  $.each(sample, function(index, value) {
      s += value + "\n\r";
  });
  return s;
}

let post_content = document.getElementById("smde")
let post_button = document.getElementById("post_button")
let message_div = document.getElementById("message_div")
let message_text = document.getElementById("message_text")
let svg_close_button = document.getElementById("svg_close_button")

post_button.addEventListener("click", async function () {
  
  message_div.style.display = 'none'

  try {
    const response = await fetch("/save_post", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({content: simplemde.value()})
    })

    let json = await response.json()
    console.log(json)

    if (json.message === "Post saved") {
      message_div.style.display = 'flex'
      message_text.innerText = "Post saved"
      message_div.style.backgroundColor = "green"
    }

    else if (json.message === "Post not saved") {
      message_div.style.display = 'flex'
      message_text.innerText = "Post not saved"
      message_div.style.backgroundColor = "red"
    }

    else if (json.message === "Error") {
      message_div.style.display = 'flex'
      message_text.innerText = "Server error! try again later"
      message_div.style.backgroundColor = "red"
    }
  } 
  
  catch( e ) {
    
    console.error("failed to post")
    message_div.style.display = 'flex'
    message_text.innerText = "Server error! try again later"
    message_div.style.backgroundColor = "red"
  }
})


svg_close_button.addEventListener("click", function () {
  message_div.style.display = 'none'
})