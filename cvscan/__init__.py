#!/usr/bin/env python
"""

Main program

"""
import os
import converter
import annotations_parser
import details_parser as dp
import language_parser as lp
import json
import dirpath
import configurations

class Cvscan():
    def __init__(self, name, path = dirpath.RESUMEPATH):
        self.path = path + '/' + name + '.pdf'
        self.path = name + '.pdf'

        if self.exists():
            self.extract()
        else:
            raise OSError("There is no file found at " + self.path)

    def exists(self):
        return configurations.isfile(self.path)

    # Extracts raw text from resume
    # Currently only supports PDF
    def extract(self):
        # add functions to convert other formats to text
        if self.path.find(".pdf") != -1:
            self.raw_text = converter.pdf_to_txt(self.path)

        if self.raw_text is not '':
            self.parse()
        else:
            raise ValueError("Error extracting resume text.")

    def parse(self):
        self.URLs = annotations_parser.fetch_pdf_urls(self.path)
        self.name = lp.fetch_name(self.raw_text)
        self.emails = dp.fetch_email(self.raw_text)
        self.phone_numbers = dp.fetch_phone(self.raw_text)
        self.address = dp.fetch_address(self.raw_text)
        self.experience = dp.calculate_experience(self.raw_text)
        self.cleaned_resume = lp.clean_resume(self.raw_text)
        self.skills = dp.fetch_skills(self.cleaned_resume)
        (self.qualifications,self.degree_info) = dp.fetch_qualifications(
            self.raw_text)
        self.job_positions, self.category = dp.fetch_jobs(self.cleaned_resume)
        self.current_employers,self.employers = lp.fetch_employers(
            self.raw_text,self.job_positions)
        self.extra_info = dp.fetch_extra(self.raw_text)

    # TODO: Add more fetch here
    def show(self):
        return {
            "name" : self.name,
            "experience" : self.experience,
            "address" : self.address,
            "phone_numbers" : self.phone_numbers,
            "emails" : self.emails,
            "urls" : self.URLs,
            "skills" : self.skills,
            "jobs" : self.job_positions,
            "job category" : self.category,
            "employers" : self.employers,
            "current_employers" : self.current_employers,
            "qualifications" : self.qualifications,
            "qualifications_info" : self.degree_info,
            "extra_info" : self.extra_info
        }
'''
scan = Cvscan("Resume")
result = scan.show()
for key, value in result.items():
    print("{} = {}\n".format(key, value))
'''

def isPassed():
    os.chdir("D:\\Workspace\\Python\\cvscan-master\\cvscan")
    num = int(input("Enter number of skills "))
    skills = list()
    optional = list()
    for i in xrange(num):
        skills.append(str(raw_input()))
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    files = filter(lambda f: f.endswith(('.pdf','.PDF')), files)
    for i in xrange(len(files)):
        cfile = files[i]
        state = True
        scan = Cvscan(cfile.split('.')[0])
        result = scan.show()
        keywords = result["skills"]
        keywords.extend(result["qualifications"])
        for i in xrange(len(skills)):
            if skills[i] not in keywords:
                state = False
                break
        if state and len(skills) != 0:
            os.rename("D:\\Workspace\\Python\\cvscan-master\\cvscan\\" + cfile, "D:\\Workspace\\Python\\cvscan-master\\cvscan\\Selected\\" + cfile)


isPassed()
