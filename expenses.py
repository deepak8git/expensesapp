from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton
from kivy.core.window import Window
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.uix.pickers import MDDatePicker
from datetime import datetime
import uuid
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.list import ThreeLineAvatarIconListItem,IconLeftWidget,IconRightWidget,OneLineAvatarIconListItem
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
#Window.size=(500,1000)

import sqlite3


screen ="""
<DrawerClickableItem@MDNavigationDrawerItem>
    padding_y: "8dp"
MDScreen:
    MDNavigationLayout:
        MDScreenManager:
            MDScreen:
                MDTopAppBar:
                    id:appbarid
                    title: "Expenses App (Expenses)"
                    left_action_items:[["menu",lambda x:nav_drawer.set_state("open")]]
                    pos_hint:{"top":1}
                    elevation:1

        ScreenManager:
            id:screen_manager
            on_current: app.change_title()
            Expenses:
            Category:
            ExpensesView:
            CategoryView:
            ChartView:

        MDNavigationDrawer:
            id:nav_drawer   

            MDNavigationDrawerMenu:
                padding: "10dp", "10dp"
                MDNavigationDrawerHeader:
                    title:"Expenses App"                    
                    title_font_size: "20sp"           
                    font_size: "16sp"                  
                    spacing:"4dp"
                    padding:"12dp",0,0,"32dp"  

                
                MDNavigationDrawerLabel:
                    text:"Menu"

                DrawerClickableItem:
                    icon:"wallet-outline"
                    text:"Expenses"
                    on_release:
                        app.root.ids.screen_manager.current = "expenses"
                        app.close_nav_drawer()
                        app.load_menu()

                DrawerClickableItem:
                    icon:"format-list-bulleted"
                    text:"Category"
                    on_release: 
                        app.root.ids.screen_manager.current = "category"
                        app.close_nav_drawer()

                DrawerClickableItem:
                    icon:"file-document-outline"
                    text:"Expenses View"
                    on_release:
                        app.root.ids.screen_manager.current = "expenseview"
                        app.close_nav_drawer()

                DrawerClickableItem:
                    icon:"folder"
                    text:"Category View"
                    on_release:
                        app.root.ids.screen_manager.current = "categoryview"
                        app.close_nav_drawer()

                DrawerClickableItem:
                    icon:"chart-areaspline"
                    text:"Chart View"
                    on_release:
                        app.root.ids.screen_manager.current = "chartview"
                        app.close_nav_drawer()
                
                MDSeparator:
                                               
               
                MDNavigationDrawerLabel:
                    text:"Settings"
                    padding: "12dp", "20dp", "0dp", "12dp"
                DrawerClickableItem:
                    icon:"cog-outline"
                    text:"Settings"
                DrawerClickableItem:
                    icon:"information-outline"
                    text:"About Me"

<Expenses>:
    name:"expenses" 
    id:expenses   
    MDBoxLayout:
        id:firstlayout
        orientation:"vertical"
        spacing:15
        padding:25
        adaptive_height:True
        pos_hint:{"top":0.86}
        

        MDBoxLayout:
            orientation: "horizontal"
            spacing: dp(10)

            MDTextField:
                id:datetimeid
                hint_text:"Date"
                mode:"fill"
                required:True 
                keyboard_mode: "managed"
                size_hint_x:0.6 
                on_focus: if self.focus:app.show_date_picker()

            MDTextField:
                id:timeid
                hint_text:"time"
                mode:"fill"
                required:True 
                size_hint_x:0.4 
                keyboard_mode: "managed"
            
        MDTextField:
            id:categoryid
            hint_text:"Category"            
            mode:"fill"
            required:True
            keyboard_mode: "managed"
            #on_focus: if self.focus: app.menu.open()

        MDTextField:
            id:itemnameid
            hint_text:"item"
            mode:"fill"
            required:True    

        MDTextField:
            id:amountid
            hint_text:"amount"
            mode:"fill"
            input_type:"number"
            required:True   

    MDSeparator:
        height: dp(1)
        pos_hint:{"top":0.64}

    MDBoxLayout:
        orientation:"horizontal"
        spacing:25
        padding:60
        adaptive_height:True
        pos_hint:{"top":0.65}

        MDRaisedButton:
            id:addbtnid
            text:"Add"
            size_hint_x:0.5
            on_release:app.add_new_record()

        MDRaisedButton:
            id:cancelbtnid
            text:"Cancel"
            size_hint_x:0.5
            on_release:app.clear_controls()

    MDSeparator:
        height: dp(1)
        pos_hint:{"top":0.56}

    MDBoxLayout:        
        padding:25        
        pos_hint:{"top":0.56}
        size_hint_y: None  # Set the height to None to allow manual adjustment
        height: dp(480) 

        MDScrollView:
            id: scroll_view           

            MDList:
                id:mylistid
                
                # TwoLineAvatarIconListItem:
                #     text: "Item 1"
                #     secondary_text: "Description for Item 1"
                #     icon: "star"
                #     ImageLeftWidget:
                #         source: "avatar1.png"
                    
<Category>:
    name:"category"  
    MDBoxLayout:    
        orientation:"vertical"
        pos_hint:{"top":0.94}
           
        MDBoxLayout:
            padding:10
            spacing:10
            pos_hint:{"y":0.95}
            size_hint_y:0.1
            
            MDTextField:
                id:catinput
                hint_text:"category"
                mode:"fill"
                required:True
                size_hint_x:0.6            
                
            MDRaisedButton:
                id:cataddbtnid
                text:"Add"
                on_release:app.add_new_category()
               
                
        MDBoxLayout:
            
            MDScrollView:
                MDList:
                    id:catlist                   
       

<ExpensesView>:
    name:"expenseview"                
    
<CategoryView>:
    name:"categoryview"   
   
    MDLabel:
        text:"Category Screen"
        halign:"center"

    MDRectangleFlatButton:
        text:"Category"
        pos_hint:{"center_x":0.5,"center_y":0.4}
           
<ChartView>:
    name:"chartview"
   
    MDLabel:
        text:"Chart View Screen"
        halign:"center"

    MDRectangleFlatButton:
        text:"ChartView"
        pos_hint:{"center_x":0.5,"center_y":0.4}
       
"""

