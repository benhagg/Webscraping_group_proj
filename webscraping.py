from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import sqlalchemy

# Part 1 _________________________________________________________________________________________________________




# Part 2 _________________________________________________________________________________________________________
query = 'SELECT * FROM general_conference'
df = pd.read_sql(query, engine)
def chart_all_talks():
    # matplotlib function to plot all talks
    pass


def chart_individual_talk(talk_id):
    # matplotlib function to plot individual talk
    pass



















if __name__ == '__main__':
    user_input = int(input("Enter 1 for Part 1 or 2 for Part 2: ")) # change the wording
    if user_input == 2:
        # 1
        user_input2 = input('You selected to see summaries \nPress 1 for summaries of all talks \nPress 2 for summaries of an indibidual talk \nPress anything else to exit')
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
