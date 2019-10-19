import csv
import datetime
import getpass
import re
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tempfile import NamedTemporaryFile

host = "smtp.gmail.com"
port = 587  # for TLS
username = "olasogbajoy37@gmail.com"
to_email = username
infodatabase = 'infodatabase1.csv'


def getId():
    with open(infodatabase, 'r') as csvfile:
        reader = csv.reader(csvfile)
        list_reader = list(reader)
        return len(list_reader)


def editInfo(uid=None, name=None, email=None, street_info=None, city_info=None, state_info=None, date=None):
    temp_file = NamedTemporaryFile(delete=False, mode='w')
    with open(infodatabase, "rb") as csvfile, temp_file:
        reader = csv.DictReader(csvfile)
        fieldnames = ['id', 'name', 'email', 'street info', 'city info', 'state info', 'date']
        writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
        '''writer.writeheader()
        print(writer)'''
        for row in reader:
            if row['id'] is not None and int(row.get('id')) == int(uid):
                if name is not None:
                    row['name'] = name
                elif email is not None:
                    row['email'] = email
                elif street_info is not None:
                    row['street info'] = street_info
                elif state_info is not None:
                    row['state info'] = state_info
                elif city_info is not None:
                    row['city info'] = city_info
                elif date is not None:
                    row['date'] = date
                else:
                    print('information not found')
            '''else:
                pass'''
            writer.writerow(row)
        shutil.move(temp_file.name, infodatabase)
        return True


