from django.shortcuts import render
from .models import Resultmanagement
from django.http import HttpResponse
import json
import numpy as np
import re


# Create your views here.

def opencsv(request, file):
    ad_file = open(file, 'r')
    ad_data = json.load(ad_file)
    data = ad_data["rules"]
    data2 = ad_data.get('rules')
    arr = []

    for x in data:
        for y in x['fields']:
            name = y.get('name')
            print(y.get('name'))
            ok = y.get('x')
            #  print(y.get('ok')


def calculator(arr):
    for x in arr:
        test = arr[x]


def check_forestmode(x):
    if re.search('Windows(2019|2016)Forest', x) is not None:
        return 'Ok'
    if re.search('Windows(2012R2|2012)Forest', x) is not None:
        return 'Warn'
    if re.search('Windows(2008R2|2008|2003|2003Interim|2000)Forest', x) is not None:
        return 'Nok'
    else:
        return 'error'


def check_schema_master(x):
    if x == re.L['SchemaMaster']:
        return 'Ok'
    if x != re.L['SchemaMaster']:
        return 'Warn'
    else:
        return 'error'


def check_operatingsystem(x):
    if re.search('Windows Server (2019|2016) .*', x) is not None:
        return 'Ok'
    if re.search('Windows Server (2012 R2|2012) .*', x) is not None:
        return 'Warn'
    if re.search('Windows Server (2008 R2|2008|2003|2000)', x) is not None:
        return 'Nok'
    else:
        return 'error'


def check_enabled(x):
    if re.L['Name'] == 'Recycle Bin Feature' and x == 'True':
        return 'Ok'
    if re.L['Name'] == 'Recycle Bin Feature' and x == 'False':
        return 'Nok'
    else:
        return 'error'


def check_schema_version(x):
    if re.search('(87|88).*', x) is not None:
        return 'Ok'
    if re.search('(56|69).*', x) is not None:
        return 'Warn'
    if re.search('(13|30|31|44|47).*', x) is not None:
        return 'Nok'
    else:
        return 'error'


def check_present(x):
    if re.search('ms-Mcs-AdmPwd', re.L['Name']) and x == 'True':
        return 'Ok'
    if re.search('ms-Mcs-AdmPwd', re.L['Name']) and x == 'False':
        return 'Warn'
    else:
        return 'error'


def check_servers(x):
    if bool(x):
        return 'Ok'
    if not x:
        return 'warn'
    else:
        return 'error'


def check_SelectiveAuthentication(x):
    if re.L['Direction'] != 'Inbound' and x == 'True':
        return 'Ok'
    if re.L['Direction'] != 'Inbound' and x == 'False':
        return 'Nok'
    else:
        return 'error'


def check_SIDFilteringForestAware(x):
    if re.L['Direction'] != 'Inbound' and x == 'True':
        return 'Ok'
    if re.L['Direction'] != 'Inbound' and x == 'False':
        return 'Nok'


def check_SIDFilteringQuarantined(x):
    if re.L['Direction'] != 'Inbound' and x == 'True':
        return 'Ok'
    if re.L['Direction'] != 'Inbound' and x == 'False':
        return 'Nok'


def check_TGTDelegation(x):
    if re.L['Direction'] != 'Inbound' and x == 'True':
        return 'Ok'
    if re.L['Direction'] != 'Inbound' and x == 'False':
        return 'Nok'


def check_domain_mode(x):
    if re.search('Windows(2019|2016)Domain', x) is not None:
        return 'Ok'
    if re.search('Windows(2012R2|2012)Domain', x) is not None:
        return 'Warn'
    if re.search('Windows(2008R2|2008|2003|2003Interim|2000)Domain', x) is not None:
        return 'Nok'
    else:
        return 'error'


def check_InfrastructureMaster(x):
    if x == int(re.L['PDCEmulator']) and x == int(re.L['RIDMaster']):
        return 'Ok'
    if x != re.L['PDCEmulator'] or x != re.L['RIDMaster']:
        return 'Warn'
    else:
        return 'error'


