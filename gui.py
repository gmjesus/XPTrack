from parent_page_class import *

#---------------------------------------------------
# Classes
#---------------------------------------------------

class StatsPage(Page):
    '''Statistics Page.'''

    def __init__(self,name,table,amount_list,year_list,month_list,day_list):
        # Constructor
        super().__init__()
        self.name = name
        self.table = table
        self.amount_list = amount_list
        self.year_list = year_list
        self.month_list = month_list
        self.day_list = day_list
        self.statsWindow()
        self.backButton()
        self.show()
     
    def statsWindow(self):
        # Display the stats window
        self.defaultWindow("XPT Statistics Page")
        title = self.defaultLabel(self.name + " Expenses Statistics",0,0)
        title.setStyleSheet("font-size: 20pt; font-weight: bold")
        title.setAlignment(Qt.AlignCenter)
        
        # Calculate the total amount spent
        date_list = []
        total = 0.00 
        for count,amount in enumerate(self.amount_list):
            total += amount
            
            # Convert dates in datetime and append to list
            date = datetime.strptime(str(self.year_list[count]) + str(self.month_list[count]) + str(self.day_list[count]),'%Y%m%d')
            date_list.append(date)
         
        oldest_date = min(date for date in date_list)
        newest_date = max(date for date in date_list)
        days_between = (newest_date - oldest_date).days

        # Calculate average daily, monthly, yearly spending
        avg_daily = round(total/(days_between+1),2)
        m_descr = y_descr = "Average"
        if(days_between >= 30):
            avg_monthly = round(total/((days_between/30.4167)+1),2)
        else:
            avg_monthly = round(avg_daily*30.4167,2)
            m_descr = "Projected"
        if(days_between >= 365):
            avg_yearly = round(total/((days_between/365)+1),2)
        else: 
            avg_yearly = round(avg_daily*365,2)
            y_descr = "Projected"
        
        totalLabel = self.defaultLabel("Total Spending on " + self.name + ": $" + str(total)+ "\nAverage Daily Spending: $"  + str(avg_daily) + \
                   "\n" + m_descr+ " Monthly Spending: $" + str(avg_monthly) + "\n" + y_descr + " Annual Spending: $" + str(avg_yearly),0,400)
        totalLabel.setStyleSheet("font-size: 16pt; font-weight: bold")
        totalLabel.adjustSize()
        totalLabel.setAlignment(Qt.AlignCenter)

    def lastWindow(self):
        # Navigate back to the input page
        self.w = InputPage(self.name)
        self.w.show()
        self.hide()

