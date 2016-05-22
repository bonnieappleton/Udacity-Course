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
import re

form = """
    <h1>Sign Up!</h1>
    <form method="post">

      <table>
        <tr>
          <td>
            Username *
          </td>
          <td>
            <input type="text" name="username" value="%(username)s">
          </td>
          <td>%(username_error)s</td>
        </tr>

        <tr>
          <td>
            Password *
          </td>
          <td>
            <input type="password" name="password" value="%(password)s">
          </td>
          <td>%(password_error)s</td>
        </tr>

        <tr>
          <td>
            Verify Password *
          </td>
          <td>
            <input type="password" name="verify-password" value="%(verifypassword)s">
          </td>
          <td>%(verify_password_error)s</td>
        </tr>

        <tr>
          <td>
            Email
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td>%(email_error)s</td>
        </td>

      </table>

      <input type="submit">
    </form>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PW_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(un):
    return USER_RE.match(un)

def valid_password(pw):
    return PW_RE.match(pw)

def valid_email(email):
    return EMAIL_RE.match(email)




class MainHandler(webapp2.RequestHandler):

    def write_form(self, username_error="", password_error="", verify_password_error="", email_error="", username="", email="", password="", verifypassword="") :
        self.response.out.write(form % {"username_error": username_error, "password_error": password_error, "verify_password_error": verify_password_error, "email_error": email_error, "username": username, "password": password, "verifypassword": verifypassword, "email": email})

    def get(self):
        self.write_form()

    def post(self):
        user_username = self.request.get("username")
        user_password = self.request.get("password")
        user_verify_password = self.request.get("verify-password")
        user_email = self.request.get("email")
        username_error = ""
        password_error = ""
        verify_password_error = ""
        email_error = ""
        valid = True

        if not valid_username(user_username) :
            username_error = "Sorry, that username is not valid"
            valid = False

        if not valid_password(user_password) :
            password_error = "Sorry, that password is invalid"
            valid = False

        if user_password != user_verify_password :
            verify_password_error = "Those passwords don't match!"
            valid = False

        if user_email and not valid_email(user_email) :
            email_error = "That email is invalid"
            valid = False

        if valid == True :
            self.redirect("/success")
        else :
            self.write_form(username_error, password_error, verify_password_error, email_error, user_username, user_email)

class SuccessHandler(webapp2.RequestHandler):
    
    def get(self):
        self.response.out.write("You have been added to our excellent website")

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/success', SuccessHandler)
], debug=True)
