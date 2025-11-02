# === AI OPTIMIZED VERSION OF THE vocalscribe1 project ===

import flet as ft
import speech_recognition as sr
import os
import threading

def main(page: ft.Page):
    page.title = "PROJECT B"
    page.window.width = 600
    page.window.height = 700
    page.window.maximizable = False
    page.window.resizable = False
    page.bgcolor = "#4D0213"
    page.window.center()
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    uploaded_file_path = None
    transcription_text = ft.TextField(
        label="Audio Transcription",
        multiline=True,
        min_lines=2,
        border_color="BROWN",
        color="white",
        read_only=True,
        width=page.window.width - 60,
        filled=True,
    )

    status_text = ft.Text("", color="WHITE60", italic=True)

    # --- File picker for upload ---
    def upload_file_result(e: ft.FilePickerResultEvent):
        nonlocal uploaded_file_path
        if e.files:
            uploaded_file_path = e.files[0].path
            status_text.value = f"✅ File uploaded: {os.path.basename(uploaded_file_path)}"
        else:
            status_text.value = "⚠️ No file selected."
        page.update()

    file_picker = ft.FilePicker(on_result=upload_file_result)
    page.overlay.append(file_picker)

    # --- File picker for saving ---
    save_picker = ft.FilePicker()
    page.overlay.append(save_picker)

    def save_file_result(e: ft.FilePickerResultEvent):
        if e.path:
            try:
                with open(e.path, "w", encoding="utf-8") as f:
                    f.write(transcription_text.value)
                status_text.value = f"💾 Saved: {os.path.basename(e.path)}"
            except Exception as err:
                status_text.value = f"⚠️ Error saving file: {err}"
        else:
            status_text.value = "⚠️ Save cancelled."
        page.update()

    save_picker.on_result = save_file_result

    # --- Transcription logic (chunked) ---
    def transcribe_audio_in_chunks(file_path):
        recognizer = sr.Recognizer()
        transcription = ""

        with sr.AudioFile(file_path) as source:
            while True:
                try:
                    # Process small chunks of audio
                    audio_data = recognizer.record(source, duration=10)  # 10-second chunks
                    if not audio_data.frame_data:
                        break
                    chunk_text = recognizer.recognize_google(audio_data)
                    transcription += chunk_text + " "
                except sr.UnknownValueError:
                    transcription += "❌ [unintelligible] "
                except sr.RequestError as e:
                    transcription += f"⚠️ [API error: {e}] "
        return transcription.strip()

    def run_transcription():
        if not uploaded_file_path:
            transcription_text.value = "Please upload a WAV file first."
            status_text.value = ""
            page.update()
            return

        transcription_text.value = ""
        status_text.value = "🎧 Transcribing, please wait..."
        page.update()

        result = transcribe_audio_in_chunks(uploaded_file_path)

        transcription_text.value = result
        status_text.value = "✅ Transcription complete!"
        page.update()

    def transcribe_clicked(e):
        threading.Thread(target=run_transcription).start()

    def download_clicked(e):
        if transcription_text.value.strip():
            save_picker.save_file(file_name="transcription.txt", allowed_extensions=["txt"])
        else:
            status_text.value = "Nothing to download yet!."
            page.update()

    # === UI ===
    page.add(
        ft.Row(
            controls=[ft.Text("🎙 VocalScribe", size=40, color=ft.Colors.WHITE60, weight=ft.FontWeight.BOLD)],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Container(height=20),
        ft.Row(
            controls=[
                ft.FilledButton(
                    text="Click Here to upload audio file",
                    icon=ft.Icons.UPLOAD_FILE,
                    bgcolor="#9d806c",
                    color="#320010",
                    height=60,
                    width=page.window.width - 60,
                    on_click=lambda _: file_picker.pick_files(
                        allow_multiple=False, allowed_extensions=["wav", "mp3", "flac"]
                    ),
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Container(height=20),
        ft.Row(controls=[transcription_text], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(height=25),
        ft.Row(
            controls=[
                ft.FilledButton(text="Transcribe", icon=ft.Icons.TEXT_SNIPPET, on_click=transcribe_clicked, bgcolor="#9d806c", color="#320010"),
                ft.FilledButton(text="Download as .TXT", icon=ft.Icons.DOWNLOAD, on_click=download_clicked, bgcolor="#9d806c", color="#320010"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        ft.Container(height=15),
        ft.Row(controls=[status_text], alignment=ft.MainAxisAlignment.CENTER),
    )

ft.app(main)




# # === SECOND VERSION ===
#
# import flet as ft
# import speech_recognition as sr
# import os
# import threading
#
# def main(page: ft.Page):
#     page.title = "PROJECT"
#     page.window.width = 600
#     page.window.height = 700
#     page.window.maximizable = False
#     page.window.resizable = False
#     page.bgcolor = "#4D0213"
#     page.window.center()
#     page.padding = 20
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER
#
#     # --- Store uploaded file path ---
#     uploaded_file_path = None
#
#     # --- Text field to show transcription ---
#     transcription_text = ft.TextField(
#         label="Audio Transcription",
#         multiline=True,
#         min_lines=2,
#         border_color="BROWN",
#         color="white",
#         read_only=True,
#         width=page.window.width - 60,
#         filled=True,
#     )
#
#     # --- Italic status text ---
#     status_text = ft.Text("", color="WHITE60", italic=True)
#
#     # --- File picker for uploading audio ---
#     def upload_file_result(e: ft.FilePickerResultEvent):
#         nonlocal uploaded_file_path
#         if e.files:
#             uploaded_file_path = e.files[0].path
#             status_text.value = f"✅ File uploaded: {os.path.basename(uploaded_file_path)}"
#         else:
#             status_text.value = "⚠️ No file selected."
#         page.update()
#
#     file_picker = ft.FilePicker(on_result=upload_file_result)
#     page.overlay.append(file_picker)
#
#     # --- File picker for saving transcription ---
#     save_picker = ft.FilePicker()
#     page.overlay.append(save_picker)
#
#     def save_file_result(e: ft.FilePickerResultEvent):
#         if e.path:
#             try:
#                 with open(e.path, "w", encoding="utf-8") as f:
#                     f.write(transcription_text.value)
#                 status_text.value = f"💾 Saved: {os.path.basename(e.path)}"
#             except Exception as err:
#                 status_text.value = f"⚠️ Error saving file: {err}"
#         else:
#             status_text.value = "⚠️ Save cancelled."
#         page.update()
#
#     save_picker.on_result = save_file_result
#
#     # --- Speech recognition ---
#     def transcribe_audio(file_path):
#         recognizer = sr.Recognizer()
#         with sr.AudioFile(file_path) as source:
#             audio_data = recognizer.record(source)
#         try:
#             text = recognizer.recognize_google(audio_data)
#             return text
#         except sr.UnknownValueError:
#             return "❌ Sorry, could not understand the audio."
#         except sr.RequestError as e:
#             return f"⚠️ Could not request results; {e}"
#
#     # --- Transcription thread ---
#     def run_transcription():
#         if not uploaded_file_path:
#             transcription_text.value = "Please upload a WAV file first."
#             status_text.value = ""
#             page.update()
#             return
#
#         transcription_text.value = ""
#         status_text.value = "🎧 Transcribing, please wait..."
#         page.update()
#
#         result = transcribe_audio(uploaded_file_path)
#
#         transcription_text.value = result
#         status_text.value = "✅ Transcription complete!"
#         page.update()
#
#     def transcribe_clicked(e):
#         threading.Thread(target=run_transcription).start()
#
#     # --- Download button handler ---
#     def download_clicked(e):
#         if transcription_text.value.strip():
#             save_picker.save_file(
#                 file_name="transcription.txt",
#                 allowed_extensions=["txt"]
#             )
#         else:
#             status_text.value = "Nothing to download yet!."
#             page.update()
#
#     # === UI ===
#     page.add(
#         ft.Row(
#             controls=[
#                 ft.Text(
#                     "🎙 VocalScribe",
#                     size=40,
#                     color=ft.Colors.WHITE60,
#                     weight=ft.FontWeight.BOLD,
#                 )
#             ],
#             alignment=ft.MainAxisAlignment.CENTER,
#         ),
#
#         ft.Container(height=20),
#
#         # Upload button
#         ft.Row(
#             controls=[
#                 ft.FilledButton(
#                     text="Click Here to upload audio file",
#                     icon=ft.Icons.UPLOAD_FILE,
#                     bgcolor="#9d806c",
#                     color="#320010",
#                     height=60,
#                     width=page.window.width - 60,
#                     on_click=lambda _: file_picker.pick_files(
#                         allow_multiple=False,
#                         allowed_extensions=["wav", "mp3", "flac"]
#                     )
#                 )
#             ],
#             alignment=ft.MainAxisAlignment.CENTER,
#         ),
#
#         ft.Container(height=20),
#
#         # Text field
#         ft.Row(
#             controls=[transcription_text],
#             alignment=ft.MainAxisAlignment.CENTER,
#         ),
#
#         ft.Container(height=25),
#
#         # Buttons
#         ft.Row(
#             controls=[
#                 ft.FilledButton(
#                     text="Transcribe",
#                     icon=ft.Icons.TEXT_SNIPPET,
#                     on_click=transcribe_clicked,
#                     bgcolor="#9d806c",
#                     color="#320010",
#                 ),
#                 ft.FilledButton(
#                     text="Download as .TXT",
#                     icon=ft.Icons.DOWNLOAD,
#                     on_click=download_clicked,
#                     bgcolor="#9d806c",
#                     color="#320010",
#                 ),
#             ],
#             alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#         ),
#
#         ft.Container(height=15),
#
#         # Status text
#         ft.Row(
#             controls=[status_text],
#             alignment=ft.MainAxisAlignment.CENTER,
#         ),
#     )
#
#
# ft.app(main)