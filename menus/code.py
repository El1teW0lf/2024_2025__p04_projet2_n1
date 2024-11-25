from direct.gui.DirectGui import DirectFrame, DirectButton, OnscreenText, DirectEntry, DirectScrolledFrame
from panda3d.core import TextNode


class CodeMenu:
    def __init__(self, base):
        self.base = base

        self.base.base.add_any_key(self.on_key_press)

        self.ide_frame = DirectFrame(
            frameColor=(0.1, 0.1, 0.1, 1),
            frameSize=(-1.2, 1.2, -0.8, 0.8),
            pos=(0, 0, 0)
        )

        self.base.base.ui["code_ide"] = self.ide_frame

        # Title
        self.title = OnscreenText(
            text="Coding IDE",
            parent=self.ide_frame,
            scale=0.1,
            pos=(0, 0.65),
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter
        )

        self.editor = OnscreenText(
            text="",
            parent=self.title,
            pos=(0,0),
            scale=0.1,
            fg=(1,1,1,1),
            align=TextNode.ALeft
        )

        self.ide_frame.hide()



    def append_code(self, text):
        print(self.code_editor["text"])
        current_code = self.code_editor["text"]
       # self.code_editor.setText(current_code + text + "\n")
       # self.text_input.enterText("")  # Clear the input box

    def run_code(self):
        print(self.code_editor["text"])
        try:
            exec(self.code_editor["text"],{"__builtins__": {
            "range": range,
            "sum": sum,
            "print": print,
        }})
        except Exception as e:
            print(f"Error: {e}")

    def clear_code(self):
        """Clear the code editor."""
        self.code_editor.setText("")

    def show(self):
        """Show the IDE frame."""
        self.ide_frame.show()

    def hide(self):
        """Hide the IDE frame."""
        self.ide_frame.hide()

    def on_key_press(self, key):
                print(f"Key pressed: {key}")