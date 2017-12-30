import sys
import telepot
from telepot.delegate import pave_event_space, per_chat_id, create_open
from bs4 import BeautifulSoup
import datetime
import urllib.request


now = datetime.datetime.now()


class MessageCounter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count = 0
        self._input=""
        global year_d
        global month_d
        global day_d
        global titlelist
        global year_y
        global searchindicate
        global cinemalist_number
        global searchmovie
        global daytext
    def on_chat_message(self, msg):
        #whatever the first input the user gives, the bot will reply that way
        if self._count == 0:
            self.sender.sendMessage("Hello, buddy. \nI am FilmLoversBot. \n\nWhich box office data do you want?\nI can help you with either daily or yearly box office.\n\nI can also help you with finding movie schedules at your nearest Singaporean cinema.")
            self._count+=1
            global year_d
            global month_d
            global day_d

        #detecting the input, whether it contains either daily or yearly. If contain, move to the next step. If not contain, ask a valid input.    
        elif self._count==1:
            self._input=msg["text"]
            if "daily" in self._input.lower():
                self.sender.sendMessage("Please input the year of box office you would like to know:")
                self._count+=1
            elif "yearly" in self._input.lower():
                self.sender.sendMessage("Please input the year of box office you would like to know:")
                self._count+=4
            elif "schedule" in self._input.lower():
                self.sender.sendMessage("""What cinema are you interested in?\n\nI can probably help you with these cinemas: GV, Cathay, Shaw, and Filmgarde.\
                \nJust enter name of the cinemas, I can search it for you. If you need help just type "guide".""")
                self._count+=5
            elif "end" or "enough" or "bored" in self._input.lower():
                self.sender.sendMessage("If you need help about best movie and cinema, don't forget you can rely on me :')")
                exit()
            else:
                self.sender.sendMessage("""Sorry, I don't understand. Please input either "daily" or "yearly" or "schedule".""")                
                self._count=1
                

        #detecting the year that user sends.        
        elif self._count == 2:
            year_d =(msg["text"])
            try:
                if int(year_d) < 1980:
                    self.sender.sendMessage("Sorry, we don't have daily box office data before 1980! Please type another year that is greater than or at least equal to 1980")
                    self._count=2
                elif int(year_d) > now.year:
                    self.sender.sendMessage("Type in a valid year!")
                    self._count=2
                else:
                    self.sender.sendMessage("Please input the month using integer format:")
                    self._count+=1
            except ValueError:
                self.sender.sendMessage("Sorry, please hand me an integer, darling.")
                self._count=2


        #detecting the month AFTER the year is already valid        
        elif self._count == 3:
            month_d=(msg["text"])
            try:
                if int(month_d) < 1 or int(month_d) > 12:
                    self.sender.sendMessage("Type in a valid month!")
                    self._count=3
                elif int(year_d) == now.year and int(month_d) > now.month:
                    self.sender.sendMessage("Type in a valid month!")
                    self._count=3
                else:
                    self.sender.sendMessage("Please input the date using this format (DD):")
                    self._count+=1
            except ValueError:
                self.sender.sendMessage("Sorry, but your plan to make my program full of errors has failed. Type in an integer, darling.")
                self._count=3
                
        #detecting the date input AFTER the month is already valid        
        elif self._count == 4:
            day_d=(msg["text"])
            leap_4 = int(year_d) % 4
            leap_100 = int(year_d) % 100
            leap_400 = int(year_d) % 400
            month_list = [1, 3, 5, 7, 8, 10, 12]
            month_list2 = [4, 6, 9, 11]
            try:
                if int(year_d) == now.year and int(month_d) == now.month and int(day_d) > now.day-1:
                    self.sender.sendMessage("Type in a valid bla date!")
                    self._count = 4
                else:
                    if int(month_d) in month_list:
                        day_limit = 31
                    elif int(month_d) in month_list2:
                        day_limit = 30
                    elif leap_4 == 0:
                        if leap_100 == 0:
                            if leap_400 == 0:
                                day_limit = 29
                            else:
                                day_limit = 28
                        else:
                            day_limit = 29
                    else:
                        day_limit = 28

                    if int(day_d) < 1 or int(day_d) > day_limit:
                        self.sender.sendMessage("Type in a valid date hua!")
                        self._count = 4
                    else:
                        url = "http://www.boxofficemojo.com/daily/chart/?view=1day&sortdate=" + str(int(year_d)) + "-" + str(int(month_d)) + "-"+ str(int(day_d)) + "&p=.htm"
                        print(url)
                        mainlist=[]
                        titlelist=[]
                        grosslist=[]
                        premiere=[]
                        scrap=78
                        scrapend=0
                        pageFile = urllib.request.urlopen(url)                           
                        pageHtml = pageFile.read()
                        soup = BeautifulSoup(pageHtml, 'html.parser')
                        for table3 in soup.findAll('table',{'border':'0'}):
                            for table1 in table3.findAll('td',{'colspan':'3'}):
                                for table in soup.findAll(('td',{'align':'right'})):
                                    for item in table.findAll('font',{'size':'2'}):
                                        mainlist.append(item.text)
                                        scrapend=scrapend+1
                        if scrapend>188:
                            scrapend=188
                        for scrap in range(78,scrapend,11):
                            titlelist.append(mainlist[scrap])
                            grosslist.append(mainlist[scrap+2])
                            premiere.append(mainlist[scrap+8])
                        for i in range(int((scrapend-78)/11)):
                            if i>0 and titlelist[i]==titlelist[0]:
                                break
                        #print("{0:50}{0}".format(titlelist[i],grosslist[i]))
                            self.sender.sendMessage(titlelist[i]+"\nBO Daily:"+grosslist[i]+"\n"+premiere[i]+" days after premiere in US.")
                        try:
                            titlelist[0]
                        except IndexError:
                            self.sender.sendMessage("Sorry, we don't have data for that date!")
                            self._count = 0
                        self.sender.sendMessage("That's all, folks!")
                        self._count = 0
            except ValueError:
                self.sender.sendMessage("Sorry, please input an integer!")
                self._count = 4

       

        #detecting the year inputted. if valid & data is available, send output
        elif self._count==5:
            year_y =(msg["text"])
            try:
                if int(year_y) < 1980:
                    self.sender.sendMessage("Sorry, we don't have daily box office data before 1980! Please type another year that is greater than or at least equal to 1980.")
                    self._count=5
                elif int(year_y) > now.year:
                    self.sender.sendMessage("Bud, " + str(int(year_y)) + " hasn't happened yet.\n//_-")
                    self._count=5
                else:
                    url = "http://www.boxofficemojo.com/yearly/chart/?yr="+str(int(year_y))+"&p=.htm"
                    pageFile = urllib.request.urlopen(url)
                    pageHtml = pageFile.read()
                    soup = BeautifulSoup(pageHtml, 'html.parser')
                    globalcount=0
                    movielist=[]
                    for i in range(100):
                        movielist.append(i)


                    count=1
                    for table in soup.findAll('tr',{'bgcolor':'#ffffff'}):
                        for item in table.findAll('font',{'size':'2'}):
                            for item1 in item.findAll('a'):
                                if count%3==1:
                                    movielist[globalcount]=item1.text
                                    globalcount+=2

                                count+=1
            
                    globalcount=1
                    count=1
                    for table in soup.findAll('tr',{'bgcolor':'#f4f4ff'}):
                        for item in table.findAll('font',{'size':'2'}):
                            for item1 in item.findAll('a'):
                                if count%3==1:
                                    movielist[globalcount]=item1.text
                                    globalcount+=2
                                count+=1
                    for i in range(10):
                        self.sender.sendMessage(movielist[i])
                    self.sender.sendMessage("Take note that this Top 10 list is the 10 movies (in the year " + str(int(year_y)) + " with the highest US Box Office Gross, not worldwide.")
                    self.sender.sendMessage("That's all, folks! Don't forget to buy popcorn and share with me!")
                        