def check_PDCEmulator(x):
    if x == int(re.L['PDCEmulator']) and x == int(re.L['RIDMaster']):
        return 'Ok'
    if x != re.L['PDCEmulator'] or x != re.L['RIDMaster']:
        return 'Warn'


def check_RIDMaster(x):
    if x == re.L['InfrastructureMaster'] and x == re.L['PDCEmulator']:
        return 'Ok'
    if x != re.L['PDCEmulator'] or x != re.L['RIDMaster']:
        return 'Warn'


def check_Source(x):
    if re.L['PDCEmulator'] == 'False' and x == '** PDC **':
        return 'Ok'
    if re.L['PDCEmulator'] == 'False' and x != '** PDC **':
        return 'Nok'


def check_PasswordHistoryCount(x):
    if re.search('\[.*\]', x) is not None and int(x) >= 24:
        return 'Ok'
    if re.search('\[.*\]', x) is not None or int(x) < 24:
        return 'Nok'
    else:
        return 'error'


def check_max_password_age(x):
    if (int('0' + (re.sub(r'\.*\d{2}:\d{2}:\d{2}', '', x))) != 0 and int(
            '0' + (re.sub(r'\.*\d{2}:\d{2}:\d{2}', '', x)))) <= 60:
        return 'Ok'
    if int('0' + (re.sub(r'\.*\d{2}:\d{2}:\d{2}', '', x))) > 60:
        return 'Warn'
    if (int('0' + (re.sub(r'\.*\d{2}:\d{2}:\d{2}', '', x)))) == 0:
        return 'Nok'
    else:
        return 'error'


def check_MinPasswordAge(x):
    if int('0' + (re.sub('\.*[\d]{2}:[\d]{2}:[\d]{2}', '', x))) >= 1:
        return 'Ok'
    if int('0' + (re.sub('\.*[\d]{2}:[\d]{2}:[\d]{2}', '', x))) < 1:
        return 'Warn'
    else:
        return 'error'


def check_Reversible_Encryption_Enabled(x):
    if x == 'False':
        return 'Ok'
    if x != 'False':
        return 'Warn'
    else:
        return 'error'


def check_ComplexityEnabled(x):
    if x == 'True':
        return 'Ok'
    if x != 'True':
        return 'Warn'
    else:
        return 'error'


def check_MinPasswordLength(x):
    if int(x) >= 14:
        return 'Ok'
    if int(x) < 14:
        return 'Warn'


def check_LockoutDuration(x):
    if (int(x.split(':')[0]) * 60 + int(x.split(':')[1])) >= 15:
        return 'Ok'
    if (int(x.split(':')[0]) * 60 + int(x.split(':')[1])) < 15:
        return 'Warn'


def check_LockoutObservationWindow(x):
    if (int(x.split(':')[0]) * 60 + int(x.split(':')[1])) >= 15:
        return 'Ok'
    if (int(x.split(':')[0]) * 60 + int(x.split(':')[1])) < 15:
        return 'Warn'


def check_lockout_threshold(x):
    if int(x) != 0 and int(x) <= 10:
        return 'Ok'
    if int(x) > 10:
        return 'Warn'
    if int(x) == 0:
        return 'Nok'
    return True


def check_AppliesTo(x):
    if bool(x):
        return 'Ok'
    if not x:
        return 'Warn'


def Name(x):
    if re.L['NBUsers'] == 0 and re.L['NBComputers'] == 0 and re.L['NBGroups'] == 0 and re.L['NBOUs'] == 1:
        return 'Warn'


def check_ProtectedFromAccidentalDeletion(x):
    if x == 'True':
        return 'Ok'
    if x == 'False':
        return 'Warn'


def check_GpoInheritanceBlocked(x):
    if x == 'False':
        return 'Ok'
    if x == 'True':
        return 'Warn'


