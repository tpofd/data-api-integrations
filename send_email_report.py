"""
This feature can help you automatically send a newsletter with business data to any corporate mailbox
"""


def send_email_report(recipients, table_name, responsible, tables, cclist, text='default'):

    """
    :param recipients: people who will get the report
    :param table_name: name of file (you can set anything)
    :param responsible: your corporate mail
    :param tables: dataframe or list of dataframe
    :param text: text of the email
    :param cclist: people who will get the copy of the report message
    :return:
    """

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    from datetime import datetime
    import io
    import pandas as pd

    current_date = datetime.now()

    # login to SMTP server
    s = smtplib.SMTP(host=YOURMAILHOST, port=YOURMAILPORT)
    s.starttls()
    s.login(YOURMAILUSER, YOURMAILPASSWORD)

    # generate message parametrs
    msg = MIMEMultipart()

    # from whom will come message
    msg['From'] = YOURDEPARTMENTEMAIL
    msg['To'] = ", ".join(recipients)
    msg['CC'] = ', '.join(cclist)

    # email theme / subject
    msg['Subject'] = 'Data upload ({0}) | {1}'.format(table_name, current_date)

    # default messsage if there are nothing in text param
    if text == 'default':
        text = f'This is a report data from {table_name}.'

    # main message text
    message = f'''
    Hi

    </br>{text}
    </br>File time upload: {current_date.strftime("%d-%m-%Y %H:%M")}.
    </br>
    </br>This email is generated automatically.
    </br>If you have any problem with this email, write {responsible}
    '''

    # some html to make your email beatiful
    html = '''
    <p>paste your company letter html template here</p>
    ''' + {message}

    # if we have only one dataframe - generate one file
    if isinstance(tables, pd.DataFrame):

        towrite = io.BytesIO()
        tables.to_excel(towrite, index=False)
        towrite.seek(0)
        binary_data = towrite.read()

        attachment = MIMEApplication(binary_data)
        attachment["Content-Disposition"] = 'attachment; filename="' + table_name + '.xlsx"'
        msg.attach(attachment)

    # if we have list of dataframe generate files from all of them
    elif isinstance(tables, list):

        for table in range(len(tables)):
            towrite = io.BytesIO()
            tables[table].to_excel(towrite, index=False)
            towrite.seek(0)
            binary_data = towrite.read()

            attachment = MIMEApplication(binary_data)
            attachment["Content-Disposition"] = 'attachment; filename="' + table_name + '.xlsx"'
            msg.attach(attachment)

    # if there are no dataframe say to users that we don't send message
    else:
        print("Variable hasn't dataframes to send. Message will be send without files")

    msg.attach(MIMEText(html, 'html'))

    # send message
    s.send_message(msg)
