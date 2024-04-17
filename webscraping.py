# General Conference Webscraping
# For this project you are going to web scrape the talks from a recent
# general conference of The Church of Jesus Christ of Latter-day Saints which you can find here.
# For those that aren’t members, general conference is when leaders of the church give talks
# (speeches basically) about different topics to the whole world. Talks have a title and a speaker,
# and typically there are many references to books of scripture (among other things). Your group’s
# task is to scrape the name of the talk, the speaker, as well as the number of references to each
# book of scripture in each talk.

# Group Members: Ryan Briggs, Joshua Gillespie, and Ben Haggard MW 12:30 - 1:45 class

# importing required libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlalchemy
from sqlalchemy import sql
import matplotlib.pyplot as plt

# Create a connection to the database
database_name = "is303"
db_user = "is303user"
db_password = "12345classpassword"
db_host = "localhost" #this just means the database is stored on your own computer
db_port = "5432" # default setting

engine = sqlalchemy.create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{database_name}')

# fake data entry TESTING PURPOSES -----------------------------------------------------------------------------------------------
# fake_data = {
#     'Speaker_Name': ['John Smith', 'Emily Johnson', 'David Williams', 'Sarah Brown', 'Michael Davis'],
#     'Talk_Name': ['Faith and Doubt', 'Hope in Adversity', 'Love and Forgiveness', 'Service and Sacrifice', 'Courage and Resilience'],
#     'Kicker': ['Inspiring Message', 'Powerful Reminder', 'Uplifting Story', 'Heartfelt Testimony', 'Motivational Speech'],
#     'Matthew': [1, 5, 2, 6, 0],
#     'Mark': [6, 8, 4, 7, 0],
#     'Luke': [0, 7, 0, 6, 1],
#     'John': [5, 6, 7, 8, 0],
#     'Acts': [1, 0, 0, 0, 1],
#     # Add fake data for the rest of the books...
#     'Articles of Faith': [0, 1, 0, 0, 0]
# }

# df = pd.DataFrame(fake_data)
# insert_data = df.to_sql("general_conference", engine, if_exists='replace', index=False) # reason to make it into a dataframe
# conn = engine.connect()
# conn.commit()
# conn.close()
# this is fake data for testing purposes delete before turning in
# END fake data entry TESTING PURPOSES -----------------------------------------------------------------------------------------------

# Part II Functions: 
def chart_all_talks(df):
    # filtered_dict = {key: value for key, value in dict.items() if value > 2}
    sum_val_df = df.drop(['Speaker_Name', 'Talk_Name', 'Kicker'], axis=1).sum()
    sum_val_df = sum_val_df[sum_val_df > 2] # filter out values less than 2
    plt.bar(sum_val_df.index, sum_val_df)
    plt.title('Standard Works Referenced in General Conference')
    plt.ylabel('Number of References')
    plt.show()

def chart_individual_talk(talk_id, df):
    talk_name = df.iloc[int(talk_id) - 1]['Talk_Name'] # gets the title value of the talk_id
    std_works = df.iloc[int(talk_id) - 1].drop(['Speaker_Name', 'Talk_Name', 'Kicker']) # drops the speaker name, talk name, and kicker
    std_works = std_works[std_works >= 1] # filter out values less than 2
    plt.bar(std_works.index, std_works) # (talk: x, talk row: y)
    plt.title(f'Standard Works Referenced in {talk_name}')
    plt.xlabel('Standard Works Books')
    plt.ylabel(f'Number of References in {talk_name}')
    return plt

# Dictionary
conference_dictionary = {"Speaker Name" : [], "Talk Name" : [], "Kicker" : []} # do we use this? - Ben
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


user_input = input("If you want to scrape data, enter 1. If you want to see summaries of stored data, enter 2. Enter any other value to exit the program: ")

if user_input == "1":
    # Part I
    # Step 1 (dropping sql query if exists)
    drop_table_query = sqlalchemy.text("drop table if exists general_conference;")
    conn = engine.connect()
    conn.execute(drop_table_query)
    conn.commit()
    conn.close()

    # Step 2
    # Creating requests and soup variables to get access to website
    response = requests.get("https://www.churchofjesuschrist.org/study/general-conference/2023/10?lang=eng ")
    soup = BeautifulSoup(response.content, "html.parser")
    talk_links = soup.find_all("li") # gets all <a> tags
    hrefs = [link.get("href") for link in talk_links]

    # Step 3
    # Create talk list and filter data
    talk_list = []
    for talks in talk_links:
        gc_talks = talks.get("href")
        if "Session" not in gc_talks:
            talk_list.append('https://www.churchofjesuschrist.org' + gc_talks)
            

    for gc_talks in talk_list:
        # Runs through requests every time the loop iterates
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
    general_conference_df.to_sql("general_conference", engine, if_exists= 'replace', index= False) # reason to make it into a dataframe

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


# Part II

elif user_input == "2":

    user_input2 = input('You selected to see summaries \nPress 1 for summaries of all talks \nPress 2 for summaries of an individual talk \nPress anything else to exit: ')
    if user_input2 not in ['1', '2']: # exit if not 1 or 2
        print('Exiting Program')
        exit()

    query = 'SELECT * FROM general_conference'
    output_df = pd.read_sql(query, engine)

    if user_input2 == '1': # all standard works with  > 2 references in general conference db
        chart_all_talks(output_df)

    elif user_input2 ==  '2': # display speaker and talk info
            print('\nThe following are the names of speakers and their talks \n')
            for row in output_df.iterrows(): # prints out id: speaker name - talk name
                print(f"{row[0] + 1}: {row[1]['Speaker_Name']} - {row[1]['Talk_Name']}")
        # 4
            user_input3 = input('\nEnter the number of the talk you want to see the summary of: ')
        # 5
            chart_individual_talk(user_input3, output_df).show()
        
else:
    print("Exiting Program")
    exit()
