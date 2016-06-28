import csv
import argparse
from sets import Set
import labels
from reportlab.graphics import shapes
from reportlab.pdfbase.pdfmetrics import stringWidth



class Guest:
    def __init__(self, first, last, guest=False, isBaby=False):
        self.first = first
        self.last = last
        self.gets_guest = guest
        self.isBaby = isBaby

    def __repr__(self):
        return "{} {}".format(self.first, self.last)


class Address:
    def __init__(self, street, city, state, zip):
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip

    def __hash__(self):
        return hash(str(self.street) + str(self.zip))
    
    def __eq__(self, other):
        return self.street == other.street and self.zip == other.zip

    def __repr__(self):
        return "\n{}\n{}, {} {}".format(self.street, self.city, self.state, self.zip)





def is_family(guests):
    """ If all last names are the same"""
    lasts = set() 
    for guest in guests:
        lasts.add(guest.last)
    return len(lasts) == 1

def count_guests(guests):
    guest_count = 0
    for guest in guests:
        if guest.gets_guest:
            guest_count += 1
    return guest_count

def cluster_by_last_name(guests):
    names = {}
    for guest in guests:
        if  not guest.last in names:
            names[guest.last] = []
        names[guest.last].append(guest.first)
    return names

def _create_labels(invites):
    _labels = []
    for key, guests in invites.iteritems():
        print "key ", key
        print "guests ", guests
        _label = []
        lastName = None 
        guest_count = 0

        #Have babies, kids
        if is_family(guests):
            lastName = guests[0].last
            _label.append("The {} Family".format(lastName))
        else:
            #guest_count = count_guests(guests)
            if len(guests) == 1 and guests[0].gets_guest:
                _label.append("{} {} and guest".format(guest.first, guest.last))
            else:
                for guest in guests:
                    _label.append("{} {}".format(guest.first, guest.last))

            """
            column_width = 90 
            for last, firsts in cluster_by_last_name(guests).iteritems():
                firstName_line = []
                for f in firsts:
                    name_width = stringWidth(f, fontName="Helvetica", fontSize=16)
                    column_width -= name_width
                    firstName_line.append(f)
            """



        _label.append("{}".format(key.street))
        _label.append("{}, {} {}".format(key.city, key.state, key.zip))
        _labels.append(_label)
    return _labels

def create_labels(invites):

    def draw_label(label, width, height, obj):
        print obj
        # Just convert the object to a string and print this at the bottom left of
        # the label.
        fontSize = 16
        d = fontSize * 1.2 
        x = 2
        y = height-d 
        for line in obj:
            #print line
            label.add(shapes.String(x, y, str(line), fontName="Helvetica", fontSize=16))
            y -= d

        #print "\n"

    sheet_width = 210
    sheed_height = 297
    columns = 2 
    rows = 8
    label_width  = 90
    label_height = 25 
    specs = labels.Specification(sheet_width, sheed_height, columns, rows, label_width, label_height, corner_radius=2)


# Create the sheet.
    sheet = labels.Sheet(specs, draw_label, border=True)

# Add a couple of labels.

# We can also add each item from an iterable.
    sheet.add_labels(_create_labels(invites))

# Note that any oversize label is automatically trimmed to prevent it messing up
# other labels.

# Save the file and we are done.
    sheet.save('basic.pdf')
    print("{0:d} label(s) output on {1:d} page(s).".format(sheet.label_count, sheet.page_count))




def parse_guests(filepath):
    invites = {}
    with open(filepath, 'rb') as csvfile:
        r = csv.DictReader(csvfile)
        for row in r:
            last = row["Last"].strip()
            first = row["First"].strip()
            street = row["Address"].strip()
            city = row["City"].strip()
            state = row["State"].strip()
            zip = row["Zip Code"].strip()

            has_guest = False 
            try:
                g = int(row["Guest"].strip())
                if g == 1:
                    has_guest = True
            except:
                pass

            isBaby = False
            try:
                x = int(row["Kid"].strip())
                if x >= 1:
                    isBaby = True
            except:
                pass
            
            try:
                x = int(row["Baby"].strip())
                if x >= 1:
                    isBaby = True
            except:
                pass
           
            #print "{} {}".format(first, last)
            #print "Is baby? ", isBaby
            guest = Guest(first, last, has_guest, isBaby = isBaby) 
            house = Address(street, city, state, zip)

            if house in invites:
                invites[house].append(guest)
            else:
                invites[house] = [guest]
   # print invites
    #create_labels(invites)
    for key,val in invites.iteritems():
        print key

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('guests')
    args = parser.parse_args()
    parse_guests(args.guests)


