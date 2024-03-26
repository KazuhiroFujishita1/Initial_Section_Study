import subprocess

#生成したRESP-Dscriptに基づいて、断面生成処理バッチを実行
def RESP_batch():
    # バッチ処理を実行するコマンド文字列
    command = r'.\bin\Debug\ModelCalcCtrlApp.exe -I "8F例題モデル_略算床荷重.dz" --generate "generator_case1.json"'

    # コマンドを実行
    try:
        subprocess.run(command, shell=True, check=True)
        print("バッチ処理が正常に完了しました。")
    except subprocess.CalledProcessError as e:
        print("バッチ処理がエラーを返しました:", e)
    except Exception as e:
        print("バッチ処理中にエラーが発生しました:", e)
