class Emitter:
    """ The Emitter object keeps track of the generated code and outputs it.
        A helper class for appending strings together.
    """

    def __init__(self, full_path):
        self.full_path: str = full_path  # The path to write the resulting C code
        self.header: str = ""  # Things to prepend to the code later on
        self.code: str = ""  # The C code to emit

    def emit_code(self, code: str) -> None:
        # Add a fragment of C code
        self.code += code

    def emit_line(self, code: str) -> None:
        # Add a fragment of C code that ends a line
        self.code += code + "\n"

    # def emit(self, code: str, newline: bool = True):
        # Add a fragment of C code, with or without a newline
        # self.code + "\n" if newline else self.code
        # self.code += code + "\n" if newline else 

    def header_line(self, code) -> None:
        # Add a line of C code to the top of the C code file
        self.header += code + "\n"
    # def headerLine(self, code):
    #     self.header += code + '\n'

    def write(self) -> None:
        # Write out the resulting C code to a file
        with open(self.full_path, "w") as output_file:
            output_file.write(self.header + self.code)

