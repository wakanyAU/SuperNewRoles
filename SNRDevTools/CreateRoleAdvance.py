## import
import PySimpleGUI as psg
import configparser
import sys
from pathlib import Path
from codecs import Codec
from encodings import utf_8
from importlib.resources import Resource



## 関数
# オブジェクト指向用
class ReturnClass:
    def WriteCodes(self, Path, OldCode, NewCode):
    # w→書く　r→読む　a→合成　r+既存を読む　w+→新規で書く　a+→追加読み書き　t→テキストモード　b→バイナリモード
        with open(BasePath+Path, mode="r", encoding="utf-8") as r:
            Template = r.read()
            print(Template)
            with open(BasePath+Path, mode="w", encoding="utf-8") as w:
                Template = Template.replace(OldCode, NewCode)
                print("ファイルを書き込みました:"+Template)
                print("パス:"+BasePath+Path)
                w.write(Template)
    #入力をゲット+戻り値として返す
    def GetInput(self, key):
        if values[key] == "":
            AllActClass.CreateErrorWindow("エラーが発生しました。\n値が空白です\n" + "Key:" + key)
            return
        else:
            print("入力した値を読み込みました:" + values[key])
            return values[key]
    #画像読み込み
    def GetResource(self, ResourceName):
        print("画像を読み込みました:" + ResourcePath + ResourceName)
        return ResourcePath + ResourceName
    #Config読み込み
    def GetConfig(self, MainPath, SubPath):
        Modify = Config_ini[MainPath][SubPath]
        print("Configを読み込みました:" + Modify)
        return Modify
    #選択から色を返す
    def GetRoleColor(self):
        if (MainClass.GetInput("ColorHash") != "ImposterRed"):
            Template = "new Color32(",MainClass.HashToRGB(),"byte.MaxValue)"
            print("ハッシュを取得しました:", Template)
            return Template
        elif (MainClass.GetInput("ImpoColor") == True):
            print("インポ色を取得しました")
            return "ImpostorRed"
        elif (MainClass.GetInput("CrewColor") == True):
            print("クルー色を取得しました")
            return "new Color32(0, 255, 0, byte.MaxValue)"
    #ハッシュをRGBに変換
    def HashToRGB(self):
        Hash = MainClass.GetInput("ColorHash")
        RGB = int(Hash[1:3],16), int(Hash[3:5],16), int(Hash[5:7],16)
        print(RGB)
        return RGB
    #チーム取得
    def GetTeam(self):
        if (MainClass.GetInput("Impo") == True):
            return "Impo"
        elif (MainClass.GetInput("Crew") == True):
            return "Crew"
        elif (MainClass.GetInput("Neut") == True):
            return "Neut"
