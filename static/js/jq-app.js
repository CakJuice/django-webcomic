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
});

function submitFormAjax($form) {
  /* Submit form via ajax.
   * param $form: DOM of form element.
  */
  var urlTarget = $form.getAttribute('action');
  if (!urlTarget) {
    urlTarget = window.location.href;
  }

//  var token = $form.children[0].value;
//  ajaxPostData(urlTarget, token, $form);
  ajaxPostData(urlTarget, $form);
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

function ajaxPostData(url, $form) {
  // Handle ajax form post data
  removeAlertForm($form);
  var xhr = getXHR();
  var formData = new FormData($form);
  $.ajax({
    method: 'POST',
    url: url,
    contentType: false,
    processData: false,
    xhr: function() {
      var jqXHR = null;
      if (window.ActiveXObject) {
        jqXHR = new window.ActiveXObject('Microsoft.XMLHTTP');
      } else {
        jqXHR = new window.XMLHttpRequest();
      }

      return jqXHR;
    },
    dataType: 'json',
    data: formData,
  }).done(function(response) {
    if (response.hasOwnProperty('success')) {
      // redirect when success
      window.location.href = response.redirect;
      return;
    }

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
  }).fail(function(response) {
    console.log("Ajax POST failed!");
  });
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