class Expenses(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)      

  
class Category(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        print("category")

class ExpensesView(Screen):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)


        self.db_handler=ExpenseDatabaseHandler()
        self.cat_db_handler=CategoryDatabaseHandler()      
        self.cat_id=""    
        self.total_amount=0      
        
        self.text_field = MDTextField(id="textid",padding=10, mode="fill", hint_text="category", size_hint=(None, None), size=(300, 40))        
        self.ids['textid'] = self.text_field

        self.load_menu()
        self.ids['textid'].bind(focus=self.on_category_focus) 

        self.layout = MDBoxLayout(orientation='vertical',pos_hint={"top":0.88},padding=15,spacing=20,size_hint_y=None,height= dp(700))    
        self.data_table = self.create_data_table(self.cat_id)   

        self.layout.add_widget(self.text_field)
        self.layout.add_widget(self.data_table) 


        self.ids['textid'].bind(focus=self.on_category_focus)
        self.ids['textid'].bind(text=self.on_category_change)
        self.add_widget(self.layout) 

        self.total_label = MDLabel(text=f"Amount: {self.total_amount}", halign="right", size_hint_y=None, height=dp(40))
        self.layout.add_widget(self.total_label)
        
        
        # print(f'There are {len(self.ids.items())} id(s)')        
        # for key, widget in self.ids.items():
        #     if hasattr(widget, 'text'):
        #         print(f"ID: {key}, Text: {widget.text}")
        #     else:
        #         print(f"ID: {key}, Widget does not have 'text' attribute")   
        #print(self.ids['textid'].text)

    def on_category_change(self, instance, value):
        if value:
            category_id = self.get_category_id(value)
            self.layout.remove_widget(self.data_table)
            self.data_table = self.create_data_table(category_id)
            self.layout.add_widget(self.data_table)

    def get_category_id(self, category_name):
        categories = self.cat_db_handler.fetch_all_category()
        for category_id, name in categories:
            if name == category_name:
                return category_id
        return None
    
       
    def create_data_table(self,category_id):
        records = self.db_handler.fetch_all_record()
        
        if category_id:
            records = [record for record in records if record[1] == category_id]
            
        self.total_amount = sum(float(record[6]) for record in records)

        self.data_table = MDDataTable(
            size_hint=(1,0.75),
            #use_pagination=True,
            rows_num=100,
            check=False,
            column_data=[
                ("[size=18]Date", dp(15)),
                ("[size=18]Time", dp(14)),
                ("[size=18]Category", dp(18)),
                ("[size=18]Item", dp(17)),
                ("[size=18]Amount", dp(10))
            ],
            row_data=[
                (f"[size=18]{record[2]}", f"[size=18]{record[3]}", f"[size=18]{record[4]}", 
                 f"[size=18]{record[5]}", f"[size=18]{record[6]}") for record in records
            ]

            # column_data=[
            #     ("[size=30]Date", dp(15)),
            #     ("[size=30]Time", dp(14)),
            #     ("[size=30]Category", dp(18)),
            #     ("[size=30]Item", dp(17)),
            #     ("[size=30]Amount", dp(10))
            # ],
            # row_data=[
            #     (f"[size=30]{record[2]}", f"[size=30]{record[3]}", f"[size=30]{record[4]}", 
            #      f"[size=30]{record[5]}", f"[size=30]{record[6]}") for record in records
            # ]
        )
        return self.data_table

    def load_menu(self):
     
        categories = self.cat_db_handler.fetch_all_category()         
        menu_items = []
        for category_id, category_name in categories:
            menu_item = {
                "viewclass": "OneLineListItem",
                "icon": "git",
                "height": dp(56),
                "text": category_name,
                "on_release": lambda x=category_name,cat_id=category_id: self.set_item(x,cat_id),
            }
            menu_items.append(menu_item)      

        self.menu = MDDropdownMenu(
            caller=self.ids['textid'],            
            items=menu_items,
            position="bottom",
            width_mult=4,
        )

        self.menu.bind(on_dismiss=self.on_menu_dismiss)
      
    def set_item(self, text__item,cat_id):
        self.ids['textid'].focus=False
        self.ids['textid'].text = text__item
        self.cat_id=cat_id      
        self.menu.dismiss()

    def on_menu_dismiss(self, instance):
        self.ids['textid'].focus=False                   
            
    def on_category_focus(self,instance, value):   
        if value:       
            self.menu.open()    
       

