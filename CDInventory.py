#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# MKot, 2022-Nov-18, Modified the code, added functions
# MKot, 2022-Nov-24, Modifies code: added error handling, binary data storage
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object

# -- PROCESSING -- #
class DataProcessor:
    """Processing the data in the memory"""
    # TODone add functions for processing here
    def newCD_processing(ID, Title, Artist, table):
        """Function to process input data into list of dictionary.

        Args:
            ID, Title, Artist - new data, entered by the user that needs to be formated and saved 
            as list of dictionary in the memory.

        Returns:
            None.
        """
        intID = int(ID)
        dicRow = {'ID': intID, 'Title': Title, 'Artist': Artist}
        table.append(dicRow)
    
    def delete_data(del_val ,table):
        """Function to delete data from list of dictionary.

        Args:
            del_val - row that needs to be deleted,
            table - list of dictionary from where the data should be deleted.

        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == del_val:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        with open(file_name, 'rb') as objFile:
            loadFile = pickle.load(objFile)
            table.clear()
            for i in range(len(loadFile)):
                dicRow = {'ID':loadFile[i]['ID'], 'Title':loadFile[i]['Title'], 'Artist': loadFile[i]['Artist']}
                table.append(dicRow)

    @staticmethod
    def write_file(file_name, table):
        """Function to manage data ingestion from list of dictionaries to a file 

        Reads the data from file dictionary by table and save line by line into the file
        file_name.

        Args:
            file_name (string): name of file where data is saved to
            table (list of dict): 2D data structure (list of dicts) that holds the data that needs to be saved.

        Returns:
            None.
        """
        # TODone Add code here
        with open(file_name, 'wb') as objFile:
            pickle.dump(table, objFile)

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    # TODone add I/O functions as needed
    def add_data():
        """Gets user input new CD


        Args:
            none

        Returns:
            strID, strTitle, StArtist: string of the users input

        """
        while True:
           strID = input('Enter ID: ').strip()
           try: 
               strID = int(strID)
               break
           except:
               print('This is not an integer. Try again!')
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        return (strID, strTitle, stArtist)

# 1. When program starts, read in the currently saved Inventory


# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            try:
                FileProcessor.read_file(strFileName, lstTbl)
                IO.show_inventory(lstTbl)
            except:
                print('\nNo data has been saved yet. There is nothing to load.\n')
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        # TODone move IO code into function
        addID, addTitle, addArtist = IO.add_data()
        # 3.3.2 Add item to the table
        # TODone move processing code into function
        DataProcessor.newCD_processing(addID, addTitle, addArtist, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        while True:
            try:
                intIDDel = int(input('Which ID would you like to delete? ').strip())
                break
            except:
                print('\nPlease enter only integers. Try again!\n')
        # 3.5.2 search thru table and delete CD
        # TODone move processing code into function
        DataProcessor.delete_data(intIDDel, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            # TODone move processing code into function
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




