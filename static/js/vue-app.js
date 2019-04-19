// ListDataAPI used for creating data list from API consume.
// It will get data with AJAX then passing to list item and list pagination.
// It needs `url` props to passing URL of API consume.
var ListDataAPI = {
  props: ['url'],
  data: function() {
    return {
      items: [],
      pagination: {
        previous: null,
        next: null,
      },
    }
  },
  computed: {
    baseUrl: function() {
      return this.url.split(/[?#]/)[0];
    }
  },
  methods: {
    fetchData: function(url) {
      var self = this;
      axios.get(url).then(function(response) {
        self.items = response.data.results;
        self.pagination = {
          count: response.data.count,
          current: response.data.current,
          end: response.data.end,
          next: response.data.next,
          numPages: response.data.num_pages,
          previous: response.data.previous,
          start: response.data.start,
        };
      });
    },
  },
  mounted: function() {
    this.fetchData(this.url);
  },
}

// ListItem used in container item of data list.
var ListItem = {
  props: ['items'],
  computed: {
    defaultThumbnail: function() {
      return DEFAULT_THUMBNAIL
    }
  },
  methods: {
    redirectUrl: function(url) {
      window.location.href = url;
    }
  },
}

// List pagination used for all pagination purpose.
Vue.component('list-pagination', {
  props: ['pagination', 'baseUrl'],
  computed: {
    pages: function() {
      var range = [];
      for (var i=this.pagination.start;i<=this.pagination.end;i++) {
        range.push({
          val: i,
          isActive: i == this.pagination.current ? true : false,
        });
      }
      return range
    }
  },
  template: '<nav aria-label="Pagination">' +
    '<ul class="pagination justify-content-center">' +
      '<li class="page-item disabled">' +
        '<span class="page-link">Page {{ pagination.current }} Of {{ pagination.numPages }}</span>' +
      '</li>' +
      '<li class="page-item" v-if="pagination.previous">' +
        '<a class="page-link" href="#" @click.prevent="clickPage(baseUrl + \'?page=1\')">&laquo;</a>' +
      '</li>' +
      '<li class="page-item" :class="{ active: page.isActive }" v-for="page in pages" :key="page.val">' +
        '<span class="page-link" v-if="page.isActive">' +
          '{{ page.val }} <span class="sr-only">(current)</span>' +
        '</span>' +
        '<a class="page-link" href="#" v-else @click.prevent="clickPage(baseUrl + \'?page=\' + page.val)">{{ page.val }}</a>' +
      '</li>' +
      '<li class="page-item" v-if="pagination.next">' +
        '<a class="page-link" href="#" @click.prevent="clickPage(baseUrl + \'?page=\' + pagination.numPages)">&raquo;</a>' +
      '</li>' +
    '</ul>' +
  '</nav>',
  methods: {
    clickPage: function(url) {
      this.$parent.fetchData(url);
    },
  },
});

// ------------ author chapter container ------------
Vue.component('author-chapter-list', {
  extends: ListItem,
  template: '<div class="row">' +
    '<div class="col col-md-6 col-12" v-for="item in items" :key="item.slug" @click="redirectUrl(item.author_url)">' +
      '<div class="row my-2 mx-1 py-2 chapter-list">' +
        '<div class="col col-4 pr-1">' +
          '<img :src="item.thumbnail" v-if="item.thumbnail" class="img-fluid" loading="lazy">' +
          '<img :src="defaultThumbnail" v-else class="img-fluid" loading="lazy">' +
        '</div>' +
        '<div class="col col-8 pl-1"><h5>{{ item.title }}</h5></div>' +
      '</div>' +
    '</div>' +
  '</div>',
});

Vue.component('author-chapter-container', {
  extends: ListDataAPI,
  template: '<div>' +
    '<author-chapter-list v-if="items.length > 0" :items="items"></author-chapter-list>' +
    '<list-pagination v-if="pagination.previous || pagination.next" :pagination="pagination" :baseUrl="baseUrl"></list-pagination>' +
  '</div>',
});
// ------------ end of author chapter container ------------

// ------------ author comic container ------------
Vue.component('author-comic-list', {
  extends: ListItem,
  template: '<div class="row">' +
    '<div class="col col-md-6 col-12" v-for="item in items" :key="item.slug" @click="redirectUrl(item.direct_url)">' +
      '<div class="row my-2 mx-1 py-2 comic-list">' +
        '<div class="col col-4 pr-1">' +
          '<img :src="item.thumbnail" v-if="item.thumbnail" class="img-fluid" loading="lazy">' +
          '<img :src="defaultThumbnail" v-else class="img-fluid" loading="lazy">' +
        '</div>' +
        '<div class="col col-8 pl-1"><h5>{{ item.title }}</h5></div>' +
      '</div>' +
    '</div>' +
  '</div>',
});

Vue.component('author-comic-container', {
  extends: ListDataAPI,
  template: '<div>' +
    '<author-comic-list v-if="items.length > 0" :items="items"></author-comic-list>' +
    '<list-pagination v-if="pagination.previous || pagination.next" :pagination="pagination" :baseUrl="baseUrl"></list-pagination>' +
  '</div>',
})
// ------------ end of author comic container ------------

// ------------ comic list container ------------
Vue.component('comic-list', {
  extends: ListItem,
  template: '<div class="row">' +
    '<div class="col col-lg-4 col-md-6 col-12" v-for="item in items" :key="item.slug" @click="redirectUrl(item.direct_url)">' +
      '<div class="row my-2 mx-1 py-2 comic-list">' +
        '<div class="col col-4 pr-1">' +
          '<img :src="item.thumbnail" v-if="item.thumbnail" class="img-fluid" loading="lazy">' +
          '<img :src="defaultThumbnail" v-else class="img-fluid" loading="lazy">' +
        '</div>' +
        '<div class="col col-8 pl-1"><h5>{{ item.title }}</h5></div>' +
      '</div>' +
    '</div>' +
  '</div>',
});

Vue.component('comic-list-container', {
  extends: ListDataAPI,
  template: '<div>' +
    '<comic-list v-if="items.length > 0" :items="items"></comic-list>' +
    '<list-pagination v-if="pagination.previous || pagination.next" :pagination="pagination" :baseUrl="baseUrl"></list-pagination>' +
  '</div>',
});
// ------------ end of comic list container ------------

// ------------ chapter list container ------------
Vue.component('chapter-list', {
  extends: ListItem,
  template: '<div class="row">' +
    '<div class="col col-12" v-for="item in items" :key="item.slug">' +
      '<div class="row my-1 mx-1 py-2 chapter-list">' +
        '<div class="col col-2 pr-1">' +
          '<img :src="item.thumbnail" v-if="item.thumbnail" class="img-fluid" loading="lazy">' +
          '<img :src="defaultThumbnail" v-else class="img-fluid" loading="lazy">' +
        '</div>' +
        '<div class="col col-10 pl-1"><h5>{{ item.title }}</h5></div>' +
      '</div>' +
    '</div>' +
  '</div>',
});

Vue.component('chapter-list-container', {
  extends: ListDataAPI,
  template: '<div>' +
    '<chapter-list v-if="items.length > 0" :items="items"></chapter-list>' +
    '<list-pagination v-if="pagination.previous || pagination.next" :pagination="pagination" :baseUrl="baseUrl"></list-pagination>' +
  '</div>',
});
// ------------ end of chapter list container ------------
