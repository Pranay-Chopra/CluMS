import gi, hashlib, json
import itertools as it
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk

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
        if uname == "force" and passwd == "e98278e51b6076b954e29a534d7f6edb57650c68d1ee43f0feb2dba3f4b912b2":
            self.builder.get_object("Window").destroy()
            Main()
        else:
            self.builder.get_object("wrong").set_text("!! Invalid Login/Password !!")


#main window
class Main():
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

    #bug fix -> add new dialogues
    def dia_del(self, dialogue, event):
        dialogue.hide()
        return True

    #editable treeview
    def mem_name_edited(self, widget, path, text):
        for i in text.split():
            if not i.isalpha():
                break
        else:
            with open("members.json", "r+") as f:
                data = json.load(f)
                data[int(path)]["name"] = text
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
            self.builder.get_object("members_list").clear()
            fjson = json.loads(open("members.json","r").read())
            for i in fjson:
                self.builder.get_object("members_list").append([i["s_no"],i["name"].title(),i["post"].title(),i["mob_no"]])

    def mem_post_edited(self, widget, path, text):
        with open("members.json", "r+") as f:
            data = json.load(f)
            data[int(path)]["post"] = text
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        self.builder.get_object("members_list").clear()
        fjson = json.loads(open("members.json","r").read())
        for i in fjson:
            self.builder.get_object("members_list").append([i["s_no"],i["name"].title(),i["post"].title(),i["mob_no"]])

    def mem_mob_edited(self, widget, path, text):
        if text.isdigit():
            with open("members.json", "r+") as f:
                data = json.load(f)
                data[int(path)]["mob_no"] = text
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
            self.builder.get_object("members_list").clear()
            fjson = json.loads(open("members.json","r").read())
            for i in fjson:
                self.builder.get_object("members_list").append([i["s_no"],i["name"].title(),i["post"].title(),i["mob_no"]])

    def team_name_edited(self, widget, path, text):
        with open("teams.json", "r+") as f:
            data = json.load(f)
            data[int(path)]["team_name"] = text
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        self.builder.get_object("teams_list").clear()
        fjson = json.loads(open("teams.json","r").read())
        for i in fjson:
            self.builder.get_object("teams_list").append([i["s_no"],i["team_name"].title(),", ".join(i["team_members"].split(',')).title()])

    def team_members_edited(self, widget, path, text):
        names = []
        for i in text.split(','):
            names.append(i)
        names=''.join(names)
        for j in names.split():
            if not j.isalpha():
                break
        else:
            with open("teams.json", "r+") as f:
                data = json.load(f)
                data[int(path)]["team_members"] = text
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
            self.builder.get_object("teams_list").clear()
            fjson = json.loads(open("teams.json","r").read())
            for i in fjson:
                self.builder.get_object("teams_list").append([i["s_no"],i["team_name"].title(),", ".join(i["team_members"].split(',')).title()])

    def eve_name_edited(self, widget, path, text):
        with open("events.json", "r+") as f:
            data = json.load(f)
            data[int(path)]["name"] = text
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        self.builder.get_object("events_list").clear()
        fjson = json.loads(open("events.json","r").read())
        for i in fjson:
            self.builder.get_object("events_list").append([i["s_no"],i["name"].title(),i["domain"].title(),i["part_no"],i["head"].title()])

    def eve_domain_edited(self, widget, path, text):
        for i in text:
            if i not in "0123456789-" and text.lower() != "open":
                break
        else:
            with open("events.json", "r+") as f:
                data = json.load(f)
                data[int(path)]["domain"] = text
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
            self.builder.get_object("events_list").clear()
            fjson = json.loads(open("events.json","r").read())
            for i in fjson:
                self.builder.get_object("events_list").append([i["s_no"],i["name"].title(),i["domain"].title(),i["part_no"],i["head"].title()])

    def eve_part_no_edited(self, widget, path, text):
        for i in text:
            if i not in "0123456789+":
                break
        else:
            with open("events.json", "r+") as f:
                data = json.load(f)
                data[int(path)]["part_no"] = text
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
            self.builder.get_object("events_list").clear()
            fjson = json.loads(open("events.json","r").read())
            for i in fjson:
                self.builder.get_object("events_list").append([i["s_no"],i["name"].title(),i["domain"].title(),i["part_no"],i["head"].title()])

    def eve_head_edited(self, widget, path, text):
        for i in text.split():
            if not i.isalpha():
                break
        else:
            with open("events.json", "r+") as f:
                data = json.load(f)
                data[int(path)]["head"] = text
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
            self.builder.get_object("events_list").clear()
            fjson = json.loads(open("events.json","r").read())
            for i in fjson:
                self.builder.get_object("events_list").append([i["s_no"],i["name"].title(),i["domain"].title(),i["part_no"],i["head"].title()])

    #delete entry handlers
    def on_mem_del_clicked(self, widget):
        with open("members.json", "r+") as f:
            data = json.load(f)
            del data[self.selected - 1]
            for i in data:
                i["s_no"] = data.index(i) + 1
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        self.builder.get_object("members_list").clear()
        fjson = json.loads(open("members.json","r").read())
        for i in fjson:
            self.builder.get_object("members_list").append([i["s_no"],i["name"].title(),i["post"].title(),i["mob_no"]])


    def on_team_del_clicked(self, widget):
        with open("teams.json", "r+") as f:
            data = json.load(f)
            del data[self.selected - 1]
            for i in data:
                i["s_no"] = data.index(i) + 1
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        self.builder.get_object("teams_list").clear()
        fjson = json.loads(open("teams.json","r").read())
        for i in fjson:
            self.builder.get_object("teams_list").append([i["s_no"],i["team_name"].title(),", ".join(i["team_members"].split(',')).title()])
            

    def on_eve_del_clicked(self, widget):
        with open("events.json", "r+") as f:
            data = json.load(f)
            del data[self.selected - 1]
            for i in data:
                i["s_no"] = data.index(i) + 1
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        self.builder.get_object("events_list").clear()
        fjson = json.loads(open("events.json","r").read())
        for i in fjson:
            self.builder.get_object("events_list").append([i["s_no"],i["name"].title(),i["domain"].title(),i["part_no"],i["head"].title()])
            


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
        for i in new_mem_name.split():
            if ((new_mem_mob_no[0] in '012345') or (len(new_mem_mob_no) != 10) or (not new_mem_mob_no.isdigit())) and (not i.isalpha()):
                self.builder.get_object("mem_wrong").set_text("!! Malformed Name and Mobile Number!!")
                break
            elif (not i.isalpha()):
                self.builder.get_object("mem_wrong").set_text("!! Malformed Name !!")
                break
            elif (new_mem_mob_no[0] in '012345') or (len(new_mem_mob_no) != 10) or (not new_mem_mob_no.isdigit()):
                self.builder.get_object("mem_wrong").set_text("!! Malformed Mobile Number !!")
                break
        else:
            with open("members.json", "r+") as f:
                data = json.load(f)
                data.append({"s_no":len(data)+1,"name":new_mem_name,"post":new_mem_post,"mob_no":new_mem_mob_no})
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
            self.builder.get_object("members_list").clear()
            fjson = json.loads(open("members.json","r").read())
            for i in fjson:
                self.builder.get_object("members_list").append([i["s_no"],i["name"].title(),i["post"].title(),i["mob_no"]])
            self.builder.get_object("mem_dia").hide()


    def on_team_dia_apply_clicked(self, widget):
        new_team_name = self.builder.get_object("new_team_name").get_text().lower()
        new_team_members = self.builder.get_object("new_team_members").get_text().lower()
        names = []
        for i in new_team_members.split(','):
            names.append(i)
        names=''.join(names)
        for j in names.split():
            if not j.isalpha():
                self.builder.get_object("team_wrong").set_text("!! Malformed Member Names !!")
                break
        else:
            with open("teams.json", "r+") as f:
                data = json.load(f)
                data.append({"s_no":len(data)+1,"team_name":new_team_name,"team_members":new_team_members})
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
            self.builder.get_object("teams_list").clear()
            fjson = json.loads(open("teams.json","r").read())
            for i in fjson:
                self.builder.get_object("teams_list").append([i["s_no"],i["team_name"].title(),", ".join(i["team_members"].split(',')).title()])
            self.builder.get_object("team_dia").hide()

    def on_eve_dia_apply_clicked(self, widget):
        new_eve_name = self.builder.get_object("new_eve_name").get_text().lower()
        new_eve_domain = self.builder.get_object("new_eve_domain").get_text().lower()
        new_eve_part_no = self.builder.get_object("new_eve_part_no").get_text().lower()
        new_eve_head = self.builder.get_object("new_eve_head").get_text().lower()
        temp1 = list(new_eve_domain)
        temp2 = list(new_eve_part_no)
        print(temp1, temp2)
        for i in temp1:
            print(i)
            if (i not in '0123456789-') and (new_eve_domain != "open"):
                self.builder.get_object("eve_wrong").set_text("!! Malformed Domain !!")
                break
        else:
            for j in temp2:
                if not (j in "0123456789+"):
                    self.builder.get_object("eve_wrong").set_text("!! Malformed No. of Participants !!")
                    break
            else:
                for k in new_eve_head.split():
                    if (not k.isalpha()):
                        self.builder.get_object("eve_wrong").set_text("!! Malformed Head Name !!")
                        break
                else:
                    with open("events.json", "r+") as f:
                        data = json.load(f)
                        data.append({"s_no":len(data)+1,"name":new_eve_name,"domain":new_eve_domain,"part_no":new_eve_part_no,"head":new_eve_head})
                        f.seek(0)
                        json.dump(data, f, indent=4)
                        f.truncate()
                    self.builder.get_object("events_list").clear()
                    fjson = json.loads(open("events.json","r").read())
                    for i in fjson:
                        self.builder.get_object("events_list").append([i["s_no"],i["name"].title(),i["domain"].title(),i["part_no"],i["head"].title()])
                    self.builder.get_object("eve_dia").hide()




if __name__ == "__main__":
    main = Login()
    gtk.main()    