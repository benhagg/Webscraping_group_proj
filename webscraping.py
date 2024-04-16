from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import sqlalchemy

# Part 1 _________________________________________________________________________________________________________
# General Conference Webscraping
# For this project you are going to web scrape the talks from a recent
# general conference of The Church of Jesus Christ of Latter-day Saints which you can find here.
# For those that aren’t members, general conference is when leaders of the church give talks
# (speeches basically) about different topics to the whole world. Talks have a title and a speaker,
# and typically there are many references to books of scripture (among other things). Your group’s
# task is to scrape the name of the talk, the speaker, as well as the number of references to each
# book of scripture in each talk.

# Group Members: Ryan Briggs, Joshua Gillespie, and Ben Haggard MW 12:30 - 1:45 class

from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlalchemy
from sqlalchemy import sql
# import matplotlib.pyplot as plot

# Create a connection to the database
database_name = "is303"
db_user = "is303user"
db_password = "12345classpassword"
db_host = "localhost" #this just means the database is stored on your own computer
db_port = "5432" # default setting

engine = sqlalchemy.create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{database_name}')

# PART I steps 1-2 (dropping sql query if exists) PUT INTO LOOP
drop_sql_query = sqlalchemy.text("drop table if exists general_conference;")
conn = engine.connect()
conn.execute(drop_sql_query)
conn.commit()
conn.close()

# DICTIONARY
conference_dictionary = {"Speaker Name" : [], "Talk Name" : [], "Kicker" : []}
standard_works_dict = {'Speaker_Name' : [], 'Talk_Name' : [], 'Kicker' : [],
'Matthew': [], 'Mark': [], 'Luke': [], 'John': [], 'Acts': [], 'Romans': [], 
'1 Corinthians': [], '2 Corinthians': [], 'Galatians': [], 'Ephesians': [],
'Philippians': [], 'Colossians': [], '1 Thessalonians': [], '2 Thessalonians': [],
'1 Timothy': [], '2 Timothy': [], 'Titus': [], 'Philemon': [], 'Hebrews': [],
'James': [], '1 Peter': [], '2 Peter': [], '1 John': [], '2 John': [], '3 John':
[], 'Jude': [], 'Revelation': [], 'Genesis': [], 'Exodus': [], 'Leviticus': [],
'Numbers': [], 'Deuteronomy': [], 'Joshua': [], 'Judges': [], 'Ruth': [], 
'1 Samuel': [], '2 Samuel': [], '1 Kings': [], '2 Kings': [], '1 Chronicles': [],
'2Chronicles': [], 'Ezra': [], 'Nehemiah': [], 'Esther': [], 'Job': [], 'Psalm': [],
'Proverbs': [], 'Ecclesiastes': [], 'Song of Solomon': [], 'Isaiah': [],
'Jeremiah': [], 'Lamentations': [], 'Ezekiel': [], 'Daniel': [], 'Hosea': [],
'Joel': [], 'Amos': [], 'Obadiah': [], 'Jonah': [], 'Micah': [], 'Nahum': [],
'Habakkuk': [], 'Zephaniah': [], 'Haggai': [], 'Zechariah': [], 'Malachi': [], 
'1 Nephi': [], '2 Nephi': [], 'Jacob': [], 'Enos': [], 'Jarom': [], 'Omni': [], 
'Wordsof Mormon': [], 'Mosiah': [], 'Alma': [], 'Helaman': [], '3 Nephi': [], '4 Nephi':
[], 'Mormon': [], 'Ether': [], 'Moroni': [], 'Doctrine and Covenants': [], 'Moses':
[], 'Abraham': [], 'Joseph Smith—Matthew': [], 'Joseph Smith—History': [],
'Articles of Faith': []}



# PART I steps 4-6
user_input = input("If you want to scrape data, enter 1. If you want to see summaries of stored data, enter 2. Enter any other value to exit the program: ")

