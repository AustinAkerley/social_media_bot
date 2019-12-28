import mechanize

class facebook_bot:
    def __init__(self, email, password, fb_url = "https://m.facebook.com", depth = 2):
        # Open facebook
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        cookies = mechanize.CookieJar()
        self.browser.set_cookiejar(cookies)
        self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.41 Safari/534.7')]
        self.browser.set_handle_refresh(False)
        self.browser.open(fb_url)
        print("LOGIN PAGE URL: ")
        print(self.browser.geturl())
        # login
        self.browser.select_form(nr = 0)       #This is login-password form -> nr = number = 0
        self.browser.form['email'] = email
        self.browser.form['pass'] = password
        response = self.browser.submit()
        self.browser.open(fb_url) # Go to Bobby Yeet's home page
        print("HOME PAGE URL: ")
        print(self.browser.geturl())

    def explore_and_whore(self, seed_url, depth = 2):
        self.depth = depth
        self.seed_url = seed_url
        self.all_urls = [] # Past depth urls
        self.current_urls = [self.seed_url] # Current depth urls
        self.new_urls =  [] # Next depth urls
        for i in range (1, self.depth):
            for url in self.current_urls:
                resp = self.browser.open(url)
                self.populate_db(url) # Should add itself to the mysql database @@@@@@@@@@@@@@@@@@
                # temporary list of friends from the current profile we're adding to the database ####################
                # Should return an empty list if profile is private, but return all of their friends if public
                new_friends_urls = self.get_friends_urls(url)
                # ####################################################################################################
                for friend in new_friends_urls:
                    if friend in self.all_urls or friend in self.current_urls or friend in self.new_urls: # If the friend of this profile already exist in the old_urls, the current_urls, or in the new_urls
                        print("link already exist")
                    else:
                        self.new_urls.append(friend)
            self.all_urls += self.current_urls
            self.current_urls = self.new_urls
            self.new_urls = []
        self.all_urls += self.current_urls

    def print_all_urls(self):
        i=0
        for url in self.all_urls:
            print("i: "+str(i))
            print(url)
            i+=1

    def populate_db(self, url_of_profile):
        #Populate the data from a profile link into our my sql db
        return None # or a response

    def get_friends_urls(self, start_url):
        finished_friends = False;
        curr_url = start_url + "/friends"
        ret_val = [];
        while(not finished_friends):
            print("CURR URL: ")
            print(curr_url)
            resp = self.browser.open(curr_url)
            resp_str = str(resp.read())
#             print(resp_str)
            i = 0
            for link in self.browser.links():
                # is a correct link (not one of the first ones, not picture or add friend link)
                if(i >= 7 and link.text != "" and link.text != "Add Friend"):
                    print(link.absolute_url)
                    ret_val.append(str(link.absolute_url));
                i += 1;
            # goto next friend page
            
            start = resp_str.find("m_more_friends\"><a href=\"")
            if(start != -1):
                start += len("m_more_friends\"><a href=\"")
                end = resp_str.find("\"", start)
                curr_url = "https://m.facebook.com" + resp_str[start:end]
            else:
                finished_friends = True;
                self.browser.open(start_url);
        
        return ret_val;