# 戻り値なし
class AllCheck:
    #すべて書く
    def AllWrite(self):
        # CustomRPC/CustomRPC.cs
        MainClass.WriteCodes("CustomRPC/CustomRPC.cs", "//RoleId", MainClass.GetInput("RoleName")+",\n        //RoleId")
        MainClass.WriteCodes("CustomRPC/CustomRPC.cs", "//新ロールクラス", 
                                """public static class ROLE!!
        {
            public static List<PlayerControl> ROLE!!Player;
            public static Color32 color = COLORS;
            public static void ClearAndReload()
            {
                ROLE!!Player = new List<PlayerControl>();
            }
        }\n        //新ロールクラス""".replace("ROLE!!",MainClass.GetInput("RoleName")).replace("COLORS",MainClass.GetRoleColor()))
        # AllRoleSetClass.cs
        MainClass.WriteCodes("AllRoleSetClass.cs", "//セットクラス",
                                """if (!(CustomOption.CustomOptions.ROLEID!!Option.getString().Replace("0%", "") == ""))
            {
                int OptionDate = int.Parse(CustomOption.CustomOptions.ROLEID!!Option.getString().Replace("0%", ""));
                RoleId ThisRoleId = RoleId.ROLEID!!;
                if (OptionDate == 10)
                {
                    TEAMonepar.Add(ThisRoleId);
                }
                else
                {
                    for (int i = 1; i <= OptionDate; i++)
                    {
                        TEAMnotonepar.Add(ThisRoleId);
                    }
                }
            }\n        //セットクラス""".replace("ROLEID!!",MainClass.GetInput("RoleName")).replace("TEAM",MainClass.GetTeam()))
        MainClass.WriteCodes("AllRoleSetClass.cs", "//プレイヤーカウント","""case (RoleId.ROLENAME):
                return CustomOption.CustomOptions.ROLENAMEPlayerCount.getFloat();\n                    //プレイヤーカウント""".replace("ROLENAME",MainClass.GetInput("RoleName")))

        # Roles/RoleHelper.cs
        MainClass.WriteCodes("Roles/RoleHelper.cs", "//ロールチェック",
                                """else if (Roles.RoleClass.ROLENAME.ROLENAMEPlayer.IsCheckListPlayerControl(player))
            {
                return CustomRPC.RoleId.ROLENAME;
            }\n            //ロールチェック""".replace("ROLENAME",MainClass.GetInput("RoleName")))
        MainClass.WriteCodes("Roles/RoleHelper.cs", "//ロールアド",
                                """case (CustomRPC.RoleId.ROLENAME):
                    Roles.RoleClass.ROLENAME.ROLENAMEPlayer.Add(player);
                    break;\n                //ロールアド""".replace("ROLENAME",MainClass.GetInput("RoleName")))
        MainClass.WriteCodes("Roles/RoleHelper.cs", "//ロールリモベ",
                                """case (CustomRPC.RoleId.ROLENAME):
                    Roles.RoleClass.ROLENAME.ROLENAMEPlayer.RemoveAll(ClearRemove);
                    break;\n                //ロールリモベ""".replace("ROLENAME",MainClass.GetInput("RoleName")))
        if (MainClass.GetInput("Neut") == True):
            MainClass.WriteCodes("Roles/RoleHelper.cs", "//第三か",
                                """case (RoleId.ROLENAME):
                    IsNeutral = true;
                    break;\n                //第三か""".replace("ROLENAME",MainClass.GetInput("RoleName")))
            MainClass.WriteCodes("Roles/RoleHelper.cs", "//タスククリアか",
                                """case (RoleId.ROLENAME):
                    IsTaskClear = true;
                    break; 
                //タスククリアか""".replace("ROLENAME",MainClass.GetInput("RoleName")))

        # Intro/IntroData.cs
        MainClass.WriteCodes("Intro/IntroData.cs", "//イントロオブジェ","""public static IntroDate ROLENAMEIntro = new IntroDate("ROLENAME", RoleClass.ROLENAME.color, 1, CustomRPC.RoleId.ROLENAME);
        //イントロオブジェ""".replace("ROLENAME",MainClass.GetInput("RoleName")))
        MainClass.WriteCodes("Intro/IntroData.cs", "//イントロ検知","""case (CustomRPC.RoleId.ROLENAME):
                    return ROLENAMEIntro;
                //イントロ検知""".replace("ROLENAME",MainClass.GetInput("RoleName")))

        # CustomOption/CustomOptionData.cs
        MainClass.WriteCodes("CustomOption/CustomOptionData", "//CustomOption", 
        """public static CustomRoleOption ROLENAMEOption;
        public static CustomOption ROLENAMEPlayerCount;\n        //CustomOption""".replace("ROLENAME",MainClass.GetInput("RoleName")))
        if (MainClass.GetInput("AddSetting") == True):
            if (MainClass.GetInput("TeamImpo") == True):
                MainClass.WriteCodes("CustomOption/CustomOptionData", "//表示設定", 
                """ROLENAMEOption = new CustomRoleOption(IDNOM, true, CustomOptionType.Impostor, "ROLENAMEName",RoleClass.ROLENAME.color, 1);
            ROLENAMEPlayerCount = CustomOption.Create(IDNUM, true, CustomOptionType.Impostor, "SettingPlayerCountName", CrewPlayers[0], CrewPlayers[1], CrewPlayers[2], CrewPlayers[3], ROLENAMEOption);\n        //表示設定""".replace("ROLENAME",MainClass.GetInput("RoleName"))).replace("IDNUM",MainClass.GetInput("OptionNumber"))
            elif (MainClass.GetInput("TeamCrew") == True):
                MainClass.WriteCodes("CustomOption/CustomOptionData", "//表示設定", 
                """ROLENAMEOption = new CustomRoleOption(IDNUM, true, CustomOptionType.Impostor, "ROLENAMEName",RoleClass.ROLENAME.color, 1);
            ROLENAMEPlayerCount = CustomOption.Create(IDNUM, true, CustomOptionType.Impostor, "SettingPlayerCountName", CrewPlayers[0], CrewPlayers[1], CrewPlayers[2], CrewPlayers[3], ROLENAMEOption);\n        //表示設定""".replace("ROLENAME",MainClass.GetInput("RoleName")).replace("IDNUM",MainClass.GetInput("OptionNumber")))
            elif (MainClass.GetInput("TeamNeut") == True):
                MainClass.WriteCodes("CustomOption/CustomOptionData", "//表示設定", 
                """ROLENAMEOption = new CustomRoleOption(IDNUM, true, CustomOptionType.Impostor, "ROLENAMEName",RoleClass.ROLENAME.color, 1);
            ROLENAMEPlayerCount = CustomOption.Create(IDNUM, true, CustomOptionType.Impostor, "SettingPlayerCountName", CrewPlayers[0], CrewPlayers[1], CrewPlayers[2], CrewPlayers[3], ROLENAMEOption);\n        //表示設定""".replace("ROLENAME",MainClass.GetInput("RoleName")).replace("IDNUM",MainClass.GetInput("OptionNumber")))

    #エラーウィンドウ作成
    def CreateErrorWindow(self, text):
        ErrorPop = psg.popup_error(text,title="エラー")
        print("エラー:"+text)
        while True:
            if ErrorPop == "Error":
                MainWindow.close()
                sys.exit()

