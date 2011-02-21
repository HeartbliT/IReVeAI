(function(){var g,h,c,i=Object.prototype.hasOwnProperty,f=function(a,b){function d(){this.constructor=a}for(var e in b)if(i.call(b,e))a[e]=b[e];d.prototype=b.prototype;a.prototype=new d;a.__super__=b.prototype;return a};g=function(){function a(b){a.__super__.constructor.apply(this,arguments);this.id="";this.set("url",b.url);this.set("name",b.name);this.set("city",b.city)}f(a,Backbone.Model);a.prototype.url="/user/";a.prototype.getName=function(){return this.get("name")};a.prototype.setName=function(b){alert(b);
this.set("name",b);return alert(this.getName())};a.prototype.setUrl=function(b){return this.set("url",b)};a.prototype.setCity=function(b){return this.set("city",b)};a.prototype.getUrl=function(){return this.get("userUrl")};a.prototype.getCity=function(){return this.get("city")};a.prototype.isNew=function(){return false};return a}();h=function(){function a(){a.__super__.constructor.apply(this,arguments)}f(a,Backbone.Collection);a.prototype.model=g;a.prototype.url="/user/";a.prototype.parse=function(b){return b.rows};
return a}();c=new (function(){function a(){a.__super__.constructor.apply(this,arguments)}f(a,Backbone.View);a.prototype.el=$("#profile");a.prototype.initialize=function(){_.bindAll(this,"onKeyUp","postUserInfo","fetch","addAll");this.users=new h;return this.users.bind("refresh",this.addAll)};a.prototype.onKeyUp=function(){return this.postUserInfo()};a.prototype.addAll=function(){this.user=this.users.first();$("#platform-profile-name").val(this.user.getName());$("#platform-profile-city").val(this.user.getCity());
$("#platform-profile-url").val(this.user.get("url"));if(!this.user.get("url")){this.tutorialOn=true;this.displayTutorial(1)}return this.users};a.prototype.fetch=function(){this.users.fetch();return this.users};a.prototype.postUserInfo=function(){var b;b=this.tutorialOn;return this.user.save({name:$("#platform-profile-name").val(),url:$("#platform-profile-url").val(),city:$("#platform-profile-city").val()},{success:function(){if(b)return $.get("/profile/tutorial/2/",function(d){return $("#tutorial-profile").html(d)})}})};
a.prototype.testTutorial=function(){if(this.tutorialOn){this.displayTutorial(2);this.tutorialOn=false}return false};a.prototype.displayTutorial=function(b){return $.get("/profile/tutorial/"+b+"/",function(d){return $("#tutorial-profile").html(d)})};a.prototype.setListeners=function(){$("#platform-profile-name").keyup(function(b){return c.onKeyUp(b)});$("#platform-profile-url").keyup(function(b){return c.onKeyUp(b)});return $("#platform-profile-city").keyup(function(b){return c.onKeyUp(b)})};a.prototype.setWidgets=
function(){$("#profile input").val(null);return $("#profile-a").addClass("disabled")};return a}());c.setWidgets();c.setListeners();c.fetch()}).call(this);
