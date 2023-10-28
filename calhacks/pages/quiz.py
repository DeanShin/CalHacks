import reflex as rx

from calhacks.state import State


class QuizState(State):
    questions = ['test 1', 'test 2', 'test 3']
    question_number: int = 0

    def on_page_opened(self):
        return rx.call_script("""
            window.mediaRecorder;
            window.chunks = []
            navigator.mediaDevices
                .getUserMedia(
                  // constraints - only audio needed for this app
                  {
                    audio: true,
                    video: true
                  },
                )
                .then(stream => {
                    window.mediaRecorder = new MediaRecorder(stream)
                    window.mediaRecorder.start();
                    console.log(window.mediaRecorder.state);
                    window.mediaRecorder.ondataavailable = (e) => {
                        window.chunks.push(e.data);
                        console.log(window.chunks);
                    };
                })
        """)

    def stop_recording(self):
        return rx.call_script(
            """
                window.mediaRecorder.onstop = () => {
                    const blob = new Blob(chunks, { type: "video/x-matroska;codecs=avc1,opus" });
                    console.log(blob)
                    const fileReader = new FileReader();
                    fileReader.onloadend = () => {
                        console.log("load end")
                        console.log(fileReader.result)
                        window.result = fileReader.result
                    }
                    fileReader.readAsArrayBuffer(blob);
                }
                window.mediaRecorder.stop()
            """
        )

    def next_question(self):
        # currently, we will only ask a single question
        return rx.call_script(
            """
                console.log("result", new Uint8Array(window.result))
                new Uint8Array(window.result)[0]
            """,
            callback=QuizState.receive_chunks
        )

    def receive_chunks(self, chunks):
        print('here')
        # print(chunks)

@rx.page()
def quiz():
    return rx.grid(
        rx.box(),
        rx.center(
            rx.heading(
                "fasdfjadsklfjdslkf asdjf asdjf lkasdjflkadsa fjklasf ldskafd",
                size="xl",
                text_align="center",
                max_width="60%"
            ),
        ),
        rx.center(
            rx.button(
                "Finish question",
                on_click=QuizState.stop_recording,
            ),
            rx.button(
                "Process recording",
                on_click=QuizState.next_question,
            )
        ),
        rx.box(),
        width="100dvw",
        height="100dvh",
        align_items="center",
        grid_template_rows="1fr 40% 20% 1fr",
        on_mount=QuizState.on_page_opened
    )
