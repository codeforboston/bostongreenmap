define(['backbone', 'marionette', 'js/templates'], function(Backbone, Marionette, templates) {
    var app = new Marionette.Application();
    app.addRegions({
        mainRegion: '#content-area'
    });

    var ArticleLayout = Marionette.Layout.extend({
        template: templates['templates/ArticleLayout.hbs'],
        regions: {
            'navRegion': '#app-nav',
            'articleRegion': '#app-articles'
        }
    });

    var Article = Backbone.Model.extend({
        defaults: {
            'title': ''
        }
    });

    var ArticleCollection = Backbone.Collection.extend({
        model: Article,
        url: 'http://www.fullstackcoder.com/api/v1/articles.jsonp',
        parse: function(response) {
            var articles = _.map(response.articles, function(article) {
                return new Article(article);
            });
            console.log(response);
            response = articles;
            return response;
        }
    });

    Article.Collection = ArticleCollection;

    var ArticleListItemView = Marionette.ItemView.extend({
        template: templates['templates/ArticleListItem.hbs'],
        tagName: 'li',
        className: 'article'
    });

    var ArticleListView = Marionette.CompositeView.extend({
        template: templates['templates/ArticleList.hbs'],
        itemView: ArticleListItemView,
        tagName: 'ul',
        className: 'article-list'
    });

    app.addInitializer(function(options) {
        var articles = new ArticleCollection();
        articles.fetch({
            'dataType': 'jsonp',
            'success': function(data) {
                var articleView = new ArticleListView({'collection': articles});

                var articleLayout = new ArticleLayout();
                articleLayout.render();
                articleLayout.articleRegion.show(articleView);
                app.getRegion('mainRegion').show(articleView);
            }
        });
    });

    return {
        startModule: function(done) {
            app.start({});
        }
    };
});
