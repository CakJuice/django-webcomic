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

//  // Handle form submit with ajax
//  var forms = document.getElementsByTagName('form');
//  for (var i=0;i<forms.length;i++) {
//    var form = forms[i];
//    var urlTarget = form.getAttribute('action');
//    if (!urlTarget) {
//      urlTarget = window.location.href;
//    }
//
//    form.addEventListener('submit', function(e) {
//      e.preventDefault();
//      formChilds = [];
//      var token = this.children[0].value;
//      ajaxPostData(urlTarget, token, this);
//    });
//  }
});

function setFormAjax($form) {
  var urlTarget = $form.getAttribute('action');
  if (!urlTarget) {
    urlTarget = window.location.href;
  }

  var token = $form.children[0].value;
  ajaxPostData(urlTarget, token, $form);
}

function getXHR() {
  // get XMLHttpRequest of browser
  if (window.XMLHttpRequest) return new window.XMLHttpRequest();
  return window.ActiveXObject('Microsoft.XMLHTTP');
}

function clearFieldStatus($field) {
  // clear message / status of field
  if ($field.classList.contains('is-valid')) {
    $field.classList.remove('is-valid');
  }

  if ($field.classList.contains('is-invalid')) {
    $field.classList.remove('is-invalid');
  }

  if ($field.classList.contains('invalid-feedback')) {
    $field.parentNode.removeChild($field);
  }
}

function getChildInputElement($parent) {
  // get element ['input', 'textarea', 'select'] inside of form
  var searchTags = ['input', 'textarea', 'select'];
  var $childs = $parent.children;
  var $inputs = []
  for (var i=0;i<$childs.length;i++) {
    var $child = $childs[i];
    clearFieldStatus($child);

    if (searchTags.indexOf($child.tagName.toLowerCase()) >= 0) {
      $inputs.push($child);
      continue;
    }

    if ($child.children.length > 0) {
      $newInputs = getChildInputElement($child)
      $inputs = $inputs.concat($newInputs);
    }
  }

  return $inputs;
}

function ajaxPostData(url, token, $form) {
  // Handle ajax form post data
  removeAlertForm($form);
  var xhr = getXHR();
  var formData = new FormData($form);
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var response = JSON.parse(this.response);
      if (response.hasOwnProperty('success')) {
        // success
        window.location.href = response.redirect;
      } else {
        // has form errors
        var isAllErrors = false;
        if (response.hasOwnProperty('__all__')) {
          isAllErrors = true;
          var $alertDOM = getAlertFormDOM(response['__all__']);
          $form.insertBefore($alertDOM, $form.firstChild);
        }

        var $formChilds = getChildInputElement($form);

        for (var i=0;i<$formChilds.length;i++) {
          var $field = $formChilds[i];
          var name = $field.getAttribute('name');
          if (isAllErrors) {
            $field.classList.add('is-invalid');
          } else {
            if (name in response) {
              $field.classList.add('is-invalid');
              var $feedback = getFieldInvalidFeedback(response[name])
              $field.parentNode.insertBefore($feedback, $field.nextSibling);
            } else {
              $field.classList.add('is-valid');
            }
          }
        }
      }
    }
  }

  xhr.open("POST", url, true);
  xhr.setRequestHeader('X-CSRFToken', token);
  xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  xhr.send(formData);
}

function getFieldInvalidFeedback(message) {
  // To get invalid message of form field.
  // return message as HTML DOM.
  var $dom = document.createElement('div');
  $dom.setAttribute('class', 'invalid-feedback');
  $dom.innerHTML = message;
  return $dom;
}

function removeAlertForm($form) {
  // To remove previous alert of form, used before form submitted.
  var $alerts = document.getElementsByClassName('alert-danger');
  for (var i=0;i<$alerts.length;i++) {
    var $alert = $alerts[i];
    if ($alert == $form.children[0]) {
      $alert.remove();
    }
  }
}

function getAlertFormDOM(message) {
  // get alert of invalid form (global error message, not field message).
  // return alert message as HTML DOM.
  var $dom = document.createElement('div');
  $dom.setAttribute('class', 'alert alert-danger');
  $dom.setAttribute('role', 'alert');
  $dom.innerHTML = '<p class="mb-1">' + message + '</p>';
  return $dom;
}

function getChapterContainer() {
  // get chapter container, used for comic detail.
  // return string of element.
  return '<div class="col col-md-9 col-12" id="chapter-container"></div>';
}

function getNoChapterText() {
  // get no chapter text, when comic don't have a chapter.
  // return string of element.
  return '<h1>Sorry there are no chapters for this comic!</h1>';
}

function getChapter(chapter) {
  // get chapter list of comic.
  // return string of element.
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
  '</div>';
}