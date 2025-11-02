# ==== MAIN AUDIO TO TEXT TRANSCRIPTION PROJECT


import flet as ft
import speech_recognition as sr
import os
import threading
def main(page: ft.Page):
    page.title = "PROJECT"
    page.window.width = 600
    page.window.height = 700
    page.window.maximizable = False
    page.window.resizable = False
    # page.bgcolor = "#76404E"
    page.bgcolor = "#4D0213"
    # page.bgcolor = "#66001F"
    page.window.center()
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    uploaded_file_path = None  # store path
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

    # italic live status text
    status_text = ft.Text("", color="WHITE60", italic=True)

    # --- file picker ---
    def upload_file_result(e: ft.FilePickerResultEvent):
        nonlocal uploaded_file_path
        if e.files:
            uploaded_file_path = e.files[0].path
            status_text.value = f"File uploaded: {os.path.basename(uploaded_file_path)}"
        else:
            status_text.value = "⚠️ No file selected."
        page.update()

    file_picker = ft.FilePicker(on_result=upload_file_result)
    page.overlay.append(file_picker)

    # --- transcription logic ---
    def transcribe_audio(file_path):
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "❌ Sorry, could not understand the audio."
        except sr.RequestError as e:
            return f"⚠️ Could not request results; {e}"

    def run_transcription():
        if not uploaded_file_path:
            transcription_text.value = "Please upload a WAV file first."
            status_text.value = ""
            page.update()
            return

        transcription_text.value = ""
        status_text.value = "🎧Transcribing, please wait..."
        page.update()

        result = transcribe_audio(uploaded_file_path)

        transcription_text.value = result
        status_text.value = "Transcription complete!"
        page.update()

    def transcribe_clicked(e):
        threading.Thread(target=run_transcription).start()

    # --- download logic ---
    def download_clicked(e):
        if transcription_text.value.strip():
            filename = "transcription.txt"
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(transcription_text.value)
                # Automatically open or show the saved file
                page.launch_url(f"file://{os.path.abspath(filename)}")
                status_text.value = f"💾 Transcription saved and opened: {filename}!"
            except Exception as err:
                status_text.value = f"Error saving file!: {err}"
        else:
            status_text.value = "Nothing to download yet!."
        page.update()

    # txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    # === UI ===
    page.add(
        ft.Row(
            controls=[
                ft.Text(
                    "🎙 VocalScribe",
                    size=40,
                    color=ft.Colors.WHITE60,
                    weight=ft.FontWeight.BOLD,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),


        ft.Container(height=20),

        # === UPLOAD BUTTON ===
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
                        allow_multiple=False,
                        allowed_extensions=["wav", "mp3", "flac"]
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),

        ft.Container(height=20),  # gap between upload and text field

        # === Text Field (now using the same one defined above) ===
        ft.Row(
            controls=[transcription_text],


            alignment=ft.MainAxisAlignment.CENTER,
        ),


        ft.Container(height=25),  # gap between text field and buttons

        # === Buttons (Transcribe + Download) ===

        ft.Row(
            controls=[
                ft.FilledButton(
                    text= "Transcribe",
                    icon=ft.Icons.TEXT_SNIPPET,
                    on_click = transcribe_clicked,
                    bgcolor="#9d806c",
                    color="#320010",

                ),

                ft.FilledButton(
                    text="Download as .TXT",
                    icon=ft.Icons.DOWNLOAD,
                    on_click=download_clicked,
                    bgcolor="#9d806c",
                    color="#320010",

                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),

        ft.Container(height=15),

        # Status text displayed below buttons
        ft.Row(
            controls=[status_text],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

ft.app(main)