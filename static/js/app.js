document.addEventListener('DOMContentLoaded', function() {

  /*
  // Attach event change on input file
  var customFileInput = document.getElementsByClassName('custom-file-input');
  for (var i=0;i<customFileInput.length;i++) {
    cf = customFileInput[i];
    cf.addEventListener('change', function(e) {
      var elem = e.target;
      var file = elem.files[0];
      elem.nextElementSibling.innerHTML = file.name;
    });
  }
  */
});

function getChapterContainer() {
  return '<div class="col col-md-9 col-12" id="chapter-container"></div>';
}

function getNoChapterText() {
  return '<h1>Sorry there are no chapters for this comic!</h1>';
}

function getChapter(chapter) {
  var chapterThumbnail;
  if (!chapter.thumbnail || chapter.thumbnail == '') {
    chapterThumbnail = '<img src="' + DEFAULT_THUMBNAIL + '" class="img-fluid">';
  } else {
    chapterThumbnail = '<img src="' + chapter.thumbnail + '" class="img-fluid">';
  }

  return '<div class="row border-bottom py-1">' +
    '<div class="col col-2">' + chapterThumbnail + '</div>' +
    '<div class="col col-8 comic-list">' +
      '<h4>' +
        '<a href="' + chapter.url + '">' + chapter.title + '</a>' +
      '</h4>' +
      '<div class="comic-info">' +
        '<span class="comic-like"><i class="fas fa-heart"></i> ' + chapter.read + '</span>' +
      '</div>' +
    '</div>' +
    '<div class="col col-2 text-center">' +
      '<h4>#' + chapter.sequence + '</h4>' +
    '</div>' +
  '</div>'
}