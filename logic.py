import sqlite3  
import random  


class CityGame:  
    def __init__(self, db_name='database.db'):  
        self.db_name = db_name  
        self.used_cities = set()  
        self.load_cities()  

    def load_cities(self):  
        self.conn = sqlite3.connect(self.db_name)  
        self.cursor = self.conn.cursor()  

    def get_city(self, last_city):  
        last_letter = last_city[-1].upper()  
        self.cursor.execute("SELECT name FROM cities WHERE name NOT IN (?) AND name LIKE ?",   
                            (tuple(self.used_cities), last_letter + '%'))  
        possible_cities = [row[0] for row in self.cursor.fetchall()]  

        if possible_cities:  
            chosen_city = random.choice(possible_cities)  
            self.used_cities.add(chosen_city)  
            return chosen_city  
        else:  
            return None   

    def close(self):  
        self.conn.close()