## 変数
'''DevPath = Path(__file__).parent
DevPath /= "../SNRDevTools/" 
BasePath = Path(__file__).parent
BasePath /= "../SuperNewRoles/" 
ConfigPath = Path(__file__).parent
ConfigPath /= "../SNRDevTools/CreateRoleAdvance/"
ResourcePath = Path(__file__).parent
ResourcePath /= "../SNRDevTools/CreateRoleAdvance/Resources/"'''
DevPath = r"../SNRDevTools/"
BasePath = r"../SuperNewRoles/"
ConfigPath = r"CreateRoleAdvance/"
ResourcePath = r"CreateRoleAdvance/Resources/"
MainClass = ReturnClass()
AllActClass = AllCheck()
## Config
# 宣言
Config_ini = configparser.ConfigParser()
Config_ini.read((ConfigPath+"Config.ini"),encoding="utf_8")









## レイアウト
# メイン画面
psg.theme(MainClass.GetConfig("Main", "Theme"))
MainTab = psg.Tab("メイン", [  
                [psg.Text("Role名(英名):",key="RoleNameText"),psg.InputText(MainClass.GetConfig("MainDefaultSetting", "RoleName"),size=(15,1),key="RoleName")],
                [psg.Text("イントロ:",key="IntroText"), psg.Combo(("役職のみ表示","陣営でも表示"),size=(30,2),default_value=MainClass.GetConfig("MainDefaultSetting", "Intro"))],
                [psg.Text("陣営:    ",key="TeamText"),psg.Radio("インポ陣営","TeamName",key="Impo",default=True),psg.Radio("クルー陣営","TeamName",key="Crew"),psg.Radio("第三陣営","TeamName",key="Neut")],
                [psg.Text("役職カラー:",key="ColorText"), psg.Radio("インポ色","RoleColor",key="ImpoColor",default=True), psg.Radio("ナイス緑色","RoleColor",key="CrewColor"),  psg.ColorChooserButton("色選択",key="ColorButton",target="ColorHash")],
                [psg.Text("取得ハッシュ:",key="ColorHashText"), psg.Input("ImposterRed",key="ColorHash")] ])
AdvanceTab = psg.Tab("詳細設定", [ 
                [psg.Check("設定を追加する",key="AddSetting")],
                [psg.Text(), psg.Text("タブ:"), psg.Radio("インポスター",group_id="OptionTab",key="TeamImpo"), psg.Radio("クルー",group_id="OptionTab",key="TeamCrew"), psg.Radio("第三陣営",group_id="OptionTab",key="TeamNeut")],
                [psg.Text(), psg.Check("SHR対応",key="AddSetting")],
                [psg.Text(), psg.Text("役職ID"), psg.Input("",key="OptionNomber")],
                [psg.Check("ベントを使える",key="A_CanVent")],
                [], ])
CreateTab = psg.Tab("作成", [
                [psg.Button("作成",key="Main_CreateButton", pad=((10,10),(10,10)), size=(15,2))] ])
MainLayOut = [[psg.TabGroup ([[MainTab, AdvanceTab, CreateTab]])]]
MainWindow = psg.Window(title=MainClass.GetConfig("Main", "WindowName"), layout=MainLayOut, size=(MainClass.GetConfig("Main", "SizeX"), MainClass.GetConfig("Main", "SizeY")), icon=MainClass.GetResource("icon.png"))
## イベントループ
while True:
    event, values = MainWindow.read()
    if event == psg.WIN_CLOSED:
        break

    elif event == "Main_CreateButton":
        LastClicked = psg.popup_ok_cancel("役職を作成します。よろしいですか？",title="確認")
        if LastClicked == "OK":
            AllActClass.AllWrite()

MainWindow.close()