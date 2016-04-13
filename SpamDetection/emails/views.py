import csv
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Email

# Create your views here.
def load_data():
    data_file = open( '../spambase/spambase.csv', 'r' )
    data = csv.reader( data_file, delimiter=',' )
    first_row = next(data)
    num_cols = len(first_row)
    row_count = sum(1 for row in data)+1

    data_file.seek(0)
    print( "tell", data_file.tell() )
    print( "row_count", row_count )
    print( "col_count", num_cols )

    j = 0;
    for line in data:
        e = Email()
        for elem in line:
            if j == 0:
                e.freq_make = float(elem)
            elif j == 1:
                e.freq_address = float(elem)
            elif j == 2:
                e.freq_all = float(elem)
            elif j == 3:
                e.freq_3d = float(elem)
            elif j == 4:
                e.freq_our = float(elem)
            elif j == 5:
                e.freq_over = float(elem)
            elif j == 6:
                e.freq_remove = float(elem)
            elif j == 7:
                e.freq_internet = float(elem)
            elif j == 8:
                e.freq_order = float(elem)
            elif j == 9:
                e.freq_mail = float(elem)
            elif j == 10:
                e.freq_receive = float(elem)
            elif j == 11:
                e.freq_will = float(elem)
            elif j == 12:
                e.freq_people = float(elem)
            elif j == 13:
                e.freq_report = float(elem)
            elif j == 14:
                e.freq_addresses = float(elem)
            elif j == 15:
                e.freq_free = float(elem)
            elif j == 16:
                e.freq_business = float(elem)
            elif j == 17:
                e.freq_email = float(elem)
            elif j == 18:
                e.freq_you = float(elem)
            elif j == 19:
                e.freq_credit = float(elem)
            elif j == 20:
                e.freq_your = float(elem)
            elif j == 21:
                e.freq_font = float(elem)
            elif j == 22:
                e.freq_000 = float(elem)
            elif j == 23:
                e.freq_money = float(elem)
            elif j == 24:
                e.freq_hp = float(elem)
            elif j == 25:
                e.freq_hpl = float(elem)
            elif j == 26:
                e.freq_george = float(elem)
            elif j == 27:
                e.freq_650 = float(elem)
            elif j == 28:
                e.freq_lab = float(elem)
            elif j == 29:
                e.freq_labs = float(elem)
            elif j == 30:
                e.freq_telnet = float(elem)
            elif j == 31:
                e.freq_857 = float(elem)
            elif j == 32:
                e.freq_data = float(elem)
            elif j == 33:
                e.freq_415 = float(elem)
            elif j == 34:
                e.freq_85 = float(elem)
            elif j == 35:
                e.freq_technology = float(elem)
            elif j == 36:
                e.freq_1999 = float(elem)
            elif j == 37:
                e.freq_parts = float(elem)
            elif j == 38:
                e.freq_pm = float(elem)
            elif j == 39:
                e.freq_direct = float(elem)
            elif j == 40:
                e.freq_cs = float(elem)
            elif j == 41:
                e.freq_meeting = float(elem)
            elif j == 42:
                e.freq_original = float(elem)
            elif j == 43:
                e.freq_project = float(elem)
            elif j == 44:
                e.freq_re = float(elem)
            elif j == 45:
                e.freq_edu = float(elem)
            elif j == 46:
                e.freq_table = float(elem)
            elif j == 47:
                e.freq_conference = float(elem)
            elif j == 48:
                e.freq_point_virgule = float(elem)
            elif j == 49:
                e.freq_parenthese = float(elem)
            elif j == 50:
                e.freq_bracket = float(elem)
            elif j == 51:
                e.freq_pt_exclamation = float(elem)
            elif j == 52:
                e.freq_dollar = float(elem)
            elif j == 53:
                e.freq_pound_sign = float(elem)
            elif j == 54:
                e.capital_len_average = float(elem)
            elif j == 55:
                e.capital_len_longest = float(elem)
            elif j == 56:
                e.capital_len_total = float(elem)
            elif j == 57:
                e.spam = int(elem)

            # affiche la ligne
            # print( elem )
            j+=1
        # print("\n")
        j=0
        e.save()
    
    return data

def index(request):
    # data = load_data()    # a decommenter pour charger le fichier dans la BDD !
    email_list = Email.objects.all()
    context = {'email_list': email_list}
    return render(request, 'emails/index.html', context)

def detail(request, email_id):
    email = get_object_or_404(Email, pk=email_id)
    return render(request, 'emails/detail.html', {'email': email})

def resultats(request, email_id):
    return HttpResponse("Results of email %s." % email_id)

