from direct.gui.DirectGui import DirectFrame, DirectButton, OnscreenText
from panda3d.core import TextNode, LVector4f
from syntax.parse import parse  # Assuming this module exists and is functional

class CodeMenu:
    def __init__(self, base):
        self.base = base

        # Set up a key listener for user input
        self.base.main.add_any_key(self.on_key_press)

        # Initialize content and UI elements
        self.content = []
        self.elements = []

        # Create the main frame for the IDE
        self.ide_frame = DirectFrame(
            frameColor=(0.1, 0.1, 0.1, 1),
            frameSize=(-1.2, 1.2, -0.8, 0.8),
            pos=(0, 0, 0)
        )

        # Terminal Frame
        self.terminal_frame = DirectFrame(
            frameColor=(0.1, 0.1, 0.1, 1),
            frameSize=(-1.2, 1.2, -0.8, 0),
            pos=(0, 0, -0.8)
        )
        self.result = OnscreenText(
            text="",
            parent=self.terminal_frame,
            scale=0.05,
            pos=(-1.15, 0.7),
            align=TextNode.ALeft,
            fg=(1, 1, 1, 1)
        )

        self.terminal_back_button = DirectButton(
            text="Back to IDE",
            parent=self.terminal_frame,
            scale=0.1,
            pos=(1.0, 0, -0.75),
            command=self.show
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

        # Run Button
        self.run_button = DirectButton(
            text="Run",
            parent=self.ide_frame,
            scale=0.1,
            pos=(0.1, 0, -0.7),
            command=self.run_code
        )

        self.ide_frame.hide()
        self.terminal_frame.hide()
        self.visible = False

    def clear_code_text(self):
        for element in self.elements:
            element.removeNode()


    def create_colored_text(self, code_lines):
        text_elements = []
        y_start = 0.5
        line_spacing = 0.1
        line_count = 0
        offset_x = 0
        space_width = 0.05  # Set a fixed width for spaces

        for i, (text, color_hex) in enumerate(code_lines):
            r, g, b = self.hex_to_rgb(color_hex)
            color = LVector4f(r, g, b, 1.0)
            text_node = TextNode(f"line-{i}")
            text_node.setText(text)
            text_node.setTextColor(color)

            # Create a new text node parented to the IDE frame
            text_np = self.ide_frame.attachNewNode(text_node)
            text_np.setScale(0.07)
            text_np.setPos(-1.15 + offset_x, 0, y_start - line_count * line_spacing)

            # Adjust line count and offset for positioning
            if text == "\n":
                line_count += 1
                offset_x = 0
            elif text == " ":
                offset_x += space_width  # Use a fixed space width for spaces
            else:
                offset_x += len(text) * 0.05  # Adjust horizontal offset based on text length

            text_elements.append(text_np)

        return text_elements



    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

    def run_code(self):
        # Combine the content list into a single code string
        code_string = "".join(self.content)
        print("Running Code:")
        print(code_string)  # Debug output

        try:
            # Capture the output using a custom print function
            output = []
            exec(
                code_string,
                {
                    "__builtins__": {
                        "range": range, "sum": sum, "print": lambda *args: output.append(" ".join(map(str, args))), "len": len
                    }
                }
            )
            self.result.setText("\n".join(output))
        except Exception as e:
            self.result.setText(f"Error: {e}")

        # Switch to the terminal frame
        self.ide_frame.hide()
        self.terminal_frame.show()
        self.visible = False  # Ensure we know the IDE is hidden

    def show(self):
        """Show the IDE frame and prepare for code input."""
        print("Showed Code IDE")
        self.visible = True
        self.ide_frame.show()
        self.terminal_frame.hide()

    def hide(self):
        """Hide both IDE and terminal frames."""
        self.visible = False
        self.ide_frame.hide()
        self.terminal_frame.hide()


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


    def show_terminal(self):
        """Show the terminal frame explicitly."""
        self.ide_frame.hide()
        self.terminal_frame.show()

    def show_ide(self):
        """Return to the IDE explicitly."""
        self.terminal_frame.hide()
        self.ide_frame.show()