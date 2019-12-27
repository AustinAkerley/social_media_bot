import facebook_bot
print(facebook_bot)
bowser_the_browser = facebook_bot.browser()
response_from_login = bowser_the_browser.login_to_facebook("bobbyyeet69@gmai.com", "BlahDahHah234!")
bowser_the_browser.list_forms()
possible_forms = bowser_the_browser.get_forms()
search_response = bowser_the_browser.search_facebook(0, "q", "Barry Akerley")
bowser_the_browser.browser_info()
