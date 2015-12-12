#coffee -w -c -o js/ coffee/

class Playground

  instance = null

  class CreateSvg
    constructor: () ->
    	return SVG("main").size('100%', '100%')

  @get: () ->
    instance ?= new CreateSvg()


class SqlViewer

	constructor: (url) ->
		@properties =
			url: url
			shema: ''
			playground: null

	init: ->
    	@getJson()
    	@createPlayground()
    	@draw()
    	return

	getJson: ->
		$(document).ready ->
			$.get @properties.url, (data) ->
				data

	createPlayground: ->
		@properties.playground = Playground.get()

	draw: ->
		alert 3


# sqlViewer = new SqlViewer('test.json')
# sqlViewer.init()
