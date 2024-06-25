import gi, hashlib, json
import itertools as it
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk
import inspect


#login window
class Login:
    def __init__(self):
        #builder set up
        gladeFile = "login.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(gladeFile)
        self.builder.connect_signals(self)

        #draw window
        window = self.builder.get_object("Window")
        window.connect("delete-event", gtk.main_quit)
        window.show()

    #submit button handler
    def on_submit_clicked(self, widget):
        #get uname and pass values
        uname = self.builder.get_object("UnameIn").get_text()
        passwd = hashlib.sha256((self.builder.get_object("PassIn").get_text()).encode()).hexdigest()
        
        #check for login
        if uname == "force" and passwd == "270361f4f17812817257e77e481a34c76b2f54d8db61395e9cfc6321d3352fde":
            self.builder.get_object("Window").destroy()
            Main()
        else:
            self.builder.get_object("wrong").set_text("!! Invalid Login/Password !!")


#main window
class Main:
    def __init__(self):
        #builder set up
        gladeFile = "main.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(gladeFile)
        self.builder.connect_signals(self)
        self.selected = None

        #draw window
        window = self.builder.get_object("main_window")
        window.connect("delete-event", gtk.main_quit)
        window.show()

        #populate treeview
        members_json = json.loads(open("members.json","r").read())
        teams_json = json.loads(open("teams.json","r").read())
        events_json = json.loads(open("events.json","r").read())

        for i in members_json:
            self.builder.get_object("members_list").append([i["s_no"],i["name"].title(),i["post"].title(),i["mob_no"]])
        for i in teams_json:
            self.builder.get_object("teams_list").append([i["s_no"],i["team_name"].title(),", ".join(i["team_members"].split(',')).title()])
        for i in events_json:
            self.builder.get_object("events_list").append([i["s_no"],i["name"].title(),i["domain"].title(),i["part_no"],i["head"].title()])


    #raise add new dialogues
    def on_mem_add_clicked(self, widget):
        self.builder.get_object("new_mem_name").set_text("")
        self.builder.get_object("new_mem_post").set_text("")
        self.builder.get_object("new_mem_mob_no").set_text("")
        self.builder.get_object("mem_wrong").set_text("")
        self.builder.get_object("mem_dia").show()
    def on_team_add_clicked(self, widget):
        self.builder.get_object("new_team_name").set_text("")
        self.builder.get_object("new_team_members").set_text("")
        self.builder.get_object("team_wrong").set_text("")
        self.builder.get_object("team_dia").show()
    def on_eve_add_clicked(self, widget):
        self.builder.get_object("new_eve_name").set_text("")
        self.builder.get_object("new_eve_domain").set_text("")
        self.builder.get_object("new_eve_part_no").set_text("")
        self.builder.get_object("new_eve_head").set_text("")
        self.builder.get_object("eve_wrong").set_text("")
        self.builder.get_object("eve_dia").show()

    def edit_data(self, f, data = None, path = None, col = None, text = None) -> None:
        if data == None:
            data = json.load(f)
        if 'apply' in inspect.stack()[1][3]:
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            f.close()
        if 'edited' in inspect.stack()[1][3]:            
            data[int(path)][col] = text
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            f.close()
        if 'del' in inspect.stack()[1][3]:
            del data[self.selected - 1]
            for i in data:
                i["s_no"] = data.index(i) + 1
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            f.close()
        if 'mem' in inspect.stack()[1][3]:
            self.builder.get_object("members_list").clear()
            fjson = json.loads(open('members.json',"r").read())
            for i in fjson:
                self.builder.get_object("members_list").append([i["s_no"],i["name"].title(),i["post"].title(),i["mob_no"]])
        if 'team' in inspect.stack()[1][3]:
            self.builder.get_object("teams_list").clear()
            fjson = json.loads(open('teams.json',"r").read())
            for i in fjson:
                self.builder.get_object("teams_list").append([i["s_no"],i["team_name"].title(),", ".join(i["team_members"].split(',')).title()])
        if 'eve' in inspect.stack()[1][3]:
            self.builder.get_object("events_list").clear()
            fjson = json.loads(open('events.json',"r").read())
            for i in fjson:
                self.builder.get_object("events_list").append([i["s_no"],i["name"].title(),i["domain"].title(),i["part_no"],i["head"].title()])
        


        

    #bug fix -> add new dialogues
    def dia_del(self, dialogue, event):
        dialogue.hide()
        return True

    #editable treeview
    def mem_name_edited(self, widget, path, text):
        if text.isalpha():
            with open('members.json', 'r+') as f:
                Main.edit_data(self, f, path=path, col='name', text=text)

    def mem_post_edited(self, widget, path, text):
        with open("members.json", "r+") as f:
           Main.edit_data(self, f, path=path, col='post', text=text) 

    def mem_mob_edited(self, widget, path, text):
        if text.isdigit():
            with open("members.json", "r+") as f:
                Main.edit_data(self, f, path=path, col='mob_no', text=text)

    def team_name_edited(self, widget, path, text):
        with open("teams.json", "r+") as f:
            Main.edit_data(self, f, path=path, col='team_name', text=text)

    def team_members_edited(self, widget, path, text):
        for i in text.split(','):
            if not i.isalpha():
                break
        else:
            with open("teams.json", "r+") as f:
                Main.edit_data(self, f, path=path, col='team_members', text=text)

    def eve_name_edited(self, widget, path, text):
        with open("events.json", "r+") as f:
            Main.edit_data(self, f, path=path, col='name', text=text)

    def eve_domain_edited(self, widget, path, text):
        for i in text:
            if i not in "0123456789-":
                break
        else:
            Main.edit_data(self, f, path=path, col='domain', text=text)

    def eve_part_no_edited(self, widget, path, text):
        for i in text:
            if i not in "0123456789+":
                break
        else:
            with open("events.json", "r+") as f:
                Main.edit_data(self, f, path=path, col='part_no', text=text)

    def eve_head_edited(self, widget, path, text):
        if text.isalpha():
            with open("events.json", "r+") as f:
                Main.edit_data(self, f, path=path, col='head', text=text)

    #delete entry handlers
    def on_mem_del_clicked(self, widget):
        with open("members.json", "r+") as f:
            Main.edit_data(self, f)


    def on_team_del_clicked(self, widget):
        with open("teams.json", "r+") as f:
            Main.edit_data(self, f)
            

    def on_eve_del_clicked(self, widget):
        with open("events.json", "r+") as f:
            Main.edit_data(self, f)
            


    #selection handlers
    def mem_select(self, user_data):
        selected = user_data.get_selected()[1]
        if selected != None:
            selection = self.builder.get_object("members_list").get(selected, 0)
            self.selected = int(selection[0])

    def team_select(self, user_data):
        selected = user_data.get_selected()[1]
        if selected != None:
            selection = self.builder.get_object("teams_list").get(selected, 0)
            self.selected = int(selection[0])


    def eve_select(self, user_data):
        selected = user_data.get_selected()[1]
        if selected != None:
            selection = self.builder.get_object("events_list").get(selected, 0)
            self.selected = int(selection[0])



    #new add button on dialogue handlers
    def on_mem_dia_apply_clicked(self, widget):
        new_mem_name = self.builder.get_object("new_mem_name").get_text().lower()
        new_mem_post = self.builder.get_object("new_mem_post").get_text().lower()
        new_mem_mob_no = self.builder.get_object("new_mem_mob_no").get_text().lower()
        if ((new_mem_mob_no[0] in '012345') or (len(new_mem_mob_no) != 10) or (not new_mem_mob_no.isdigit())) and (not new_mem_name.isalpha()):
            self.builder.get_object("mem_wrong").set_text("!! Malformed Name and Mobile Number!!")
        elif (new_mem_mob_no[0] in '012345') or (len(new_mem_mob_no) != 10) or (not new_mem_mob_no.isdigit()):
            self.builder.get_object("mem_wrong").set_text("!! Malformed Mobile Number !!")
        else:
            for i in new_mem_name:
                if i.lower() not in 'abcdefghijklmnopqrstuvwxyz ':
                    self.builder.get_object("mem_wrong").set_text("!! Malformed Name !!")
                    break
            else:
                with open("members.json", "r+") as f:
                    data = json.load(f)
                    data.append({"s_no":len(data)+1,"name":new_mem_name,"post":new_mem_post,"mob_no":new_mem_mob_no})
                    Main.edit_data(self, f, data=data)
                self.builder.get_object('mem_dia').hide()
                


    def on_team_dia_apply_clicked(self, widget):
        new_team_name = self.builder.get_object("new_team_name").get_text().lower()
        new_team_members = self.builder.get_object("new_team_members").get_text().lower()
        temp = new_team_members.split(',')
        flag = False
        for i in temp:
                for j in i:
                    if j.lower() not in 'abcdefghijklmnopqrstuvwxyz ':
                        self.builder.get_object("team_wrong").set_text("!! Malformed Member Names !!")
                        flag = True                              
        if not flag:
            with open("teams.json", "r+") as f:
                data = json.load(f)
                data.append({"s_no":len(data)+1,"team_name":new_team_name,"team_members":new_team_members})
                Main.edit_data(self, f, data=data)
            self.builder.get_object('teams_dia').hide()
            
    def on_eve_dia_apply_clicked(self, widget):
        new_eve_name = self.builder.get_object("new_eve_name").get_text().lower()
        new_eve_domain = self.builder.get_object("new_eve_domain").get_text().lower()
        new_eve_part_no = self.builder.get_object("new_eve_part_no").get_text().lower()
        new_eve_head = self.builder.get_object("new_eve_head").get_text().lower()
        temp1 = list(new_eve_domain)
        temp2 = list(new_eve_part_no)
        flag = False
        for i,j in it.zip_longest(temp1, temp2):
            if not (i in '0123456789-') and (new_eve_domain != "open"):
                self.builder.get_object("eve_wrong").set_text("!! Malformed Domain !!")
                print(not (i in '0123456789-' ), (new_eve_domain != "open"))
                break
            elif j != None and new_eve_domain != None: 
                if j not in '0123456789+':
                    self.builder.get_object("eve_wrong").set_text("!! Malformed No. of Participants !!")
                    break
            else:
                for k in new_eve_head:
                    if k.lower() not in 'abcdefghijklmnopqrstuvwxyz ':
                        self.builder.get_object("eve_wrong").set_text("!! Malformed Head Name !!")
                        flag = True
        else:
            if not flag:
                with open("events.json", "r+") as f:
                    data = json.load(f)
                    data.append({"s_no":len(data)+1,"name":new_eve_name,"domain":new_eve_domain,"part_no":new_eve_part_no,"head":new_eve_head})
                    Main.edit_data(self, f, data=data)
                self.builder.get_object('eve_dia').hide()





if __name__ == "__main__":
    main = Login()
    gtk.main()    