def check_GroupswithSIDHistory(x):
    if x == '0':
        return 'Ok'
    if x != '0':
        return 'Warn'


def check_Members1(x):
    if not x:
        return 'Ok'
    if bool(x):
        return 'Warn'


def check_Members2(x):
    if not x:
        return 'Ok'
    if bool(x):
        return 'Nok'


def check_Members3(x):
    if x == '0':
        return 'Warn'


def check_Users(x):
    if (re.L['GroupScope'] == 'DomainLocal' and x == '0') or (re.L['GroupScope'] == 'Universal' and int(x) > 0) or (
            re.L['GroupScope'] == 'Global' and int(x) > 0):
        return 'Ok'
    if re.L['GroupScope'] == 'DomainLocal' and int(x) > 0:
        return 'Nok'


def check_Groups(x):
    if re.L['GroupScope'] == 'DomainLocal' and x == '0':
        return 'Warn'


def check_GlobalGroups(x):
    if (re.L['GroupScope'] == 'DomainLocal' and int(x) > 0) or (re.L['GroupScope'] == 'Universal' and int(x) > 0) or (
            re.L['GroupScope'] == 'Global' and int(x) > 0):
        return 'Ok'


def check_UniversalGroups(x):
    if (re.L['GroupScope'] == 'DomainLocal' and int(x) > 0) or (re.L['GroupScope'] == 'Universal' and int(x) > 0):
        return 'Ok'


def check_ModificationTime(x):
    if (re.L['DisplayName'] == 'Default Domain Policy') and (re.L['CreationTime'] != x):
        return 'Ok'


def check_Enabled(x):
    if x == 'True':
        return 'Ok'
    if x == 'False':
        return 'Nok'


def check_Enforced(x):
    if x == 'False':
        return 'Ok'
    if x == 'True':
        return 'Warn'


def check_Type(x):
    if x == 'Inherited':
        return 'Ok'
    if x == 'Linked':
        return 'Warn'


def check_AllUsersWhosePasswordNeverExpires(x):
    if x == '0':
        return 'Ok'
    if int(x) > 0:
        return 'Nok'


def check_AllUsersWithPasswordNotRequired(x):
    if x == '0':
        return 'Ok'
    if int(x) > 0:
        return 'Nok'


def check_AllUsersWhoCannotChangePassword(x):
    if x == '0':
        return 'Ok'
    if int(x) > 0:
        return 'Nok'


def check_AllUsersWithSIDHistory(x):
    if x == '0':
        return 'Ok'
    if int(x) > 0:
        return 'Nok'


def check_AllUsersWithBadPrimaryGroup(x):
    if x == '0':
        return 'Ok'
    if int(x) > 0:
        return 'Nok'


def check_ActiveUsersWhosePasswordNeverExpires(x):
    if x == '0':
        return 'Ok'
    if int(x) > 0:
        return 'Nok'


def check_ActiveUsersWithPasswordNotRequired(x):
    if x == '0':
        return 'Ok'
    if int(x) > 0:
        return 'Nok'


def check_ActiveUsersWhoCannotChangePassword(x):
    if x == '0':
        return 'Ok'
    if int(x) > 0:
        return 'Nok'


def check_MemberOf(x):
    if re.L['Enabled'] == 'False' and bool(x):
        return 'Ok'
    if re.L['Enabled'] == 'False' and not x:
        return 'Nok'


def check_PasswordLastSet(x):
    if (re.L['Name'] == 'krbtgt') and (re.L['Created'] != x):
        return 'Ok'
    if (re.L['Name'] == 'krbtgt') and (re.L['Created'] == x):
        return 'Nok'


def check_PasswordNeverExpires(x):
    if x == 'False':
        return 'Ok'
    if x == 'True':
        return 'Nok'


def check_PasswordNotRequired(x):
    if x == 'False':
        return 'Ok'
    if x == 'True':
        return 'Nok'


