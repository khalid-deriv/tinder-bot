function readURL(input) {
  if (input.files && input.files[0]) {

    var reader = new FileReader();

    reader.onload = function(e) {
      $('.image-upload-wrap').hide();

      $('.file-upload-image').attr('src', e.target.result);
      $('.file-upload-content').show();

      $('.image-title').html(input.files[0].name);

      $(".rate-content").show();
    };

    reader.readAsDataURL(input.files[0]);

  } else {
    removeUpload();
  }
}
  
function removeUpload() {
  $('.file-upload-input').replaceWith($('.file-upload-input').clone());
  $('.file-upload-content').hide();
  $(".rate-content").hide()
  $('.image-upload-wrap').show();
}

$('.image-upload-wrap').bind('dragover', function () {
  $('.image-upload-wrap').addClass('image-dropping');
});

$('.image-upload-wrap').bind('dragleave', function () {
  $('.image-upload-wrap').removeClass('image-dropping');
});

function rateImage() {

  $(".image-title-wrap").hide();
  $(".rate-content").hide()
  $(".loading").show();

  var file = $(".file-upload-input")[0].files[0];
  
  const fd = new FormData();
  fd.append('image', file);
  

  fetch(`${window.origin}/rate`, {
    method: "POST",
    body: fd,
    cache: "no-cache",
  })
  .then(function(response) {
    if (response.status !== 200) {
      console.log(`Looks like there was a problem. Status code: ${response.status}`);
      $(".rate-content").hide()
      $(".loading").hide();
      $(".error").show();
      $(".again").show();
      return;
    }
    response.json().then(function(data) {
      var rating = parseFloat(data.rating).toFixed(1)
      $(".loading").hide();
      $(".rating h3").html(rating + " / 10")
      $(".rating").show();
      $(".again").show();
    });
  })
  .catch(function(error) {
    console.log("Fetch error: " + error);
    $(".rate-content").hide()
    $(".loading").hide();
    $(".error").show();
    $(".again").show();
  });

}

function again() {
  $(".error").hide();
  $(".again").hide();
  $(".rating").hide();
  $(".image-title-wrap").show(); // show remove button before hiding its parent
  removeUpload();
}
  