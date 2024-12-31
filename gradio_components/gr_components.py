import gradio as gr
from modules import tab1_func as t1
from modules import tab2_func as t2
from modules import tab3_func as t3
from modules import tab4_func as t4
from modules import tab5_func as t5
from modules import tab7_func as t7
from modules import tab8_func as t8
from modules import moz_split as sp
from modules import jsonplussrt as json_rv

import pandas as pd



def gr_components():

    with gr.Blocks() as UI:
        gr.Markdown(
            """
            <h1 style="color:'darkblue'; font-family :'Arial', sans-serif;font-size:36px;"> PeriOz web　- Transcribe & Edit - </h1>
            <p style="color:gray; letter-spacing:0.05em;">OpenAIのfaster-whisperを使っています。字幕の区切りを必ずピリオドにできるのがこのアプリの特徴です。それにより翻訳精度が保たれます。</p>
            """)
        
        ### Gradio-Tab1 ###
                   
        with gr.Tab("文字起こし",elem_classes="Tab1"):
            gr.Markdown("> 字幕ファイル（srtファイル）、テキストファイル2種、Google翻訳用ワード、エクセルファイルが表示されます。Google翻訳用のファイルが必要な場合はアコーディオンを開いてね。") 
            with gr.Row():
                with gr.Column():
                    param1 = gr.File(label="ファイルをアップロードしてね",type="filepath",file_types=['.mp3','.mp4','.webm','.mkv','.wav'])#,file_types=['mp3','mp4','webm','mkv']
                    with gr.Row():
                        exec_btn = gr.Button("データファイルの作成", variant="primary")
                        t1_clear_Button=gr.Button(value='クリア')
                    param2 = gr.Dropdown(["medium", "large-v1", "large-v2", "large-v3-turbo", "large-v3"], value="large-v2", label="モデルを選ぶ")
                    param3 = gr.Radio(["int8", "float16", "float32","int8_float16","int8_float32"], value="float32", label="演算方法を選ぶ")
                    with gr.Row():
                        param4 = gr.Radio(["英語"], value="英語", label="言語を選ぶ")
                        param0 = gr.Radio(["cuda","cpu"],value="cuda",label="デバイスを選択してください。")

                    param5 = gr.Slider(label="ビームサイズ", value=5, minimum=1, maximum=10, step=1)
                    param6 = gr.Checkbox(label="Vad-Filterの使用", value=True)
                    with gr.Accordion(label="音声の調整",open=False):
                        hp_dp=gr.Dropdown(["None","8000Hz","10000Hz","12000Hz"],value="None",label="高音域のカット境界")
                        lp_dp=gr.Dropdown(["None","50Hz","100Hz","150Hz"],value="None",label="低音域のカット境界")
                        NR_dp=gr.Dropdown(["None","-60dB","-30dB","-20dB"],value="None",label="ノイズリダクションの程度")
                    with gr.Accordion(label="Google翻訳用docs",open=False):
                        doc_download_path=gr.File(label="Wordファイルのダウンロード",file_count="multiple")
                    
                    '''with gr.Accordion(label="Json（ワードスタンプ）", open=False):
                        result_json_file = gr.File(label="JSONファイルをダウンロード")
                        result_json_content = gr.TextArea(label="JSONファイルの内容を表示", autoscroll=False, show_copy_button=True)
                    '''
                with gr.Column():
                    reversal_button=gr.Button(value="ファイルの復活")               
                    reversal_info=gr.Textbox(label="文字起こしコメント",placeholder="whisperファイルの復活の要否に関する情報です。")
                    main_files_path = gr.File(label="SRT,TXT(NR,R)ファイルのダウンロード", file_count="multiple")
                    Dammy_Fiiles=gr.File(file_count="multiple",visible=False)
                    

                    with gr.Column():
                        result_srt_content = gr.TextArea(label="SRTファイルの内容を表示", autoscroll=False, show_copy_button=True)
                        result_txt_nr_content = gr.TextArea(label='「改行なし（NR）」のTXTファイルの内容を表示', autoscroll=False, show_copy_button=True)
                        result_txt_r_content = gr.TextArea(label='ピリオド区切りで「改行した（R）」のTXTファイルの内容を表示', autoscroll=False, show_copy_button=True)


        ### Gradio-Tab2 ###
        
        with gr.Tab("翻訳お手伝い①"):
            gr.Markdown("> 文字起こし直後に行う翻訳ファイル作成を手伝います。翻訳文を貼り付けて日本語ファイルを作ります。SRTファイルを作成するときは、同時に日英字幕が記載されたExcelファイルも作成されます。")
            with gr.Column():
                filename_output=gr.Textbox(label="ファイルのベースネーム",placeholder="ファイル名が空、または間違っているときは記入してね。")
                extension_choices = gr.CheckboxGroup(["srt", "txt(nr)", "txt(r)"],value=["srt"], label="ファイルの種類を選んで下さい。")
            with gr.Column():
                gr.Markdown("ここに翻訳コピーを貼り付けます。")
                with gr.Row():
                    translate_srt = gr.TextArea(label="Translate Content for _ja.srt", visible=True)
                    translate_nr_txt = gr.TextArea(label="Translate Content for _NR_ja.txt", visible=False)
                    translate_r_txt = gr.TextArea(label="Translate Content for _R_ja.txt", visible=False)
                    dummy=gr.Textbox(label="後で非表示" ,visible=False)

                with gr.Row():
                    html_srt = gr.HTML(visible=True)
                    html_nr_txt = gr.HTML(visible=False)
                    html_r_txt= gr.HTML(visible=False)
                with gr.Accordion(label="英語dataframe",open=False):
                    gr_components_df=gr.HTML()

            with gr.Row():
                generate_files_button = gr.Button("日本語ファイルの生成",variant="primary")
                t2_clear_button=gr.Button("クリア")
            download_translated_files = gr.File()
            button2_df=gr.HTML()

        def update_visibility(extensions):
            return {
            translate_srt: gr.update(visible="srt" in extensions),
            translate_nr_txt: gr.update(visible="txt(nr)" in extensions),
            translate_r_txt: gr.update(visible="txt(r)" in extensions),
            html_srt:gr.update(visible="srt" in extensions),
            html_nr_txt:gr.update(visible="txt(nr)" in extensions),
            html_r_txt:gr.update(visible="txt(r)" in extensions)
            }




 


        ##クリアボタン追加分をまとめる。
        def t1_clear():
            empty_html_table = pd.DataFrame({'1': [''], '2': [''], '3': ['']}).to_html(index=False)
            return "",None,"","","",[],[],"","","","","",empty_html_table,[]

       

        def t2_clear():
            return "","","",[],pd.DataFrame({'1': [''], '2': [''],'3': ['']})
        def t4_clear():
            empty_html_table = pd.DataFrame({'1': [''], '2': [''], '3': ['']}).to_html(index=False)
            return None,"","",[],[],empty_html_table

        '''def t6_clear():
            return None,None,[]'''
        
        def t7_clear():
            empty_html_table = pd.DataFrame({'1': [''], '2': [''], '3': ['']}).to_html(index=False)
            return None,None,None,None,None,None,empty_html_table

        def param1_change_clear():
            return "",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None

        ### Tab1 イベントリスナー ###
        param1.change(fn=param1_change_clear,
                      inputs=[],
                      outputs=[reversal_info,result_srt_content,result_txt_nr_content,result_txt_r_content
                               ,main_files_path,doc_download_path,html_srt,html_nr_txt,html_r_txt,filename_output,dummy,gr_components_df,
                               translate_srt,translate_nr_txt,translate_r_txt,download_translated_files,button2_df])
        exec_btn.click(
            fn=t1.run_with_progress,
            inputs=[hp_dp,lp_dp,NR_dp,param1, param2, param3, param4, param5, param6,param0],
            outputs=[reversal_info,result_srt_content,result_txt_nr_content, result_txt_r_content, main_files_path,doc_download_path,html_srt,html_nr_txt,html_r_txt,filename_output,dummy,gr_components_df,Dammy_Fiiles])
        reversal_button.click(
            fn=json_rv.run_spacy2,
            inputs=[Dammy_Fiiles],
            outputs=[reversal_info,result_srt_content,result_txt_nr_content, result_txt_r_content, main_files_path,doc_download_path,html_srt,html_nr_txt,html_r_txt,filename_output,dummy,gr_components_df]

        )
        t1_clear_Button.click(
            fn=t1_clear,inputs=[],outputs=[reversal_info,param1,result_srt_content,result_txt_nr_content,result_txt_r_content,main_files_path,doc_download_path,html_srt,html_nr_txt,html_r_txt,filename_output,dummy,gr_components_df,Dammy_Fiiles]
        )
        ### Tab2 イベントリスナー ###
        
        extension_choices.change(fn=update_visibility, 
                                inputs=extension_choices,
                                outputs=[translate_srt, translate_nr_txt, translate_r_txt,html_srt,html_nr_txt,html_r_txt])
        
        generate_files_button.click(
            fn=t2.create_translate_files,
            inputs=[filename_output, 
                    translate_srt,
                    translate_nr_txt,
                    translate_r_txt, 
                    extension_choices,
                    dummy],
            outputs=[download_translated_files,button2_df]) 
        t2_clear_button.click(fn=t2_clear,inputs=[],outputs=[translate_srt,translate_nr_txt,translate_r_txt,download_translated_files,button2_df])


        with gr.Tab("配布字幕の再編"):
               
            gr.Markdown('> "ピリオドを基準に字幕ファイルを再編、翻訳に使います。ピリオド区切りのファイルは字幕の区切りが長くなるため、Subtitle Editなどのアプリで「長い文の自動分割機能」を使うと読みやすくなります。例えば、HealingAlSのvimeo動画に付属する字幕をピリオド区切りに再編し、さらに翻訳した字幕ファイルを作ります')
            with gr.Row(equal_height=True):
                vtt_input = gr.File(label="vtt/srtファイルをアップロードしてください。",file_types=['.srt','.vtt'])  # input用のoriginal vtt,srt ",file_types=['srt','vtt']
                with gr.Column():
                    vtt_output_2 = gr.File(label="ピリオド区切りの英語字幕ファイルとワードファイルです。",file_count="multiple")  # 分割・結合処理後のvtt,srtファイル
                    vtt_translated_file = gr.File(label="ピリオド区切りの英文から作った日本語字幕ファイルです。")  # 翻訳されたvtt,srtファイルの出力
            with gr.Row():
                t7_clear_button = gr.Button("クリア")  
                t7_translate_button = gr.Button("日本語vtt,srtの作成",variant='primary')
            with gr.Row():
                vtt_output_1 = gr.HTML()  # 分割・結合処理後のHTML表示
                vtt_translated_content = gr.TextArea(label="翻訳された字幕情報を貼り付けてください。")  # 翻訳処理後の内容を貼り付け。 
                dummy_file=gr.File(visible=False)       

            with gr.Column():
                with gr.Accordion(label="英語dataframe" ,open=False):
                    t7_dataframe=gr.HTML()        

        with gr.Tab("翻訳お手伝い②"):
        
            gr.Markdown(">ピリオドに基づく再編は含まれません。主にtxtファイル、ピリオド再編が不要なsrt,vttファイルが対象です。srt,vtt,txtのいずれかの英文ファイルをアップロードすると内容が表示されます。次にGoogle翻訳で得た翻訳をテキストエリアに入力します。「翻訳ファイルを作成」ボタンを押して、入力ファイルと同形式のファイルに保存します。ファイル名に _ja が付加されます。")
            with gr.Row(equal_height=True):
                file_input = gr.File(label="Upload file", file_count="single",file_types=['.txt','.srt','.vtt'])# ,file_types=['.txt','.srt','.vtt']
                with gr.Column():
                    t4_excel_path=gr.File(label="Excel or Word file for Google translate",type="filepath",file_count="multiple")
                    output_file = gr.File(label="Translated file" ,type='filepath',file_count="multiple")

            with gr.Row():
                t4_clear_button=gr.Button("クリア")
                translate_button = gr.Button("翻訳ファイル作成", variant='primary')
            
            with gr.Row():
                file_content = gr.HTML(label="File content")
                translated_text = gr.TextArea(label="Translated text")
            with gr.Column():
                with gr.Accordion(label="英語dataframe" ,open=False):

                    t4_dataframe=gr.HTML()

        with gr.Tab("whisperファイルの復活"):
            gr.Markdown('> whisperがピリオドを打たなくなったSRTファイルの内容にピリオドを追加して、ピリオド区切りのファイルを生成します。')            
            with gr.Row(equal_height=True):
                with gr.Column():
                    jsonfile=gr.File(label="jsonファイルをアップロードしてください。",type='filepath',file_count="multiple",file_types=['.json'])
                    srtfile=gr.File(label="srtファイルをアップロードしてください。",type='filepath',file_count="multiple",file_types=['.srt'])
                revj=gr.File(label="修復後のファイルです。",type='filepath',file_count="multiple")
            with gr.Row():
                json_execute=gr.Button("ファイルの修復",variant='primary')
                json_clear=gr.Button("クリア")
         
        ### Gradio-Tab5 ###
        with gr.Tab("Word/Excel↔SRT/VTT/TXT"):
            gr.Markdown("> 日本語のword,Excelファイルをsrt/vtt/txt形式に戻すためのプログラムです。wordファイルは末尾が[_srt.xlsx][_vtt.xlsx][_txtnr.docx],[_txtr.docx]、あるいは[_srt (1).xlsx]のように（1）の付加された日本語ファイルが対象です。複数のファイルを一度に扱えますが、アップロードは1回で行う必要があります。")  
            with gr.Column():
                with gr.Row():
                    to_srttxt_input = gr.File(label="Upload docx/xlsx for srt/txt", file_count="multiple", type='filepath',file_types=[".docx",".xlsx"])#,file_types=["docx","xlsx"]
                    to_srttxt_output = gr.File(label="Converted srt/vtt/txt")
                with gr.Row():
                    to_srttxt_button = gr.Button("DOCX/XLSX　→　SRT/TXT", variant='primary')
                    to_srttxt_clear_button = gr.Button("クリア")

            gr.Markdown("> 翻訳準備として、英語のsrt,vttあるいはtxtファイルをword,excel形式に変換するためのプログラムです。srt,vttまたはtxtファイルは末尾が[.srt][.vtt][_NR.txt][_R.txt]のファイルのみ入力できます。複数のファイルを一度に扱えますが、アップロードは1回で行う必要があります。")
            with gr.Row():
                various_file_input = gr.File(file_count='multiple', label="Upload srt/vtt/txt for docx/xlsx",file_types=['.srt','.vtt','.txt'])#,file_types=['srt','vtt','txt']
                output_doc_files = gr.File(file_count='multiple', label="Converted doc/xlsx")
                
            with gr.Row():
                submit_transform_button = gr.Button("SRT/VTT/TXT　→　DOCX/XLSX",variant='primary')
                clear_transform_button = gr.Button("クリア")
                 
        
        

        #tab8
            
        with gr.Tab("日本語srt/vttの句点分割"):
            gr.Markdown("> 日本語字幕ファイルを句点分割します。セグメントが長すぎる字幕に使ってみましょう。これでも長い場合はSubtitle Editをご利用ください。") 
            with gr.Row():
                input_files = gr.File(label="Upload SRT/VTT Files", file_count="multiple",file_types=['.srt','.vtt'])#,file_types=['srt','vtt']
                output_files = gr.File(label="Download SRT/VTT Files")
            with gr.Row():
                process_btn = gr.Button("句点分割",variant="primary")
                clear_btn = gr.Button("Clear")

            process_btn.click(t8.process_and_display, inputs=[input_files], outputs=[output_files])
            clear_btn.click(t8.clear_files, outputs=[input_files, output_files])
        ### Gradio-Tab3 ###
        
        with gr.Tab("SRT/VTT→Excel(2言語)"):
            gr.Markdown("> 英語と日本語を並べて読むためのツールです。文字起こしの際に作成できるexcelファイルと同じです。2つのsrtファイルはタイムスタンプが一致している必要があります。")   
            lang_for_xls_choice = gr.Radio(
                choices=["English and Japanese", "only English", "only Japanese"],
                label="どんなExcelファイルを作りますか？",
                interactive=True,
                value="English and Japanese"
            )
            with gr.Row(equal_height=True):
                english_file = gr.File(label="英語のSRT,VTTファイルをアップロード", visible=True,file_types=['.srt','.vtt'])#,file_types=['srt','vtt']
                japanese_file = gr.File(label="日本語のSRT,VTTファイルをアップロード", visible=True,file_types=['.srt','.vtt'])#,file_types=['srt','vtt']
                
            with gr.Row():        
                submit_button = gr.Button("Excelファイル作成",variant='primary')
                clear_button = gr.Button("クリア")   
            excel_output = gr.File(label="Excelファイルをダウンロード。")       
            dataframe_output = gr.HTML()
        
            
            # クリアボタンをクリックした時にファイルをクリア
            clear_button.click(
                fn=t3.clear_all_files,
                outputs=[english_file, japanese_file, dataframe_output, excel_output]
            )

            # ラジオボタンの選択変更でファイルのクリアとコンポーネントの表示を更新
            lang_for_xls_choice.change(
                fn=t3.update_visibility_and_clear,
                inputs=[lang_for_xls_choice],
                outputs=[english_file, japanese_file, dataframe_output, excel_output]
            )
            
        # ファイルを処理してデータフレームとExcelファイルを生成する
        def process_files(english_file, japanese_file, choice):
            if english_file is None and japanese_file is None:
                return pd.DataFrame({'1': [''], '2': [''], '3': ['']}), None
            
            
            if choice == "only English":
                excel_path, df = t3.create_excel_from_srt(english_path=english_file,tail="")
            elif choice == "only Japanese":
                excel_path, df = t3.create_excel_from_srt(japanese_path=japanese_file,tail="")
            else:  # "English and Japanese"
                excel_path, df = t3.create_excel_from_srt(english_path=english_file, japanese_path=japanese_file,tail="")
            
            df=t1.dataframe_to_html_table(df)
            df=f"""
                <div class="my-table-container">
                    {df}
                </div>
            """                        
            
            
            return df, excel_path
        
        #tab9 License
        with gr.Tab("LICENSES"):
            gr.Markdown("> LICENSE条項です。お読みの上、ご利用ください。")
            # mdファイルを読み込む
            # mdファイルを読み込んでHTMLに変換する
            import markdown2
            def load_md_to_html():
                with open("LICENSES.md", "r", encoding="utf-8") as file:
                    content = file.read()
                # markdown2のtables拡張機能を有効にしてHTMLに変換
                html_content = markdown2.markdown(content, extras=["tables"])
                return html_content

            gr.HTML(load_md_to_html)




        ##クリアボタン追加分をまとめる。
        '''def t1_clear():
            empty_html_table = pd.DataFrame({'1': [''], '2': [''], '3': ['']}).to_html(index=False)
            return None,"","","",[],[],"","","","","",empty_html_table
        def t2_clear():
            return "","","",[],pd.DataFrame({'1': [''], '2': [''],'3': ['']})'''
        def t4_clear():
            empty_html_table = pd.DataFrame({'1': [''], '2': [''], '3': ['']}).to_html(index=False)
            return None,"","",[],[],empty_html_table

        '''def t6_clear():
            return None,None,[]'''
        
        def t7_clear():
            empty_html_table = pd.DataFrame({'1': [''], '2': [''], '3': ['']}).to_html(index=False)
            return None,None,None,None,None,None,empty_html_table
        

        ### Tab3 イベントリスナー　###
        submit_button.click(
                fn=process_files,
                inputs=[english_file, japanese_file, lang_for_xls_choice],
                outputs=[dataframe_output, excel_output]
            )

        ### Tab4 イベントリスナー ###
        file_input.change(fn=t4.display_file_content, inputs=file_input, outputs=[file_content, t4_excel_path,t4_dataframe])

        translate_button.click(fn=t4.translate, inputs=[file_input, translated_text], outputs=output_file)

        t4_clear_button.click(fn=t4_clear,inputs=[],outputs=[file_input,file_content,translated_text,output_file,t4_excel_path,t4_dataframe])
        ### Tab5 イベントリスナー ###
        to_srttxt_button.click(
        fn=t5.convert_docx_to_srttxt,
        inputs=to_srttxt_input,
        outputs=to_srttxt_output
        )
        
        to_srttxt_clear_button.click(
            fn=t5.clear_inputs,
            inputs=[],
            outputs=[to_srttxt_input, to_srttxt_output]
        )

        submit_transform_button.click(t5.process_doc_files, inputs=various_file_input, outputs=output_doc_files)
        clear_transform_button.click(t5.clear_both, inputs=None, outputs=[various_file_input, output_doc_files])   
        ### Tab6 イベントリスナー ###
        '''generate_voice.click(
            fn=t6.tts,
            inputs=[input_audio,voice_select],
            outputs=[output_audio,download_audio] )
        t6_clear_button.click(
            fn=t6_clear,
            inputs=[],
            outputs=[input_audio,output_audio,download_audio]
        )'''
        ### Tab7 イベントリスナー ###
        vtt_input.upload(
        fn=t7.process_file, inputs=[vtt_input], outputs=[vtt_output_1, vtt_output_2,dummy_file,t7_dataframe])
        t7_translate_button.click(
            fn=t7.vtt_translate,
            inputs=[vtt_input, vtt_translated_content,dummy_file],
            outputs=[vtt_translated_file]
        )
        t7_clear_button.click(
            fn=t7_clear,
            inputs=[],
            outputs=[vtt_input,vtt_translated_content,vtt_translated_file,vtt_output_1,vtt_output_2,dummy_file,t7_dataframe]
        )
        def fn_j_clear():
            return [],[],[]
        
        json_clear.click(
            fn=fn_j_clear,
            inputs=[],
            outputs=[jsonfile,srtfile,revj]
        )
        json_execute.click(
            fn=json_rv.run_spacy,
            inputs=[jsonfile,srtfile],
            outputs=[revj]
        )



        return UI