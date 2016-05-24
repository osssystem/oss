# coding: utf-8

from django.test import TestCase
import re
from django_webtest import WebTest


class OssWebTests(WebTest):
#    fixtures = ['users.json']

    def testRegisterandLogin(self):
        register_form = self.app.get('/').click(u'register').form

        register_form['email'] = 'example2@example.com'
        register_form['username'] = 'test'
        register_form['password1'] = '123456'
        register_form['password2'] = '123456'
        result_page = register_form.submit().follow()
        #print(result_page)
        assert u'Hello. Log in, please!' in result_page

        login_form = result_page.click('login', index=0).form
        login_form['username'] = 'test'
        login_form['password'] = '123456'
        result_page = login_form.submit().follow()
        assert u'logout' in result_page

    def testLogoutAndLogin(self):
        page = self.app.get('/', user='test')
        page = page.click(u'logout').maybe_follow()
        assert u'logout' not in page
        login_form = page.click(u'login', index=0).form
        login_form['username'] = 'test'
        login_form['password'] = '123456'
        result_page = login_form.submit()
        assert u'Please enter a correct username and password' in result_page


    def testDevelopers(self):
        page = self.app.get('/developers', user='test')
        assert u'Developer name' in page

    def testUserProfile(self):
        page = self.app.get('/users/user_profile', user='andyzt')
        assert u'Welcome to your profile' in page

    def testProjects(self):
        page = self.app.get('/projects', user='test')
        assert u'Available projects' in page

    def testProjectPage(self):
        self.testUserProfile()
        page = self.app.get('/project/1/', user='andyzt')
        assert u'Project page' in page







