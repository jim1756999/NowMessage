# i18n.py

from config import LANGUAGE


if LANGUAGE == "zh_cn":
    Wait_Conn = "等待连接..."
    Admin_Announce = "管理员: "
    Join_Room = "加入了聊天室。"
    Exit_Room = "退出了聊天室。"
elif LANGUAGE == "en_uk":
    Wait_Conn = "Waiting for connection..."
    Admin_Announce = "Admin: "
    Join_Room = " joins the chatting room."
    Exit_Room = " exits the chatting room."
else:
    Wait_Conn = "Waiting for connection..."