class InputPage(Page):
    '''Page for user to enter all their expenses in table'''
    def __init__(self,name):
        # Constructor
        super().__init__()
        self.name = name
        self.table = QTableWidget(self)
        self.currentRowCount = 0
        self.inputWindow()
        self.printTable()
        self.addButton()
        self.statsButton()
        self.backButton()
        self.show()

    def inputWindow(self):
        # Display the input page
        self.defaultWindow("XPT Input Page")
        label = self.defaultLabel(self.name + " Expenses",0,0)
        label.setStyleSheet("font-size: 20pt; font-weight: bold")
        label.adjustSize()
        label.setAlignment(Qt.AlignCenter)

    def printTable(self):
        # Display the user input table
        self.table.setStyleSheet("background-color: white; border: 1px solid black")
        self.table.setRowCount(1)
        self.table.setColumnCount(6)
        self.table.resize(922,800)
        self.table.move(0,50)
        
        font = QFont()
        font.setBold(True)
        font.setPointSize(11)
        columns = ["Description","Year (YYYY)","Month (MM)","Day (DD)","Payment Type","Amount ($)"]
        #Set up each of the table's columns
        for count, column in enumerate(columns):
            item = QTableWidgetItem()
            item.setText(column)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(0,count, item)
            self.table.item(0,count).setFont(font)
        
    def addButton(self):
        # Display the add a row button
        pushButton = self.defaultButton("+",922,85,24,"Add an item",78,50)
        pushButton.clicked.connect(self.addRow) 
    
    def addRow(self):
        # Add a row to the table
        self.currentRowCount += 1
        self.table.insertRow(self.currentRowCount)

    def statsButton(self):
        # Display the stats button
        pushButton = self.defaultButton("Statistics",440,850,16,"View your expenses stats",125,50)
        pushButton.clicked.connect(lambda: self.nextWindow(self.name,self.table))
       
    def nextWindow(self,name,table):
        # Navigate to the statistics page with valid input
        amount_list = []
        year_list = []
        month_list = []
        day_list = []
        for count in range(1,self.table.rowCount()):
            # Check for valid amount input 
            try:
                amount = float(self.table.item(count,5).text())
                amount_list.append(round(amount,2))
            except:
                self.errorMessage("Invalid Amount Input")
                return None

            # Check for valid year input
            try:
                year = int(self.table.item(count,1).text())
                assert year > 999 and year < 3000
                year_list.append(year)
            except:
                self.errorMessage("Invalid Year Input")
                return None

            # Check for valid month input
            try:
                month = int(self.table.item(count,2).text())
                assert month > 0 and month < 13
                month_list.append(month)
            except:
                self.errorMessage("Invalid Month Input")
                return None
            
            # Check for valid day input
            try:
                day = int(self.table.item(count,3).text())
                assert day > 0 and day < 32
                day_list.append(day)
            except:
                self.errorMessage("Invalid Day Input")
                return None

        # Check for complete input 
        if(amount_list == [] or year_list == [] or month_list == [] or day_list == []):
            self.errorMessage("No Input")
            return None

        # Navigate to the stats page
        self.w = StatsPage(name,table,amount_list,year_list,month_list,day_list)
        self.w.show()
        self.hide() 

    def lastWindow(self):
        # Navigate back to the main page
        self.w = MainPage()
        self.w.show()
        self.hide()
        
class MainPage(Page): 
    '''Main page for user to select their type of category.'''                        
    def __init__(self):
        # Constructor
        super().__init__()
        self.mainWindow()
        types_expenses = ["Education","Housing","Utilities","Gas","Food","Entertainment","Travel","Clothing","Other"]
        for y,expense in enumerate(types_expenses):
            self.expenseButton(expense,440,75+y*95)
        self.backButton() 
        self.show() 
    
    def mainWindow(self):
        # Display the main page
        self.defaultWindow("XPT Main Page")
        label = self.defaultLabel("Select Category:",0,0)
        label.setStyleSheet("font-size: 20pt; font-weight: bold")
        label.adjustSize()
        label.setAlignment(Qt.AlignCenter)
           
    def expenseButton(self,name,x,y):
        # Display the expense button
        pushButton = self.defaultButton(name,x,y,16,name +" Expenses",125,50)
        pushButton.clicked.connect(lambda: self.nextWindow(name))
    
    def lastWindow(self):
        # Naviagte back to the intro page
        self.w = IntroPage()
        self.w.show()
        self.hide()   

    def nextWindow(self,name):
        # Navigate to the input page
        self.w = InputPage(name)
        self.w.show()
        self.hide()

class LoginPage(Page):
    '''Login page with username and password.'''

    def __init__(self):
        # Constructor
        super().__init__()
        self.loginWindow()
        self.backButton()
        self.submitButton()
        self.show()
        
    def loginWindow(self):
        # Display the login page 
        self.defaultWindow("XPT Login Page")

        username = self.defaultLabel("Username:",300,400)
        username.setStyleSheet("font-size: 16pt; font-weight: bold")
        username.adjustSize()

        password = self.defaultLabel("Password:",300,450)
        password.setStyleSheet("font-size: 16pt; font-weight: bold")
        password.adjustSize()

        input1 = QLineEdit(self)
        input1.setStyleSheet("background-color: white")
        input1.move(475,405)

        input2 = QLineEdit(self)
        input2.setEchoMode(input2.Password)
        input2.setStyleSheet("background-color: white")
        input2.move(475,455)

    def submitButton(self):
        # Display the submit button
        pushButton = self.defaultButton("Continue",475,500,12,"Submit form",100,30)
        pushButton.clicked.connect(self.nextWindow) 

    def lastWindow(self):
        # Navigate back to the intro page
        self.w = IntroPage()
        self.w.show()
        self.hide()

    def nextWindow(self):  
        #Navigate to the main page                                
        self.w = MainPage()
        self.w.show()
        self.hide()

