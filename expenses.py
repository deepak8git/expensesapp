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
from kivymd.uix.list import ThreeLineAvatarIconListItem,IconLeftWidget,IconRightWidget
#Window.size=(500,1000)

import sqlite3


screen ="""

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
                MDNavigationDrawerHeader:
                    title:"Expenses App"                    
                    title_font_size: "20sp"           
                    font_size: "16sp"                  
                    spacing:"4dp"
                    padding:"12dp",0,0,"32dp"  
        
<Expenses>:
    name:"expenses"
    on_enter: root.update_scroll_pos()
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
            on_focus: if self.focus: app.menu.open()

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
    MDLabel:
        text:"Expenses Screen"
        halign:"center"

    MDRectangleFlatButton:
        text:"First"
        pos_hint:{"center_x":0.5,"center_y":0.4}
        #on_press:root.manager.current="category"

<ExpensesView>:
    name:"expensesview"        

<CategoryView>:
    name:"categoryview"   
    
<ChartView>:
    name:"chartview"

"""

class Expenses(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
      
class Category(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        print("category")

class ExpensesView(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        print("expense view")

class CategoryView(Screen):
    pass
class ChartView(Screen):
    pass

class DatabaseHandler:

    def __init__(self):
        self.conn=sqlite3.connect("expensetodo.db")
        command="CREATE TABLE IF NOT EXISTS expensetable (id TEXT, categoryid TEXT, expensedate TEXT, expensetime TEXT, categoryname TEXT,itemname TEXT,expenseamount TEXT)"
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

class ExpenseApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_handler=DatabaseHandler()

        self.screen = Builder.load_string(screen)
        self.record_id=""
        self.amount_value=""
        self.item_value=""
        self.cat_value=""
        self.date_value=""
        self.time_value=""
        
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "icon": "git",
                "height": dp(56),
                "text": f"Item {i}",
                "on_release": lambda x=f"Item {i}": self.set_item(x),
            } for i in range(5)]
        
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.screen_manager.get_screen("expenses").ids.categoryid,            
            items=menu_items,
            position="bottom",
            width_mult=2,
        )

        self.menu.bind(on_dismiss=self.on_menu_dismiss)
        self.date_dialog = MDDatePicker()
        self.date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)

    def set_item(self, text__item):
        self.screen.ids.screen_manager.get_screen("expenses").ids.categoryid.focus=False
        self.screen.ids.screen_manager.get_screen("expenses").ids.categoryid.text = text__item
        self.menu.dismiss()
        
    def on_menu_dismiss(self, instance):
        self.screen.ids.screen_manager.get_screen("expenses").ids.categoryid.focus=False        

    def change_title(self):
        current_screen = self.screen.ids.screen_manager.current_screen
        title_text = current_screen.name.replace('_', ' ').capitalize() if current_screen else "Expenses"
        self.screen.ids.appbarid.title =f"Expenses App ({title_text})" 
        boxlayout = current_screen.ids.firstlayout
        print(boxlayout)

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
        return  self.screen
    
    def on_start(self):
        self.change_title()
        self.load_records()

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
            self.db_handler.insert_record(item_id,0,self.date_value,self.time_value,self.cat_value,self.item_value,self.amount_value)
        
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
        
        self.clear_controls()    

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



if __name__=="__main__":
    ExpenseApp().run()