import pandas as pd
from django.core.management.base import BaseCommand
import os
from shoppingwebsites.models import Users,Products,Orders,Order_Details,Shopping_Cart

# Custom command class for managing data import from an CSV file
class Command(BaseCommand):
    help='Load data from CSV file'  # Description of the command

    def handle(self, *args, **kwargs):
        # Constructing the file path to the CSV file
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'marketing_sample_for_walmart_com-ecommerce__20191201_20191231__30k_data.csv')
        absolute_file_path = os.path.abspath(file_path)  # Getting absolute path

        try:
            # Attempting to read the data from the CSVfile
            data_df = pd.read_csv(absolute_file_path,nrows=7000)  # Reading data
        except FileNotFoundError:  # Handling the case where the file is not found
            self.stderr.write(f"File not found at path: {absolute_file_path}")  
            return

        # Debugging output: print the column names from both sheets
        self.stdout.write("Data Columns: " + str(data_df.columns.tolist()))  
        
        object_to_create = []  
        filtered_df['Item Number'] = filtered_df['Item Number'].str.replace('', '99')
        for index,row in data_df.iterrows():
            object_to_create.append(Products(
                product_name=row['Product Name'],
                description=row['Description'],
                product_url=row['Product Url'],
                price=row['List Price'],
                discount_price=row['Sale Price'],
                stock=row['Item Number'],
                category=row['Category'],
            ))
        

        self.stdout.write(self.style.SUCCESS('Successfully imported data from CSV file'))
