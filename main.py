import gi, hashlib, json
import itertools as it
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk
import inspect
import mysql.connector


#login window
class Login:
    mysql_flag = False
    db = []
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


        try:
            data = []
            with open('mysql.conf', "r") as f:
                for i in f.read().strip().split('\n'):
                    data.append(i.split('=')[1].strip())
            f.close()
            Login.db = mysql.connector.connect(
                host = data[0],
                user = data[1],
                password = data[2],
                database = data[3],
                charset="utf8mb4",
                collation="utf8mb4_unicode_520_ci"
            )
            Login.mysql_flag = True
            self.builder.get_object('sql_status').set_markup('<span foreground=\"#3333d1d17a7a\">MySQL Connected</span>')

        except:
            self.builder.get_object('sql_status').set_markup('<span foreground=\"#e0e01b1b2424\">MySQL Disconnected</span>')


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

    def on_sql_button_clicked(self, widget):
        self.builder.get_object('sql_host').set_text('')
        self.builder.get_object('sql_uname').set_text('')
        self.builder.get_object('sql_db_name').set_text('')
        self.builder.get_object('sql_passwd').set_text('')
        self.builder.get_object('sql_dialogue').show()

    def dia_del(self, dialogue, event):
        dialogue.hide()
        return True

    def save_sql_config(self, widget):
        sql_host = self.builder.get_object('sql_host').get_text()
        sql_uname = self.builder.get_object('sql_uname').get_text()
        sql_db_name = self.builder.get_object('sql_db_name').get_text()
        sql_passwd = self.builder.get_object('sql_passwd').get_text()

        try:
            Login.db = mysql.connector.connect(
                host = 'localhost' if sql_host == '' else sql_host,
                user = sql_uname,
                password = sql_passwd,
                database = 'clums_db' if sql_db_name == '' else sql_db_name,
                charset="utf8mb4",
                collation="utf8mb4_unicode_520_ci"
            )

        except:
            Login.db = mysql.connector.connect(
                host = 'localhost' if sql_host == '' else sql_host,
                user = sql_uname,
                password = sql_passwd,
                charset="utf8mb4",
                collation="utf8mb4_unicode_520_ci"
            )
            cur = Login.db.cursor()
            cur.execute(f'CREATE DATABASE {"clums_db" if sql_db_name == "" else sql_db_name}')
            cur.close()
            Login.db = mysql.connector.connect(
                host = 'localhost' if sql_host == '' else sql_host,
                user = sql_uname,
                password = sql_passwd,
                database = 'clums_db' if sql_db_name == '' else sql_db_name,
                charset="utf8mb4",
                collation="utf8mb4_unicode_520_ci"
            )
        if Login.db.is_connected():
            self.builder.get_object('sql_status').set_markup('<span foreground=\"#3333d1d17a7a\">MySQL Connected</span>')
            with open('mysql.conf', 'w+') as f:
                f.write(f'\
                        host = {"localhost" if sql_host == "" else sql_host}\n\
                        user = {sql_uname}\n\
                        password = {sql_passwd}\n\
                        database = {"clums_db" if sql_db_name == "" else sql_db_name}\n\
                    charset="utf8mb4"\n\
                    collation="utf8mb4_unicode_520_ci"')
                f.close()
            Login.mysql_flag = True

            self.builder.get_object('sql_dialogue').hide()



