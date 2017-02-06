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

def build_page(user_val='', email_val='', error_username='', error_password='', error_verify='', error_email=''):
    u_name_label = "<label>Username</label>"
    u_name = "<input type= 'text' name= 'username' value = "'+ user_val + '" />"

    p_label = "<label>Password</label>"
    pass_ = "<input type = 'password' name = 'password' />"

    ver_label = "<label>Verify Password</label>"
    p_verify = "<input type = 'password' name = 'verify' />"

    email_label = "<label>Email(optional)</label>"
    email = "<input type = 'email' name ='email' value ="'+ email_val +'" />"

    header = "<h2>Signup</h2>"
    submit = "<input type ='submit'/>"

    form = "<form action= '/' method='post'>" + \
           u_name_label + u_name + "<span class='error'>" + error_username + "</span>" + "<br>" + \
           p_label + pass_ + "<span class='error'>" + error_password + " </span>" + "<br>" + \
           ver_label + p_verify + "<span class='error'>" + error_verify + "</span>" + "<br>" + \
           email_label + email + "<span class='error'>" + error_email + "</span>" + "<br>" + \
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
        esc_username = cgi.escape(self.request.get('username'))
        esc_password = cgi.escape(self.request.get('password'))
        esc_verify = cgi.escape(self.request.get('verify'))
        esc_email = cgi.escape(self.request.get('email'))

        error_username = ''
        error_password = ''
        error_verify = ''
        error_email = ''


        if not valid_username(esc_username):
            error_username = "That's not a valid username."
            have_error = True

        if not valid_password(esc_password):
            error_password = "That wasn't a valid password."
            have_error = True

        elif esc_password != esc_verify:
            error_verify = "Your passwords didn't match."
            have_error = True

        if not valid_email(esc_email) and not esc_email == '' :
            error_email = "That's not a valid email."
            have_error = True

        if have_error:
            page_content = build_page(esc_username, esc_email, error_username, error_password, error_verify, error_email)
            content = page_header + page_content + page_footer
            self.response.write(content)

        else:
            self.redirect('/welcome?username=' + esc_username)


class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        page_content = "<p>Welcome " + username + "</p>"
        content = page_header + page_content + page_footer
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome),
    ], debug=True)
