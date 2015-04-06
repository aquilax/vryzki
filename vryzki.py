# -*- encoding: utf-8 -*-
import os
import urllib

from data import *
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
  def get(self):
    q = MyVertice.all().filter('status =', 1).order('-created')
    data = {
      'facts': q.fetch(10),
      'title': "Начало",
      'content': "templates/index.html",
    }
    path = os.path.join(os.path.dirname(__file__), 'main.html')
    self.response.out.write(template.render(path, data))

class Sitemap(webapp.RequestHandler):
  def get(self):
    facts= MyNode.gql("where status=1");
    output =  '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" >'
    for fact in facts:
      output = output + '<url><loc>http://vryzki.appspot.com/show/%s</loc><changefreq>never</changefreq><priority>0.8</priority></url>'  %(fact.key().id())
    output = output + '</urlset>'
    self.response.headers["Content-Type"] = 'text/xml'
    self.response.out.write(output)

class EditPage(webapp.RequestHandler):
  def get(self, id):
    pass

class EditSavePage(webapp.RequestHandler):
  def get(self):
    pass

class ShowPage(webapp.RequestHandler):
  def get(self, id):
    id = int(id)
    node = MyNode.get_by_id(id)

    l = MyVertice.all()
    l.filter("left =", node)
    l.order("created")
    left = l.fetch(None);

    r = MyVertice.all()
    r.filter("right =", node)
    r.order("created")
    right = r.fetch(None);
    
    data = {
      'left': left,
      'right': right,
      'center': node,
      'title': node.name,
      'content': "templates/show.html",
    }
    path = os.path.join(os.path.dirname(__file__), 'main.html')
    self.response.out.write(template.render(path, data))

class AddPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
    else:
      if users.is_current_user_admin():
#        q = MyNode.all();
#        nodesq = q.fetch(10000);
#        nodes = '['
#        for node in nodesq:
#          nodes += '"'+node.name+'",'
#        nodes += '];'
#
#        q = MyAction.all();
#        nodesq = q.fetch(10000);
#        actions = '['
#        for node in nodesq:
#          actions += '"'+node.name+'",'
#        actions += '];'
#
#        include = '<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>';
#        include += '<script type="text/javascript" src="/js/tag.js"></script>';
#        include += '<script type="text/javascript">'
#        include += 'nodes='+nodes
#        include += 'actions='+actions
#        include += "$(document).ready(function(){$(function () {$('input#left').tagSuggest({tags: nodes});$('input#right').tagSuggest({tags: nodes});$('input#action').tagSuggest({tags: actions});});});"
#        include += '</script>'
        data = {
          'title': "Добавяне на връзка",
          'content': "templates/add.html",
#          'include': include,
        }
        path = os.path.join(os.path.dirname(__file__), 'main.html')
        self.response.out.write(template.render(path, data))
      else:
        self.redirect('/')

class AddSavePage(webapp.RequestHandler):
  def post(self):
    save(self.request);
    self.redirect('/');

  def get(self):
    data = {
      'title': "Добави връзка",
      'content': "templates/search.html",
    }
    path = os.path.join(os.path.dirname(__file__), 'main.html')
    self.response.out.write(template.render(path, data))

class SearchPage(webapp.RequestHandler):
  def get(self):
    data = {
      'title': "Търсене",
      'content': "templates/search.html",
    }
    path = os.path.join(os.path.dirname(__file__), 'main.html')
    self.response.out.write(template.render(path, data))



application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/show/(.*)', ShowPage),
                                      ('/add', AddPage),
                                      ('/addsave', AddSavePage),
                                      ('/search', SearchPage),
                                      ('/sitemap.xml', Sitemap),
                                      ('/edit/(.*)', EditPage),
                                      ('/editsave', EditSavePage),
                                      ],
                                     debug=False)

def profile_main():
    # This is the main function for profiling
    # We've renamed our original main() above to real_main()
    import cProfile, pstats
    prof = cProfile.Profile()
    prof = prof.runctx("real_main()", globals(), locals())
    print "<pre>"
    stats = pstats.Stats(prof)
    stats.sort_stats("time")  # Or cumulative
    stats.print_stats(80)  # 80 = how many to print
    # The rest is optional.
    # stats.print_callees()
    # stats.print_callers()
    print "</pre>"

def real_main():
    run_wsgi_app(application)

main = real_main

if __name__ == "__main__":
    main()