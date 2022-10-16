from datetime import datetime
from gedcom import individual;
from gedcom import family;
from prettytable import PrettyTable;

from enum import Enum;

SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60;
DATE_FORMAT = "%Y-%m-%d";

global US11_Problems;
class EUS11_FAILURE(Enum):
    US11_FAIL_HUSB_MULTMARR = 0,
    US11_FAIL_WIFE_MULTMARR = 1

class cUS11_Failure:
    hIndividual = None;
    SpouseIDs = None;

    Failure_Type = None;

    def __init__(self):
        self.hIndividual = None;
        self.SpouseIDs = [];
        self.Failure_Type = None;

def US11_Test(hParser):
    global US11_Problems;

    US11_Problems = [];
    US11_Problems.clear();

    # Log 2(O^2) ???    :(
    for i in hParser.families:
        if ( (hParser.families[i].married == True) and (hParser.families[i].divorced == False) ):
            id = hParser.families[i].id;
            Husb = hParser.individuals[hParser.families[i].husband_id];
            Wife = hParser.individuals[hParser.families[i].wife_id];

            US11_Failure_HUSB = cUS11_Failure();
            US11_Failure_WIFE = cUS11_Failure();

            for j in hParser.families:
                if (i != j):
                    if ( (hParser.families[j].married == True) and (hParser.families[j].divorced == False) ):
                        Husb2 = hParser.individuals[hParser.families[j].husband_id];
                        Wife2 = hParser.individuals[hParser.families[j].wife_id];

                        if (Husb.id == Husb2.id):
                            US11_Failure_HUSB.hIndividual = Husb;
                            US11_Failure_HUSB.SpouseIDs.append(Wife);
                            US11_Failure_HUSB.Failure_Type = EUS11_FAILURE.US11_FAIL_HUSB_MULTMARR;

                        if (Wife.id == Wife2.id):
                            US11_Failure_WIFE.hIndividual = Wife;
                            US11_Failure_WIFE.SpouseIDs.append(Husb);
                            US11_Failure_WIFE.Failure_Type = EUS11_FAILURE.US11_FAIL_WIFE_MULTMARR;

            if (len(US11_Failure_HUSB.SpouseIDs) > 0):
                US11_Problems.append(US11_Failure_HUSB);

            if (len(US11_Failure_WIFE.SpouseIDs) > 0):
                US11_Problems.append(US11_Failure_WIFE);

def US11_DisplayResults():
    global US11_Problems;

    print ("");
    print ("US11 test failures:");

    pt = PrettyTable();
    pt.field_names = [
        "ID",
        "Name",
        "Spouses",
        "Failure type"
    ];

    #for i in US11_Problems:
    for i in range(0, len(US11_Problems)):
        Spouses = "";
        for j in range(0, len(US11_Problems[i].SpouseIDs)):
            Spouses += (US11_Problems[i].SpouseIDs[j].name) + " ";

        Spouses = Spouses[:-1];

        pt.add_row(
            [
                US11_Problems[i].hIndividual.id,
                US11_Problems[i].hIndividual.name,
                Spouses,
                str(US11_Problems[i].Failure_Type)
            ]
        );

    #pt.sortby = "ID"

    print (pt.get_string());
    return pt.get_string();

def Execute(hParser):
    US11_Test(hParser);
    return US11_DisplayResults();