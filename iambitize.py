#! /usr/bin/env python
"""
Filename: iambitize.py
Author: Emily Daniels
Date: May 2017
Purpose: Creates iambic pentameters out of text.
"""
import pronouncing
from sys import argv
import os
import re


class Iambitize(object):

    def __init__(self):
        self.iamb_pat = "0101010101"

    def phones_count(self, new_sent):
        try:
            phones = [pronouncing.phones_for_word(p)[0] for p in
                      new_sent.split()]
            return sum([pronouncing.syllable_count(p) for p in phones])
        except:
            return 0

    def cut_into_iamb(self, new_sent):
        count = 0
        cut_sent = ""
        sents = []
        for word in new_sent.split():
            pronunciations = pronouncing.phones_for_word(word)
            pat = pronouncing.stresses(pronunciations[0])
            cut_sent += word + " "
            count += len(pat)
            if count >= 10:
                sents.append(cut_sent)
                cut_sent = ""
                count = 0
        return sents

    def is_iambic(self, new_sent):
        sent_pat = ""
        for word in new_sent.split():
            pronunciations = pronouncing.phones_for_word(word)
            pat = pronouncing.stresses(pronunciations[0])
            sent_pat += pat
        if sent_pat == self.iamb_pat:
            return True
        else:
            return False

    def iambitize_text(self, text):
        sents = []
        iambic_sents = []
        for line in text:
            new_sent = re.sub(r'[^\w\s]', '', line)
            sent_phones = self.phones_count(new_sent)
            if sent_phones == 10:
                sents.append(new_sent)
            elif sent_phones > 10:
                cut_sents = self.cut_into_iamb(new_sent)
                for sent in cut_sents:
                    sents.append(sent)
        for sent in sents:
            if self.is_iambic(sent):
                iambic_sents.append(sent)
        return iambic_sents

    def write(self, text_file, sents):
        filename = 'Iambitized_' + os.path.splitext(
            os.path.basename(text_file))[0] + '.txt'
        with open(filename, "w") as f:
            for sent in sents:
                f.write("%s\n" % sent)

if __name__ == "__main__":
    book = argv
    print("Importing source text...")
    with open(book[1], "rU") as f:
        t = f.read()
    text = t.split("\n")
    print("Finding iambic pentameters...")
    iambitize = Iambitize()
    sents = iambitize.iambitize_text(text)
    print("Writing to file...")
    iambitize.write(book[1], sents)


