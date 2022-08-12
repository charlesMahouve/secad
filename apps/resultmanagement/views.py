from charset_normalizer import md
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.rules_management.models import AdminFileManager
from apps.rules_management.views import all_rules_interpreter, all_cis_recos_interpreter, all_report_interpreter,\
    all_recos_interpreter
from django.http import HttpResponse
from calendar import c
from fnmatch import fnmatch
from glob import glob
import html
import os
from os import path
import json
import datetime
import base64
import argparse
import fnmatch
import re
import csv
from json2html import *

rules_reports_recos = AdminFileManager.objects.get(pk=1)
all_cis_recos = all_cis_recos_interpreter(rules_reports_recos.all_cis_recos)
recos_anssi = all_recos_interpreter(rules_reports_recos.recos_anssi)
recos_cert = all_recos_interpreter(rules_reports_recos.recos_cert)
report_adds = all_report_interpreter(rules_reports_recos.report_adds)
report_anssi = all_report_interpreter(rules_reports_recos.report_anssi)
report_cert = all_report_interpreter(rules_reports_recos.report_cert)
report_dhcp = all_report_interpreter(rules_reports_recos.report_dhcp)
report_gpo = all_report_interpreter(rules_reports_recos.report_gpo)
rules_adds = all_rules_interpreter(rules_reports_recos.rules_adds)
rules_anssi = all_rules_interpreter(rules_reports_recos.rules_anssi)
rules_cert = all_rules_interpreter(rules_reports_recos.rules_cert)
rules_dhcp = all_rules_interpreter(rules_reports_recos.rules_dhcp)


@login_required
def inventaire_des_strategies_de_groupe2(request):

    context = {
    }
    return render(request, 'results/inventaire_des_strategies_de_groupe.html', context)


