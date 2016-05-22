#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))




class Handler(webapp2.RequestHandler):
    #write to browser
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    #get template
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    #write template to browser
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(Handler):

    def write_form(self, **params):
        self.render("rot_13.html", **params)
        #self.response.out.write(form % {"error": error, "text": text})

    def get(self):
        self.write_form()

    def post(self):
        user_input = self.request.get("text")

        if user_input:
            text = rot_text(user_input)
            escaped_text = cgi.escape(text, quote=True)

            self.write_form(error = "Yep that works.", text = escaped_text)
        else:
            self.write_form(error = "Enter some text first!", text = "")

#Computes ROT13 value of input
def rot_text(text):
    new_text = ""
    for character in text:
        if character.isalpha():
            character_order = ord(character) + 13
            #Wrap the letters for uppercase and lowercase letters which are at different character orders
            if character.isupper():
                if character_order > 90:
                    character_order = character_order - 26
            else:
                if character_order > 122:
                    character_order = character_order - 26
            character = chr(character_order)
        new_text = new_text + character

    return new_text

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