class CategoryView(Screen):
    pass
class ChartView(Screen):
    pass

class ExpenseDatabaseHandler:

    def __init__(self):
        self.conn=sqlite3.connect("expensetodo.db")
        command="CREATE TABLE IF NOT EXISTS expensetable (id TEXT, categoryid TEXT, expensedate TEXT, expensetime TEXT, categoryname TEXT,itemname TEXT,expenseamount TEXT)"
        self.conn.execute(command)

        command="CREATE TABLE IF NOT EXISTS categorytable (categoryid TEXT, categoryname TEXT)"
        self.conn.execute(command)
        self.conn.commit() 
        #id,categoryid,expensedate,expensetime,categoryname,itemname,expenseamount

    def insert_record(self,item_id,categoryid,expensedate,expensetime,categoryname,itemname,expenseamount):
        self.conn.execute("INSERT INTO expensetable (id,categoryid,expensedate,expensetime,categoryname,itemname,expenseamount) VALUES (?,?,?,?,?,?,?)",(item_id,categoryid,expensedate,expensetime,categoryname,itemname,expenseamount))
        self.conn.commit()        
    
    def update_record(self, item_id,expensedate,expensetime,categoryname,itemname,expenseamount):        
        self.conn.execute("UPDATE expensetable SET expensedate=?,expensetime=?,categoryname=?,itemname=?,expenseamount=? WHERE id = ?", (expensedate,expensetime,categoryname,itemname,expenseamount, item_id))       
        self.conn.commit()

    def delete_record(self,item_id):
        self.conn.execute("DELETE FROM expensetable WHERE id = ?",(item_id,))
        self.conn.commit()

    def fetch_all_record(self):
        cursor=self.conn.execute("SELECT * FROM expensetable")
        records=cursor.fetchall()    
        return records

    def __del__(self):
        self.conn.close()

