import reflex as rx


from calhacks.state import State


class QuizState(State):
    questions = ['Question 1', 'Question 2', 'Question 3', 'Question 4']
    question_number: int = 0

    def on_page_opened(self):
        return rx.call_script("""
            window.mediaRecorder;
            window.onDownloadComplete = () => {
            
            }
            window.questionNumber = 0
            navigator.mediaDevices
                .getUserMedia(
                  {
                    audio: true,
                    video: true
                  },
                )
                .then(stream => {
                    window.mediaRecorder = new MediaRecorder(stream, {mimeType: 'video/webm'})
                    window.mediaRecorder.ondataavailable = (e) => {
                        const url = URL.createObjectURL(e.data);
                        
                        // Create a link element
                        const link = document.createElement("a");
                        
                        // Set link's href to point to the Blob URL
                        link.href = url;
                        link.download = 'question_' + questionNumber + '.webm';
                        // I do not wish this code upon my worst enemy
                        questionNumber++;
                        
                        link.dispatchEvent(
                            new MouseEvent('click', {
                                bubbles: true, 
                                cancelable: true, 
                                view: window 
                            })
                        );
                        
                        window.onDownloadComplete();
                    };
                    window.mediaRecorder.start();
                })
        """)

    def on_next_question_pressed(self):
        self.question_number += 1
        if self.question_number == len(self.questions):
            return rx.call_script(
                """
                    window.onDownloadComplete = () => {
                        window.location.href = "/results"
                    }
                    window.mediaRecorder.stop()
                """,
            )
        return rx.call_script(
            f"""
                window.mediaRecorder.stop()
                window.mediaRecorder.start()
            """
        )


@rx.page()
def quiz():
    return rx.grid(
        rx.box(),
        rx.center(
            rx.heading(
                QuizState.questions[QuizState.question_number],
                size="xl",
                text_align="center",
                max_width="60%"
            ),
        ),
        rx.center(
            rx.button(
                "Next question",
                on_click=QuizState.on_next_question_pressed,
            )
        ),
        rx.box(),
        width="100dvw",
        height="100dvh",
        align_items="center",
        grid_template_rows="1fr 40% 20% 1fr",
        on_mount=QuizState.on_page_opened
    )
