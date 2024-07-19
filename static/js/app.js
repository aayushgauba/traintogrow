// Banner Bg
$(".banner__bgSlider").slick({
  slidesToShow: 1,
  slidesToScroll: 1,
  arrows: false,
  autoplay: true,
  asNavFor: ".banner__thumbnails",
});

// Banner Thumbnails
$(".banner__thumbnails").slick({
  slidesToShow: 5,
  slidesToScroll: 1,
  centerMode: true,
  asNavFor: ".banner__bgSlider",
  dots: false,
  arrows: true,
  focusOnSelect: true,
  responsive: [
    {
      breakpoint: 576,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
      },
    },
  ],
});
// Testimonials Slider
$(".testimonials__contentSlider").slick({
  slidesToShow: 1,
  slidesToScroll: 1,
  arrows: false,
  autoplay: true,
  asNavFor: ".testimonials__detailsSlider",
});
$(".testimonials__detailsSlider").slick({
  slidesToShow: 3,
  slidesToScroll: 1,
  centerMode: true,
  asNavFor: ".testimonials__contentSlider",
  dots: false,
  arrows: true,
  focusOnSelect: true,
});

$(document).ready(function () {
  // Initialize Fancybox
  if ($('[data-fancybox="gallery"]').length > 0) {
    $('[data-fancybox="gallery"]').fancybox({
      buttons: ["slideShow", "fullScreen", "thumbs", "close"],
    });
  }
});


// Select Date
$(function () {
  $('input[name="birthday"]').daterangepicker(
    {
      singleDatePicker: true,
      showDropdowns: true,
      minYear: 1901,
      maxYear: parseInt(moment().format("YYYY"), 10),
    },
    function (start, end, label) {
      var years = moment().diff(start, "years");
      alert("You are " + years + " years old!");
    }
  );
});
