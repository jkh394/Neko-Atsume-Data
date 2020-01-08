# -*- coding: utf-8 -*-

import csv

def create_script():
    lines_written = 0
    
    try:
        in_file = open('Neko Atsume Data 1.13.0.csv', 'r')
    except:
        print("Neko Atsume Data 1.13.0.csv not found or could not be opened.")
    else:
        print("Starting to write out the script! Please wait...")
        
        out_sql_file = open('asg5_jkh394_neko_atsume_SQL.sql', 'w')
        
        out_sql_file.write("DROP TABLE IF EXISTS Item_Table;\n")
        out_sql_file.write("DROP TABLE IF EXISTS Food_Table;\n")
        out_sql_file.write("DROP TABLE IF EXISTS Cat_Table;\n")
    
        out_sql_file.write("\nCREATE TABLE Cat_Table (\n")
        out_sql_file.write("cat_name VARCHAR(20) NOT NULL,\n")
        out_sql_file.write("cat_power_level INT NULL,\n")
        out_sql_file.write("cat_regular TINYINT NULL,\n")
        out_sql_file.write("cat_fish_gift_factor INT NULL,\n")
        out_sql_file.write("PRIMARY KEY (cat_name));\n")
    
        out_sql_file.write("\nCREATE TABLE Food_Table (\n")
        out_sql_file.write("food_name VARCHAR(20) NOT NULL,\n")
        out_sql_file.write("food_preference INT NULL,\n")
        out_sql_file.write("food_cat_name VARCHAR(20) NULL,\n")
        out_sql_file.write("PRIMARY KEY (food_name, food_cat_name),\n")
        out_sql_file.write("CONSTRAINT food_cat_name FOREIGN KEY (food_cat_name) REFERENCES Cat_Table (cat_name));\n")
        
        out_sql_file.write("\nCREATE TABLE Item_Table (\n")
        out_sql_file.write("item_name VARCHAR(50) NOT NULL,\n")
        out_sql_file.write("item_preference INT NULL,\n")
        out_sql_file.write("item_cat_name VARCHAR(20) NULL,\n")
        out_sql_file.write("PRIMARY KEY (item_name, item_cat_name),\n")
        out_sql_file.write("CONSTRAINT item_cat_name FOREIGN KEY (item_cat_name) REFERENCES Cat_Table (cat_name));\n")
        
        reader = csv.reader(in_file, delimiter=',')
        out_csv_file = open('asg5_jkh394_transpose_neko_atsume.csv', 'w')
        
        array = []
        for line in reader:
            array.append(line)
        
        for i in range(len(array[0])):
            for j in range(len(array)):
                if (j == len(array)-1):
                    out_csv_file.write(array[j][i])
                else:    
                    out_csv_file.write(array[j][i] + ",")
            out_csv_file.write("\n")
                
        in_file.close()
        out_csv_file.close()
        
    try:
        in_file2 = open('asg5_jkh394_transpose_neko_atsume.csv', 'r')
    except:
        print("asg5_jkh394_transpose_neko_atsume.csv not found or could not be opened.")
    else:
        reader2 = csv.reader(in_file2, delimiter=',')
        
        cat_counter = 0
        cat_name = []
        cat_power_level = []
        cat_regular = []
        cat_fish_gift_factor = []
        
        food_counter = 0
        food_name = []
        food_preference = []
        food_index = []
        
        item_counter = 0
        item_name = []
        item_preference = []
        item_index = []
        
        for line in reader2:
            if cat_counter > 1:
                cat_name.append(line[0])
                cat_power_level.append(line[2])
                cat_regular.append(line[3])
                cat_fish_gift_factor.append(line[4])
            cat_counter += 1
            
            if food_counter < 1:
                for item in line:
                    if "Food:" in item:
                        food_name.append(item.replace("Food: ", ""))
                        food_index.append(line.index(item))           
            elif food_counter > 1:  
                for index in food_index:
                    food_preference.append(line[index])
            food_counter += 1
            
            if item_counter < 1:
                for item in line:
                    if (line.index(item) > 27) & (item not in item_name):
                        item_name.append(item)
                        item_index.append(line.index(item))
            elif item_counter > 1:
                for index in item_index:
                    item_preference.append(line[index])        
            item_counter += 1
        
        out_sql_file.write("\n")
        #Insert data into Cat Table
        for cat in range(len(cat_name)):
            if cat_regular[cat] == "TRUE":
                out_sql_file.write("INSERT INTO Cat_Table VALUES ('" + cat_name[cat] + "'," + cat_power_level[cat] + ",1," + cat_fish_gift_factor[cat] + ");\n")
            else:
                out_sql_file.write("INSERT INTO Cat_Table VALUES ('" + cat_name[cat] + "'," + cat_power_level[cat] + ",0," + cat_fish_gift_factor[cat] + ");\n")
        
        out_sql_file.write("\n")
        #Insert data into Food Table
        for cat in range(len(cat_name)):
            for food in range(len(food_name)):
                out_sql_file.write("INSERT INTO Food_Table VALUES ('" + food_name[food] + "'," + food_preference[0] + ",'" + cat_name[cat] + "');\n")
                del food_preference[0]
        
        out_sql_file.write("\n")
        #Insert data into Item Table
        cat_counter = 0
        for cat in range(len(cat_name)):
            for item in range(len(item_name)):
                out_sql_file.write("INSERT INTO Item_Table VALUES ('" + item_name[item] + "'," + item_preference[0] + ",'" + cat_name[cat] + "');\n")
                del item_preference[0]
    
        in_file2.close()
        out_sql_file.close()
        print("Script writing finished! Thank you for waiting :D")
        print("Lines written: ", lines_written)
        
create_script()