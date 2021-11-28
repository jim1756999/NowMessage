# i18n.py

from config import LANGUAGE


if LANGUAGE == "zh_cn":
    Wait_Conn = "等待连接..."
    Admin_Announce = "管理员: "
elif LANGUAGE == "en_uk":
    Wait_Conn = "Waiting for connection..."
    Admin_Announce = "Admin: "
else:
    Wait_Conn = "Waiting for connection..."