#main window
class Main(Login):
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
        if Login.mysql_flag:
            self.cur = Login.db.cursor()
            self.cur.execute('SHOW TABLES')
            data = self.cur.fetchall()
            table_list = data if len(data) != 0 else []


            for i in [('members',), ('teams',), ('events',)]:
                if i not in table_list:
                    if i == ('members',):
                        self.cur.execute("CREATE TABLE members (s_no int, name varchar(255), post varchar(255), mob_no varchar(255))")
                        self.cur.execute('SHOW TABLES')
                        data = self.cur.fetchall()
                        table_list = data if len(data) != 0 else []
                    elif i == ('teams',):
                        self.cur.execute("CREATE TABLE teams (s_no int, team_name varchar(255), team_members varchar(255))")
                        self.cur.execute('SHOW TABLES')
                        data = self.cur.fetchall()
                        table_list = data if len(data) != 0 else []
                    elif i == ('events',):
                        self.cur.execute("CREATE TABLE events (s_no int, name varchar(255), domain varchar(255), part_no varchar(255), head varchar(255))")
                        self.cur.execute('SHOW TABLES')
                        data = self.cur.fetchall()
                        table_list = data if len(data) != 0 else []

            self.cur.execute('SELECT * FROM members')
            members_data = self.cur.fetchall()
            self.cur.execute('SELECT * FROM teams')
            teams_data = self.cur.fetchall()
            self.cur.execute('SELECT * FROM events')
            events_data = self.cur.fetchall()

            for i in members_data:
                self.builder.get_object("members_list").append([i[0],i[1].title(),i[2].title(),i[3]])
            for i in teams_data:
                self.builder.get_object("teams_list").append([i[0],i[1].title(),", ".join(i[2].split(',')).title()])
            for i in events_data:
                self.builder.get_object("events_list").append([i[0],i[1].title(),i[2].title(),i[3],i[4].title()])


        else:
            members_data = json.loads(open("members.json","r").read())
            teams_data = json.loads(open("teams.json","r").read())
            events_data = json.loads(open("events.json","r").read())

            for i in members_data:
                self.builder.get_object("members_list").append([i["s_no"],i["name"].title(),i["post"].title(),i["mob_no"]])
            for i in teams_data:
                self.builder.get_object("teams_list").append([i["s_no"],i["team_name"].title(),", ".join(i["team_members"].split(',')).title()])
            for i in events_data:
                self.builder.get_object("events_list").append([i["s_no"],i["name"].title(),i["domain"].title(),i["part_no"],i["head"].title()])

    #bug fix -> add new dialogues
    def dia_del(self, dialogue, event):
        dialogue.hide()
        return True

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

    def edit_json_data(self, f, data = None, path = None, col = None, text = None) -> None:
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




    def edit_sql_data(self, table, path = None, text = None, col = None) -> None:
        if 'apply' in inspect.stack()[1][3]:
            self.cur.execute(f'INSERT INTO {table} ({col}) VALUES ({text})')
            Login.db.commit()
        if 'edited' in inspect.stack()[1][3]:
            self.cur.execute(f'UPDATE {table} SET {col} = \'{text}\' WHERE s_no = {int(path)+1}')
            Login.db.commit()
        if 'del' in inspect.stack()[1][3]:
            self.cur.execute(f'DELETE FROM {table} WHERE s_no = {self.selected}')
            Login.db.commit()
            self.cur.execute(f'SELECT * FROM {table}')
            data = self.cur.fetchall()
            self.cur.execute(f'DELETE FROM {table}')

            for i in range(1, len(data)+1):
                temp_list = list(data[i-1])
                temp_list[0] = i
                for i in range(len(temp_list)):
                    if type(temp_list[i]) is int:
                        temp_list[i] = f'{str(temp_list[i])}'
                    elif type(temp_list[i]) is str:
                        temp_list[i] = f'\'{temp_list[i]}\''
                self.cur.execute(f'INSERT INTO {table} ({col}) VALUES ({",".join(temp_list)})')
            Login.db.commit()
        if 'mem' in inspect.stack()[1][3]:
            self.builder.get_object("members_list").clear()
            self.cur.execute('SELECT * FROM members')
            members_data = self.cur.fetchall()
            for i in members_data:
                self.builder.get_object("members_list").append([i[0],i[1].title(),i[2].title(),i[3]])
        if 'team' in inspect.stack()[1][3]:
            self.builder.get_object("teams_list").clear()
            self.cur.execute('SELECT * FROM teams')
            teams_data = self.cur.fetchall()
            for i in teams_data:
                self.builder.get_object("teams_list").append([i[0],i[1].title(),", ".join(i[2].split(',')).title()])
        if 'eve' in inspect.stack()[1][3]:
            self.builder.get_object("events_list").clear()
            self.cur.execute('SELECT * FROM events')
            events_data = self.cur.fetchall()
            for i in events_data:
                self.builder.get_object("events_list").append([i[0],i[1].title(),i[2].title(),i[3],i[4].title()])




    #editable treeview
    def mem_name_edited(self, widget, path, text):
        for i in text:
            if i.isalpha or i.isspace:
                pass
            else:
                break
        else:
            if Login.mysql_flag:
                self.edit_sql_data('members', path=path, col='name', text=text)
            else:
                with open('members.json', 'r+') as f:
                    self.edit_json_data(f, path=path, col='name', text=text)

    def mem_post_edited(self, widget, path, text):
        if Login.mysql_flag:
            self.edit_sql_data('members', path=path, col='post', text=text)
        else:
            with open("members.json", "r+") as f:
                self.edit_json_data(f, path=path, col='post', text=text)

    def mem_mob_edited(self, widget, path, text):
        if text.isdigit():
            if Login.mysql_flag:
                self.edit_sql_data('members', path=path, col='mob_no', text=text)
            else:
                with open("members.json", "r+") as f:
                    self.edit_json_data(f, path=path, col='mob_no', text=text)

    def team_name_edited(self, widget, path, text):
        if Login.mysql_flag:
            self.edit_sql_data('teams', path=path, col='team_name', text=text)
        else:
            with open("teams.json", "r+") as f:
                self.edit_json_data(f, path=path, col='team_name', text=text)

    def team_members_edited(self, widget, path, text):
        for i in text.split(','):
            if i.isalpha() or i.isspace:
                pass
            else:
                break
        else:
            if Login.mysql_flag:
                self.edit_sql_data('teams', path=path, col='team_members', text=text)
            else:
                with open("teams.json", "r+") as f:
                    self.edit_json_data(f, path=path, col='team_members', text=text)

    def eve_name_edited(self, widget, path, text):
        if Login.mysql_flag:
            self.edit_sql_data('events', path=path, col='name', text=text)
        else:
            with open("events.json", "r+") as f:
                self.edit_json_data(f, path=path, col='name', text=text)

    def eve_domain_edited(self, widget, path, text):
        for i in text:
            if i not in "0123456789-":
                break
        else:
            if Login.mysql_flag:
                self.edit_sql_data('events', path=path, col='domain', text=text)
            else:
                with open("events.json", "r+") as f:
                    self.edit_json_data(f, path=path, col='domain', text=text)

    def eve_part_no_edited(self, widget, path, text):
        for i in text:
            if i not in "0123456789+":
                break
        else:
            if Login.mysql_flag:
                self.edit_sql_data('events', path=path, col='part_no', text=text)
            else:
                with open("events.json", "r+") as f:
                    self.edit_json_data(f, path=path, col='part_no', text=text)

    def eve_head_edited(self, widget, path, text):
        for i in text:
            if i.isalpha() or i.isspace():
                pass
            else:
                break
        else:
            if Login.mysql_flag:
                self.edit_sql_data('events', path=path, col='head', text=text)
            else:
                with open("events.json", "r+") as f:
                    self.edit_json_data(f, path=path, col='head', text=text)

    #delete entry handlers
    def on_mem_del_clicked(self, widget):
        if Login.mysql_flag:
            self.edit_sql_data('members', col='s_no,name,post,mob_no')
        else:
            with open("members.json", "r+") as f:
                self.edit_json_data(f)


    def on_team_del_clicked(self, widget):
        if Login.mysql_flag:
            self.edit_sql_data('teams', col='s_no,team_name,team_members')
        else:
            with open("teams.json", "r+") as f:
                self.edit_json_data(f)


    def on_eve_del_clicked(self, widget):
        if Login.mysql_flag:
            self.edit_sql_data('events', col='s_no,name,domain,part_no,head')
        else:
            with open("events.json", "r+") as f:
                self.edit_json_data(f)



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
                if Login.mysql_flag:
                    self.cur.execute(f'SELECT * FROM members')
                    data = self.cur.fetchall()
                    new_data = f'{len(data)+1},\'{new_mem_name}\',\'{new_mem_post}\',\'{new_mem_mob_no}\''
                    self.edit_sql_data('members', text=new_data, col='s_no,name,post,mob_no')
                else:
                    with open("members.json", "r+") as f:
                        data = json.load(f)
                        data.append({"s_no":len(data)+1,"name":new_mem_name,"post":new_mem_post,"mob_no":new_mem_mob_no})
                        self.edit_json_data(f, data=data)
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
            if Login.mysql_flag:
                self.cur.execute(f'SELECT * FROM teams')
                data = self.cur.fetchall()
                new_data = f'{len(data)+1},\'{new_team_name}\',\'{new_team_members}\''
                self.edit_sql_data('teams', text=new_data, col='s_no,team_name,team_members')
            else:
                with open("teams.json", "r+") as f:
                    data = json.load(f)
                    data.append({"s_no":len(data)+1,"team_name":new_team_name,"team_members":new_team_members})
                    self.edit_json_data(f, data=data)
            self.builder.get_object('team_dia').hide()

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
                if Login.mysql_flag:
                    self.cur.execute(f'SELECT * FROM events')
                    data = self.cur.fetchall()
                    new_data = f'{len(data)+1},\'{new_eve_name}\',\'{new_eve_domain}\',\'{new_eve_part_no}\',\'{new_eve_head}\''
                    self.edit_sql_data('events', text=new_data, col='s_no,name,domain,part_no,head')
                else:
                    with open("events.json", "r+") as f:
                        data = json.load(f)
                        data.append({"s_no":len(data)+1,"name":new_eve_name,"domain":new_eve_domain,"part_no":new_eve_part_no,"head":new_eve_head})
                        self.edit_json_data(f, data=data)
                self.builder.get_object('eve_dia').hide()





if __name__ == "__main__":
    main = Login()
    gtk.main()
