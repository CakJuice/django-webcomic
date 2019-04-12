document.addEventListener('DOMContentLoaded', function() {
  document.addEventListener('click', function(e) {
    /* Event listener handler for document element.
     * This code will be executed when user clicked on all document area.
    */
    if (e.target.className == 'nav-link dropdown-toggle') {
      // Check whether element is 'nav-link dropdown toggle'.
      // Set nextElementSibling to toggling 'show' class name.
      var sibling = e.target.nextElementSibling;
      sibling.classList.toggle('show');
    } else {
      hideNavDropdown();
    }
  });

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

function hideNavDropdown() {
  // To hide all shown navbar dropdown.
  var navDropdowns = document.getElementsByClassName('nav-link dropdown-toggle');
  for (var i=0;i<navDropdowns.length;i++) {
    var dropdown = navDropdowns[i];
    var sibling = dropdown.nextElementSibling;
    if (sibling.classList.contains('show')) {
      sibling.classList.remove('show');
    }
  }
}

function submitFormAjax($form) {
  /* Submit form via ajax.
   * param $form: DOM of form element.
  */
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

function getChapterList(chapter) {
  // get chapter list of comic.
  // return string of element.
  var thumbnail;
  if (!chapter.thumbnail || chapter.thumbnail == '') {
    thumbnail = DEFAULT_THUMBNAIL;
  } else {
    thumbnail = chapter.thumbnail;
  }

  var chapterThumbnail = '<img src="' + thumbnail + '" class="img-fluid" loading="lazy" alt="' + chapter.title + '">';

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

function getNoComicText() {
  // get no comic text, for genre detail.
  // return string of element.
  return '<div class="col col-12"><h4>Sorry there are no comics for this time!</h4></div>';
}

function clickComicList($elem) {
  console.log($elem);
  window.location.href = $elem.getAttribute('data-href');
}

function getComicList(comic) {
  /* Get comic list for genre detail.
   * param comic: Object. Comic object to display as a list.
   * return String of element.
  */
  var thumbnail;
  if (!comic.thumbnail || comic.thumbnail == '') {
    thumbnail = DEFAULT_THUMBNAIL;
  } else {
    thumbnail = comic.thumbnail;
  }

  var comicThumbnail = '<img src="' + thumbnail + '" class="img-fluid" loading="lazy" alt="' + comic.title + '">';

  return '<div class="col col-lg-4 col-md-6 col-12" onclick="clickComicList(this);" data-href="' + comic.direct_url + '">' +
    '<div class="row my-2 mx-1 py-2 comic-list">' +
      '<div class="col col-4 pr-1">' + comicThumbnail + '</div>' +
      '<div class="col col-8 pl-1"><h5>' + comic.title + '</h5>' +
    '</div>'
  '</div>';
}

function getComicContainer() {
  /* Get comic list container.
   * return: DOM of comic list container.
  */
  return document.getElementById('comic-container');
}

function getPaginationContainer() {
  /* Get pagination container.
   * return: DOM of pagination container.
  */
  return document.getElementById('pagination-container');
}

function ajaxComicListData(url) {
  /* Get comic list data via ajax (XMLHttpRequest).
   * params url: String. URL of comic ajax.
  */
  var xhr = getXHR();
  var $container = getComicContainer();
  var $paginationContainer = getPaginationContainer();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var response = JSON.parse(this.response);
      $paginationContainer.innerHTML = '';
      $container.innerHTML = '';
      if (response.count > 0) {
        for (var i=0;i<response.results.length;i++) {
          var result = response.results[i];
          $container.innerHTML += getComicList(result);
        }

        if (response.next || response.previous) {
          var pagination = {
            count: response.count,
            next: response.next,
            previous: response.previous,
            start: response.start,
            current: response.current,
            end: response.end,
            num_pages: response.num_pages,
          }

          var paginationStr = getPagination(pagination, url);
          $paginationContainer.innerHTML = paginationStr;
        }
      } else {
        $container.innerHTML = getNoComicText();
      }
    }
  }

  xhr.open('GET', url, true);
  xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  xhr.send();
}

function getPaginationDisabled(pagination) {
  /* Get pagination disabled text, ex: "Page 1 Of 5".
   * param pagination: Object. Pagination data object.
   * return: String of element.
  */
  return '<li class="page-item disabled">' +
    '<span class="page-link">Page ' + pagination.current + ' Of ' + pagination.num_pages + '</span>'
  '</li>';
}

function clickPaginationItem($link) {
  /* Handle onclick of pagination item link. When item link clicked, it will trigger ajaxComicListData.
   * param dom: Object. DOM of item link.
  */
  ajaxComicListData($link.getAttribute('href'));
}

function getPaginationItem(url, text, active) {
  /* Get pagination item list.
   * param url: String. URL for pagination item.
   * param text: String. Text of pagination.
   * param active: Boolean. Set if pagination item is active or not.
   * return: String of element.
  */
  active = active || false;
  if (active) {
    return '<li class="page-item active">' +
      '<span class="page-link">' +
        text + '<span class="sr-only">(current)</span>' +
      '</span>' +
    '</li>';
  }

  return '<li class="page-item">' +
    '<a class="page-link" href="' + url + '" onclick="clickPaginationItem(this); return false;">' + text + '</a>' +
  '</li>';
}

function getPagination(pagination, url) {
  /* Get pagination for general purpose.
   * param pagination: Object. Pagination data object.
   * param url: String. URL for pagination link.
   * return: String of element.
  */
  var baseUrl = url.split(/[?#]/)[0];
  var pageDisabled = getPaginationDisabled(pagination);
  var pageFirst = pagination.previous ? getPaginationItem(baseUrl + '?page=1', '&laquo;') : '';
  var pageMain = ''
  for (var i=pagination.start;i<=pagination.end;i++) {
    pageMain += getPaginationItem(baseUrl + '?page=' + i, i, i == pagination.current);
  }
  var pageLast = pagination.next ? getPaginationItem(baseUrl + '?page=' + pagination.num_pages, '&raquo;') : '';

  return '<nav aria-label="Pagination">' +
    '<ul class="pagination justify-content-center">' +
      pageDisabled +
      pageFirst +
      pageMain +
      pageLast +
    '</ul>' +
  '</nav>';
}