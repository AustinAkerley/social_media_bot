import mechanize
import time
import os
import json
import numpy as np
from PIL import Image
import face_recognition
from BeautifulSoup import BeautifulSoup
from bs4.diagnose import profile

class facebook_bot:
    def __init__(self, account_file = "./facebook_login.txt", depth = 2):
        self.account_file = account_file
        self.curr_account = 0
        self.account_offsets = []
        offset = 0
        f = open(self.account_file, "rb", 0)
        for line in f:
            self.account_offsets.append(offset)
            offset += len(line)
        f.close()
        self.switch_account();
        self.browser.open("https://m.facebook.com") # Go to Bobby Yeet's home page
        print("HOME PAGE URL: ")
        print(self.browser.geturl())

    def switch_account(self):
        f = open(self.account_file, "rb", 0)
        f.seek(self.account_offsets[self.curr_account])
        email, password = f.next().split(",");
        f.close();

        # Open facebook
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        cookies = mechanize.CookieJar()
        self.browser.set_cookiejar(cookies)
        self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.41 Safari/534.7')]
        self.browser.set_handle_refresh(False)
        self.browser.open("https://m.facebook.com")
        print("LOGIN PAGE URL: ")
        print(self.browser.geturl())
        # login
        self.browser.select_form(nr = 0)       #This is login-password form -> nr = number = 0
        self.browser.form['email'] = email
        self.browser.form['pass'] = password
        self.browser.submit()
        self.curr_account = (self.curr_account + 1) % len(self.account_offsets)
        return email, password

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
            for url in self.current_urls:
                new_friends_urls = self.get_friends_urls(url)
                # ####################################################################################################
                for friend in new_friends_urls:
                    if friend in self.all_urls or friend in self.current_urls or friend in self.new_urls: # If the friend of this profile already exist in the old_urls, the current_urls, or in the new_urls
                        print("profile: "+str(friend)+" already exist")
                    else:
                        self.new_urls.append(friend)
            self.all_urls += self.current_urls
            self.current_urls = self.new_urls
            self.new_urls = []
        for url in self.current_urls:
            resp = self.browser.open(url)
            self.populate_db(url)
        self.all_urls += self.current_urls

    def populate_db(self, url_of_profile):
        resp = self.browser.open(url_of_profile)
        print("Current URL of Page: "+self.browser.geturl())
        folder_name = url_of_profile.split("/")[-1]
        links_till_profile_pic = 3
        is_after_menu = False
        profile_pic_link = None
        for link in self.browser.links(): # Getting the profile picture link
            #print(link.absolute_url)
            #print(link.text)
            if link.text == "Menu":
                is_after_menu = True
            if is_after_menu:
                links_till_profile_pic-=1
            if links_till_profile_pic == 0:
                profile_pic_link = link.absolute_url
                break

        resp = self.browser.open(profile_pic_link) # go to profile picture link
        print("Profile Pic URL: "+self.browser.geturl())
        os.system("mkdir -p ./profiles/"+folder_name) # Create new directory based off of unique link name

        first_pic = None
        end_loop = False
        i = 0
        print(" FOLDER NAME: "+str(folder_name))



        while i<50 and end_loop!=True: # This loop populates the profile pictures folder with all of the users profile pictures, up to 50 prof pics
            print("On Profile Picture {"+str(i)+"}")
            soup = BeautifulSoup(resp)
            image_tags = soup.findAll("img")
            if image_tags is None or image_tags is []:
                print("No image tags ")
                break
            picture_exists = False
            for image in image_tags:
                link_name = image['src']
                if link_name.find("https://scontent") != -1:
                    picture_exists = True
                    data = self.browser.open(link_name).read()
                    self.browser.back()
                    if data == first_pic:
                        end_loop = True
                        break;
                    save = open("./profiles/"+folder_name+"/profpic"+str(i)+".jpg", "wb")
                    save.write(data)
                    save.close()
                    if first_pic is None: # establish first picture
                        first_pic = data
            if not picture_exists:
                self.switch_account()
                self.browser.open(profile_pic_link);
                print("GOT BANNED AND SWITCHED ACCOUNTS")
                continue;

            for link in self.browser.links():
                if link.text == "Next":
                    time.sleep(7)
                    profile_pic_link = link.absolute_url;
                    resp = self.browser.open(profile_pic_link)

            i+=1
        folder_dir = "./profiles/"+folder_name
        db_profile = self.process_prof_pics(folder_dir)
        # Get general info, no implemeneted yet.
        #self.get_general_profile_info(url_of_profile)

        profile_dict = {url_of_profile: db_profile}
        # Now get general info like sex, hometown, etc... Whatever they provide
        with open('profiles.json','a') as f:
            profile_dict_str = json.dumps(profile_dict)
            f.write(profile_dict_str + ",\n")

        return None

    def get_general_profile_info(self, profile_url):
        resp = self.browser.open(profile_url)
        print("Current URL: "+self.browser.geturl())

    def process_prof_pics(self, dir):
        pic_num = 0
        file_path = dir +"/profpic" + str(pic_num)+".jpg"
        prof_name = dir.split("/")[-1]
        persons = {"person0" : []};
        persons_pictures = {"person0": []}
        while (os.path.isfile(file_path)): # Iterate through all of the profile pictures
            image = face_recognition.load_image_file(file_path)
            face_locations = face_recognition.face_locations(image) # List of top, bottom, left, rights
            print("PICTURE "+str(pic_num)+": ")
            print("I found {} face(s) in this photograph.".format(len(face_locations)))

            if len(face_locations) == 0:
                pic_num+=1
                file_path = dir +"/profpic" + str(pic_num)+".jpg"
                continue; # skip this picture and go to the next

            encodings = face_recognition.face_encodings(image, face_locations) # List of arrays size 128
            face_image = None
            face_iterator = 0
            for encoding in encodings: # Iterate through all of the face encodings of the picture
                found_person = False
                top, right, bottom, left = face_locations[face_iterator]
                face_image = (image, image[top:bottom, left:right])
                for person in persons:
                    if person is []: # Person doesn't have a picture yet, assign the face to that person
                        persons[person] += encoding
                        persons_pictures[person].append(face_image)
                        break
                    compares = face_recognition.compare_faces(persons[person], encoding) # Compare each existing face encoding of a person to this new face encoding creates a list of True or False values
                    matches = 0
                    for compare in compares:
                        if compare:
                            matches += 1
                    if (matches >= len(compares) / 2): # Successful majority match to an existing person, add this new encoding to that persons list of face encodings
                        persons[person].append(encoding)
                        persons_pictures[person].append(face_image)
                        found_person = True;
                        break;
                if not found_person:
                        persons.update({"person" + str(len(persons)) : [encoding]})
                        persons_pictures.update({ "person" + str(len(persons_pictures)) : [face_image]})
                face_iterator+=1
            pic_num+=1
            file_path = dir +"/profpic" + str(pic_num)+".jpg"
        # find person with the most faces in all the profiles pictures
        longest = None
        for person in persons:
            if longest is None or len(persons[person]) > len(longest):
                longest = person
        # Find the image that matches all the other images in the most often face the most (most average face)
        best_img = None
        best_img_match = 0
        best_img_loc = None
        for i in range(0,len(persons[longest])):
            if best_img_loc is None:
                best_img_loc = i
                best_img = persons_pictures[longest][i]
                dists = face_recognition.face_distance(persons[longest], persons[longest][i])
                best_img_match = np.mean(dists)
            else:
                dists = face_recognition.face_distance(persons[longest], persons[longest][i])
                avg = np.mean(dists)
                if avg < best_img_match:
                    best_img_loc = i;
                    best_img = persons_pictures[longest][i]
                    best_img_match = avg
        prof_name_list = []
        prof_full_name = ""
        for name in prof_name.split("."):
            if not name.isdigit(): #If the name isn't a digit
                prof_name_list.append(name)
                if name != prof_name.split(".")[-1]:
                    prof_full_name = prof_full_name + name + " "
                else:
                    prof_full_name += name

        face_id = persons[longest][best_img_loc] if best_img_loc is not None else None;

        os.system("rm -rf "+dir+"/*")

        path_to_file = None;
        if best_img is not None:
            path_to_file = dir+"/profile.jpg"
            pil_image = Image.fromarray(best_img[1])
            pil_image.save(path_to_file)
            path_to_file = dir+"/original_picture.jpg"
            pil_image = Image.fromarray(best_img[0])
            pil_image.save(path_to_file)
            face_id = face_id.tolist()

        print("Name: " + prof_full_name)
        print("Profile Face ID: "+ str(face_id))
        print("Profile Picture: ")

        return{"name" : prof_full_name, "face_id" : face_id, "prof_pic" : path_to_file}

    def get_friends_urls(self, start_url):
        finished_friends = False;
        curr_url = start_url + "/friends"
        ret_val = [];
        while(not finished_friends):
            #print("CURR URL: ")
            #print(curr_url)
            resp = self.browser.open(curr_url)
            resp_str = str(resp.read())
#             print(resp_str)
            i = 0
            friends_on_page = 0
            for link in self.browser.links():
                # is a correct link (not one of the first ones, not picture or add friend link)
                if(link.text != "" and link.text != "Add Friend" and link.absolute_url.find("?fref=fr_tab") != -1):
                    print("Gathering friends from link: " + start_url)
                    print("FOUND: "+link.text)
                    ret_val.append(str(link.absolute_url).split("?")[0]);
                    friends_on_page += 1;
                    #print("\nProfile:")
                    #print(str(link.absolute_url).split("?")[0])
                    #print(link.text)
                i += 1;
            # goto next friend page

            start = resp_str.find("m_more_friends\"><a href=\"")
            if(start != -1):
                time.sleep(20)
                start += len("m_more_friends\"><a href=\"")
                end = resp_str.find("\"", start)
                curr_url = "https://m.facebook.com" + resp_str[start:end]
            elif friends_on_page == 0:
                self.switch_account();
            else:
                finished_friends = True;
                self.browser.open(start_url);
        #print("END @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        return ret_val;


    def print_all_urls(self):
        i=0
        for url in self.all_urls:
            print("i: "+str(i))
            print(url)
            i+=1
