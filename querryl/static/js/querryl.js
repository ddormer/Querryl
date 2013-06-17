// Generated by CoffeeScript 1.6.1
(function() {
  var Block, BlockView, Blocks, BlocksView, Network, Networks, NetworksView, Querryl, Result, ResultView, Results, ResultsView, SearchView, Settings, SettingsView, hashCode, hsb, wave,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
    _this = this;

  Settings = (function(_super) {

    __extends(Settings, _super);

    function Settings() {
      return Settings.__super__.constructor.apply(this, arguments);
    }

    Settings.prototype.initialize = function() {
      Backbone.Model.prototype.initialize.apply(this, arguments);
      this.fetch();
      return this.bind('change', this.save);
    };

    Settings.prototype.defaults = {
      seperator: '|',
      leftBracket: '<',
      rightBracket: '>',
      backlogLimit: 5,
      date: false,
      time: true
    };

    Settings.prototype.getItem = function(key) {
      return localStorage.getItem(key);
    };

    Settings.prototype.sync = function(method, model, options) {
      var attr, item, _i, _j, _len, _len1, _ref, _ref1, _results;
      if (options == null) {
        options = {};
      }
      _.defaults(options, {
        'seperator': this.get('seperator'),
        'leftBracket': this.get('leftBracket'),
        'rightBracket': this.get('rightBracket'),
        'backlogLimit': this.get('backlogLimit'),
        'date': this.get('date'),
        'time': this.get('time')
      });
      if (method === 'read') {
        _ref = ['seperator', 'leftBracket', 'rightBracket', 'backlogLimit', 'date', 'time'];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          attr = _ref[_i];
          item = this.getItem(attr);
          if (attr === 'date' || attr === 'time') {
            item = JSON.parse(item);
          }
          this.set(attr, item != null ? item : options[attr]);
        }
      }
      if (method === 'update' || method === 'create') {
        _ref1 = ['seperator', 'leftBracket', 'rightBracket', 'backlogLimit', 'date', 'time'];
        _results = [];
        for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
          attr = _ref1[_j];
          _results.push(localStorage.setItem(attr, options[attr]));
        }
        return _results;
      }
    };

    return Settings;

  })(Backbone.Model);

  SettingsView = (function(_super) {

    __extends(SettingsView, _super);

    function SettingsView() {
      return SettingsView.__super__.constructor.apply(this, arguments);
    }

    SettingsView.prototype.el = '#settings';

    SettingsView.prototype.initialize = function() {
      Backbone.View.prototype.initialize.apply(this, arguments);
      rivets.configure({
        adapter: {
          subscribe: function(obj, keypath, callback) {
            return obj.on('change:' + keypath, callback);
          },
          unsubscribe: function(obj, keypath, callback) {
            return obj.off('change:' + keypath, callback);
          },
          read: function(obj, keypath) {
            return obj.get(keypath);
          },
          publish: function(obj, keypath, value) {
            return obj.set(keypath, value);
          }
        }
      });
      return rivets.bind(this.el, {
        settings: this.model
      });
    };

    return SettingsView;

  })(Backbone.View);

  Network = (function(_super) {

    __extends(Network, _super);

    function Network() {
      return Network.__super__.constructor.apply(this, arguments);
    }

    Network.prototype.idAttribute = 'networkid';

    return Network;

  })(Backbone.Model);

  Networks = (function(_super) {

    __extends(Networks, _super);

    function Networks() {
      return Networks.__super__.constructor.apply(this, arguments);
    }

    Networks.prototype.url = '/networks';

    Networks.prototype.model = Network;

    return Networks;

  })(Backbone.Collection);

  NetworksView = (function(_super) {

    __extends(NetworksView, _super);

    function NetworksView() {
      return NetworksView.__super__.constructor.apply(this, arguments);
    }

    NetworksView.prototype.el = '#network-select';

    NetworksView.prototype.initialize = function() {
      Backbone.View.prototype.initialize.apply(this, arguments);
      this.collection = new Networks;
      this.collection.fetch();
      rivets.configure({
        adapter: {
          subscribe: function(obj, keypath, callback) {
            return obj.on('sync', callback);
          },
          unsubscribe: function(obj, keypath, callback) {
            return obj.off('sync', callback);
          },
          read: function(obj, keypath) {
            if (obj instanceof Backbone.Collection) {
              return obj["models"];
            } else {
              return obj.get(keypath);
            }
          },
          publish: function(obj, keypath, value) {
            return obj.set(keypath, value);
          }
        }
      });
      return rivets.bind(this.el, {
        networks: this.collection
      });
    };

    return NetworksView;

  })(Backbone.View);

  Block = (function(_super) {

    __extends(Block, _super);

    function Block() {
      return Block.__super__.constructor.apply(this, arguments);
    }

    Block.prototype.idAttribute = 'messageid';

    return Block;

  })(Backbone.Model);

  Blocks = (function(_super) {

    __extends(Blocks, _super);

    function Blocks() {
      return Blocks.__super__.constructor.apply(this, arguments);
    }

    Blocks.prototype.url = '/block';

    Blocks.prototype.model = Block;

    Blocks.prototype.fetch = function() {
      this.messageid = arguments[0].data.messageid;
      return Backbone.Collection.prototype.fetch.apply(this, arguments);
    };

    return Blocks;

  })(Backbone.Collection);

  BlockView = (function(_super) {

    __extends(BlockView, _super);

    function BlockView() {
      var _this = this;
      this.render = function(messageid) {
        return BlockView.prototype.render.apply(_this, arguments);
      };
      return BlockView.__super__.constructor.apply(this, arguments);
    }

    BlockView.prototype.clasName = 'block-result';

    BlockView.prototype.tagName = 'li';

    BlockView.prototype.render = function(messageid) {
      var nickColor, template;
      if (this.model.id === messageid) {
        this.$el.addClass('highlight');
      }
      nickColor = Querryl.colourize(this.model.get('sender'));
      template = _.template("        <span><%= Querryl.formatDate(time, Querryl.Settings.get('date'), Querryl.Settings.get('time')) %></span>        <%=_.escape(Querryl.Settings.get('leftBracket'))%><span style='color: rgb(" + nickColor + ");'><%= sender %></span><%=_.escape(Querryl.Settings.get('rightBracket'))%>        <span><%= message %></span>");
      return this.$el.append(template(this.model.toJSON()));
    };

    return BlockView;

  })(Backbone.View);

  BlocksView = (function(_super) {

    __extends(BlocksView, _super);

    function BlocksView() {
      var _this = this;
      this.renderResult = function(item) {
        return BlocksView.prototype.renderResult.apply(_this, arguments);
      };
      return BlocksView.__super__.constructor.apply(this, arguments);
    }

    BlocksView.prototype.className = 'block-results';

    BlocksView.prototype.initialize = function() {
      Backbone.View.prototype.initialize.apply(this, arguments);
      $('#' + this.id).after("<ul id='block-" + this.id + "' class='" + this.className + "'></ul>");
      this.setElement($("#block-" + this.id));
      this.collection = new Blocks;
      this.listenTo(this.collection, 'reset', this.render);
      this.listenTo(this.collection, 'request', this.request);
      this.listenTo(this.collection, 'sync', this.sync);
      this.listenTo(this.collection, 'error', this.error);
      return this.alertify = {};
    };

    BlocksView.prototype.request = function() {
      return this.alertify.request = Alertify.log.info('Retrieving...', 0);
    };

    BlocksView.prototype.sync = function() {
      return this.alertify.request.close();
    };

    BlocksView.prototype.error = function(collection, error) {
      var message;
      message = 'An error occured';
      if (error.responseText) {
        message = JSON.parse(error.responseText).error;
      }
      this.alertify.error = Alertify.log.error(message, 0);
      if (this.alertify.request) {
        return this.alertify.request.close();
      }
    };

    BlocksView.prototype.toggle = function() {
      return this.$el.toggle();
    };

    BlocksView.prototype.render = function(collection) {
      this.$el.empty();
      return collection.each(this.renderResult);
    };

    BlocksView.prototype.renderResult = function(item) {
      var result;
      result = new BlockView({
        model: item
      });
      result.render(this.collection.messageid);
      return this.$el.append(result.el);
    };

    return BlocksView;

  })(Backbone.View);

  Result = (function(_super) {

    __extends(Result, _super);

    function Result() {
      return Result.__super__.constructor.apply(this, arguments);
    }

    return Result;

  })(Backbone.Model);

  Results = (function(_super) {

    __extends(Results, _super);

    function Results() {
      return Results.__super__.constructor.apply(this, arguments);
    }

    Results.prototype.model = Result;

    Results.prototype.url = '/search';

    Results.prototype.success = function() {
      return alertify.log('search complete');
    };

    return Results;

  })(Backbone.Collection);

  ResultView = (function(_super) {

    __extends(ResultView, _super);

    function ResultView() {
      var _this = this;
      this.render = function() {
        return ResultView.prototype.render.apply(_this, arguments);
      };
      return ResultView.__super__.constructor.apply(this, arguments);
    }

    ResultView.prototype.tagName = 'li';

    ResultView.prototype.className = 'result';

    ResultView.prototype.events = {
      'click': 'clicked'
    };

    ResultView.prototype.clicked = function(e) {
      var data;
      $(e).parents('.block-results').css('color', 'red');
      if (!this.blocksView) {
        this.blocksView = new BlocksView({
          id: this.model.get('messageid')
        });
        data = {
          'bufferid': this.model.get('bufferid'),
          'messageid': this.model.get('messageid'),
          'backlogLimit': Querryl.Settings.get('backlogLimit')
        };
        this.blocksView.collection.fetch({
          data: data,
          reset: true
        });
        return;
      }
      return this.blocksView.toggle();
    };

    ResultView.prototype.render = function() {
      var nickColor, template;
      nickColor = Querryl.colourize(this.model.get('sender'));
      template = _.template("        <span><%= Querryl.formatDate(time, Querryl.Settings.get('date'), Querryl.Settings.get('time')) %></span>        <%=_.escape(Querryl.Settings.get('leftBracket'))%><span style='color: rgb(" + nickColor + ");'><%= sender %></span><%=_.escape(Querryl.Settings.get('rightBracket'))%>        <span><%= message %></span>");
      return this.$el.append(template(this.model.toJSON()));
    };

    return ResultView;

  })(Backbone.View);

  SearchView = (function(_super) {

    __extends(SearchView, _super);

    function SearchView() {
      return SearchView.__super__.constructor.apply(this, arguments);
    }

    SearchView.prototype.el = '#search';

    return SearchView;

  })(Backbone.View);

  ResultsView = (function(_super) {

    __extends(ResultsView, _super);

    function ResultsView() {
      var _this = this;
      this.renderResult = function(item) {
        return ResultsView.prototype.renderResult.apply(_this, arguments);
      };
      return ResultsView.__super__.constructor.apply(this, arguments);
    }

    ResultsView.prototype.el = '#search-results';

    ResultsView.prototype.initialize = function() {
      Backbone.View.prototype.initialize.apply(this, arguments);
      this.collection = new Results;
      this.listenTo(this.collection, 'request', this.request);
      this.listenTo(this.collection, 'sync', this.sync);
      this.listenTo(this.collection, 'reset', this.render);
      this.listenTo(this.collection, 'error', this.error);
      return this.alertify = {};
    };

    ResultsView.prototype.render = function(collection) {
      this.$el.empty();
      return collection.each(this.renderResult);
    };

    ResultsView.prototype.renderResult = function(item) {
      var result;
      $('#search-error').hide();
      result = new ResultView({
        model: item,
        id: item.get('messageid')
      });
      result.render();
      return this.$el.append(result.el);
    };

    ResultsView.prototype.sync = function() {
      return this.alertify.request.close();
    };

    ResultsView.prototype.request = function() {
      this.alertify.request = Alertify.log.info("Searching...", 0);
      if (this.alertify.error) {
        return this.alertify.error.close();
      }
    };

    ResultsView.prototype.error = function(collection, error) {
      var message;
      message = 'An error occured';
      if (error.responseText) {
        message = JSON.parse(error.responseText).error;
      }
      this.alertify.error = Alertify.log.error(message, 0);
      if (this.alertify.request) {
        return this.alertify.request.close();
      }
    };

    return ResultsView;

  })(Backbone.View);

  wave = function(i) {
    return Math.cos(i / 3 * 2 * Math.PI) / 2;
  };

  hsb = function(h, s, b) {
    var n, _i, _results;
    if (s == null) {
      s = 1.0;
    }
    if (b == null) {
      b = 0.5;
    }
    _results = [];
    for (n = _i = 0; _i <= 2; n = ++_i) {
      _results.push(s * wave(h - n) + b);
    }
    return _results;
  };

  hashCode = function(string) {
    var char, hash, i;
    hash = 0;
    if (string.length === 0) {
      return hash;
    }
    i = 0;
    while (i < string.length) {
      char = string.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
      i++;
    }
    return hash;
  };

  Querryl = {
    initialize: function() {
      this.Settings = new Settings;
      return this.views = {
        searchView: new SearchView,
        resultsView: new ResultsView,
        settingsView: new SettingsView({
          model: this.Settings
        }),
        networksView: new NetworksView
      };
    },
    Router: Backbone.Router.extend({
      routes: {
        '': 'index',
        'search': 'index',
        'settings': 'settings'
      },
      index: function() {
        $(Querryl.views.searchView.el).show();
        return $(Querryl.views.settingsView.el).hide();
      },
      settings: function() {
        $(Querryl.views.settingsView.el).show();
        return $(Querryl.views.searchView.el).hide();
      }
    }),
    handleSubmit: function(form) {
      var collection, data;
      data = {};
      $(form).find('input').each(function(i, field) {
        return data[field.name] = field.value;
      });
      data['networkid'] = $(form).find(':selected').val();
      if (!data.channel) {
        Alertify.dialog.alert("Channel cannot be empty.");
        return false;
      }
      collection = Querryl.views.resultsView.collection;
      collection.fetch({
        data: data,
        reset: true
      });
      return false;
    },
    colourize: function(word) {
      var c, h, maxRange, s, _i, _len, _ref, _results;
      maxRange = Math.pow(2, 30);
      h = (hashCode(word) % maxRange) / maxRange * 3;
      s = 0.8;
      _ref = hsb(h, s);
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        c = _ref[_i];
        _results.push(parseInt(c * 255));
      }
      return _results;
    },
    formatDate: function(timestamp, d, t) {
      var date, formatString;
      if (!t && !d) {
        return timestamp;
      }
      date = new XDate(timestamp * 1000);
      if (d === true) {
        formatString = "yyyy-mm-dd";
      }
      if (t === true) {
        if (d === true) {
          formatString += ", HH:mm:ss";
        } else {
          formatString = "HH:mm:ss";
        }
      }
      return date.toString(formatString);
    }
  };

  $(function() {
    $('#query').focus();
    $('#settings').hide();
    Querryl.initialize();
    new Querryl.Router;
    Backbone.history.start();
    return window.Querryl = Querryl;
  });

}).call(this);
