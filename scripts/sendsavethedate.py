import emails
from optparse import OptionParser
import csv
from emails.template import JinjaTemplate as T
import yaml

class SaveTheDateSender:

    def __init__(self, config_file):
        self._load_config(config_file)

    def _load_config(self, config_file):
        with open(config_file, 'rb') as stream:
            cfg = yaml.safe_load(stream)
            self.smtp = cfg['smtp'] 
            self.email = cfg['email']
        
    def send(self, csvFilePath, message_template, subject):
        with open(csvFilePath, 'rb') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                name = row[0]
                email = row[1]
                self._send_single(name, email)

    def _send_single(self, name, email):
        message = emails.html(html=self.email['message'], subject=self.email['subject'], mail_from=(self.email['mail_from'], self.email['mail_from_email']))
        r = message.send(to = (name, recipient), render = self.email['message_render'], smtp = smtp)
        if response.status_code not in [250, ]:
            print "Failed to send to: ", email


if __name__ == "__main__":
    usage = "usage: %prog [options] [Config File] [CSV File]"
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.print_help()
        exit()

    sender = SaveTheDateSender(args[0])
    
