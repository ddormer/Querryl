class Settings extends Backbone.Model
    initialize: ->
        Backbone.Model.prototype.initialize.apply(@, arguments)
        @fetch()
        @bind('change', @save)

    defaults: {
        seperator: '|'
        leftBracket: '<'
        rightBracket: '>'
        backlogLimit: 5
        date: false
        time: true
    }

    getItem: (key) ->
        return localStorage.getItem(key)

    sync: (method, model, options = {}) ->
        _.defaults(options, {
            'seperator': @get('seperator')
            'leftBracket': @get('leftBracket')
            'rightBracket': @get('rightBracket')
            'backlogLimit': @get('backlogLimit')
            'date': @get('date')
            'time': @get('time')
        })

        if method is 'read'
            for attr in ['seperator', 'leftBracket', 'rightBracket', 'backlogLimit', 'date', 'time']
                item = @getItem(attr)
                if attr in ['date', 'time']
                    item = JSON.parse(item)
                @set(attr, item ? options[attr])

        if method in ['update', 'create']
            for attr in ['seperator', 'leftBracket', 'rightBracket', 'backlogLimit', 'date', 'time']
                localStorage.setItem(attr, options[attr])



class SettingsView extends Backbone.View
    el: '#settings'

    initialize: () ->
        Backbone.View.prototype.initialize.apply(@, arguments)
        rivets.configure({
          adapter: {
            subscribe: (obj, keypath, callback) ->
              obj.on('change:' + keypath, callback)

            unsubscribe: (obj, keypath, callback) ->
              obj.off('change:' + keypath, callback)

            read: (obj, keypath) ->
              return obj.get(keypath)

            publish: (obj, keypath, value) ->
              obj.set(keypath, value)
          }
        })
        rivets.bind(@el, {settings: @model})


class Network extends Backbone.Model
    idAttribute: 'networkid'

class Networks extends Backbone.Collection
    url: '/networks'
    model: Network

class NetworksView extends Backbone.View
    el: '#network-select'

    initialize: () ->
        Backbone.View.prototype.initialize.apply(@, arguments)
        @collection = new Networks
        @collection.fetch()

        rivets.configure({
          adapter: {
            subscribe: (obj, keypath, callback) ->
                obj.on('sync', callback)

            unsubscribe: (obj, keypath, callback) ->
                obj.off('sync', callback)

            read: (obj, keypath) ->
                if obj instanceof Backbone.Collection
                then obj["models"]
                else obj.get(keypath)

            publish: (obj, keypath, value) ->
                obj.set(keypath, value)
          }
        })
        rivets.bind(@el, {networks: @collection})



class Block extends Backbone.Model
    idAttribute: 'messageid'



class Blocks extends Backbone.Collection
    url: '/block'
    model: Block

    fetch: () ->
        @messageid = arguments[0].data.messageid
        Backbone.Collection.prototype.fetch.apply(@, arguments)



