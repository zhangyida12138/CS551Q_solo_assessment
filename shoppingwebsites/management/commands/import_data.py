import pandas as pd
from django.core.management.base import BaseCommand
import os
import sys
print(sys.path)
# debug path
from shoppingwebsites.models import Users,Products,Orders,Order_Details,Shopping_Cart

# Custom command class for managing data import from an CSV file
class Command(BaseCommand):
    help='Load data from CSV file'  # Description of the command

    def handle(self, *args, **kwargs):
        # Constructing the file path to the CSV file
        self.import_Applicances()
        self.import_Car()
        self.import_Foods()
        self.import_Home()
        self.import_Pet()
        self.import_Sports()
        self.import_Makeup()

    def import_Applicances(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'All Appliances.csv')
        absolute_file_path = os.path.abspath(file_path)  # Getting absolute path
        
        try:
            data_df = pd.read_csv(absolute_file_path, nrows=2000)
        except FileNotFoundError:
            self.stderr.write(f"File not found at path: {absolute_file_path}")
            return
        except pd.errors.ParserError:
            self.stderr.write(f"Error parsing the file at path: {absolute_file_path}")
            return
        except Exception as e:
            self.stderr.write(f"An unexpected error occurred: {str(e)}")
            return

        # Debugging output: print the column names from both sheets
        self.stdout.write("Data Columns: " + str(data_df.columns.tolist()))  
        
        object_to_create = []  
        # Check 'Item Number' and replace non-integer values with 99
        # 1. Filter out rows where no_of_ratings or ratings is not a number or is 0
        data_df = data_df[pd.to_numeric(data_df['no_of_ratings'], errors='coerce').notnull()]
        # This function attempts to convert the no_of_ratings column of data_df into a number. If the conversion encounters an error (for example, if some of the values in the column are text), instead of throwing an error, it sets those values that cannot be converted to NaN (i.e., not a number). This is achieved through the errors='coerce' parameter.
        # This method returns a Boolean sequence. For non-NaN elements in the original sequence, it returns True; for NaN elements, it returns False.
        data_df = data_df[data_df['no_of_ratings'] != 0]
        # This part of the code uses the boolean sequence generated above to filter data_df. Only rows where no_of_ratings can be successfully converted to numbers (that is, rows where notnull() is True) will be retained.

        data_df = data_df[pd.to_numeric(data_df['ratings'], errors='coerce').notnull()]
        data_df = data_df[data_df['ratings'] != 0]

        # 2. Extract the numbers in actual_price and discount_price
        data_df['actual_price'] = data_df['actual_price'].replace('[^\d.]', '', regex=True).astype(float)
        data_df['discount_price'] = data_df['discount_price'].replace('[^\d.]', '', regex=True).astype(float)

        # 3. Delete any other data with empty items
        data_df = data_df.dropna()

        for index,row in data_df.iterrows():
            object_to_create.append(Products(
                product_name=row['name'],
                description=f"This product is {row['name']}, and sold by this shopping websites.",
                product_url=row['image'],
                price=row['actual_price'],
                discount_price=row['discount_price'],
                stock=999,
                category=row['main_category'],
                no_of_ratings=row['no_of_ratings'],
            ))
        
        # Bulk create to optimize database insertions, assuming all entries are valid
        Products.objects.bulk_create(object_to_create)

        self.stdout.write(self.style.SUCCESS('Successfully imported data from CSV file'))

    def import_Car(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'All Car and Motorbike Products.csv')
        absolute_file_path = os.path.abspath(file_path)  # Getting absolute path

        try:
            # Attempting to read the data from the CSVfile
            data_df = pd.read_csv(absolute_file_path)  # Reading data
        except FileNotFoundError:
            self.stderr.write(f"File not found at path: {absolute_file_path}")
            return
        except pd.errors.ParserError:
            self.stderr.write(f"Error parsing the file at path: {absolute_file_path}")
            return
        except Exception as e:
            self.stderr.write(f"An unexpected error occurred: {str(e)}")
            return

        # Debugging output: print the column names from both sheets
        self.stdout.write("Data Columns: " + str(data_df.columns.tolist())) 

        object_to_create = []
        # Check 'Item Number' and replace non-integer values with 99
        # 1. Filter out rows where no_of_ratings or ratings is not a number or is 0
        data_df = data_df[pd.to_numeric(data_df['no_of_ratings'], errors='coerce').notnull()]
        # This function attempts to convert the no_of_ratings column of data_df into a number. If the conversion encounters an error (for example, if some of the values in the column are text), instead of throwing an error, it sets those values that cannot be converted to NaN (i.e., not a number). This is achieved through the errors='coerce' parameter.
        # This method returns a Boolean sequence. For non-NaN elements in the original sequence, it returns True; for NaN elements, it returns False.
        data_df = data_df[data_df['no_of_ratings'] != 0]
        # This part of the code uses the boolean sequence generated above to filter data_df. Only rows where no_of_ratings can be successfully converted to numbers (that is, rows where notnull() is True) will be retained.

        data_df = data_df[pd.to_numeric(data_df['ratings'], errors='coerce').notnull()]
        data_df = data_df[data_df['ratings'] != 0]

        # 2. Extract the numbers in actual_price and discount_price
        data_df['actual_price'] = data_df['actual_price'].replace('[^\d.]', '', regex=True).astype(float)
        data_df['discount_price'] = data_df['discount_price'].replace('[^\d.]', '', regex=True).astype(float)

        # 3. Delete any other data with empty items
        data_df = data_df.dropna()

        for index,row in data_df.iterrows():
            object_to_create.append(Products(
                product_name=row['name'],
                description=f"This product is {row['name']}, and sold by this shopping websites.",
                product_url=row['image'],
                price=row['actual_price'],
                discount_price=row['discount_price'],
                stock=999,
                category=row['main_category'],
                no_of_ratings=row['no_of_ratings'],
            ))
        
        # Bulk create to optimize database insertions, assuming all entries are valid
        Products.objects.bulk_create(object_to_create)

        self.stdout.write(self.style.SUCCESS('Successfully imported data from CSV file'))


    def import_Foods(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'All Grocery and Gourmet Foods.csv')
        absolute_file_path = os.path.abspath(file_path)  # Getting absolute path

        try:
            # Attempting to read the data from the CSVfile
            data_df = pd.read_csv(absolute_file_path)  # Reading data
        except FileNotFoundError:
            self.stderr.write(f"File not found at path: {absolute_file_path}")
            return
        except pd.errors.ParserError:
            self.stderr.write(f"Error parsing the file at path: {absolute_file_path}")
            return
        except Exception as e:
            self.stderr.write(f"An unexpected error occurred: {str(e)}")
            return

        # Debugging output: print the column names from both sheets
        self.stdout.write("Data Columns: " + str(data_df.columns.tolist())) 

        object_to_create = []
        # Check 'Item Number' and replace non-integer values with 99
        # 1. Filter out rows where no_of_ratings or ratings is not a number or is 0
        data_df = data_df[pd.to_numeric(data_df['no_of_ratings'], errors='coerce').notnull()]
        # This function attempts to convert the no_of_ratings column of data_df into a number. If the conversion encounters an error (for example, if some of the values in the column are text), instead of throwing an error, it sets those values that cannot be converted to NaN (i.e., not a number). This is achieved through the errors='coerce' parameter.
        # This method returns a Boolean sequence. For non-NaN elements in the original sequence, it returns True; for NaN elements, it returns False.
        data_df = data_df[data_df['no_of_ratings'] != 0]
        # This part of the code uses the boolean sequence generated above to filter data_df. Only rows where no_of_ratings can be successfully converted to numbers (that is, rows where notnull() is True) will be retained.

        data_df = data_df[pd.to_numeric(data_df['ratings'], errors='coerce').notnull()]
        data_df = data_df[data_df['ratings'] != 0]

        # 2. Extract the numbers in actual_price and discount_price
        data_df['actual_price'] = data_df['actual_price'].replace('[^\d.]', '', regex=True).astype(float)
        data_df['discount_price'] = data_df['discount_price'].replace('[^\d.]', '', regex=True).astype(float)

        # 3. Delete any other data with empty items
        data_df = data_df.dropna()

        for index,row in data_df.iterrows():
            object_to_create.append(Products(
                product_name=row['name'],
                description=f"This product is {row['name']}, and sold by this shopping websites.",
                product_url=row['image'],
                price=row['actual_price'],
                discount_price=row['discount_price'],
                stock=999,
                category=row['main_category'],
                no_of_ratings=row['no_of_ratings'],
            ))
        
        # Bulk create to optimize database insertions, assuming all entries are valid
        Products.objects.bulk_create(object_to_create)

        self.stdout.write(self.style.SUCCESS('Successfully imported data from CSV file'))


    def import_Home(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'All Home and Kitchen.csv')
        absolute_file_path = os.path.abspath(file_path)  # Getting absolute path

        try:
            # Attempting to read the data from the CSVfile
            data_df = pd.read_csv(absolute_file_path)  # Reading data
        except FileNotFoundError:
            self.stderr.write(f"File not found at path: {absolute_file_path}")
            return
        except pd.errors.ParserError:
            self.stderr.write(f"Error parsing the file at path: {absolute_file_path}")
            return
        except Exception as e:
            self.stderr.write(f"An unexpected error occurred: {str(e)}")
            return

        # Debugging output: print the column names from both sheets
        self.stdout.write("Data Columns: " + str(data_df.columns.tolist()))  

        object_to_create = []           
        # Check 'Item Number' and replace non-integer values with 99
        # 1. Filter out rows where no_of_ratings or ratings is not a number or is 0
        data_df = data_df[pd.to_numeric(data_df['no_of_ratings'], errors='coerce').notnull()]
        # This function attempts to convert the no_of_ratings column of data_df into a number. If the conversion encounters an error (for example, if some of the values in the column are text), instead of throwing an error, it sets those values that cannot be converted to NaN (i.e., not a number). This is achieved through the errors='coerce' parameter.
        # This method returns a Boolean sequence. For non-NaN elements in the original sequence, it returns True; for NaN elements, it returns False.
        data_df = data_df[data_df['no_of_ratings'] != 0]
        # This part of the code uses the boolean sequence generated above to filter data_df. Only rows where no_of_ratings can be successfully converted to numbers (that is, rows where notnull() is True) will be retained.

        data_df = data_df[pd.to_numeric(data_df['ratings'], errors='coerce').notnull()]
        data_df = data_df[data_df['ratings'] != 0]

        # 2. Extract the numbers in actual_price and discount_price
        data_df['actual_price'] = data_df['actual_price'].replace('[^\d.]', '', regex=True).astype(float)
        data_df['discount_price'] = data_df['discount_price'].replace('[^\d.]', '', regex=True).astype(float)

        # 3. Delete any other data with empty items
        data_df = data_df.dropna()

        for index,row in data_df.iterrows():
            object_to_create.append(Products(
                product_name=row['name'],
                description=f"This product is {row['name']}, and sold by this shopping websites.",
                product_url=row['image'],
                price=row['actual_price'],
                discount_price=row['discount_price'],
                stock=999,
                category=row['main_category'],
                no_of_ratings=row['no_of_ratings'],
            ))
        
        # Bulk create to optimize database insertions, assuming all entries are valid
        Products.objects.bulk_create(object_to_create)

        self.stdout.write(self.style.SUCCESS('Successfully imported data from CSV file'))

    
    def import_Makeup(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'Make-up.csv')
        absolute_file_path = os.path.abspath(file_path)  # Getting absolute path

        try:
            # Attempting to read the data from the CSVfile
            data_df = pd.read_csv(absolute_file_path)  # Reading data
        except FileNotFoundError:
            self.stderr.write(f"File not found at path: {absolute_file_path}")
            return
        except pd.errors.ParserError:
            self.stderr.write(f"Error parsing the file at path: {absolute_file_path}")
            return
        except Exception as e:
            self.stderr.write(f"An unexpected error occurred: {str(e)}")
            return

        # Debugging output: print the column names from both sheets
        self.stdout.write("Data Columns: " + str(data_df.columns.tolist()))  

        object_to_create = []           
        # Check 'Item Number' and replace non-integer values with 99
        # 1. Filter out rows where no_of_ratings or ratings is not a number or is 0
        data_df = data_df[pd.to_numeric(data_df['no_of_ratings'], errors='coerce').notnull()]
        # This function attempts to convert the no_of_ratings column of data_df into a number. If the conversion encounters an error (for example, if some of the values in the column are text), instead of throwing an error, it sets those values that cannot be converted to NaN (i.e., not a number). This is achieved through the errors='coerce' parameter.
        # This method returns a Boolean sequence. For non-NaN elements in the original sequence, it returns True; for NaN elements, it returns False.
        data_df = data_df[data_df['no_of_ratings'] != 0]
        # This part of the code uses the boolean sequence generated above to filter data_df. Only rows where no_of_ratings can be successfully converted to numbers (that is, rows where notnull() is True) will be retained.

        data_df = data_df[pd.to_numeric(data_df['ratings'], errors='coerce').notnull()]
        data_df = data_df[data_df['ratings'] != 0]

        # 2. Extract the numbers in actual_price and discount_price
        data_df['actual_price'] = data_df['actual_price'].replace('[^\d.]', '', regex=True).astype(float)
        data_df['discount_price'] = data_df['discount_price'].replace('[^\d.]', '', regex=True).astype(float)

        # 3. Delete any other data with empty items
        data_df = data_df.dropna()

        for index,row in data_df.iterrows():
            object_to_create.append(Products(
                product_name=row['name'],
                description=f"This product is {row['name']}, and sold by this shopping websites.",
                product_url=row['image'],
                price=row['actual_price'],
                discount_price=row['discount_price'],
                stock=999,
                category=row['main_category'],
                no_of_ratings=row['no_of_ratings'],
            ))
        
        # Bulk create to optimize database insertions, assuming all entries are valid
        Products.objects.bulk_create(object_to_create)

        self.stdout.write(self.style.SUCCESS('Successfully imported data from CSV file'))


    def import_Sports(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'All Sports Fitness and Outdoors.csv')
        absolute_file_path = os.path.abspath(file_path)  # Getting absolute path

        try:
            # Attempting to read the data from the CSVfile
            data_df = pd.read_csv(absolute_file_path)  # Reading data
        except FileNotFoundError:
            self.stderr.write(f"File not found at path: {absolute_file_path}")
            return
        except pd.errors.ParserError:
            self.stderr.write(f"Error parsing the file at path: {absolute_file_path}")
            return
        except Exception as e:
            self.stderr.write(f"An unexpected error occurred: {str(e)}")
            return

        # Debugging output: print the column names from both sheets
        self.stdout.write("Data Columns: " + str(data_df.columns.tolist()))  

        object_to_create = []           
        pass

    def import_Pet(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'All Pet Supplies.csv')
        absolute_file_path = os.path.abspath(file_path)  # Getting absolute path

        try:
            # Attempting to read the data from the CSVfile
            data_df = pd.read_csv(absolute_file_path)  # Reading data
        except FileNotFoundError:
            self.stderr.write(f"File not found at path: {absolute_file_path}")
            return
        except pd.errors.ParserError:
            self.stderr.write(f"Error parsing the file at path: {absolute_file_path}")
            return
        except Exception as e:
            self.stderr.write(f"An unexpected error occurred: {str(e)}")
            return

        # Debugging output: print the column names from both sheets
        self.stdout.write("Data Columns: " + str(data_df.columns.tolist()))  

        object_to_create = []           
        # Check 'Item Number' and replace non-integer values with 99
        # 1. Filter out rows where no_of_ratings or ratings is not a number or is 0
        data_df = data_df[pd.to_numeric(data_df['no_of_ratings'], errors='coerce').notnull()]
        # This function attempts to convert the no_of_ratings column of data_df into a number. If the conversion encounters an error (for example, if some of the values in the column are text), instead of throwing an error, it sets those values that cannot be converted to NaN (i.e., not a number). This is achieved through the errors='coerce' parameter.
        # This method returns a Boolean sequence. For non-NaN elements in the original sequence, it returns True; for NaN elements, it returns False.
        data_df = data_df[data_df['no_of_ratings'] != 0]
        # This part of the code uses the boolean sequence generated above to filter data_df. Only rows where no_of_ratings can be successfully converted to numbers (that is, rows where notnull() is True) will be retained.

        data_df = data_df[pd.to_numeric(data_df['ratings'], errors='coerce').notnull()]
        data_df = data_df[data_df['ratings'] != 0]

        # 2. Extract the numbers in actual_price and discount_price
        data_df['actual_price'] = data_df['actual_price'].replace('[^\d.]', '', regex=True).astype(float)
        data_df['discount_price'] = data_df['discount_price'].replace('[^\d.]', '', regex=True).astype(float)

        # 3. Delete any other data with empty items
        data_df = data_df.dropna()

        for index,row in data_df.iterrows():
            object_to_create.append(Products(
                product_name=row['name'],
                description=f"This product is {row['name']}, and sold by this shopping websites.",
                product_url=row['image'],
                price=row['actual_price'],
                discount_price=row['discount_price'],
                stock=999,
                category=row['main_category'],
                no_of_ratings=row['no_of_ratings'],
            ))
        
        # Bulk create to optimize database insertions, assuming all entries are valid
        Products.objects.bulk_create(object_to_create)

        self.stdout.write(self.style.SUCCESS('Successfully imported data from CSV file'))