if user_input == "1":
    # PART I steps 1-2 (dropping sql query if exists) PUT INTO LOOP
    drop_sql_query = sqlalchemy.text("drop table if exists general_conference;")
    conn = engine.connect()
    conn.execute(drop_sql_query)
    conn.commit()
    conn.close()

    # creating requests and soup variables to get access to website
    response = requests.get("https://www.churchofjesuschrist.org/study/general-conference/2023/10?lang=eng ")
    soup = BeautifulSoup(response.content, "html.parser")

    # extracting talk links
    talk_links = [link.get("href") for link in soup.find_all("a", class_="lumen-tile__link")]

    # talk list
    talk_list = []
    for talks in talk_links:
        gc_talks = talks.get("href")
        if "Session" not in gc_talks:
            talk_list.append('https://www.churchofjesuschrist.org' + gc_talks)
            

    for gc_talks in talk_list:
        # runs through requests every time the loop iterates
        print(f"Trying to scrape url: {gc_talks}")
        response = requests.get(gc_talks)
        specific_talk = BeautifulSoup(response.content, "html.parser") # parses the specific talks and setting up for eliminating session and sustaining
        print(gc_talks)
        # this is where if statement for preventing "sustaining" will go
        if "Sustain" in gc_talks:
            continue


        # REST OF CODE IS IN THE FOR LOOP

        # speakers name
        name_element = specific_talk.find("p", attrs= {"class" : "author-name"}).get_text()
        standard_works_dict["Speaker Name"].append(name_element.text.strip())
        print(name_element)

        # talk name (same formula as above)
        talk_name_element = specific_talk.find("h1", attrs= {"id" : "title1"}).get_text()
        standard_works_dict["Talk Name"].append(talk_name_element.text.strip()[3:])
        print(talk_name_element)

        # kicker (same formula as above)
        kicker_element = specific_talk.find("p", attrs= {"id" : "kicker1"}).get_text()
        standard_works_dict["Kicker"].append(kicker_element.text.strip())
        print(kicker_element)

        # counting references
        footnote_section = specific_talk.find('footer', attrs= {'class' : 'notes'})
        if footnote_section is not None:
            footnote_section.count(specific_talk.find('footer', attrs= {'class' : 'notes'}))
        else:
            continue

    general_conference_df = pd.DataFrame(standard_works_dict)
    general_conference_df.to_sql("books_practice", engine, if_exists= 'replace', index= False) # reason to make it into a dataframe

    # for url in specific_talk:

    #     print(f"requesting url: {url}")
    #     response = requests.get(url)
    #     specific_talk = BeautifulSoup(response.content, "html.parser")
    #     name_element = table_cells[0].get_text()
    #     talk_name_element = table_cells[4].get_text()
    #     kicker_element = specific_talk.get_text()

    #     general_conference_dictionary['name_element'].append(name_element)
    #     general_conference_dictionary['talk_name_element'].append(talk_name_element)
    #     general_conference_dictionary['kicker'].append(kicker_element)
    #     general_conference_dictionary['footnote_section'].append(footnote_section)

    # df_books_data = pd.DataFrame(general_conference_dictionary)
    # df_books_data.to_sql("books_practice", engine, if_exists= 'replace', index= False) # reason to make it into a dataframe
    print("You've saved the scraped data to your postgres database.")





# Part 2 _________________________________________________________________________________________________________
    def chart_all_talks(df):
        plt.plot(df.loc[id] == )
        plt.title('Standard Works Referenced in General Conference')
        plt.xlabel('Standard Works')
        plt.ylabel('Number of References')


    def chart_individual_talk(talk_id, df):
        talk_name = df.loc[df['id'] == talk_id, 'title']
        plt.plot(talk_name, df.lod[df['id'] == talk_id])
        plt.title(f'Standard Works Referenced in {talk_name}')
        plt.xlabel('Standard Works Books')
        plt.ylabel('Number of References')
        plt.show()


elif user_input == "2":
    user_input2 = input('You selected to see summaries \nPress 1 for summaries of all talks \nPress 2 for summaries of an individual talk \nPress anything else to exit')
    if user_input2 == 1:
        query = 'SELECT * FROM general_conference'
        output_df = pd.read_sql_query(query, engine)

    elif user_input2 ==  2:
            print('The following are the names of speakers and their talks')
            for row in output_df.iterrows():
                print(f"{row['id']}: {row['speaker']} - {row['title']}")
        # 4
            user_input3 = input('Enter the number of the talk you want to see the summary of: ')
        # 5
            chart_individual_talk(user_input3)





















if __name__ == '__main__':
    user_input = int(input("Enter 1 for Part 1 or 2 for Part 2: ")) # change the wording
    if user_input == 2:
        # 1
       
        # 2
        if user_input2 == 1:
            chart_all_talks()
        if user_input2 ==  2:
            print('The following are the names of speakers and their talks')
            for row in df.iterrows():
                print(f"{row['id']}: {row['speaker']} - {row['title']}")
        # 4
            user_input3 = input('Enter the number of the talk you want to see the summary of: ')
        # 5
            chart_individual_talk(user_input3)
