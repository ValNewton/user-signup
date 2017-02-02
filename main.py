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
import re
from string import letters

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>FlickList</title>
    <style>
        .error {
            color: red;
        }
    </style>
</head>
<body>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

def build_page():
    
    u_name_label = "<label>Username</label>"
    u_name_label = "<input type= "text" name= "username" />"

    p_label = "<label>Password</label>"
    pass_ = "<input type = "password" name = "password"  />"

    ver_label = "<label>Verify Password</label>"
    p_verify = "<input type = "password" name = "verify" />"

    email_label = "<label>Email(optional)</label>"
    email = "<input type = "email" name = "email" />"

    header = "<h2>Signup</h2>"
    submit = "<input type ='submit'/>"

    form = "<form action= "/welcome" method="post">" + \
            u_name_label + u_name + "<span class="error"></span>" + "<br>" + \
            p_label + pass_ +"<br>" + "<span class="error"></span>" + "<br>" + \
            ver_label + p_verify + "<span class="error"></span>" + "<br>" + \
            submit + "</form>"

    return header + form

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Index(webapp2.RequestHandler):
    def get(self):
        page_content = build_page()
        content = page_header + page_content + page_footer
        self.response.write(content)

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        params = dict(username=username,
                      email=email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True

        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.redirect('/welcome?username=' + username)


class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        greeting = "Welcome, " + username
        content = "<p>" + greeting + "</p>"
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome),
    ], debug=True)
