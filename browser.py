#Must be in python2
import mechanize
import re

class browser:
    def __init__(self, cookies = None, headers = None):
        browser = mechanize.Browser()
        browser.set_handle_robots(False)
        cookies = mechanize.CookieJar()
        browser.set_cookiejar(cookies)
        browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.41 Safari/534.7')]
        browser.set_handle_refresh(False)
        self.browser = browser

    def login_to_facebook(self, email, password, url = 'http://www.facebook.com' ): #edits self.browser to now be logged in
        self.browser.open(url)
        self.browser.select_form(nr = 0)       #This is login-password form -> nr = number = 0
        self.browser.form['email'] = email
        self.browser.form['pass'] = password
        response = self.browser.submit()
        return response

    def get_forms(self):
        return self.browser.forms()

    def list_forms(self): #List forms by there action field
        i = 0
        for form in self.get_forms():
            print("Form Number: " + str(i))
            print("ACTION: ")
            print(form.action)

    def search_facebook(self, form_number=0, field = "q", field_value = None):
        self.browser.select_form(nr = form_number)       #This is login-password form -> nr = number = 0
        self.browser.form[field] = field_value
        response = self.browser.submit()
        return response

    def search(person):
        print("hi")

    def browser_info(self):
        print("URL: ")
        print(self.browser.geturl())
        print("INFO: ")
        print(self.browser.response().info())

    def seed(self, url):
        self.browser.open(url)

    def see_more_friends(self):
        friends_url = self.browser.geturl() + "/friends"
        resp = str(self.browser.open(friends_url).read())
        start = resp.find("m_more_friends\",href:\"") + len("m_more_friends\",href:\"")
        end = resp.find("\"", start)
        self.browser.open("https://m.facebook.com" + resp[start:end])
        return self.browser.geturl();

    def print_links(self):
        print("START ---------------------------------")
        i = 0
        for link in self.browser.links():
            print("I: "+str(i))
            print("ABS LINK: " + str(link.absolute_url))
            print("url: " + str(link.url))
            print("base_url: " + str(link.base_url))
            print("text: " + str(link.text))
            print("tag: " + str(link.tag))
            print("")
            i+= 1

        print("FORMS")
        self.list_forms()
