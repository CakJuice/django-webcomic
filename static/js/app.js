const html = document.getElementsByTagName('html')[0];

html.addEventListener('click', function(e) {
  /* Event listener handler for html element.
  * This code will be executed when user clicked on all html area.
  */

  if (e.target.className === 'nav-link dropdown-toggle') {
    // Check whether element is 'nav-link dropdown toggle'.
    // Set nextElementSibling to toggling 'show' class name.
    const sibling = e.target.nextElementSibling;
    sibling.classList.toggle('show');
  } else {
    // hide all shown navbar dropdown
    hideNavDropdown();
  }
});

function hideNavDropdown() {
  /* To hide all shown navbar dropdown.
  */

  const navDropdowns = document.getElementsByClassName('nav-link dropdown-toggle');

  for (let i=0;i<navDropdowns.length;i++) {
    const dropdown = navDropdowns[i];
    const sibling = dropdown.nextElementSibling;
    if (sibling.classList.contains('show')) {
      sibling.classList.remove('show');
    }
  }
}

/*
function getGenreDropdown(name, url) {
  return '<a class="dropdown-item" href="' + url + '">' + name + '</a>';
}

function getPaginationDisabled(pagination) {
  return '<li class="page-item disabled">' +
    '<span class="page-link">Page ' + pagination.current + ' Of ' + pagination.num_pages + '</span>'
  '</li>';
}

function getPaginationPage(pagination, url, text) {
  if (!pagination.has_prev) {
    return '';
  }

  return '<li class="page-item">' +
    '<a class="page-link" href="' + url + '">' + text + '</a>' +
  '</li>';
}
*/

/*
function getPagination(pagination) {
  var pageDisabled = getPaginationDisabled(pagination);
  var pagePrev = getPaginationPage(pagination, '?page=1', '&laquo;');
  var pageMain = ''
  for (var i=pagination.start;i<=pagination.end;i++) {
    pageMain += '';
  }
  return '<nav aria-label="Pagination">' +
    '<ul class="pagination justify-content-center">' +
      pageDisabled +
      pagePrev +
      {% for page in pagination %}
        <li class="page-item{% if page == objects.number %} active{% endif %}">
          {% if page == objects.number %}
            <span class="page-link">
              {{ page }}
              <span class="sr-only">(current)</span>
            </span>
          {% else %}
            <a class="page-link" href="?page={{ page }}">
              {{ page }}
            </a>
          {% endif %}
        </li>
      {% endfor %}
      {% if objects.has_next %}
        <li class="page-item">
          <a class="page-link" href="?page={{ objects.paginator.num_pages }}">&raquo;</a>
        </li>
      {% endif %}
    </ul>
  </nav>`
}
*/