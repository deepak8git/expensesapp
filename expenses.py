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
        pos_hint:{"top":0.92}

        MDTextField:
            id:datetimeid
            hint_text:"Date"
            mode:"fill"
            required:True    
            on_focus: app.show_date_picker()

        MDTextField:
            id:categoryid
            hint_text:"Category"
            mode:"fill"
            required:True 
            on_focus: if self.focus: app.menu.open()

        MDTextField:
            id:inputtodo
            hint_text:"item"
            mode:"fill"
            required:True    

        MDTextField:
            id:inputtodo
            hint_text:"amount"
            mode:"fill"
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
            text:"Add"
            size_hint_x:0.5

        MDRaisedButton:
            text:"Cancel"
            size_hint_x:0.5

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
                TwoLineAvatarIconListItem:
                    text: "Item 1"
                    secondary_text: "Description for Item 1"
                    icon: "star"
                    ImageLeftWidget:
                        source: "avatar1.png"
                TwoLineAvatarIconListItem:
                    text: "Item 2"
                    secondary_text: "Description for Item 2"
                    icon: "heart"
                    ImageLeftWidget:
                        source: "avatar2.png"
                TwoLineAvatarIconListItem:
                    text: "Item 3"
                    secondary_text: "Description for Item 3"
                    icon: "android"
                    ImageLeftWidget:
                        source: "avatar3.png"
                TwoLineAvatarIconListItem:
                    text: "Item 4"
                    secondary_text: "Description for Item 1"
                    icon: "star"
                    ImageLeftWidget:
                        source: "avatar1.png"
                TwoLineAvatarIconListItem:
                    text: "Item 5"
                    secondary_text: "Description for Item 2"
                    icon: "heart"
                    ImageLeftWidget:
                        source: "avatar2.png"
                TwoLineAvatarIconListItem:
                    text: "Item 6"
                    secondary_text: "Description for Item 3"
                    icon: "android"
                    ImageLeftWidget:
                        source: "avatar3.png"
                TwoLineAvatarIconListItem:
                    text: "Item 7"
                    secondary_text: "Description for Item 1"
                    icon: "star"
                    ImageLeftWidget:
                        source: "avatar1.png"
                TwoLineAvatarIconListItem:
                    text: "Item 8"
                    secondary_text: "Description for Item 2"
                    icon: "heart"
                    ImageLeftWidget:
                        source: "avatar2.png"
                TwoLineAvatarIconListItem:
                    text: "Item 9"
                    secondary_text: "Description for Item 3"
                    icon: "android"
                    ImageLeftWidget:
                        source: "avatar3.png"
                TwoLineAvatarIconListItem:
                    text: "Item 10"
                    secondary_text: "Description for Item 1"
                    icon: "star"
                    ImageLeftWidget:
                        source: "avatar1.png"
                TwoLineAvatarIconListItem:
                    text: "Item 11"
                    secondary_text: "Description for Item 2"
                    icon: "heart"
                    ImageLeftWidget:
                        source: "avatar2.png"
                TwoLineAvatarIconListItem:
                    text: "Item 12"
                    secondary_text: "Description for Item 3"
                    icon: "android"
                    ImageLeftWidget:
                        source: "avatar3.png"
                    
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
        self.conn=sqlite3.connect("expense.db")
        command="CREATE TABLE IF NOT EXISTS todo (id TEXT, task TEXT)"
        self.conn.execute(command)
        self.conn.commit() 

    def insert_record(self,item_id,record):
        self.conn.execute("INSERT INTO todo (id,task) VALUES (?,?)",(item_id,record))
        self.conn.commit()        
    
    def update_record(self, item_id,value):        
        self.conn.execute("UPDATE todo SET task = ? WHERE id = ?", (value, item_id))       
        self.conn.commit()

    def delete_record(self,item_id):
        self.conn.execute("DELETE FROM todo WHERE id = ?",(item_id,))
        self.conn.commit()

    def fetch_all_record(self):
        cursor=self.conn.execute("SELECT * FROM todo")
        records=cursor.fetchall()    
        return records

    def close_connection(self):
        self.conn.close()

class ExpenseApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(screen)
        
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

        self.date_dialog = MDDatePicker()
        self.date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)

    def set_item(self, text__item):
        self.screen.ids.screen_manager.get_screen("expenses").ids.categoryid.text = text__item
        self.menu.dismiss()


    def on_save(self, instance, value, date_range):
        
        self.screen.ids.screen_manager.get_screen("expenses").ids.datetimeid.text = value.strftime("%d") + "/" + value.strftime("%m") + "/" + value.strftime("%Y")
        self.date_dialog.dismiss()

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
        self.date_dialog.dismiss()

    def show_date_picker(self):
        
        self.date_dialog.open()


    def build(self):
        #self.sc=Builder.load_string(screen)                
        return  self.screen
    
    def on_start(self):
        self.change_title()
        self.access_scroll_y()

    def change_title(self):
        current_screen = self.screen.ids.screen_manager.current_screen
        title_text = current_screen.name.replace('_', ' ').capitalize() if current_screen else "Expenses"
        self.screen.ids.appbarid.title =f"Expenses App ({title_text})" 
        boxlayout = current_screen.ids.firstlayout
        print(boxlayout)

    def access_scroll_y(self):
        # Accessing the Expenses screen
        expenses_screen = self.screen.ids.screen_manager.get_screen("expenses")        
        scroll_view = expenses_screen.ids.scroll_view
        scroll_y = scroll_view.scroll_y
        print("Scroll Y:", scroll_y)    

        
    
if __name__=="__main__":
    ExpenseApp().run()