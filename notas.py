from tkinter import Misc
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.validation import add_regex_validation


class Gradebook(ttk.Frame):
    def __init__(self, master_window):
        super().__init__(master_window, padding=(20,10))
        self.pack(fill=BOTH, expand=YES)
        self.name = ttk.StringVar(value="")
        self.student_id = ttk.StringVar(value="")
        self.course_name = ttk.StringVar(value="")
        self.final_score = ttk.DoubleVar(value=0)
        self.data = []
        self.colors = master_window.style.colors

        instruction_text = "Por favor, entre com suas informações: "
        instruction = ttk.Label(self, text=instruction_text, width=50)
        instruction.pack(fill=X, pady=10)

        self.create_form_entry("Nome: ", self.name)
        self.create_form_entry("RA: ", self.student_id)
        self.create_form_entry("Nome do curso: ", self.course_name)
        self.final_score_input = self.create_form_entry("Resultado final: ", self.final_score)

        self.create_meter()
        self.create_buttonbox()

        self.table = self.create_table()



    def create_form_entry(self, label,variable):
        form_field_container = ttk.Frame(self)
        form_field_container.pack(fill=X, expand=YES,pady=5)

        form_field_label = ttk.Label(master=form_field_container, text=label,width=15)
        form_field_label.pack(side=LEFT, pady=12)

        form_input = ttk.Entry(master=form_field_container, textvariable=variable)
        form_input.pack(side=LEFT, padx=5, fill="x", expand=YES)

        add_regex_validation(form_input, r'^[a-zA-z0-9_]*$')
        return form_input

    
    def create_meter(self):
        meter = ttk.Meter(
            master=self,
            metersize=150,
            padding = 5,
            amounttotal=100,
            amountused=50,
            metertype="full",
            subtext="Resultado Final",
            interactive=True
        )
        meter.pack()
        self.final_score.set(meter.amountusedvar)
        self.final_score_input.configure(textvariable=meter.amountusedvar)



    def create_buttonbox(self):
        button_container = ttk.Frame(self)
        button_container.pack(fill='x', expand=YES, pady=(15,10))

        cancel_btn = ttk.Button(
            master= button_container,
            text="Cancelar",
            command= self.on_cancel,
            bootstyle = DANGER,
            width=7
        )
        cancel_btn.pack(side = 'right',padx = 5)

        submit_btn = ttk.Button(
            master= button_container,
            text="Enviar",
            command= self.on_submit,
            bootstyle = SUCCESS,
            width=6
        )
        submit_btn.pack(side = 'right', padx = 5)
    
    
    def on_submit(self):
        name = self.name.get()
        student_id = self.student_id.get()
        course_name = self.course_name.get()
        final_score = self.final_score_input.get()
        
        toast = ToastNotification(
            title="Enviado com sucesso",
            message="Seus dados foram enviados com sucesso!",
            duration=3000
        )
        toast.show_toast()
        self.data.append({name, student_id, course_name, final_score})
        self.table.destroy()
        self.table = self.create_table()
    
    def on_cancel(self):
        self.quit()

    
    def create_table(self):
        coldata = [
            {"text": "Nome"},
            {"text": "RA", "stretch":False},
            {"text": "Nome do Curso"},
            {"text": "Resultado Final", "stretch" : False}
        ]
        table = Tableview(master=self,coldata=coldata,rowdata=self.data, paginated=True,
                          searchable=True,bootstyle=PRIMARY, stripecolor=(self.colors.light,None))


        table.pack(fill=BOTH, expand=YES, padx=10,pady=10)
        return table
        
    



if __name__ == "__main__":

    app = ttk.Window("Notas Alunos", "vapor", resizable=(False, False))
    Gradebook(app)
    app.mainloop()