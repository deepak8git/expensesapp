from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
import sqlite3

screen ="""

MDScreen:
    MDNavigationLayout:
        MDScreenManager:
            MDScreen:
                MDTopAppBar:
                    title:"Expenses App"
                    left_action_items:[["menu",lambda x:nav_drawer.set_state("open")]]
                    pos_hint:{"top":1}
                    elevation:1

        ScreenManager:
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
    MDLabel:
        text:"Expenses Screen"
        halign:"center"

    MDRectangleFlatButton:
        text:"First"
        pos_hint:{"center_x":0.5,"center_y":0.4}
        on_press:root.manager.current="category"

<Category>:
    name:"category"
   
    MDLabel:
        text:"Category Screen"
        halign:"center"

    MDRectangleFlatButton:
        text:"Second"
        pos_hint:{"center_x":0.5,"center_y":0.4}
        on_press:root.manager.current="expenses"


<ExpensesView>:
    name:"expensesview"
<CategoryView>:
<ChartView>:


"""

class Expenses(Screen):
    pass
class Category(Screen):
    pass
class ExpensesView(Screen):
    pass
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

    def build(self):
        self.sc=Builder.load_string(screen)
        return self.sc
    
if __name__=="__main__":
    ExpenseApp().run()

# class ExpenseApp(MDApp):
#     def build(self):
#         self.sc = Builder.load_string(screen)
#         self.screen_manager = self.sc.ids.nav_drawer.ids.screen_manager
#         self.screen_manager.bind(current=self.on_screen_change)  # Bind the current screen change event
#         return self.sc

#     def on_screen_change(self, instance, screen):
#         current_screen_name = screen.name
#         if current_screen_name == "expenses":
#             self.sc.ids.top_app_bar.title = "Expenses Screen"
#         elif current_screen_name == "category":
#             self.sc.ids.top_app_bar.title = "Category Screen"
#         # Add conditions for other screens as needed
