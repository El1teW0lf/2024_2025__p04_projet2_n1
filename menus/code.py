from direct.gui.DirectGui import DirectFrame, DirectButton, OnscreenText
from panda3d.core import TextNode, LVector4f
from syntax.parse import parse  # Assuming this module exists and is functional
import multiprocessing
import time


class TimeoutException(Exception):
    pass

class CodeMenu:
    def __init__(self, base):
        self.base = base

        # Set up a key listener for user input
        self.base.main.add_any_key(self.on_key_press)

        # Initialize content and UI elements
        self.content = []
        self.elements = []
        self.base.main.accept('shift', self.on_shift_press)  # Listen for shift press
        self.base.main.accept('shift-up', self.on_shift_release)  # Listen for shift release
        self.is_shift_pressed = False

        # Create the main frame for the IDE
        self.ide_frame = DirectFrame(
            frameColor=(0.1, 0.1, 0.1, 1),
            frameSize=(-1.2, 1.2, -0.8, 0.8),
            pos=(0, 0, 0)
        )

        # Terminal Frame
        self.terminal_frame = DirectFrame(
            frameColor=(0.1, 0.1, 0.1, 1),
            frameSize=(-1.2, 1.2, -0.8, 0.8),
            pos=(0, 0, 0)
        )
        self.terminal_title = OnscreenText(
            text="Result",
            parent=self.terminal_frame,
            scale=0.1,
            pos=(0, 0.65),
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter
        )
        self.result = OnscreenText(
            text="",
            parent=self.terminal_frame,
            scale=0.05,
            pos=(-1.0, 0.5),
            align=TextNode.ALeft,
            fg=(1, 1, 1, 1)
        )

        self.terminal_back_button = DirectButton(
            text="Back to IDE",
            parent=self.terminal_frame,
            scale=0.1,
            pos=(0.1, 0, -0.7),
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

    def on_shift_press(self):
        # Set the flag when Shift is pressed
        self.is_shift_pressed = True

    def on_shift_release(self):
        # Reset the flag when Shift is released
        self.is_shift_pressed = False

    def clear_code_text(self):
        for element in self.elements:
            element.removeNode()


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

    def run_code(self, timeout=5):
        code_string = "".join(self.content)
        print("Running Code:")
        print(code_string)  

        def execute_code(output_queue):
            try:
                output = []
                exec(
                    code_string,
                    {
                        "__builtins__": {
                            "range": range,
                            "sum": sum,
                            "print": lambda *args: output.append(" ".join(map(str, args))),
                            "len": len
                        }
                    }
                )
                output_queue.put("\n".join(output))
            except Exception as e:
                output_queue.put(f"Error: {e}")

        output_queue = multiprocessing.Queue()
        print("Created Process queue")

        process = multiprocessing.Process(target=execute_code, args=(output_queue,))
        process.start()
        print("Started Child thread")

        process.join(timeout)
        
        if process.is_alive():
            process.terminate()  
            process.join()  
            self.result.setText("Error: Execution timed out!")
        else:
            if not output_queue.empty():
                output = output_queue.get()
                self.result.setText(output)

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
            if self.is_shift_pressed and len(key) == 1:
                self.content.append(key.upper())
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