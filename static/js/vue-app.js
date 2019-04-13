Vue.component('author-chapter-item', {
  data: function() {
    return {
      value: 'this is item'
    }
  },
  template: '<div class="col col-md-4 col-6">{{value}}</div>',
});

Vue.component('author-chapter-list', {
  data: function() {
    return {
      value: 'blablabla',
      items: [],
    }
  },
  template: '<author-chapter-item v-if="items.length > 0"></author-chapter-item>',
  beforeMount: function() {
    console.log('before mount called');
  },
})

new Vue({
  el: '#author-chapter-container'
})