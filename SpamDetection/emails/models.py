from __future__ import unicode_literals
from django.db import models


class Email(models.Model):
    email_id = models.IntegerField( primary_key=True )
    # Floats
    freq_make = models.FloatField(default=0)
    freq_address = models.FloatField(default=0)
    freq_all = models.FloatField(default=0)
    freq_3d = models.FloatField(default=0)
    freq_our = models.FloatField(default=0)
    freq_over = models.FloatField(default=0)
    freq_remove = models.FloatField(default=0)
    freq_internet = models.FloatField(default=0)
    freq_order = models.FloatField(default=0)
    freq_mail = models.FloatField(default=0)
    freq_receive = models.FloatField(default=0)
    freq_will = models.FloatField(default=0)
    freq_people = models.FloatField(default=0)
    freq_report = models.FloatField(default=0)
    freq_addresses = models.FloatField(default=0)
    freq_free = models.FloatField(default=0)
    freq_business = models.FloatField(default=0)
    freq_email = models.FloatField(default=0)
    freq_you = models.FloatField(default=0)
    freq_credit = models.FloatField(default=0)
    freq_your = models.FloatField(default=0)
    freq_font = models.FloatField(default=0)
    freq_000 = models.FloatField(default=0)
    freq_money = models.FloatField(default=0)
    freq_hp = models.FloatField(default=0)
    freq_hpl = models.FloatField(default=0)
    freq_george = models.FloatField(default=0)
    freq_650 = models.FloatField(default=0)
    freq_lab = models.FloatField(default=0)
    freq_labs = models.FloatField(default=0)
    freq_telnet = models.FloatField(default=0)
    freq_857 = models.FloatField(default=0)
    freq_data = models.FloatField(default=0)
    freq_415 = models.FloatField(default=0)
    freq_85 = models.FloatField(default=0)
    freq_technology = models.FloatField(default=0)
    freq_1999 = models.FloatField(default=0)
    freq_parts = models.FloatField(default=0)
    freq_pm = models.FloatField(default=0)
    freq_direct = models.FloatField(default=0)
    freq_cs = models.FloatField(default=0)
    freq_meeting = models.FloatField(default=0)
    freq_original = models.FloatField(default=0)
    freq_project = models.FloatField(default=0)
    freq_re = models.FloatField(default=0)
    freq_edu = models.FloatField(default=0)
    freq_table = models.FloatField(default=0)
    freq_conference = models.FloatField(default=0)
    # Chars
    freq_point_virgule = models.FloatField(default=0)
    freq_parenthese = models.FloatField(default=0)
    freq_bracket = models.FloatField(default=0)
    freq_pt_exclamation = models.FloatField(default=0)
    freq_dollar = models.FloatField(default=0)
    freq_pound_sign = models.FloatField(default=0)
    # Capitals
    capital_len_average = models.FloatField(default=0) # average length of uninterrupted sequences of capital letters
    capital_len_longest = models.FloatField(default=0) # length of longest uninterrupted sequence of capital letters
    capital_len_total = models.FloatField(default=0) # total number of capital letters in the e-mail
    # Spam ?
    spam = models.IntegerField(default=0)

    def is_a_spam(self):
        return (self.spam == 1)

