Vue.component('author-chapter-list', {
  props: ['items'],
  data: function() {
    return {
      value: 'this is item',
      defaultThumbnail: DEFAULT_THUMBNAIL,
    }
  },
  template: '<div class="row">' +
      '<div class="col col-md-6 col-12" v-for="item in items">' +
        '<div class="row my-2 mx-1 py-2 chapter-list">' +
          '<div class="col col-4 pr-1">' +
            '<img v-bind:src="item.thumbnail" v-if="item.thumbnail" class="img-fluid" loading="lazy">' +
            '<img v-bind:src="defaultThumbnail" v-else class="img-fluid" loading="lazy">' +
          '</div>' +
          '<div class="col col-8 pl-1"><h5>{{item.title}}</h5></div>' +
        '</div>' +
      '</div>' +
    '</div>',
});

Vue.component('author-chapter-container', {
  props: ['url'],
  data: function() {
    return {
      items: [],
    }
  },
  template: '<div><author-chapter-list v-if="items.length > 0" v-bind:items="items"></author-chapter-list></div>',
  mounted: function() {
    var self = this;
    axios.get(this.url).then(function(response) {
      self.items = response.data.results;
    });
  },
});