def check_DisplayName(x):
    if (re.L['LinksToEnabled'] == 'True' and re.L['ComputerExtensionData'] == 'False' and re.L[
        'UserExtensionData'] == 'False') or (
            re.L['LinksToEnabled'] == 'True' and re.L['GpoStatus'] == 'AllSettingsDisabled'):
        return 'Warn'


def check_LinksToEnabled(x):
    if x == 'True':
        return 'Ok'
    if x == 'False':
        return 'Warn'


def check_GpoStatus(x):
    if re.L['LinksToEnabled'] == 'True' and ((x == 'ComputerSettingsDisabled' and re.L[
        'ComputerExtensionData'] == 'True' and re.L['UserExtensionData'] == 'False') or (
                                                     x == 'UserSettingsDisabled' and
                                                     re.L['ComputerExtensionData'] == 'False' and re.L[
                                                         'UserExtensionData'] == 'True') or (
                                                     x == 'AllSettingsEnabled' and
                                                     re.L['ComputerExtensionData'] == 'True' and re.L[
                                                         'UserExtensionData'] == 'True')):
        return 'Ok'
    if re.L['LinksToEnabled'] == 'True' and (
            x == 'AllSettingsEnabled' and re.L['ComputerExtensionData'] == 'False') or (
            x == 'AllSettingsEnabled' and re.L['UserExtensionData'] == 'False'):
        return 'Nok'


def check_ComputerExtensionDatas(x):
    if re.L['LinksToEnabled'] == 'True' and re.L['GpoStatus'] == 'ComputerSettingsDisabled' and x == 'False':
        return 'Ok'
    if re.L['LinksToEnabled'] == 'True' and re.L['GpoStatus'] == 'AllSettingsEnabled' and x == 'False':
        return 'Nok'


def check_UserExtensionData(x):
    if re.L['LinksToEnabled'] == 'True' and re.L['GpoStatus'] == 'UserSettingsDisabled' and x == 'False':
        return 'Ok'
    if re.L['LinksToEnabled'] == 'True' and re.L['GpoStatus'] == 'AllSettingsEnabled' and x == 'False':
        return 'Nok'


def check_ComputerSysvolVersion(x):
    if x == re.L['ComputerSysvolVersion']:
        return 'Ok'
    if x != re.L['ComputerSysvolVersion']:
        return 'Nok'


def check_UserSysvolVersion(x):
    if x == re.L['UserDSVersion']:
        return 'Ok'
    if x != re.L['UserDSVersion']:
        return 'Nok'


def check_LinksTo(x):
    if bool(x):
        return 'Ok'
    if not x:
        return 'Nok'


def checkosversion(x):
    if int(re.L['Active']) > 0 and re.search('Windows.*( 10| 2012| 2016| 2019).*', x) is not None:
        return 'Ok'
    if int(re.L['Active']) > 0 and re.search('Windows.*( 8.1).*', x) is not None:
        return 'Warn'
    if int(re.L['Active']) > 0 and re.search('Windows.*( 2008 R2| 2008| 2003| 2000| XP| NT| 7|7| Vista| 8 ).*',
                                             x) is not None:
        return 'Nok'
    return True


def check_active(x):
    if int(x) > 0 and re.search('Windows.*( 10| 2012| 2016| 2019).*', re.L['OSVersion']):
        return 'Ok'
    if int(x) > 0 and re.search('Windows.*( 8.1).*', re.L['OSVersion']):
        return 'Warn'
    if int(x) > 0 and re.search('Windows.*( 2008 R2| 2008| 2003| 2000| XP| NT| 7|7| Vista| 8 ).*', re.L['OSVersion']):
        return 'Nok'
    return True


def check_OperatingSystem(x):
    if re.search('Windows Server (2019|2016) .*', x) is not None:
        return 'Ok'
    if re.search('Windows Server (2012 R2|2012) .*', x) is not None:
        return 'Warn'
    if re.search('Windows Server (2008 R2|2008|2003|2000 .*)', x) is not None:
        return 'Nok'


