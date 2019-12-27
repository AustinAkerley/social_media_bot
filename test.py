#!/usr/bin/python2
import social_media_bot
print("test start")
bowser_the_browser = social_media_bot.browser()
response_from_login = bowser_the_browser.login_to_facebook("bobbyyeet69@gmai.com", "BlahDahHah234!")
bowser_the_browser.list_forms()
possible_forms = bowser_the_browser.get_forms()
search_response = bowser_the_browser.search_facebook(0, "q", "Barry Akerley")

bowser_the_browser.seed("https://m.facebook.com/lenzi.johnson")
#Create Lenzi's facial recognition id

# Go to Friends link
# bowser_the_browser.browser_info()
ret_val = bowser_the_browser.see_more_friends()
print("SEE MORE FRIENDS LINK: ")
print(ret_val)
# bowser_the_browser.browser_info()
bowser_the_browser.print_links()
# Go to each friend, create face id profile
