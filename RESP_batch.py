import subprocess

#生成したRESP-Dscriptに基づいて、断面生成処理バッチを実行
def RESP_batch(resp_path,resp_model_create,resp_opt):

    # コマンドを実行
    if resp_model_create == "Activate":#モデル作成のみする場合
        if resp_opt == "NonActivate":
            command = fr'{resp_path} -I "initial_model.dz" --generate "generator_case1.json"'
            subprocess.run(command, shell=True)
            print("バッチ処理が正常に完了しました。")

    if resp_opt == "Activate":#断面算定処理を行う場合
        command = fr'{resp_path} -I "initial_model.dz" --generate "generator_case1.json" --optimize'
        subprocess.run(command, shell=True)
        print("バッチ処理が正常に完了しました。")