class CategoryDatabaseHandler:
    def __init__(self):       
        self.conn=sqlite3.connect("expensetodo.db")
        command="CREATE TABLE IF NOT EXISTS categorytable (categoryid TEXT, categoryname TEXT)"
        self.conn.execute(command)
        self.conn.commit() 
        #id,categoryid,expensedate,expensetime,categoryname,itemname,expenseamount

    def insert_category(self,categoryid,categoryname):
        self.conn.execute("INSERT INTO categorytable (categoryid,categoryname) VALUES (?,?)",(categoryid,categoryname))
        self.conn.commit()        
    
    def update_category(self,categoryid,categoryname):        
        self.conn.execute("UPDATE categorytable SET categoryname=? WHERE categoryid = ?", (categoryname, categoryid))       
        self.conn.commit()

    def delete_category(self,categoryid):
        self.conn.execute("DELETE FROM categorytable WHERE categoryid = ?",(categoryid,))
        self.conn.commit()

    def fetch_all_category(self):
        cursor=self.conn.execute("SELECT * FROM categorytable")
        records=cursor.fetchall()    
        return records

    def __del__(self):
        self.conn.close()

class ExpenseApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_handler=ExpenseDatabaseHandler()
        self.cat_db_handler=CategoryDatabaseHandler()
       
        self.screen = Builder.load_string(screen)
        self.record_id=""
        self.amount_value=""
        self.item_value=""
        self.cat_value=""
        self.date_value=""
        self.time_value=""
        self.cat_id=""        
        
        self.date_dialog = MDDatePicker()
        self.date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)     
        self.load_menu()  

        
        
    def load_menu(self):
     
        categories = self.cat_db_handler.fetch_all_category()         
        menu_items = []
        for category_id, category_name in categories:
            menu_item = {
                "viewclass": "OneLineListItem",
                "icon": "git",
                "height": dp(56),
                "text": category_name,
                "on_release": lambda x=category_name,cat_id=category_id: self.set_item(x,cat_id),
            }
            menu_items.append(menu_item)      

        self.menu = MDDropdownMenu(
            caller=self.screen.ids.screen_manager.get_screen("expenses").ids.categoryid,            
            items=menu_items,
            position="bottom",
            width_mult=4,
        )

        self.menu.bind(on_dismiss=self.on_menu_dismiss)
      
    def set_item(self, text__item,cat_id):
        self.screen.ids.screen_manager.get_screen("expenses").ids.categoryid.focus=False
        self.screen.ids.screen_manager.get_screen("expenses").ids.categoryid.text = text__item
        self.cat_id=cat_id
        self.menu.dismiss()

    def on_menu_dismiss(self, instance):
        self.screen.ids.screen_manager.get_screen("expenses").ids.categoryid.focus=False      
       
    def close_nav_drawer(self):
        self.root.ids.nav_drawer.set_state("close") 

    def change_title(self):
        current_screen = self.screen.ids.screen_manager.current_screen
        title_text = current_screen.name.replace('_', ' ').capitalize() if current_screen else "Expenses"
        self.screen.ids.appbarid.title =f"Expenses App ({title_text})"        

    # ************** Date Picker ***************
    def on_save(self, instance, value, date_range):
        self.screen.ids.screen_manager.get_screen("expenses").ids.datetimeid.text = value.strftime("%d") + "/" + value.strftime("%m") + "/" + value.strftime("%Y")
        current_time = datetime.now().strftime("%I:%M %p")
        self.screen.ids.screen_manager.get_screen("expenses").ids.timeid.text = current_time
        self.date_dialog.dismiss()

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
        self.date_dialog.dismiss()

    def show_date_picker(self):
        self.date_dialog.open()
        self.screen.ids.screen_manager.get_screen("expenses").ids.datetimeid.focus=False
        self.screen.ids.screen_manager.get_screen("expenses").ids.timeid.focus=False
    # *******************************************
    
    def build(self):
        #self.sc=Builder.load_string(screen)                
        return self.screen
    
    def on_start(self):
        self.change_title()
        self.load_records()
        self.load_category()   
        self.screen.ids.screen_manager.get_screen("expenses").ids.categoryid.bind(focus=self.on_category_focus)      

            
    def on_category_focus(self,instance, value):   
        if value:       
            self.menu.open()
        

    def clear_controls(self):
        self.screen.ids.screen_manager.get_screen("expenses").ids.categoryid.text = ""
        self.screen.ids.screen_manager.get_screen("expenses").ids.timeid.text =""
        self.screen.ids.screen_manager.get_screen("expenses").ids.datetimeid.text =""
        self.screen.ids.screen_manager.get_screen("expenses").ids.itemnameid.text =""
        self.screen.ids.screen_manager.get_screen("expenses").ids.amountid.text =""
        self.screen.ids.screen_manager.get_screen("expenses").ids.addbtnid.text ="Add"      

    def load_records(self):

        records=self.db_handler.fetch_all_record()
        mylist = self.screen.ids.screen_manager.get_screen("expenses").ids.mylistid 
        records.reverse()
        for row in records:
            ids=row[0]
            self.date_value=row[2]
            self.time_value=row[3]
            self.cat_value=row[4]
            self.item_value=row[5]
            self.amount_value=row[6]

            mylist.add_widget(
                ThreeLineAvatarIconListItem(
                    IconLeftWidget(
                        icon="pencil",                        
                        #on_release=lambda x: self.editbtn(item_id,datevalue,timevalue,catvalue,itemvalue,amountvalue)
                        on_release=lambda x,item_id=ids: self.editbtn(item_id)
                    ),
                    IconRightWidget(
                        icon="delete",
                        on_release=lambda x,item_id=ids:self.deletebtn(item_id)
                    ),
                    id=ids,
                    text=f"{self.amount_value} - {self.item_value}",
                    secondary_text=self.cat_value,
                    tertiary_text=f"{self.date_value} - {self.time_value}"
                ) 
            )        

    def add_new_record(self):

        if self.screen.ids.screen_manager.get_screen("expenses").ids.addbtnid.text=="Add":
            
            item_id=str(uuid.uuid4())         
            mylist = self.screen.ids.screen_manager.get_screen("expenses").ids.mylistid  # Accessing mylistid properly
            self.cat_value=str(self.screen.ids.screen_manager.get_screen("expenses").ids.categoryid.text)
            self.time_value=str(self.screen.ids.screen_manager.get_screen("expenses").ids.timeid.text )
            self.date_value=str(self.screen.ids.screen_manager.get_screen("expenses").ids.datetimeid.text )
            self.item_value=str(self.screen.ids.screen_manager.get_screen("expenses").ids.itemnameid.text)
            self.amount_value=str(self.screen.ids.screen_manager.get_screen("expenses").ids.amountid.text)

            if not all([self.cat_value, self.time_value, self.date_value, self.item_value, self.amount_value]):       
                return

            mylist.add_widget(
                
                ThreeLineAvatarIconListItem(
                    IconLeftWidget(
                        icon="pencil",                        
                        on_release=lambda x: self.editbtn(item_id)
                    ),
                    IconRightWidget(
                        icon="delete",
                        on_release=lambda x:self.deletebtn(item_id)
                    ),
                    id=item_id,
                    text=f"{self.amount_value} - {self.item_value}",
                    secondary_text=self.cat_value,
                    tertiary_text=f"{self.date_value} - {self.time_value}"
                ) 
            )  
 
            self.db_handler.insert_record(item_id,self.cat_id,self.date_value,self.time_value,self.cat_value,self.item_value,self.amount_value)
            mylist.clear_widgets()
            self.load_records()

        elif self.screen.ids.screen_manager.get_screen("expenses").ids.addbtnid.text=="Update":
    
            mylist = self.screen.ids.screen_manager.get_screen("expenses").ids.mylistid
            self.date_value=str(self.screen.ids.screen_manager.get_screen("expenses").ids.datetimeid.text )
            self.time_value=str(self.screen.ids.screen_manager.get_screen("expenses").ids.timeid.text )
            self.cat_value=str(self.screen.ids.screen_manager.get_screen("expenses").ids.categoryid.text)                      
            self.item_value=str(self.screen.ids.screen_manager.get_screen("expenses").ids.itemnameid.text)
            self.amount_value=str(self.screen.ids.screen_manager.get_screen("expenses").ids.amountid.text)

            for child in mylist.children:
                if child.id==self.record_id:
                    child.text=f"{self.amount_value} - {self.item_value}"
                    child.secondary_text=str(self.cat_value)
                    child.tertiary_text=f"{self.date_value} - {self.time_value}"
             
            self.db_handler.update_record(self.record_id,self.date_value,self.time_value,self.cat_value,self.item_value,self.amount_value)
        
        #self.clear_controls()    

    def deletebtn(self,dataid):
        
        mylist = self.screen.ids.screen_manager.get_screen("expenses").ids.mylistid
        for child in mylist.children:
            if child.id==dataid:             
                mylist.remove_widget(child) 
        self.db_handler.delete_record(dataid)

    def editbtn(self,item_id):
    
        mylist = self.screen.ids.screen_manager.get_screen("expenses").ids.mylistid
        for child in mylist.children:
            if child.id==item_id:
                self.amount_value,self.item_value = child.text.split("-")
                self.cat_value = child.secondary_text
                self.date_value,self.time_value= child.tertiary_text.split("-")

        self.record_id=item_id
        self.screen.ids.screen_manager.get_screen("expenses").ids.categoryid.text = self.cat_value.strip()
        self.screen.ids.screen_manager.get_screen("expenses").ids.timeid.text =self.time_value.strip()
        self.screen.ids.screen_manager.get_screen("expenses").ids.datetimeid.text =self.date_value.strip()
        self.screen.ids.screen_manager.get_screen("expenses").ids.itemnameid.text =self.item_value.strip()
        self.screen.ids.screen_manager.get_screen("expenses").ids.amountid.text =self.amount_value.strip()       
        self.screen.ids.screen_manager.get_screen("expenses").ids.addbtnid.text ="Update"  

    def add_new_category(self):

        if self.screen.ids.screen_manager.get_screen("category").ids.cataddbtnid.text=="Add":
            
            category_id=str(uuid.uuid4())         
            categorylist = self.screen.ids.screen_manager.get_screen("category").ids.catlist  # Accessing mylistid properly
            self.cat_value=str(self.screen.ids.screen_manager.get_screen("category").ids.catinput.text)          

            if not all([self.cat_value]):       
                return

            categorylist.add_widget(
                    
                OneLineAvatarIconListItem(
                    IconLeftWidget(
                        icon="pencil",                        
                        on_release=lambda x: self.editbtn(category_id)
                    ),
                    IconRightWidget(
                        icon="delete",
                        on_release=lambda x:self.deletebtn(category_id)
                    ),
                    id=category_id,
                    text=self.cat_value                    
                ) 
            )  
    
            self.cat_db_handler.insert_category(category_id,self.cat_value)

            categorylist.clear_widgets()
            self.load_category()
            

        elif self.screen.ids.screen_manager.get_screen("category").ids.cataddbtnid.text=="Update":
    
            categorylist = self.screen.ids.screen_manager.get_screen("category").ids.catlist
            self.cat_value=str(self.screen.ids.screen_manager.get_screen("category").ids.catinput.text)  

            for child in categorylist.children:
                if child.id==self.record_id:
                    child.text=self.cat_value                  
             
            self.cat_db_handler.update_category(self.record_id,self.cat_value)
        
        self.clear_category_controls()
            
    def load_category(self):
        records=self.cat_db_handler.fetch_all_category()
        categorylist = self.screen.ids.screen_manager.get_screen("category").ids.catlist 
        records.reverse()
        for row in records:
            category_id=row[0]           
            self.cat_value=row[1]           

            categorylist.add_widget(
                OneLineAvatarIconListItem(
                    IconLeftWidget(
                        icon="pencil",                        
                        #on_release=lambda x: self.editbtn(item_id,datevalue,timevalue,catvalue,itemvalue,amountvalue)
                        on_release=lambda x,item_id=category_id: self.edit_category(item_id)
                    ),
                    IconRightWidget(
                        icon="delete",
                        on_release=lambda x,item_id=category_id:self.delete_category(item_id)
                    ),
                    id=category_id,
                    text=self.cat_value   
                    
                ) 
            ) 

    def edit_category(self,category_id):
        categorylist = self.screen.ids.screen_manager.get_screen("category").ids.catlist 
        for child in categorylist.children:
            if child.id==category_id:                
                self.cat_value = child.text             

        self.record_id=category_id
        self.screen.ids.screen_manager.get_screen("category").ids.catinput.text = self.cat_value.strip()          
        self.screen.ids.screen_manager.get_screen("category").ids.cataddbtnid.text="Update"  

    def clear_category_controls(self):
        self.screen.ids.screen_manager.get_screen("category").ids.catinput.text = ""           

    def delete_category(self,category_id):
        categorylist = self.screen.ids.screen_manager.get_screen("category").ids.catlist 
        for child in categorylist.children:
            if child.id==category_id:             
                categorylist.remove_widget(child) 
        self.cat_db_handler.delete_category(category_id)


if __name__=="__main__":
    ExpenseApp().run()