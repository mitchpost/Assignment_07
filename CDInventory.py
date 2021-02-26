#------------------------------#
#------------------------------------------#
# Title: Assignment07.py
# Desc: Pickles, I/O error Handling.
# Change Log: (Who, When, What)
# POST, 0800-FEB-15, Created File
# POST, 0900-FEB-15, pulled out code for functions and organized for task
# POST, 1100-FEB-15, assigned all code to defintions according to appropriate class
# POST, 1200-FEB-15, troubleshot nested code append
# POST, 1300-FEB-15, Tested code succesfully
# POST, 0815-FEB17, RE ORG FUNCTIONS/CLASS
# POST, 0900-FEB-24, Updated code accordigng to recomandations from grading
# POST, 1200-FEB-24, Added i/o handling 
# POST, 1400-FEB-24, Troubleshoot pickle functions - tested succesfully
#------------------------------------------#
#------------------------------#


# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = ('CDInventory.dat')  # data storage file
objFile = None  # file object
value1 = None # is this neccessary? for "def delete_cd(value1):" Do i have to none out variables

import pickle
# -- PROCESSING -- #
class DataProcessor:
    """Processing the data from input to Dict"""
    @staticmethod
    def input_append(lstTbl, strID, strTitle, stArtist): ##Added lstbl pass in per sugestions 
        """This function appends the information take from DataProcessor. input_user(strFileName, lstTbl)
        then uses it to append dicrRow
         Args:
            dicRow: dictionary row.
            Table (List of dicts)
         Returns:
             None
            
        """
        intID = int(strID)
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': stArtist}
        lstTbl.append(dicRow) 
        return lstTbl
    @staticmethod
    def delete_cd(lstTbl, id_to_remove): ## updated 'value one to id_to_remove'
        """ Deletion function added here to I/o class 
        
        Args:
            None.

        Returns:
            id_to_remove User input to select ID to be deleted 
            
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x
        User input is required to delete desired CD"""
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == id_to_remove:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        return lstTbl ## Returning list as precuation since updating list

# -- File Proccessing -- #
class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name taken from pickle.load this outputs the contents exactly as it was saved
        From program.
        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        try:
           with open(file_name, "rb+") as objFile:
            table = pickle.load(objFile)
            return table
        except:
                   print("\n\n\n***CDInventory.dat not found***\n\n\n")
                   
    @staticmethod
    def write_file(strFileName, lstTbl): # fixed typo 
        """ Additional file proccesing function to save file to .txt
        
        Function pickle plugin dump utility saving Lstbl to .dat file"""
        with open(strFileName, "wb+") as objFile:
            pickle.dump(lstTbl, objFile)
            
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
        
    @staticmethod
    def input_user():
        """User input taken then assigned to strID, strTitle, and stArtist
        Nested function Io.input_append used to take local variable then
        Appended to DICT list
        
        Args:
           IO.input_append(strID, strTitle, stArtist): Function used to take read and append local returns
            
        Returns:
            strID = input ('Enter ID: ')
            strTitle = input ('What is the CD\'s title? ')
            stArtist = input ('What is the Artist\'s name? ')  
        """
        while True:
            try:
                intID = int(input('Enter ID: ').strip())
                strTitle = input('What is the CD\'s title? ').strip()
                stArtist = input('What is the Artist\'s name? ').strip()
                break
            except ValueError:
                print("Invalid entry. ID must be integer")
        return intID, strTitle, stArtist

   #### When program starts, read in the currently saved Inventory (no change)
lstTbl = FileProcessor.read_file(strFileName, lstTbl)

##### start main loop ### (no change)
while True:
   
    IO.print_menu()
    strChoice = IO.menu_choice()
    if strChoice == 'x':
        break
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl = FileProcessor.read_file(strFileName, lstTbl) # assign lstbl back to main loop from return of function
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top (No Change)
    elif strChoice == 'a':  
        
        strID, strTitle, stArtist = IO.input_user()
        lstTbl = DataProcessor.input_append(lstTbl, strID, strTitle, stArtist) ## passed in lstbl this is update from recomendations 
        IO.show_inventory(lstTbl)

        continue  # start loop back at top.
    
    elif strChoice == 'i':
        IO.show_inventory(lstTbl) ## Calls for show function dispalying user inventory
        continue  # start loop back at top.
   
    elif strChoice == 'd':  
        try:
            intIDDel = int(input('Which ID would you like to delete? ').strip())
        except:
            print("\n\n\n\n****Invalid CD ID.. Please continue***\n\n\n\n")    
        IO.show_inventory(lstTbl) ## Calls for show function dispalying user inventory
        lstTbl = DataProcessor.delete_cd(lstTbl, intIDDel) ## Calls function to delete desired CD
        continue  # start loop back at top.
  
    elif strChoice == 's':
        IO.show_inventory(lstTbl) ## Calls for show function dispalying user inventory
        

        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()

        if strYesNo.lower() in ['yes', 'y']:
            FileProcessor.write_file(strFileName, lstTbl) ## Calls for to save inventory to target .txt file 

        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')

        continue  # start loop back at top.

    ### catch-all should not be possible, as user choice gets vetted in IO, but to be save (no change):
    else:
        print('General Error') 