class BlockView extends Backbone.View
    clasName: 'block-result'
    tagName: 'li'

    render: (messageid) =>
        if @model.id is messageid
            @$el.addClass('highlight')

        nickColor = Querryl.colourize(@model.get('sender'))
        template = _.template("
        <span><%= Querryl.formatDate(time, Querryl.Settings.get('date'), Querryl.Settings.get('time')) %></span>
        <%=_.escape(Querryl.Settings.get('leftBracket'))%><span style='color: rgb(#{nickColor});'><%= sender %></span><%=_.escape(Querryl.Settings.get('rightBracket'))%>
        <span><%= message %></span>")
        @$el.append(template(@model.toJSON()))



class BlocksView extends Backbone.View
    className: 'block-results'

    initialize: () ->
        Backbone.View.prototype.initialize.apply(@, arguments)
        $('#' + @id).after("<ul id='block-#{@id}' class='#{@className}'></ul>")
        @setElement($("#block-#{@id}"))
        @collection = new Blocks
        @listenTo(@collection, 'reset', @render)
        @listenTo(@collection, 'request', @request)
        @listenTo(@collection, 'sync', @sync)
        @listenTo(@collection, 'error', @error)
        @alertify = {}

    request: ->
        @alertify.request = Alertify.log.info('Retrieving...', 0)

    sync: ->
        @alertify.request.close()

    error: (collection, error) ->
        message = 'An error occured'
        if error.responseText
            message = JSON.parse(error.responseText).error
        @alertify.error = Alertify.log.error(message, 0)
        if @alertify.request
            @alertify.request.close()

    toggle: () ->
        @$el.toggle()

    render: (collection) ->
        @$el.empty()
        collection.each(@renderResult)

    renderResult: (item) =>
        result = new BlockView({model: item})
        result.render(@collection.messageid)
        @$el.append(result.el)



class Result extends Backbone.Model



class Results extends Backbone.Collection
    model: Result
    url: '/search'

    success: ->
        alertify.log('search complete')


class ResultView extends Backbone.View
    tagName: 'li'
    className: 'result'
    events: {
        'click': 'clicked'
    }

    clicked: (e) ->
        $(e).parents('.block-results').css('color', 'red')
        if not @blocksView
            @blocksView = new BlocksView({id: @model.get('messageid')})
            data = {'bufferid': @model.get('bufferid'), 'messageid': @model.get('messageid'), 'backlogLimit': Querryl.Settings.get('backlogLimit')}
            @blocksView.collection.fetch(
                {data: data, reset: true})
            return
        @blocksView.toggle()

    render: () =>
        nickColor = Querryl.colourize(@model.get('sender'))
        template = _.template("
        <span><%= Querryl.formatDate(time, Querryl.Settings.get('date'), Querryl.Settings.get('time')) %></span>
        <%=_.escape(Querryl.Settings.get('leftBracket'))%><span style='color: rgb(#{nickColor});'><%= _.escape(sender) %></span><%=_.escape(Querryl.Settings.get('rightBracket'))%>
        <span><%= _.escape(message) %></span>")
        @$el.append(template(@model.toJSON()))



class SearchView extends Backbone.View
    el: '#search'



class ResultsView extends Backbone.View
    el: '#search-results'

    initialize: () ->
        Backbone.View.prototype.initialize.apply(@, arguments)
        @collection = new Results
        @listenTo(@collection, 'request', @request)
        @listenTo(@collection, 'sync', @sync)
        @listenTo(@collection, 'reset', @render)
        @listenTo(@collection, 'error', @error)
        @alertify = {}

    render: (collection) ->
        @$el.empty()
        collection.each(@renderResult)

    renderResult: (item) =>
        $('#search-error').hide()
        result = new ResultView({model: item, id: item.get('messageid')})
        result.render()
        @$el.append(result.el)


    sync: ->
        @alertify.request.close()


    request: ->
        @alertify.request = Alertify.log.info("Searching...", 0)
        if @alertify.error
            @alertify.error.close()

    error: (collection, error) ->
        message = 'An error occured'
        if error.responseText
            message = JSON.parse(error.responseText).error
        @alertify.error = Alertify.log.error(message, 0)
        if @alertify.request
            @alertify.request.close()


wave = (i) ->
    Math.cos(i / 3 * 2 * Math.PI) / 2


hsb = (h, s=1.0, b=0.5) ->
    (s * wave(h - n) + b for n in [0..2])


hashCode = (string) ->
	hash = 0
	if (string.length == 0)
        return hash
    i = 0
    while i < string.length
        char = string.charCodeAt(i)
        hash = ((hash << 5) - hash) + char
        hash = hash & hash # Convert to 32bit integer
        i++
	return hash


Querryl = {
    initialize: ->
        @Settings = new Settings
        @views = {
            searchView: new SearchView
            resultsView: new ResultsView
            settingsView: new SettingsView({model: @Settings})
            networksView: new NetworksView
        }


    Router: Backbone.Router.extend({
        routes: {
            '': 'index'
            'search': 'index'
            'settings': 'settings'
        }
        index: ->
            $(Querryl.views.searchView.el).show()
            $(Querryl.views.settingsView.el).hide()

        settings: ->
            $(Querryl.views.settingsView.el).show()
            $(Querryl.views.searchView.el).hide()
        })


    handleSubmit: (form) ->
        data = {}
        $(form).find('input').each((i, field) ->
            data[field.name] = field.value
        )
        data['networkid'] = $(form).find(':selected').val()

        if not data.channel
            Alertify.dialog.alert("Channel cannot be empty.")
            return false

        collection = Querryl.views.resultsView.collection
        collection.fetch(
            {data: data, reset: true})
        return false


    colourize: (word) ->
        maxRange = Math.pow(2, 30)
        h = (hashCode(word) % maxRange) / maxRange * 3
        s = 0.8
        (parseInt(c*255) for c in hsb(h, s))


    formatDate: (timestamp, d, t) ->
        # d: include the date?
        # t: include the time?
        if not t and not d
            return timestamp

        date = new XDate(timestamp*1000)
        if d is true
            formatString = "yyyy-mm-dd"
        if t is true
            if d is true
                formatString += ", HH:mm:ss"
            else
                formatString = "HH:mm:ss"

        return date.toString(formatString)
}

$ ->
    $('#query').focus()
    $('#settings').hide()
    Querryl.initialize()
    new Querryl.Router
    Backbone.history.start()
    window.Querryl = Querryl


