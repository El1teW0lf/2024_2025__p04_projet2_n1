from direct.gui.DirectGui import DirectFrame, DirectButton, OnscreenText, DirectEntry, DirectScrolledFrame
from panda3d.core import TextNode
from syntax.parse import parse
from panda3d.core import TextNode, LVector4f

class CodeMenu:
    def __init__(self, base):
        self.base = base

        self.base.main.add_any_key(self.on_key_press)

        self.content = []
        self.elements = []

        self.ide_frame = DirectFrame(
            frameColor=(0.1, 0.1, 0.1, 1),
            frameSize=(-1.2, 1.2, -0.8, 0.8),
            pos=(0, 0, 0)
        )

        self.base.main.ui["code_ide"] = self.ide_frame

        # Title
        self.title = OnscreenText(
            text="Coding IDE",
            parent=self.ide_frame,
            scale=0.1,
            pos=(0, 0.65),
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter
        )

        self.ide_frame.hide()
        self.visible = False

    def create_colored_text(self, code_lines):
        text_elements = []
        y_start = 0.5
        line_spacing = 0.1
        line_count = 0
        offset_x = 0
        for i, (text, color_hex) in enumerate(code_lines):
            r, g, b = self.hex_to_rgb(color_hex)
            color = LVector4f(r, g, b, 1.0)
            text_node = TextNode(f"line-{i}")
            text_node.setText(text)
            text_node.setTextColor(color)
            text_np = self.title.attachNewNode(text_node)
            text_np.setScale(0.07)
            text_np.setPos(-1.0 + offset_x, 0, y_start - line_count * line_spacing)

            if text == "\n":
                line_count += 1
                offset_x = 0
            else:
                offset_x += text_node.getWidth() * text_np.getScale()[0]

            text_elements.append(text_np)

        return text_elements


    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

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
        print("Showed Code IDE")
        self.visible = True
        self.ide_frame.show()

    def hide(self):
        self.visible = False
        self.ide_frame.hide()

    def get_code_text(self):
        result = ""
        for i in self.content:
            result += i
        return result

    def clear_code_text(self):
        for element in self.elements:
            element.removeNode()

    def on_key_press(self, key):
                
        big_keys=["enter","tab","space"]
        big_chars=["\n","\t"," "]
        print(key)
        if self.visible:
            if len(key) == 1:
                self.content.append(key)
            elif key in big_keys:
                self.content.append(big_chars[big_keys.index(key)])
            elif key == "backspace":
                self.content.pop()

        self.clear_code_text()
        self.elements = self.create_colored_text(parse(self.content + ["\n"]))
        