class setUsers:
    def __init__(self):
        self.name = input("Name: ")
        self.email = input("Email Address*: ")
        self.street_info = input("Address\n\tStreet Info: ")
        self.city_info = input("\tCity Info(e.g. GRA, Ikeja): ")
        self.state_info = input("\tState Info(e.g. Lagos, NG): ")
        self.date = datetime.date.today()
        self.data = {}
        self.id = getId()

    def formatInformation(self):
        self.name = self.name.upper()
        self.data.update({'id': self.id})
        self.data.update({'name': self.name})
        self.data.update({'email': self.email})
        self.data.update({'street info': self.street_info})
        self.data.update({'city info': self.city_info})
        self.data.update({'state info': self.state_info})
        self.data.update({'date': self.date})
        return

    def addUser(self):
        #        try:
        with open(infodatabase, 'a', newline='') as csvfile:
            fieldnames = ['id', 'name', 'email', 'street info', 'city info', 'state info', 'date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(self.data)
            return 'user added'


#        except:
#            return 'user not added'


class getUserInfo():

    def printAllUserInfo(self):
        with open(infodatabase, 'r') as csvfile:
            fieldnames = ['id', 'name', 'email', 'street info', 'city info', 'state info', 'date']
            reader = csv.DictReader(csvfile, fieldnames=fieldnames)
            for row in reader:
                print("\n", row.get('id'), row.get('name'), row.get('email'), row.get('street info'),
                      row.get('city info'), row.get('state info'), row.get('date'), "\n\n", sep=', ')
            return True


class sendMessage():

    def messageAllCustomers(self):

        #        try:
        if getId() > 0:
            email_conn = smtplib.SMTP(host, port)
            # email_conn = smtplib.SMTP_SSL(host, port, timeout=20)
            email_conn.ehlo()
            email_conn.starttls()
            print("Enter your gmail password:")
            password = getpass.getpass()
            email_conn.login(username, password)
            with open(infodatabase, 'r') as csvfile:
                fieldnames = ['id', 'name', 'email', 'street info', 'city info', 'state info', 'date']
                reader = csv.DictReader(csvfile, fieldnames=fieldnames)
                for row in reader:
                    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', row.get('email'))  # email id structure
                    if match is not None:
                        the_msg = MIMEMultipart("alternative")
                        the_msg['subject'] = "WHAT CVHUB AFRICA CAN DO FOR " + row.get('name')
                        the_msg['from'] = 'CVHUB4AFRICA <joy@cvhub4africa.com>'
                        address = row.get('street info') + ",\n" + row.get('city info') + ",\n" + row.get('state info')
                        address_2t = row.get('street info') + ",<br>" + row.get('city info') + ",<br>" + row.get(
                            'state info')
                        plain_text = "From,\nCVHUB\nNO. 4b Pepple Street,\nCOMP. village, Ikeja,\nLagos, Nigeria.\n\nTo,\n{2}\n{1}\n{0}\n\nDear Sir/Madam,\n\nGood day.\nWe understand how important leveraging information technology is for a corporate entity like {2} in this day and age. We know that your organization can transform its visibility and sales by equipping it's staff with the right knowledge of how to use some Information Technology tools.\n\nWe, CVhub4africa, are a fully registered company in Nigeria, we are into software development and deployment. We offer advanced IT training and we also offer bootcamp & incubation programs. We focus on a data-oriented engineering framework that unearths value for enterprises and relieve them of the engagement process.\n\nOur works stands as a proof of our excellence.\n\nWWe have developed software products that have impacted people and businesses on different continents while maintaining a local connection. Our expansive experience working with new age technologies for diverse audiences over the past decade has helped us master the act of crafting a best-fit solution regardless of your niche.The pressure seems to be mounting with the days remaining till the end of the year.\n\nDo you still have targeted audience out there?\nWhat about the website you envisioned for your business at the beginning of the year?\nThe IT skills you desire to acquire?\n Have you hit your goals yet?\n\n The year is ending - but it’s never too late; you can still take some actions and achieve your goals.\n\nYou can contact us if you require services like Bootcamp, Incubation, Software development, Digital marketing and professional IT training.  We guarantee your satisfaction and we will do our best to deliver an excellent service to you.\n\nWe look forward to discussing this further. Kindly contact us via email or a phone call.\nOur website is www.cvhub4africa.com\n\nThank you.\n\n\nYours sincerely,\nJoy Olasogba\n08037990018, 08080808585\njoy@cvhub4africa.com\ncvhub4africa@gmail.com\n\n".format(row.get('date'), address, row.get('name'))
                        html_text = "<html><body style='background-color:RGB(247, 247, 247)'><section style='background-color:white; padding:5px; margin:10px; border: solid 2px RGB(213, 213, 213); color:RGB(104, 104, 104);'><img src='https://cvhub4africa.com/wp-content/uploads/2019/05/site-logo.png'><br><br><hr><br>From,<br><u>CVHUB</u><br><u>NO. 4b Pepple Street,</u><br><u>COMP. village, Ikeja,</u><br><u>Lagos, Nigeria.</u><br><br>To,<br><u>{2}</u><br><u>{1}</u><br><br><em>Date: {0}</em><br><br><br>Dear Sir/Madam,<br><br>Good day.<br><br>We understand how important leveraging information technology is for a corporate entity like {2} in this day and age. We know that your organization can transform its visibility and sales by equipping it's staff with the right knowledge of how to use some Information Technology tools.<br><br>CVHUB is a fully registered company in Nigeria, we are <b>into software development and deployment</b>. We offer <b>advanced IT training</b> and we also offer <b>bootcamp & incubation programs</b>. We focus on a data-oriented engineering framework that unearths value for enterprises and relieve them of the engagement process.<br><br><i>Our works stands as a proof of our excellence.</i><br><br>We have <b>developed software products that have impacted people and businesses</b> on different continents while maintaining a local connection. Our expansive experience working with new age technologies for diverse audiences over the past decade has helped us master the act of crafting a best-fit solution regardless of your niche.The pressure seems to be mounting with the days remaining till the end of the year.<br><br> Do you still have targeted audience out there?<br>What about the website you envisioned for your business at the beginning of the year?<br>The IT skills you desire to acquire?<br>Have you hit your goals yet?<br><br>The year is ending - but it's never too late; you can still take some actions and achieve your goals.<br><br>You can contact us if you require services like <i>Bootcamp, Incubation, Software development, Digital marketing and professional IT training</i>.<b> We guarantee your satisfaction and we will do our best to deliver an excellent service to you.</b><br><br>We look forward to discussing this further. Kindly contact us via email or a phone call.<br>Our website is www.cvhub4africa.com<br><br>Thank you.<br><br><br><i>Yours sincerely,</i><br><i>Joy Olasogba</i><br><i>08037990018, 08080808585</i><br><i>joy@cvhub4africa.com</i><br><i>cvhub4africa@gmail.com</i><br><hr></section></body></html>".format(
                            row.get('date'), address_2t, row.get('name'))

                        part1 = MIMEText(plain_text, 'plain')
                        part2 = MIMEText(html_text, 'html')

                        the_msg.attach(part1)
                        the_msg.attach(part2)
                        user_email = row.get('email')

                        email_conn.sendmail('joy@cvhub4africa.com', user_email, the_msg.as_string())
                        print(f'sent to {user_email}')
                email_conn.quit()
                return "Emails Sent"
        else:
            return ">>> No data in database <<<\n"

        # except:
        #     return "Error Sending Message"


def main():
    while (0 < 1):

        print(
            "********************************************\n\n CUSTOMER MESSENGER SOFTWARE.\n\n********************************************\n\nEnter the corresponding number/letter to do any of the following;\n  n.    Create a new database\n  e.    Edit customer info\n  1.    Add a new customer to existing database\n  3.    Print all users information(no message)\n  5.    Send mail to all customers\n  6.    Quit\n\n")

        #        try:
        option = input(">>> ")

        if option == 'n':
            answer = input("ARE YOU SURE YOU WANT TO CREATE NEW DATABASE???\n\ny\tyes\nn.\tno ")
            if answer.lower() == 'n':
                return
            elif answer.lower() == 'y':
                with open(infodatabase, 'w', newline='') as csvfile:
                    fieldnames = ['id', 'name', 'email', 'street info', 'city info', 'state info', 'date']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    print('Database created')

        elif option == 'e':
            userid = input('Enter the users ID: ')
            whatToChange = input(
                'Enter the number corresponding to what you want to change\n '
                '1. name\n 2. email\n 3. street_info\n 4. city_info\n 5. date\n\n  >> ')
            if whatToChange == '1':
                new_Name = input('Enter new name: ')
                editInfo(uid=userid, name=new_Name)
                break
            elif whatToChange == '2':
                new_Email = input('Enter new email: ')
                editInfo(uid=userid, email=new_Email)
                break
            elif whatToChange == '3':
                street_info = input("Enter new 'street info': ")
                editInfo(uid=userid, street_info=street_info)
                break
            elif whatToChange == '4':
                city_info = input("Enter new 'city info': ")
                editInfo(uid=userid, city_info=city_info)
                break
            elif whatToChange == '5':
                print('Enter new date: ')
                yyyy = int(input("Date\n\tYEAR: "))
                mm = int(input("\tMM: "))
                dd = int(input("\tDD: "))
                new_date = datetime.date(yyyy, mm, dd)
                editInfo(uid=userid, date=new_date)
                break

        elif option == '1':
            newUser = setUsers()
            newUser.formatInformation()
            addcheck = newUser.addUser()
            print(addcheck)

        elif option == '3':
            getInfo = getUserInfo()
            getInfo.printAllUserInfo()

        elif option == '5':
            messageSender = sendMessage()
            sendMssgCheck = messageSender.messageAllCustomers()
            print(sendMssgCheck)

        elif option == '6':
            break
            exit()

        '''except:
            print(">>>>> Wrong value entered <<<<<\n")'''


if __name__ == '__main__':
    main()