def check_MaximumKilobytes(x):
    if (re.L['LogDisplayName'] in ['Application', 'Anwendung', 'System', 'SystÃ¨me'] and int(x) >= 2048) or (
            re.L['LogDisplayName'] in ['Security', 'SÃ©curitÃ©', 'Sicherheit'] and int(x) >= 10240):
        return 'Ok'
    if (re.L['LogDisplayName'] in ['Application', 'Anwendung', 'System', 'SystÃ¨me'] and int(x) < 2048) or (
            re.L['LogDisplayName'] in ['Security', 'SÃ©curitÃ©', 'Sicherheit'] and int(x) < 10240):
        return 'Nok'


def check_TotalPhysicalMemory(x):
    if float(x.replace(',', '.')) >= 4:
        return 'Ok'
    if float(x.replace(',', '.')) < 4:
        return 'Nok'


def check_BIOS(x):
    if x == 'UEFI':
        return 'Ok'
    if x != 'UEFI':
        return 'Nok'


def check_FreeSpace(x):
    if re.L['FileSystem'] == 'NTFS' and (int(x) / int(re.L['Size'])) > 0.1:
        return 'Ok'
    if re.L['FileSystem'] == 'NTFS' and (int(x) / int(re.L['Size'])) <= 0.1:
        return 'Nok'


def check_DHCPEnabled(x):
    if x == 'False':
        return 'Ok'
    if re.search('True', x) is not None:
        return 'Nok'


def check_TcpipNetbiosOptions(x):
    if x == 'DisableNetbios':
        return 'Ok'
    if x != 'DisableNetbios':
        return 'Nok'


def check_Enabled3(x):
    if x == 'True' or x == '1':
        return 'Ok'
    if x != 'True' and x != '1':
        return 'Nok'


def check_Transport(x):
    if x == 'HTTPS':
        return 'Ok'
    if x == 'HTTP':
        return 'Warn'


def check_name1(x):
    if re.search('^(DHCP|SNMP-Service|Web-Server|AD-Certificate|FS-SMB1|RDS-Licensing|NPAS-Policy-Server)$',
                 x) is not None and re.L['InstallState'] == 'Installed':
        return 'Nok'


def check_InstallState(x):
    if re.search('^(DHCP|SNMP-Service|Web-Server|AD-Certificate|FS-SMB1|RDS-Licensing|NPAS-Policy-Server)$',
                 re.L['Name']) and x == 'Installed':
        return 'Nok'


def check_UserAuthenticationRequired(x):
    if x == '1':
        return 'Ok'
    if x != '1':
        return 'Nok'


def check_ScavengingState(x):
    if x == 'True':
        return 'Ok'
    if x == 'False':
        return 'Nok'


def check_IPAddress(x):
    if re.search('8.8.8.8', x) is not None:
        return 'Warn'


def check_ReplicationScope(x):
    if x != 'Legacy':
        return 'Ok'
    if x == 'Legacy':
        return 'Nok'


def check_IsDsIntegrated(x):
    if (re.L['ZoneFile'] != '' or re.L['ReplicationScope'] != 'None') and x == 'True':
        return 'Ok'
    if (re.L['ZoneFile'] != '' or re.L['ReplicationScope'] != 'None') and x != 'True':
        return 'Nok'


def check_IsShutdown(x):
    if x == 'False':
        return 'Ok'
    if x == 'True':
        return 'Nok'


def check_AgingEnabled(x):
    if x == 'True':
        return 'Ok'
    if x == 'False':
        return 'Nok'


def check_TestResult(x):
    if x == 'passed' or x == 'a rÃ©ussi':
        return 'Ok'
    if x == 'failed' or x == 'a Ã©chouÃ©':
        return 'Nok'


def check_percentage_passed():
    return 0