@login_required
def inventaire_des_strategies_de_groupe(request):
    def getGPOElement(element):
        attribs = {}
        if element.hasAttributes():
            attr = ""
            for i in range(element.attributes.length):
                attr = element.attributes.item(i)
                doMatch = re.match("xmlns.*|xsi.*|clsid.*", attr.name)
                if not doMatch:
                    re_outer = re.compile(r'([^A-Z ])([A-Z])')
                    re_inner = re.compile(r'(?<!^)([A-Z])([^A-Z])')
                    xx = re_outer.sub(r'\1 \2', re_inner.sub(r' \1\2', str(attr.localName)))
                    if len(attr.value) > 255:
                        attribs.update({xx: "<mark>TRUNCATED: " + attr.value[:20] + "...</mark>"})
                    else:
                        attribs.update({xx: attr.value})

        if element.hasChildNodes():
            cn = element.childNodes
            if len(cn) == 1:
                if attribs != {}:
                    obj = []
                    obj.append(attribs)
                    obj.append({"<mark>value</mark>": cn[0].nodeValue})
                    return obj
                else:
                    if cn[0].nodeValue.find(" ") == -1 and len(cn[0].nodeValue) > 255:
                        return "<mark>TRUNCATED: " + cn[0].nodeValue[:20] + "...</mark>"
                    else:
                        return cn[0].nodeValue
            else:
                obj = {}
                last = ""
                if attribs != {}:
                    obj = attribs
                for node in cn:
                    re_outer = re.compile(r'([^A-Z ])([A-Z])')
                    re_inner = re.compile(r'(?<!^)([A-Z])([^A-Z])')
                    xx = re_outer.sub(r'\1 \2', re_inner.sub(r' \1\2', str(node.localName)))
                    if xx == last:
                        if node.nodeType != node.TEXT_NODE:
                            arr = []
                            if type(obj[xx]) is dict:
                                arr = [obj[xx]]
                            elif type(obj[xx]) is str:
                                arr = [obj[xx]]
                            else:
                                arr = obj[xx]
                            arr.append(getGPOElement(node))
                            obj.update({xx: arr})
                    else:
                        if node.nodeType != node.TEXT_NODE:
                            label = xx
                            if label.startswith("Setting") and label != "Settings":
                                label = "Setting"
                            if label in ["Extension Data", "Links To"]:
                                obj.update({label: [getGPOElement(node)]})
                            else:
                                obj.update({label: getGPOElement(node)})
                            last = label
                if element.localName == "Member" and len(obj) == 1:
                    obj.update({"Name": "<code>unknown user</code>"})
                if element.localName == "RegistrySetting" and len(obj) == 2:
                    obj.update({"Value": ""})
                return obj

        else:
            if attribs != {}:
                return attribs
            else:
                return []

    datetime_format = "%Y-%m-%dT%H:%M:%S"

    # Récupération des paramètres de la ligne de commande
    parser = argparse.ArgumentParser("Build GPO Report")
    parser.add_argument("Client", type=str, help="Nom du client")
    parser.add_argument("Folder", type=str, help="Répertoire qui contient les fichiers xml")
    parser.add_argument("--Rapports", type=str, help="Répertoire où est créé le rapport HTML")
    parser.add_argument("--Language", type=str, help="Langue du rapport", default="fr")
    parser.add_argument("--Logo", type=str, help="Emplacement du fichier qui contient le logo du client")
    parser.add_argument("--DR", help="Document tagué DIFFUSION RESTREINTE", action="store_true")
    parser.add_argument("--DP", help="Document tagué DIFFUSION PROTEGEE", action="store_true")
    args = parser.parse_args()
    myDir = args.Folder
    myClient = args.Client
    language = args.Language

    comp_labels = {
        "en": ["Compliant", "To check", "Non compliant"],
        "fr": ["Conforme", "A vérifier", "Non conforme"]
    }

    detail_labels = {
        "en": ["Domain", "Links", "No linkks", "Computer extensions", "No computer extension", "User extensions",
               "No user extensions", "Security descriptor"],
        "fr": ["Domaine", "Liaisons", "Aucune liaison", "Paramètres ordinateur", "Aucun paramètre ordinateur",
               "Paramètres utilisateur", "Aucun paramètre utilisateur", "Descripteur de sécurité"]
    }

    title_labels = {
        "en": ["GPO inventory", "Group policies objects inventory", "Policies", "Statistics", "Context"],
        "fr": ["Inventaire GPO", "Inventaire des stratégies de groupe", "Stratégies", "Statistiques", "Contexte"]
    }

    match language:
        case "en":
            stats_labels = {
                "NoLinks": "No links",
                "ComputerExtensions": "Computer Extensions",
                "UserExtensions": "User Extensions",
                "NotDefined": "Not Defined"
            }
            doc_conf = "CONFIDENTIAL"
            if args.DR:
                doc_conf = "RESTRICTED"
            if args.DP:
                doc_conf = "PROTECTED DIFFUSION"
        case "fr":
            stats_labels = {
                "Empty": "Vides",
                "Policies": "Stratégies",
                "NoLinks": "Pas de liaison",
                "ComputerExtensions": "Paramètres ordinateurs",
                "UserExtensions": "Paramètres utilisateus",
                "Disabled": "Désactivés",
                "Defined": "Définis",
                "Activated": "Activés",
                "NotDefined": "Non définis",
                "Themes": "Thèmes"
            }
            doc_conf = "CONFIDENTIEL"
            if args.DR:
                doc_conf = "DIFFUSION RESTREINTE"
            if args.DP:
                doc_conf = "DIFFUSION PROTEGEE"

    lbl_emp = "Empty"
    if lbl_emp in stats_labels.keys():
        lbl_emp = stats_labels[lbl_emp]
    lbl_ce = "ComputerExtensions"
    if lbl_ce in stats_labels.keys():
        lbl_ce = stats_labels[lbl_ce]
    lbl_ue = "UserExtensions"
    if lbl_ue in stats_labels.keys():
        lbl_ue = stats_labels[lbl_ue]
    lbl_pol = "Policies"
    if lbl_pol in stats_labels.keys():
        lbl_pol = stats_labels[lbl_pol]
    lbl_nl = "NoLinks"
    if lbl_nl in stats_labels.keys():
        lbl_nl = stats_labels[lbl_nl]
    lbl_dis = "Disabled"
    if lbl_dis in stats_labels.keys():
        lbl_dis = stats_labels[lbl_dis]
    lbl_def = "Defined"
    if lbl_def in stats_labels.keys():
        lbl_def = stats_labels[lbl_def]
    lbl_act = "Activated"
    if lbl_act in stats_labels.keys():
        lbl_act = stats_labels[lbl_act]
    lbl_nd = "NotDefined"
    if lbl_nd in stats_labels.keys():
        lbl_nd = stats_labels[lbl_nd]

    stats = {
        "Total": 0,
        lbl_emp: {
            "Total": 0,
            lbl_pol: []
        },
        lbl_nl: {
            "Total": 0,
            lbl_pol: []
        },
        lbl_ce: {
            lbl_dis: 0,
            lbl_def: [],
            lbl_act: 0,
            lbl_nd: []
        },
        lbl_ue: {
            lbl_dis: 0,
            lbl_def: [],
            lbl_act: 0,
            lbl_nd: []
        },
        "Themes": {}
    }

    logo = ""
    if args.Logo:
        file_logo = args.Logo
        with open(file_logo, "rb") as img_file:
            logo = base64.b64encode(img_file.read()).decode("utf-8")

    # Lecture des fichiers XML
    result = []
    WHEN = ""
    context = {}
    print("Lecture des fichiers XML du répertoire \033[92m{0}\033[0m...".format(myDir))
    for file in os.listdir(myDir):
        # print(file)
        if file.endswith(".xml"):
            print("FICHIER: \033[93m{0}\033[0m".format(os.path.join(myDir, file)))
            doc = md.parse(os.path.join(myDir, file))
            if WHEN == "":
                WHEN = datetime.datetime.fromtimestamp(os.path.getctime(os.path.join(myDir, file))).strftime("%d/%m/%Y")
                # print(WHEN)
            oneGPO = {}
            gpo = doc.childNodes[0]
            cn = gpo.childNodes
            last = ""
            for node in cn:
                re_outer = re.compile(r'([^A-Z ])([A-Z])')
                re_inner = re.compile(r'(?<!^)([A-Z])([^A-Z])')
                xx = re_outer.sub(r'\1 \2', re_inner.sub(r' \1\2', str(node.localName)))
                if xx == last:
                    if node.nodeType != node.TEXT_NODE:
                        arr = []
                        if type(oneGPO[xx]) is dict:
                            arr = [oneGPO[xx]]
                        else:
                            arr = oneGPO[xx]
                        arr.append(getGPOElement(node))
                        oneGPO.update({xx: arr})
                else:
                    if node.nodeType != node.TEXT_NODE:
                        oneGPO.update({xx: getGPOElement(node)})
                        last = xx
            result.append({"GPO": oneGPO})
        if file == "Context.csv":
            ori_context = {}
            reader = csv.DictReader(open(os.path.join(myDir, file), "r", encoding="utf-8"))
            ori_context = dict(list(reader)[0])
            for k, v in ori_context.items():
                # Traitement des caractères chelous
                l = k.split('"')[1::2]
                if l:
                    context[l[0]] = v.replace(";", "<br>")
                else:
                    context[k] = v.replace(";", "<br>")

    stats["Total"] = len(result)
    print("Lecture terminée : {0} fichiers.".format(len(result)))

    # Création d'un fichier json -- Mode DEBUG
    # f = open("D:\SCRIPTS\KEEAD\gpo.json", "w")
    # f.write(json.dumps(result, indent=4))
    # f.close()

    datetime_format_re = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    # Traitement des gpo
    all = []
    theDomain = ""
    bm = 0
    nb_ec = nb_dc = nb_eu = nb_du = nb_e = nb_nl = 0
    nb_c = nb_n = nb_w = 0
    ref_c = []
    ref_nc = []
    ref_u = []
    ref_nu = []
    ref_e = []
    ref_nl = []

    for gpo in result:
        compliant = "C"
        bm += 1
        created = datetime.datetime.strptime(gpo["GPO"]["Created Time"], datetime_format).strftime("%d/%m/%Y")
        modified = datetime.datetime.strptime(gpo["GPO"]["Modified Time"], datetime_format).strftime("%d/%m/%Y")

        # Paramètres Ordinateur
        comp = gpo["GPO"]["Computer"]["Enabled"]
        comp_ext = {}
        if "Extension Data" in gpo["GPO"]["Computer"]:
            for ext in gpo["GPO"]["Computer"]["Extension Data"]:
                if "Extension" in ext:
                    if len(ext["Extension"]) == 0:
                        comp_ext[ext["Name"]] = "<code>empty</code>"
                    else:
                        comp_ext[ext["Name"]] = ext["Extension"]
                if "Error" in ext:
                    comp_ext["<span class=\"bg-danger text-white\">" + ext["Name"] + "</span>"] = ext["Error"]
                    compliant = "W"

        # Paramètres Utilisateur
        user = gpo["GPO"]["User"]["Enabled"]
        user_ext = {}
        if "Extension Data" in gpo["GPO"]["User"]:
            for ext in gpo["GPO"]["User"]["Extension Data"]:
                if "Extension" in ext:
                    if len(ext["Extension"]) == 0:
                        comp_ext[ext["Name"]] = "<code>empty</code>"
                    else:
                        user_ext[ext["Name"]] = ext["Extension"]
                if "Error" in ext:
                    user_ext["<span class=\"bg-danger text-white\">" + ext["Name"] + "</span>"] = ext["Error"]
                    compliant = "W"

        # Descritpeur de sécurité
        secd = []
        try:
            secd = gpo["GPO"]["Security Descriptor"]
        except:
            secd = []

        # Liens
        links = []
        try:
            links = gpo["GPO"]["Links To"]
            if type(links) != list:
                links = [gpo["GPO"]["Links To"]]
        except:
            links = []

        # Conformité des paramètres Ordinateur
        if (comp == 'true' and len(comp_ext) > 0) or (comp == 'false' and len(comp_ext) == 0):
            sComp = "<div class=\"text-center text-white bg-success\">" + comp + "</div>"
        else:
            sComp = "<div class=\"text-center text-black bg-warning\">" + comp + "</div>"
            if compliant != "N":
                compliant = "W"
        if comp == 'false' and len(comp_ext) > 0:
            nb_dc += 1
            ref_c.append(gpo["GPO"]["Name"])
            if compliant != "N":
                compliant = "W"
        if comp == 'true' and len(comp_ext) == 0:
            nb_ec += 1
            ref_nc.append(gpo["GPO"]["Name"])
            compliant = "N"

        # Conformtité des paramètres Utilisateur
        if (user == 'true' and len(user_ext) > 0) or (user == 'false' and len(user_ext) == 0):
            sUser = "<div class=\"text-center text-white bg-success\">" + user + "</div>"
        else:
            sUser = "<div class=\"text-center text-black bg-warning\">" + user + "</div>"
            if compliant != "N":
                compliant = "W"
        if user == 'false' and len(user_ext) > 0:
            nb_du += 1
            ref_u.append(gpo["GPO"]["Name"])
            if compliant != "N":
                compliant = "W"
        if user == 'true' and len(user_ext) == 0:
            nb_eu += 1
            ref_nu.append(gpo["GPO"]["Name"])
            compliant = "N"

        # Conformité des liaisons
        if len(links) > 0:
            sLinks = "<div class=\"text-center text-white bg-success\">" + str(len(links)) + "</div>"
        else:
            nb_nl += 1
            ref_nl.append(gpo["GPO"]["Name"])
            sLinks = "<div class=\"text-center text-black bg-warning\">0</div>"
            if compliant != "N":
                compliant = "W"

        # Détail GPO
        gpo_detail = "<div class=\"alert alert-info\">"
        gpo_detail += "{0} = {1} - ID = {2}".format(detail_labels[language][0], gpo["GPO"]["Identifier"]["Domain"],
                                                    gpo["GPO"]["Identifier"]["Identifier"])
        gpo_detail += "</div>"
        if theDomain == "":
            theDomain = gpo["GPO"]["Identifier"]["Domain"]
        gpo_detail += "<h4>{0}</h4><div class=\"card border-dark p-3 mb-3\">".format(detail_labels[language][1])
        if len(links) > 0:
            gpo_detail += "<div class=\"card-body\">\n"
            table_attributes = "class=\"table table-bordered table-striped table-hover table-sm\""
            gpo_detail += json2html.convert(json=links, table_attributes=table_attributes, escape=False)
            gpo_detail += "</div>\n"
        else:
            gpo_detail += "<h5 class=\"bg-warning\" m-3>{0}</h5>".format(detail_labels[language][2])
        gpo_detail += "</div>"
        gpo_detail += "<h4>{0}</h4><div class=\"card border-dark p-3 mb-3\">".format(detail_labels[language][3])
        if len(comp_ext) > 0:
            for k, v in comp_ext.items():
                gpo_detail += "<div class=\"card border-dark mb-3\">"
                gpo_detail += "<div class=\"card-body\"><h5 class=\"text-primary\">" + k + "</h5><div class=\"table-responsive\">"
                table_attributes = "class=\"table table-bordered table-striped table-hover table-sm\""
                gpo_detail += json2html.convert(json=v, table_attributes=table_attributes, clubbing=True, escape=False)
                gpo_detail += "</div></div></div>\n"
                if k not in stats["Themes"].keys():
                    stats["Themes"][k] = [gpo["GPO"]["Name"] + " (C)"]
                else:
                    arr = []
                    arr = stats["Themes"][k]
                    arr.append(gpo["GPO"]["Name"] + " (C)")
                    arr.sort()
                    stats["Themes"][k] = arr
        else:
            gpo_detail += "<h5 class=\"bg-warning\" m-3>{0}</h5>".format(detail_labels[language][4])
        gpo_detail += "</div>"
        gpo_detail += "<h4>{0}</h4><div class=\"card border-dark p-3 mb-3\">".format(detail_labels[language][5])
        if len(user_ext) > 0:
            for k, v in user_ext.items():
                gpo_detail += "<div class=\"card border-dark mb-3\">"
                gpo_detail += "<div class=\"card-body\"><h5 class=\"text-primary\">" + k + "</h5><div class=\"table-responsive\">"
                table_attributes = "class=\"table table-bordered table-striped table-hover table-sm\""
                gpo_detail += json2html.convert(json=v, table_attributes=table_attributes, clubbing=True, escape=False)
                gpo_detail += "</div></div></div>\n"
                if k not in stats["Themes"].keys():
                    stats["Themes"][k] = [gpo["GPO"]["Name"] + " (U)"]
                else:
                    arr = []
                    arr = stats["Themes"][k]
                    arr.append(gpo["GPO"]["Name"] + " (U)")
                    arr.sort()
                    stats["Themes"][k] = arr
        else:
            gpo_detail += "<h5 class=\"bg-warning\" m-3>{0}</h5>".format(detail_labels[language][6])
        gpo_detail += "</div>"
        gpo_detail += "<h4>{0}</h4><div class=\"card border-dark mb-3\">".format(detail_labels[language][7])
        if len(secd) > 0:
            gpo_detail += "<div class=\"card-body\">\n"
            table_attributes = "class=\"table table-bordered table-striped table-hover table-sm\""
            gpo_detail += json2html.convert(json=secd, table_attributes=table_attributes, clubbing=True, escape=False)
            gpo_detail += "</div>\n"
        else:
            gpo_detail += "<h5 class=\"bg-warning\" m-3>No Security descriptors</h5>"
        gpo_detail += "</div>"

        if len(comp_ext) == 0 and len(user_ext) == 0:
            nb_e += 1
            ref_e.append(gpo["GPO"]["Name"])
            name = "<div class=\"text-black bg-warning\" title=\"The gpo is empty !\">" + gpo["GPO"]["Name"] + "</div>"
        else:
            name = gpo["GPO"]["Name"]

        match language:
            case "en":
                obj = {
                    "Detail": "",
                    "Name": "<span id=\"BM" + str(bm) + "\">" + name + "</span>",
                    "Created": created,
                    "Modified": modified,
                    "Computer enabled": sComp,
                    "Computer extensions": "<br>".join(comp_ext.keys()),
                    "User enabled": sUser,
                    "User extensions": "<br>".join(user_ext.keys()),
                    "Links To": sLinks,
                    "Compliant": compliant,
                    "Child": gpo_detail
                }
            case "fr":
                obj = {
                    "Détail": "",
                    "Nom": "<span id=\"BM" + str(bm) + "\">" + name + "</span>",
                    "Création": created,
                    "Modification": modified,
                    "Paramètres ordinateur activés": sComp,
                    "Paramètres ordinateur": "<br>".join(comp_ext.keys()),
                    "Paramètres utilisateur activés": sUser,
                    "Paramètres utilisateur": "<br>".join(user_ext.keys()),
                    "Liaisons": sLinks,
                    "Compliant": compliant,
                    "Child": gpo_detail
                }

        all.append(obj)
        if compliant == "C":
            nb_c += 1
        if compliant == "N":
            nb_n += 1
        if compliant == "W":
            nb_w += 1

    # Création des statistiques
    ref_c.sort()
    ref_nc.sort()
    ref_u.sort()
    ref_nu.sort()
    ref_e.sort()
    ref_nl.sort()

    stats[lbl_ce][lbl_dis] = "<span class=\"bg-warning text-black p-1\">" + str(nb_dc) + "</span>"
    stats[lbl_ce][lbl_def] = ref_c
    stats[lbl_ce][lbl_act] = "<span class=\"bg-danger text-white p-1\">" + str(nb_ec) + "</span>"
    stats[lbl_ce][lbl_nd] = ref_nc
    stats[lbl_ue][lbl_dis] = "<span class=\"bg-warning text-black p-1\">" + str(nb_du) + "</span>"
    stats[lbl_ue][lbl_def] = ref_u
    stats[lbl_ue][lbl_act] = "<span class=\"bg-danger text-white p-1\">" + str(nb_eu) + "</span>"
    stats[lbl_ue][lbl_nd] = ref_nu
    stats[lbl_emp]["Total"] = "<span class=\"bg-warning text-black p-1\">" + str(nb_e) + "</span>"
    stats[lbl_emp][lbl_pol] = ref_e
    stats[lbl_nl]["Total"] = "<span class=\"bg-warning text-black p-1\">" + str(nb_nl) + "</span>"
    stats[lbl_nl][lbl_pol] = ref_nl

    # Création du document
    title = myClient + " - " + title_labels[language][0]
    page_head = "<head><title>{0}</title>\n<meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">".format(
        title)
    page_head += "<link rel=\"icon\" href=\"data:image/x-icon;base64,AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAAMMOAADDDgAAAAAAAAAAAAD////////////////9/f///Pz////////9/f///Pz+///////9/f///Pz///z8///9/f////////z8/v/9/f///Pz+//7+///8/P///Pz///7+///8/P///Pz///7+///8/P7//Pz+//z7/v/9/f///////////////////////////////////////////////////fz///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////39////////s7Hz/5WS7v//////xsX2/3p26v/o6Pv/z833/4mG7P+Gg+z/xsT2//z8//+mpPH/h4Ts/5KP7f/m5fv/lJHu/7Cu8v/p6fv/sK7y/5KP7f/Z2Pn/iofs/4J+6/+Miez/3Nv5///////+/v///////////////////Pz///////99eur/Lijd/7i29P9CPeD/bmro//Hx/f86Nd//g4Dr/4aD6/94den/qafx/zUw3v+mpPH/YFzl/66s8v+Ihez/LSfd/2xo5/8uKN3/fXnq/9LQ+P8hG9v/kI3t/2xo5/9BPOD/7Oz8///+///+/v/////////////8/P///////4uI7P89OOD/NC7e/0pG4v//////9vX9/0E84P9xbej/Xlrl/2to5/+1s/P/NC/e/4mG7P88N+D/ravy/+np/P8/OuD/qafx/z044P/e3vr/2dj5/y8p3f/29v3/4eH6/yQe3P/R0Pj///////39//////////////z8////////d3Pp/0lE4v+3tfP/My7e/5KP7f/6+v7/1dT4/5aT7v+al+//4N/6//////+1s/P/kI3t/6yq8f/29v7//////29r6P8jHdv/Y1/m///////Fw/b/Ihzb/3d06f9XU+T/Uk7j//Ly/f/+/v///v7//////////////v7////////Hxvb/srDz///////My/f/o6Hw//T0/f/////////////////////////////////////////////////+/v//3Nv5/5mW7v/W1Pj//////+zt/P+urPL/qKbx/66s8v/v7vz///////7+//////////////////////////7//////////v//19L4//Dt/P/08f3/6OX7//////////////////z8/v/8/P7/6eb5/9rY9P/q6Pn//Pz+//39///////////////////l4fr/6eX7//Pw/f/o5Pv////////////+/v/////////////////////////////+/v///Pz+/+7s/P+Lfer/NyDb/0Is3f9HMd7/eWnn/8O89P/y8f3///////////+Edtf/EwCz/5OH2////////////+7t/P+6s/P/cWDl/0Yx3f9DLd3/OSLb/5GF6//x8P3//f3///7+//////////////////////////////////////////////////+upPD/Pifc/0Eq3P87JNv/OiPb/0453/9xYOX/lIfs/2BO2f8rFcj/aFbb/5SI7P9uXeT/TDfe/zki2/89Jtz/Pyjc/0Uw3f+/uPP////////////////////////////////////////////////////////////+/v///fz////////GwPX/RC7d/0Mt3f9JNN7/Uz/g/zcg2/8sFNn/PCXe/0s14/86I93/LRTZ/zsj2/9UQOD/STPe/0Eq3P9NON//1dD3///////8/P7/////////////////////////////////////////////////////////////////+/v+///////LxPX/Qyzd/zsk2/+Rhev/4t/6/8S99P9pV9n/JxHF/3Rj3P/IwvX/5eH6/4d56f85Idv/SzXe/9nV+P//////+/v+////////////////////////////////////////////////////////////////////////////+/v+//////++tvP/OyTb/zwl3P/BuvP//////4N11v8PALH/k4ba//////+zqvH/OCDb/0Eq3P/Nx/b///////z7/v//////////////////////////////////////////////////////////////////////////////////////+/v+//////+dke3/MxvZ/0043v/RzPf/d2jY/yAMvf+Edtz/zcf2/0Yw3P81Hdr/rqTw///////7+/7////////////////////////////////////////////////////////////////////////////////////////////+/v///Pz///39//9sW+b/Lxfd/zUe3v84Id7/OiLf/zgh3v81Ht3/LBbc/3hs5//9//3/+Pv9//7+/v/////////////////////////////////////////////////////////////////////////////////////////////////9/f7//////9nU7P+JetL/koTW/5CB1f+QgdX/j4HV/5CD1f+Ufdb/8uH2//////////////////z+/v//////////////////////////////////////////////////////////////////////////////////////////////////////6uXa/+fhyv/m4M3/5uDM/+XfzP/q4s3/8+TQ/8Dcuv+N07L/jN7A/6zn0P/x+/j///////3+/v/////////////////////////////////////////////////////////////////////////////////////////////////h29X/2dHI/+bgzf/k3sz/59/N/9rVzP9SwJf/ALV2/wCvZ/8AsGj/ALVx/x++g/+z6tf///////3+/v///////////////////////////////////////////////////////////////////////////////////////v7///Tx7v/a1Nz/opXT/6OY0v+tl9f/SLeY/wC3bf8Asm3/e9q4/0PKmv8As23/ALd1/wS3df/P8eX///////3+/v/////////////////////////////////////////////////////////////////////////////////+/v////////Hw//8/KuD/Lg/i/yot0v8Asnj/Crl2/5/jy//W8+n/4ffv/1rQpP8As23/ALNt/2XUrP//////+/79///////////////////////////////////////////////////////////////////////////////////////+/v7//////7au3v+lj9b/g57C/wC3c/8Ou3//gdy8/wC3dv8tw4v/5vjy/4Lbu/8Fs23/T82g///////8/v3//////////////////////////////////////////////////////////////////////////////////////////v//////9/Xh//XtyP/h6sb/FcN6/wC4df8As27/Abh4/wC0b/8Zv4T/rOjT/wS3dP922bX///////v+/f///////////////////////////////////////////////////////////////////////////////////////f3+///////Vz+7/in3S/5+G3P9Ija7/ALRt/wC3df8AuHf/Arl5/wC2dP8ArWP/I8CH/+r59P/+//7//v/+///////////////////////////////////////////////////////////////////////////////////////9/P///////8jC9/8nD97/Lxnf/zsa4/97usb/LMqK/wO2d/8At3X/D7p7/1vPpP/j9/D///////7//v////////////////////////////////////////////////////////////////////////////////////////////7+////////6uj6/3hn2f92Zdf/dmfY//rt///9//3/2PPp/9Dx5f/l9/D////////////+//7///////////////////////////////////////////////////////////////////////////////////////////////////////////////n/8e3P/+3ny//y7dD//f/5///////////////////////9/v7//f/+///////////////////////////////////////////////////////////////////////////////////////////////////////+/v///////+rn9P+9s9//x77i/7603//r6PX//v////z9/f/9/v7//f/+//////////////////////////////////////////////////////////////////////////////////////////////////////////////////38////////y8X2/0cy3v9CLN3/RzLf/87J9v///////f3///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////7+////////5uP6/1M/4P/i3vn///////7+/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////v7////////y8P3/VEDg/+7s/P///////v7///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////r6/v/Cu/T/+fj+////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=\">"
    files_style = ["bootstrap-5.1.3-dist/css/bootstrap.min.css",
                   "DataTables/DataTables-1.11.3/css/dataTables.bootstrap5.min.css",
                   "DataTables/Buttons-2.0.1/css/buttons.bootstrap5.min.css", "keeAD.css"]
    for file in files_style:
        f = open("files/" + file, "r", encoding="utf8")
        page_head += "<style type=\"text/css\">"
        page_head += f.read()
        page_head += "</style>\n"
        f.close
    page_head += "<style>body { position:relative; font-family:\"Trebuchet MS\",sans-serif; }</style>\n"
    page_head += "</head>\n"

    page_header = "<div class=\"container-fluid\">"
    page_header += "<div class=\"d-flex justify-content-between mb-3\">"
    if logo:
        page_header += "<div class=\"p-2 mr-3\" ><img class=\"bg-secondary\" src=\"data:image/png;base64,{0}\" title=\"{1}\" alt=\"logo client\" style=\"width:50%;\"></div>\n".format(
            logo, myClient)
    else:
        page_header += "<h1 class=\"bg-light text-black p-3 mr-3\">{0}</h1>\n".format(myClient)
    page_header += "<div class=\"p-1\"><h1><span class=\"badge bg-primary\">{0}</span></h1>".format(
        title_labels[language][1])
    page_header += "<h6 class=\"text-center\"><span class=\"badge bg-primary\">{0}</span>  <span class=\"badge bg-secondary\">{1}</span></h6>\n</div>\n".format(
        theDomain, WHEN)
    page_header += "<div class=\"p-2\"><div class=\"border border-5 border-danger rounded\"><div class=\"myconf text-danger m-1\">{0}</div>\n</div>\n</div>\n".format(
        doc_conf)
    page_header += "</div>\n</div>\n"

    page_footer = "<div class=\"container-fluid border-top\">"
    page_footer += "<div class=\"d-flex mb-3 justify-content-between bg-light\">"
    page_footer += "<div class=\"p-2\">"
    page_footer += "<a href=\"https://spie-ics.com\" target=\"_blanck\"><img src=\"files/logo-spie-group.svg\" alt=\"SPIE ICS\"/></a>"
    page_footer += "</div>\n"
    page_footer += "<div class=\"p-2\">\n"
    page_footer += "<p>Copyright &#169; 2022 SPIE ICS</p>\n"
    page_footer += "</div>\n"
    page_footer += "</div>\n</div>\n"

    page_navmenu = "<!-- Nav Tabs -->\n"
    page_navmenu += "<ul id=\"myTab\" class=\"nav nav-tabs\" role=\"tablist\">\n"
    page_navmenu += "<li class=\"nav-item\" role=\"presentation\">\n"
    page_navmenu += "<button class=\"nav-link active\" id=\"TABGPO-tab\" data-bs-toggle=\"tab\" type=\"button\" aria-controls=\"TABGPO\" aria-selected=\"true\" role=\"tab\" data-bs-target=\"#TABGPO\">{0}</button>\n".format(
        title_labels[language][2])
    page_navmenu += "</li>\n"
    page_navmenu += "<li class=\"nav-item\" role=\"presentation\">\n"
    page_navmenu += "<button class=\"nav-link\" id=\"TABSTAT-tab\" data-bs-toggle=\"tab\" type=\"button\" aria-controls=\"TABSTAT\" aria-selected=\"false\" role=\"tab\" data-bs-target=\"#TABSTAT\">{0}</button>\n".format(
        title_labels[language][3])
    page_navmenu += "</li>\n"
    if context:
        page_navmenu += "<li class=\"nav-item\" role=\"presentation\">\n"
        page_navmenu += "<button class=\"nav-link\" id=\"TABCONT-tab\" data-bs-toggle=\"tab\" type=\"button\" aria-controls=\"TABCONT\" aria-selected=\"false\" role=\"tab\" data-bs-target=\"#TABCONT\">{0}</button>\n".format(
            title_labels[language][4])
        page_navmenu += "</li>\n"
    page_navmenu += "</ul>\n"

    page_tabs = "<!-- Tab panes -->\n<div class=\"tab-content\">\n"
    page_tabs += "<div id=\"TABGPO\" class=\"tab-pane active\" role=\"tabpanel\" aria-labelledby=\"TABGPO-tab\">\n"
    table_attributes = "id=\"GPO\" class=\"table table-bordered table-striped table-hover table-sm align-middle\""
    page_tabs += "<div id=\"CARDGPO\" class=\"card border-dark mb-3\">\n"
    page_tabs += "<div class=\"card-header\">\n"
    page_tabs += "<ul id=\"COMPGPO\" class=\"list-group list-group-horizontal\">\n"
    page_tabs += "<li class=\"list-group-item list-group-item-success d-flex flex-fill p-2 justify-content-between align-items-center\">\n"
    page_tabs += "<div><input class=\"form-check-input me-1\" type=\"checkbox\" value=\"C\" checked onclick=\"showhideGPO('GPO', 'C')\">{0}</div>\n".format(
        comp_labels[language][0])
    page_tabs += "<span class=\"badge bg-primary rounded-pill\">{0}</span>\n".format(str(nb_c))
    page_tabs += "</li>\n"
    page_tabs += "<li class=\"list-group-item list-group-item-warning d-flex flex-fill p-2 justify-content-between align-items-center\">\n"
    page_tabs += "<div><input class=\"form-check-input me-1\" type=\"checkbox\" value=\"W\" checked onclick=\"showhideGPO('GPO', 'W')\">{0}</div>\n".format(
        comp_labels[language][1])
    page_tabs += "<span class=\"badge bg-primary rounded-pill\">{0}</span>\n".format(str(nb_w))
    page_tabs += "</li>\n"
    page_tabs += "<li class=\"list-group-item list-group-item-danger d-flex flex-fill p-2 justify-content-between align-items-center\">\n"
    page_tabs += "<div><input class=\"form-check-input me-1\" type=\"checkbox\" value=\"N\" checked onclick=\"showhideGPO('GPO', 'N')\">{0}</div>\n".format(
        comp_labels[language][2])
    page_tabs += "<span class=\"badge bg-primary rounded-pill\">{0}</span>\n".format(str(nb_n))
    page_tabs += "</li>\n"
    page_tabs += "</ul>\n"
    page_tabs += "</div>\n"
    page_tabs += "<div class=\"card-body table-responsive\">\n"
    page_tabs += json2html.convert(json=all, table_attributes=table_attributes, escape=False)
    page_tabs += "</div></div></div>\n"
    page_tabs += "<div id=\"TABSTAT\" class=\"tab-pane fade\" role=\"tabpanel\" aria-labelledby=\"TABSTAT-tab\">\n"
    # table_attributes = "id=\"STATS\" class=\"table table-bordered table-striped table-hover table-sm align-middle\""
    table_attributes = "class=\"table table-bordered table-striped table-hover table-sm align-middle\""
    page_tabs += json2html.convert(json=stats, table_attributes=table_attributes, escape=False)
    page_tabs += "</div>\n"
    if context:
        page_tabs += "<div id=\"TABCONT\" class=\"tab-pane fade\" role=\"tabpanel\" aria-labelledby=\"TABCONT-tab\">\n"
        table_attributes = "class=\"table table-bordered table-striped table-hover table-sm align-middle\""
        page_tabs += json2html.convert(json=context, table_attributes=table_attributes, escape=False)
        page_tabs += "</div>\n"
    page_tabs += "</div>\n"

    html = "<!doctype html>"
    html += "<html lang=\"{0}\">".format(language)
    html += page_head
    html += "<body>"
    html += page_header
    html += "<div class=\"container-fluid\">\n"
    html += "<button id=\"btnTop\" type=\"button\" onclick=\"topPage()\" title=\"Haut de page\">&#x2191;</button>\n"
    html += "<button id=\"btnSum\" type=\"button\" onclick=\"openTab(event, TABGPO)\" title=\"Statistiques\">&#x21B0;</button>\n"
    html += "<div id=\"CGPO\" class=\"card border-dark mb-3\"><div class=\"card-body table-responsive\">\n"

    html += page_navmenu
    html += page_tabs
    table_attributes = "id=\"GPO\" class=\"table table-bordered table-striped table-hover table-sm align-middle\""

    html += "</div></div></div>\n"
    html += page_footer
    files_scripts = ["jquery-3.6.0.min.js", "bootstrap-5.1.3-dist/js/bootstrap.bundle.min.js",
                     "DataTables/JSZip-2.5.0/jszip.min.js", "DataTables/pdfmake-0.1.36/pdfmake.min.js",
                     "DataTables/pdfmake-0.1.36/vfs_fonts.js",
                     "DataTables/DataTables-1.11.3/js/jquery.dataTables.min.js",
                     "DataTables/DataTables-1.11.3/js/dataTables.bootstrap5.min.js",
                     "DataTables/Buttons-2.0.1/js/dataTables.buttons.min.js",
                     "DataTables/Buttons-2.0.1/js/buttons.bootstrap5.min.js",
                     "DataTables/Buttons-2.0.1/js/buttons.html5.min.js", "keeAD.js"]
    for file in files_scripts:
        f = open("files/" + file, "r", encoding="utf8")
        html += "<script>"
        html += f.read()
        html += "</script>\n"
    html += "</body>\n</html>\n"

    # Création du fichier de sortie
    if args.Rapports:
        out_file = os.path.join(args.Rapports, myClient + "-Inventaire GPO-" + str(WHEN.replace("/", "")) + ".html")
    else:
        out_file = os.path.join(os.getcwd(), myClient + "-Inventaire GPO-" + str(WHEN.replace("/", "")) + ".html")
    print("RESULTAT: \033[96m{0}\033[0m".format(out_file))
    f = open(out_file, "w", encoding="utf8")
    f.write(html)
    f.close

    return HttpResponse(html)


def points_de_controle_ad(request):
    context = {
    }
    return render(request, 'results/points_de_controle_ad.html', context)


def rapport_de_conf_ad(request):
    context = {
    }
    return render(request, 'results/rapport_de_conf_ad.html', context)


def rapport_d_inventaire_ad(request):
    context = {
    }
    return render(request, 'results/rapport_d_inventaire_ad.html', context)