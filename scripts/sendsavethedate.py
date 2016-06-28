import emails
from optparse import OptionParser
import csv
from emails.template import JinjaTemplate as T
import yaml
import time

class SaveTheDateSender:

    def __init__(self, config_file):
        self._load_config(config_file)


    def _load_message(self, message_file):
        with open(message_file, 'r') as myfile:
            self.message = myfile.read()

    def _load_config(self, config_file):
        with open(config_file, 'rb') as stream:
            cfg = yaml.safe_load(stream)
            self.smtp = cfg['smtp'] 
            self.email = cfg['email']
        
    def send(self, csvFilePath, message_file):
        self._load_message(message_file)
        with open(csvFilePath, 'rb') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                name = row[0].strip()
                email = row[1].strip()
                if name and email:
                    self._send_single(name, email)
                    time.sleep(1)


    def _send_single(self, name, email):
        message = emails.html(html=T(self.message), subject=self.email['subject'], mail_from=(self.email['mail_from'], self.email['mail_from_email']))
        if self.email['hasevent']:
            message.attach(data=open(self.email['calendarevent'], 'rb'), filename='Event.ics')
        response = message.send(to = (name, email), render = {'firstname': name}, smtp = self.smtp)
        if response.status_code not in [250, ]:
            print "Failed to send to: ", email
        else:
            print "Email successfully sent to {} at {}".format(name, email)


if __name__ == "__main__":
    usage = "usage: %prog [options] [Config File] [CSV File] [Message file]"
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()

    if len(args) != 3:
        parser.print_help()
        exit()

    sender = SaveTheDateSender(args[0])
    sender.send(args[1], args[2])
    
