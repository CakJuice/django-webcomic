Vue.component('author-chapter-list', {
  data: function() {
    return {
      value: 'this is item'
    }
  },
  template: '<div class="col col-md-4 col-6">{{value}}</div>',
});

Vue.component('author-chapter-container', {
  data: function() {
    return {
      value: 'blablabla',
      items: [],
    }
  },
  template: '<div class="row"><author-chapter-list v-if="items.length > 0"></author-chapter-list></div>',
  beforeMount: function() {
    console.log('before mount called');
  },
})
