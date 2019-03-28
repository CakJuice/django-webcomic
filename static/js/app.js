var formChilds = [];

document.addEventListener('DOMContentLoaded', function() {
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

  // Handle form submit with ajax
  var forms = document.getElementsByTagName('form');
  for (var i=0;i<forms.length;i++) {
    var form = forms[i];
    var urlTarget = form.getAttribute('action');
    if (!urlTarget) {
      urlTarget = window.location.href;
    }

    form.addEventListener('submit', function(e) {
      e.preventDefault();
      formChilds = [];
      var token = this.children[0].value;
      ajaxPostData(urlTarget, token, this);
    });
  }
});

function getXHR() {
  // get XMLHttpRequest of browser
  if (window.XMLHttpRequest) return new window.XMLHttpRequest();
  return window.ActiveXObject('Microsoft.XMLHTTP');
}

function clearFieldStatus(field) {
  // clear message / status of field
  if (field.classList.contains('is-valid')) {
    field.classList.remove('is-valid');
  }

  if (field.classList.contains('is-invalid')) {
    field.classList.remove('is-invalid');
  }

  if (field.classList.contains('invalid-feedback')) {
    field.parentNode.removeChild(field);
  }
}

function getChildInputElement(parent) {
  // get element ['input', 'textarea', 'select'] inside of form
  var searchTags = ['input', 'textarea', 'select'];
  var childs = parent.children;
  for (var i=0;i<childs.length;i++) {
    var child = childs[i];
    clearFieldStatus(child);

    if (searchTags.indexOf(child.tagName.toLowerCase()) >= 0) {
      formChilds.push(child);
      continue;
    }

    if (child.children.length > 0) {
      getChildInputElement(child);
    }
  }
}

function ajaxPostData(url, token, form) {
  // Handle ajax form post data
  var xhr = getXHR();
  var formData = new FormData(form);
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var response = JSON.parse(this.response);
      if (response.hasOwnProperty('pk')) {
        // success
        console.log('form submit success');
        window.location.href = response.redirect;
      } else {
        // has form errors
        getChildInputElement(form);

        for (var i=0;i<formChilds.length;i++) {
          var field = formChilds[i];
          var name = field.getAttribute('name')
          if (name in response) {
            field.classList.add('is-invalid');

            var msg = document.createElement('div')
            msg.classList.add('invalid-feedback')
            msg.innerHTML += response[name];
            field.parentNode.appendChild(msg);
          } else {
            field.classList.add('is-valid');
          }
        }

        formChilds = []
      }
    }
  }

  xhr.open("POST", url, true);
  xhr.setRequestHeader('X-CSRFToken', token);
  xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  xhr.send(formData);
}

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