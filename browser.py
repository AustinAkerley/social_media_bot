#Must be in python2
import mechanize

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

    def search_facebook(self, form_number=0, field = "q", q = None):
        self.browser.select_form(nr = 0)       #This is login-password form -> nr = number = 0
        self.browser.form[field] = q
        response = self.browser.submit()
        return response

    def search(person):
        print("hi")

    def browser_info(self):
        print("URL: ")
        print(self.browser.geturl())
        print("INFO: ")
        print(self.browser.response().info())