class RegisterPage(Page):
    '''Register page to create an account.'''

    def __init__(self):
        # Constructor
        super().__init__()
        self.registerWindow()
        self.submitButton()
        self.backButton()
        name = None
        username = None
        password = None
        self.show()
    
    def registerWindow(self):
        # Display the register page to create an account
        self.defaultWindow("XPT Register Page")

        name = self.defaultLabel("Name:",300,350)
        name.setStyleSheet("font-size: 16pt; font-weight: bold")
        name.adjustSize()

        username = self.defaultLabel("Username:",300,400)
        username.setStyleSheet("font-size: 16pt; font-weight: bold")
        username.adjustSize()

        password = self.defaultLabel("Password:",300,450)
        password.setStyleSheet("font-size: 16pt; font-weight: bold")
        password.adjustSize()

        input1 = QLineEdit(self)
        input1.setStyleSheet("background-color: white")
        input1.move(475,355)
        
        input2 = QLineEdit(self)
        input2.setStyleSheet("background-color: white")
        input2.move(475,405)

        input3 = QLineEdit(self)
        input3.setEchoMode(input3.Password)
        input3.setStyleSheet("background-color: white")
        input3.move(475,455)

    def submitButton(self):
        # Display the submit page
        pushButton = self.defaultButton("Continue",475,500,12,"Submit form",100,30)
        pushButton.clicked.connect(self.nextWindow) 

    def lastWindow(self):
        # Navigate back to the intro page
        self.w = IntroPage()
        self.w.show()
        self.hide()

    def nextWindow(self):              
        # Navigate to the main page 
        self.w = MainPage()
        self.w.show()
        self.hide()

class IntroPage(Page):
    '''Home Page.'''

    def __init__(self):
        # Constructor
        super().__init__()
        self.introWindow()  
        self.loginButton()
        self.registerButton()
        self.getStartedButton()
        self.show()
        
    def introWindow(self):
        # Display the intro page
        self.defaultWindow("XPT Welcome Page")
 
        title = self.defaultLabel("Welcome To XPTrack!",0,200)
        title.setStyleSheet("font-size: 30pt; font-weight: bold")
        title.adjustSize()
        title.setAlignment(Qt.AlignCenter)

        descr = self.defaultLabel("A financial management application to help track your expenses",0,300)
        descr.setStyleSheet("font-size: 17pt; font-style: italic")
        descr.adjustSize()
        descr.setAlignment(Qt.AlignCenter)

        name = self.defaultLabel("By: Jesus Garcia Moreno",0,650)
        name.setStyleSheet("font-size: 12pt")
        name.adjustSize()
        name.setAlignment(Qt.AlignCenter)

    def loginButton(self):
        # Display the login button
        pushButton = self.defaultButton("Login",440,400,14,"Login into XPTrack",125,50)
        pushButton.clicked.connect(self.loginWindow)
    
    def registerButton(self):
        # Display the register button
        pushButton = self.defaultButton("Register",440,462.5,14,"Register an Account",125,50)
        pushButton.clicked.connect(self.registerWindow) 
    
    def getStartedButton(self):
        # Display the continue button as a guest
        pushButton = self.defaultButton("Continue as Guest",440,525,14,"Start the Session",125,50)
        pushButton.clicked.connect(self.nextWindow)   
           
    def nextWindow(self):    
        # Navigate to the main page                              
        self.w = MainPage()
        self.w.show()
        self.hide()

    def loginWindow(self):
        # Navigate to the login page
        self.w = LoginPage()
        self.w.show()
        self.hide()

    def registerWindow(self):
        # Navigate to the register page
        self.w = RegisterPage()
        self.w.show()
        self.hide()

#---------------------------------------------------
# Main Code
#---------------------------------------------------

if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = IntroPage()
    sys.exit(app.exec_())
