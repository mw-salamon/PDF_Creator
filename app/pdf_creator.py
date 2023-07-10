from fpdf import FPDF
from datetime import datetime
import os, tempfile

class PDF(FPDF):
    def create(self, dict):
        self.set_font('Helvetica', '', 30)
        self.add_page()
        self.cell(75, 10, '', ln=0) 
        self.cell(55, 10, 'SKUP', ln=0) 
        self.cell(70, 10, 'SPRZEDAZ', ln=1)
        i = 1
        pdf_name = ''
        for key, value in dict.items():
            self.rect(4.8, (i*45) - 15.2, 40.4, 25.4, 'F')
            self.image(value[0], 5, (i*45) - 15, 40, 25)
            self.set_font('helvetica', '', 30)
            self.text(50, i*45, f'{key}')
            self.set_font('helvetica', '', 40)
            self.text(85, i*45, f'{value[1]}')
            self.text(145, i*45, f'{value[2]}')
            pdf_name += key+"_"
            i += 1
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        pdf_name += date+".pdf"
        pdf_path = os.path.join(tempfile.gettempdir(), pdf_name)
        self.output(pdf_path)
        return pdf_path