#error nya gabisa kerja please fix(kalo inputnya ga integer gmna, trs klo no data gmna) ak ga ngrti cra pake except
                        
            except ValueError:
                self.sender.sendMessage("Sorry, please input an integer!")
                self._count=5
            except NameError:
                self.sender.sendMessage("Oops! We don't have the data for that date!")
            except IndexError:
                self.sender.sendMessage("Oops! We don't have the data for that date!")
            self._count=0

        elif self._count == 6:
            searchindicate=(msg["text"]).lower() #so we can choose between type "guide" or "name the place (ex: VivoCity)" here or "back".  
            global listmerk
            global listcinema
            global searchindicate_final
            
            listmerk=["0","golden-village","cathay-cineplexes","shaw-theatres","filmgarde"]
            listcinema=["0","gv-bishan","cathay-amk-hub","shaw-balestier","cathay-cineleisure","gv-plaza-singapura","cathay-the-cathay","gv-grand","gv-grand-gold-class-","filmgarde-bugis","shaw-lido","gv-tiong-bahru","2","3","cathay-west-mall","5","gv-yishun","gv-vivocity-gold-class-","gv-vivocity","filmgarde-leisure-park","shaw-lot-one","gv-vivocity-cinema-europa","gv-vivocity-gvmax","gv-jurong-point","gv-tampines","cathay-causeway-point","cathay-downtown-east","shaw-century-square","shaw-nex","cathay-the-cathay-platinum","cathay-the-grand-cathay","shaw-bugis","gv-katong","gv-katong-gold-class-","shaw-jcube","gv-city-square","cathay-jem","cathay-jem-platinum","cathay-cineleisure-platinum","gv-suntec-gold-class-","gv-city-square-gemini-","gv-grand-gemini-","gv-bishan-dbox-","gv-anz-grand-seats","gv-suntec","shaw-seletar-mall","shaw-waterway-point"]
            if "back" in searchindicate: # If "back" id the input, direct it to daily,yearly,schedule input again.
                self.sender.sendMessage("So, would you like to look at daily box office, yearly box office, or would you like to look at movie schedules?")
                self._count=1
            elif not "guide" in searchindicate: #if we input the name of the place, e.g.vivocity
                searchindicate_lower=searchindicate.lower() #to assume VivOciTY and vivocity is the same.
                searchindicate_lower_cineplex=(searchindicate_lower.replace("cineplex ","")).replace(" cineplex","") #sometimes people enter "cineplex" for the cinema name.

                #This cineplex name is not important or can be ommited. We use replace("cineplex ","")).replace(" cineplex","") or we use it twice because if we just use use replace("cineplex ","")):
                #cathay cineplex cathay --> cathay cathay
                #cathay cineplex-->the computer cant detect because no space after "cineplex"
                
                searchindicate_lower_goldenvillage=searchindicate_lower_cineplex.replace("golden village","gv")
                searchindicate_lower_golden=searchindicate_lower_goldenvillage.replace("golden","gv")
                searchindicate_lower_gv=searchindicate_lower_golden.replace("village","gv")
                
                #This command is use for assume (gv bishan) and (bishan gv) is the same. Order of the writing is not important after this command.
                
                searchindicate_split=searchindicate_lower_gv.split()
                
                #gv bishan --> [gv,bishan]
                
                searchindicate_sort=sorted(searchindicate_split)
                
                #[gv,bishan]--> [bishan,gv]
                
                searchindicate_final='-'.join(searchindicate_sort)
                
                #[bishan,gv]--> bishan-gv
                #'-'.join(searchindicate_sort) means i join every element in searchindicate_sort(type=list) with "-"
                
                self.sender.sendMessage("The cinema/place you typed in is "+searchindicate+".")
                
            # output= "The cinema/place is "gv bishan."
                self.sender.sendMessage("""What's the name of the movie you want to watch? If you want to look all of the cinema's schedule, type in "All".""")
                self._count+=3
                
            # The program ask if the user wants to look of all schedule or specific schedule.
            else: #if the user ask for guide.
                self.sender.sendMessage("Which cinema are you interested in?\nI can probably help you with these cinemas:\n1 --> GV \n2 --> Cathay \n3 --> Shaw \n4 --> Filmgarde")
                self._count+=1
                
        elif self._count == 7: #Self count 7 to 8 is used for inputing cinema with numbers as we provide, a.k.a user input "guide" in self._count 6.
            global cinemacategory
            global ruleofinput
            cinemacategory=(msg["text"])
            if "1" in cinemacategory: #Which cinema are you interested in?\n I probably can help you with these cinemas:\n1.GV, \n2.Cathay, \n3.Shaw, and..
                #if we input 1 for gv then:
                self.sender.sendMessage("Which GV cinema?\n 43.ANZ Grand Seats,1.Bishan,35.City Square,7.Grand,8.Grand Gold Class,23.Jurong Point,32.Katong,33.Katong Gold Class,5.Plaza Singapura,44.Suntec,39.Suntec Gold Class,40.City Square Gemini,24.Tampines,11.Tiong Bahru, 18.VivoCity, 17.VivoCity Gold Class,16.Yishun,21.VivoCity Cinema Europa,22.VivoCity GV Max,41.Grand Gemini,42.Bishan Box".replace("."," --> ").replace(",","\n"))
                cinemacategory=1
                ruleofinput=["43","1","35","7","8","23","32","33","5","44","39","40","24","11","18","17","16","21","22","41","42"] #sometimes people input number which is not provided by the message.
                #for example: I input "3" even though I ask for "GV". This ruleofinput is used for limit the user for the input. 
                self._count+=1
            elif "3" in cinemacategory:
                #if we input 3 for shaw then:
                self.sender.sendMessage("Which Shaw cinema?\n3.Balestier,31.Bugis,27.Century Square,34.J-Cube,10.Lido,20.Lot One,28.Nex,45.Seletar Mall,46.Waterway Point,6.The Cathay".replace("."," --> ").replace(",","\n"))                    
                self._count+=1
                ruleofinput=["3","31","27","34","10","20","28","45","46","6"]
            elif "2" in cinemacategory:
                #if we input 2 for cathay then:
                self.sender.sendMessage("Which Cathay cinema?\n2.AMK Hub,25.Causeway Point,4.Cineleisure,6.The Cathay,26.Downtown East,36.JEM,14.Westmall,29.Cathay the Cathay Premium,30.Cathay the Grand Cathay,37.JEM Premium,38.Cineleisure Premium".replace("."," --> ").replace(",","\n"))
                self._count+=1
                ruleofinput=["2","25","4","6","26","36","14","45","46","6","29","30","37","38"]
            elif "4" in cinemacategory:
                #if we input 4 for filmgarde then:
                self.sender.sendMessage("Which cinema do you prefer?\n9 --> Bugis\nor\n19 --> Leisure Park?")
                self._count+=1
                ruleofinput=["9","19"]
            elif "back" in cinemacategory: # If "back" id the input, direct it to daily,yearly,schedule input again.
                self.sender.sendMessage("So, would you like to look at daily box office, yearly box office, or would you like to look at movie schedules?")
                self._count = 1
            else: # bot only provided input until 4 but we input "8". The bot ask again the number.
                self.sender.sendMessage("Please input the number as our guide.")
                self._count = 7
                
        elif self._count == 8:
            cinemalist_number=(msg["text"])
            if cinemalist_number in ruleofinput: #Ex I input "43" after I choose gv" a. k. a correct input, lead to this cchoice.
                #We convert it into string because cinemalist_number is a string type. if (string type)=(integer type) also invalid in python.
                listcinema=["0","gv-bishan","cathay-amk-hub","shaw-balestier","cathay-cineleisure","gv-plaza-singapura","cathay-the-cathay","gv-grand","gv-grand-gold-class-","filmgarde-bugis","shaw-lido","gv-tiong-bahru","2","3","cathay-west-mall","5","gv-yishun","gv-vivocity-gold-class-","gv-vivocity","filmgarde-leisure-park","shaw-lot-one","gv-vivocity-cinema-europa","gv-vivocity-gvmax","gv-jurong-point","gv-tampines","cathay-causeway-point","cathay-downtown-east","shaw-century-square","shaw-nex","cathay-the-cathay-platinum","cathay-the-grand-cathay","shaw-bugis","gv-katong","gv-katong-gold-class-","shaw-jcube","gv-city-square","cathay-jem","cathay-jem-platinum","cathay-cineleisure-platinum","gv-suntec-gold-class-","gv-city-square-gemini-","gv-grand-gemini-","gv-bishan-dbox-","gv-anz-grand-seats","gv-suntec","shaw-seletar-mall","shaw-waterway-point"]
                searchindicate_begin=(listcinema[int(cinemalist_number)]).replace("-"," ")
                #listcinema[int(cinemalist_number)]-> list[i], "i" must be an integer, but cinemalist_number is a string.
                #for example we input "1" after we input gv, we want to search information about gv-bishan.
                #but as we see, we have also to sort it to bishan-gv. 
                searchindicate_split=searchindicate_begin.split()
                searchindicate_sort=sorted(searchindicate_split)
                searchindicate_final='-'.join(searchindicate_sort)
                self.sender.sendMessage("""Which movie which do you want to watch? If you want to look all schedule, type "All".""")
                #After we already input all information about the cinema according to the guide, we can go to decide what schedule movie that we want to watch.
                self._count+=1
            elif "back" in cinemalist_number: #if I want to change from filmgarde to gv for example.
                self.sender.sendMessage("Which cinema are you interested in?\n I probably can help you with these cinemas:\n1 --> GV\n2 --> Cathay\n3 --> Shaw, and \n4 --> Filmgarde")
                self._count=7
            else: # if for example I choose gv but I input "9" which is filmgarde, the ruleofinput creates the condition "false" for "if cinemalist_number in str(ruleofinput)":
                #No 9 in the ruleofinput of gv!(as if we input 1.gv, the rule input is 43,1,35,etc)
                self.sender.sendMessage("There's no such number in that type of cinema.")
                self._count=8
    
                
            
        elif self._count == 9: #This self count is for filter the movie that we want to watch. We direct to self count 9 after the user fill in the cinema location, with or without guide.
            #If we input "all" here, then searchmovie="all". Later in self._count 10 we indicate that if the input is all, no need to filter the movie!
            searchmovie=(msg["text"])
            global searchmovie_lower
            searchmovie_lower=searchmovie.lower() #if we input AVatar, avatar and AVatar is the same, meh!
            if "back" in searchmovie: #If I want to change the location, for ex: from filmgarde bugis to gv bishan.
                self.sender.sendMessage("""What cinema are you interested in?\n I probably can help you with these cinemas:GV, Cathay, Shaw, and Filmgarde.\
                \n just enter the place or the cinemas, I can search it for you. If you need help just type "guide" """)
                self._count=6
            else: #If we don't input "back"a.k.a we input "All" or the title of the movie.
                self.sender.sendMessage("Do you want to see today's movie schedule or tomorrow's movie schedule?")
                self._count+=1
            
        elif self._count == 10: #this used for looking at today or tomorrow schedule or false input.
            global dayindicator
            daytext=(msg["text"]) #daytext read what the input is.
            if "today" in daytext.lower():#if daytext detects "today or TOday or tODAY", the dayindicator, which will be used in Beautifulsoupscraping, assign to "today" 
                dayindicator="today"
            elif "tomorrow" in daytext.lower():#the same lah as above :)
                dayindicator="tomorrow"
            else:
                dayindicator="Unavailable"
            if dayindicator=="today" or dayindicator=="tomorrow": #if the user input "today"or "tomorrow", which assign dayindicator today or tomorrow.   
                listmore=[]
                listmerk=["0-0","golden-village","cathay-cineplexes","shaw-theatres","filmgarde"]
                listcinema=["0-0","gv-bishan","cathay-amk-hub","shaw-balestier","cathay-cineleisure","gv-plaza-singapura","cathay-the-cathay","gv-grand","gv-grand-gold-class-","filmgarde-bugis","shaw-lido","gv-tiong-bahru","2-2","3-3","cathay-west-mall","5-5","gv-yishun","gv-vivocity-gold-class-","gv-vivocity","filmgarde-leisure-park","shaw-lot-one","gv-vivocity-cinema-europa","gv-vivocity-gvmax","gv-jurong-point","gv-tampines","cathay-causeway-point","cathay-downtown-east","shaw-century-square","shaw-nex","cathay-the-cathay-platinum","cathay-the-grand-cathay","shaw-bugis","gv-katong","gv-katong-gold-class-","shaw-jcube","gv-city-square","cathay-jem","cathay-jem-platinum","cathay-cineleisure-platinum","gv-suntec-gold-class-","gv-city-square-gemini-","gv-grand-gemini-","gv-bishan-dbox-","gv-anz-grand-seats","gv-suntec","shaw-seletar-mall","shaw-waterway-point"]
                for i in range(47):
                    listcinema_begin=listcinema[i].replace("-"," ")
                    listcinema_split=listcinema_begin.split()
                    listcinema_sort=sorted(listcinema_split)
                    listcinema_extra=listcinema_sort #to overcome point-shaw-waterway and shaw-waterway-point problem. (3 sort name problem)
                    #if we enter waterway point, it will convert to -point-waterway- and no point-waterway in point-shaw-waterway, but it is in -shaw-waterway-point
                    listcinema_extra[0],listcinema_extra[1]=listcinema_extra[1],listcinema_extra[0]
                    listcinema_sort=sorted(listcinema_extra)
                    listcinema_final='-'.join(listcinema_sort)
                    listcinema_extra_final='-'.join(listcinema_extra)
                    if searchindicate_final in listcinema_final:
                        listmore.append(i)
                    if searchindicate_final in listcinema_extra_final: #if cannot detect
                        if not i in listmore:
                            listmore.append(i)
                            
                #This is the hardest part of all this schedule program. So, I just give the example yaa. A user want to watch at vivocity.
                #This program transform listcinema into sort.
                #if the user input as the guide, user have to CHOOSE what type of cinema:
                        # ex between:21.Vivocity cinema europa and 22.vivocity gv max, only can pick one! He choose 21 or list number 22
                        #searchindicate_final=sorted[vivocity-cinema-europa-]-->[cinema-europa-vivocity'-]
                #if the user only input "vivo"(not as guide, many possible right! vivocity europa and vivocity gv meet the requirement.)
                        
                #for i in range(47): --> at the beginning, i=0, 
                #   listcinema_begin=listcinema[i].replace("-"," ")-->listcinema[0]=0, the replace command is useless
                #   listcinema_split=listcinema_begin.split() -->no use
                #   listcinema_sort=sorted(listcinema_split)-->no use
                #   listcinema_final='-'.join(listcinema_sort)-->no use
                #   if searchindicate_final in listcinema_final: vivo not the same as 0!, this condition is not fulfilled.
                #        listmore.append(i)
                
                #for i in range(47): --> at now, i=1, 
                #   listcinema_begin=listcinema[i].replace("-"," ")-->listcinema[1]=gv-bishan, the replace command change (gv-bishan -->gv bishan)
                #   split function only work if the whitespace seperate the words!, so have to replace it. Split change string to list type.
                #   listcinema_split=listcinema_begin.split() --> (gv bishan) is split into [gv,bishan]
                #   listcinema_sort=sorted(listcinema_split)-->[gv,bishan]-->[bishan,gv]
                #   listcinema_final='-'.join(listcinema_sort)-->join all inside list with -, a.k.a bishan-gv --> convert list to string
                #   if searchindicate_final in listcinema_final: vivo not the same with bishan-gv, so the condition is false
                #        listmore.append(i)
                
                #for i in range(47): --> at now, i=21, 
                #   listcinema_begin=listcinema[i].replace("-"," ")-->listcinema[21]=vivocity-cinema-europa, the replace command change it to (vivocity cinema europa)
                #   split function only work if the whitespace seperate the words!, so have to replace it. Split change string to list type.
                #   listcinema_split=listcinema_begin.split() --> (vivocity cinema europa) is split into [vivocity,cinema,europa]
                #   listcinema_sort=sorted(listcinema_split)-->[vivocity,cinema,europa]-->[cinema,europa,vivocity]
                #   listcinema_final='-'.join(listcinema_sort)-->join all inside list with -, a.k.a cinema-europa-vivocity --> convert list to string
                #   if searchindicate_final in listcinema_final: vivo is inside cinema-europa-vivocity, so the condition is true
                #        listmore.append(i) --> listmore =[21]

                #for i in range(47): --> at now, i=22,
                #   listcinema_begin=listcinema[i].replace("-"," ")-->listcinema[22]=vivocity-gv-max, the replace command change it to (vivocity gv max)
                #   split function only work if the whitespace seperate the words!, so have to replace it. Split change string to list type.
                #   listcinema_split=listcinema_begin.split() --> (vivocity gv max) is split into [vivocity,gv,max]
                #   listcinema_sort=sorted(listcinema_split)-->[vivocity,gv,max]-->[gv,max,vivocity]
                #   listcinema_final='-'.join(listcinema_sort)-->join all inside list with -, a.k.a gv-max-vivocity --> convert list to string
                #   if searchindicate_final in listcinema_final: vivo is inside gv-max-vivocity, so the condition is true
                #        listmore.append(i) --> listmore =[21,22]
                #Listmore indicate data that we want to scrap, in this case in list. 21 and list.22
                
                try:
                    listmore[0] #If no data that suitable,no data in the listmore which will result in IndexError!
                except IndexError:
                    self.sender.sendMessage("Sorry, I have no information about that cinema.")
                for cinema_int in listmore:#for example: listmore=[21,22], first, cinema_int=21, then cinema_int number 22, we print all that fulfilled the condition!
                    d=listcinema[(cinema_int)] #d=listcinema[21]
                    self.sender.sendMessage(d.upper())
                    if "gv" in d: #if you see clearly, b is inside d ringht?, so dont have to declare twice
                        b=listmerk[1]
                    elif "cathay" in d:
                        b=listmerk[2]
                    elif "shaw" in d:
                        b=listmerk[3]
                    else:
                        b=listmerk[4]
                    combine=[]
                    pageFile=urllib.request.urlopen("http://www.popcorn.sg/" + b + "/" + d + "/cinema/" + str(cinema_int))
                    pageHTML=pageFile.read()
                    soup=BeautifulSoup(pageHTML,"html.parser")
                    listschedule=[]
                    listtiming=[]
                    for item1 in soup.findAll('div',{'id':dayindicator}):
                        for item2 in item1.findAll('a',{'class':'xbtn xbtn-default'}):
                            listschedule.append((item2.text).lower())
                    for item3 in soup.findAll('div',{'id':dayindicator}):
                        for item4 in item3.findAll('div',{'class':'col-md-9 col-sm-8 col-xs-12'}):
                            listtiming.append(item4.text)
                            listtimingsp=[k.replace("M", "M ".upper()) for k in listtiming]
                    for i in range(len(listschedule)):
                        combine.append(listschedule[i]+" "+listtimingsp[i])
                    if searchmovie_lower !="all": # If I want to seach this movie name:"
                        for j in combine:
                            if searchmovie_lower in j: #this is the filter condition :3
                                self.sender.sendMessage(j.title())
                    else: #No filter condition
                        for j in combine:
                                self.sender.sendMessage(j.title())
                    self.sender.sendMessage("-----------")
                    self.sender.sendMessage("-----------")
                self.sender.sendMessage("That's all folks! Enjoy watching!")
                self._count = 0
                
            elif "back" in daytext.lower(): #if daytext detects "back" in the input, or the user want to change the title of the movie s/he want to watch.
                dayindicator="Unavailable"
                self.sender.sendMessage("Which movie which do you want to watch? If you want to look all schedule, type 'All'.")
                self._count = 9
            else: # if the user is mistype or naughty, not input today or tomorrow, which assign dayindicator = unavailable.
                self.sender.sendMessage("Please indicate today or tomorrow.")
                self._count = 10
             




"""
explanation of the date system:
31 - 1, 3, 5, 7, 8, 10, 12
30 - 4, 6, 9, 11
29 - 2 if leap = 0
28 - 2 if leap != 0

if (year is not divisible by 4) then (it is a common year)
else if (year is not divisible by 100) then (it is a leap year)
else if (year is not divisible by 400) then (it is a common year)
else (it is a leap year)
"""

TOKEN = "286160223:AAGcnjI85AI_NanTyOq5AQ6byTxWx0gfiGQ" # get token from command-line

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=600),
])
bot.message_loop(run_forever='Listening ...')
