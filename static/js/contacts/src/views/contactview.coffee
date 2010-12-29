### Main view for contact application
###

class ContactView extends Backbone.View
  el: $("#news")

  # Local variable needed to test if user type a CTRL+Enter keyboard shortcut
  # while typing his post content.
  isCtrl: false

  events:
    "click #contact-post-button" : "onPostClicked"
    "submit #contact-post-button" : "onPostClicked"
    "click #contact-alm-button" : "onAllClicked"
    "click #contact-pending-button" : "onPendingClicked"
    "click #contact-request-button" : "onRequestClicked"

  constructor: ->
    super

  ##
  # Initiliaze bind functions to this view, sets up contact collection
  # behaviour.
  initialize: ->
    _.bindAll(this, 'postNewContact', 'appendOne', 'prependOne', 'addAll')
    _.bindAll(this, 'onPostClicked')

    @contacts = new ContactCollection
    
    @contacts.bind('add', @prependOne)
    @contacts.bind('refresh', @addAll)
        

  ### Events
  ###

  ##
  # When key control is up it set is ctrl pressed variable to false.
  onKeyUp: (event) ->
    if(event.keyCode == 17)
      @isCtrl = false
    event

  ##
  # When key is down, if enter and CTRL are down together, the contact request
  # is posted.
  onKeyDown: (event) ->

    if(event.keyCode == 17)
      @isCtrl = true

    if (event.keyCode == 13 and @isCtrl)
      @isCtrl = false
      @postNewContact()
    event
 
  ##
  # When post button is clicked the contact request is posted.
  onPostClicked: (event) ->
    event.preventDefault()
    @postNewContact()
    event

  onAllClicked: (event) ->
    event.preventDefault()
    @reloadContacts("/platform/contacts/")

  onPendingClicked: (event) ->
    event.preventDefault()
    @reloadContacts("/platform/contacts/pending/")

  onRequestClicked: (event) ->
    event.preventDefault()
    @reloadContacts("/platform/contacts/requested/")

  reloadContacts: (url) ->
    @clearContacts()
    @contacts.url = url
    @contacts.fetch()
    @contacts


  ### Functions
  ###

  ##
  # Clears contact list then display more news button.
  clearContacts: ->
    $("#contacts").empty()


  ##
  # Adds all retrieved contacts to current contact list.
  addAll: ->
    @contacts.each(@appendOne)
    @contacts

  ## 
  # Append *contact* to the beginning of current post list (render it).
  appendOne: (contact) ->
    row = new ContactRow contact
    el = row.render()
    $("#contacts").prepend(el)
    row

  ## 
  # Prepend *contact* to the end of current contact list (render it).
  prependOne: (contact) ->
    row = new ContactRow contact
    el = row.render()
    $("#contacts").prepend(el)
    row

  ##
  # Clear post field and focus it.
  clearPostField: () ->
    $("#contact-url-field").val(null)
    $("#contact-url-field").focus()
    $("#contact-url-field")

  # Reload contact list.
  fetch: () ->
    @contacts.fetch()
    @contacts

  ##
  # Send a post request to server and add post at the beginning of current 
  # post list.
  postNewContact: ()->
    @contacts.create(url : $("#contact-url-field").val())
    $("#contact-url-field").val(null)
    $("#contact-url-field").focus()
    false


  ### UI Builders
  ###

  ##
  # Set listeners and corresponding callbacks on view widgets.
  setListeners: ->
      
    $("#contact-url-field").keyup((event) -> contactApp.onKeyUp(event))
    $("#contact-url-field").keydown((event) -> contactApp.onKeyDown(event))
    $("#contact-post-button").submit((event) -> contactApp.onPostClicked(event))
    $("#contact-post-button").click((event) -> contactApp.onPostClicked(event))
    $("#contact-all-button").click((event) -> contactApp.onAllClicked(event))
    $("#contact-pending-button").click((event) ->
        contactApp.onPendingClicked(event))
    $("#contact-request-button").click((event) ->
        contactApp.onRequestClicked(event))

  ##
  # Build JQuery widgets.
  setWidgets: ->
    $("#contact-all-button").button()
    $("#contact-pending-button").button()
    $("#contact-request-button").button()
    $("input#contact-post-button").button()
    $("#contact-a").addClass("disabled")
