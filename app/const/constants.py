from string import ascii_letters, digits
import os

PRINTABLE_CHARS = ascii_letters + digits

UID = 'UID_'
"User ID"
PID = 'PID_'
"Project ID"
CID = 'CID_'
"Channel ID"
MID = 'MID_'
"Misconduct ID"
LID = 'LID_'
"Likes ID"
AID = 'AID_'
"Applied ID"
GID = 'GID_'
"Location ID"
ID_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'ids.content'))


MALE = M = 'Male'
FEMALE = F = 'Female'
PREFER_NOT = PN = 'Prefer Not to Say'
OTHERS = OT = 'Others'

PUBLIC = 'Public'
PRIVATE = 'Private'
