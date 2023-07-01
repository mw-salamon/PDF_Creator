from fpdf import FPDF

pdf = FPDF('P', 'mm', 'A4')

class PDF(FPDF):
    def create(dict) -> None:
        pdf.set_font('Helvetica', '', 30)

        pdf.add_page()

        pdf.cell(75, 10, '', ln = 0) 
        pdf.cell(55, 10, 'SKUP', ln = 0) 
        pdf.cell(70, 10, 'SPRZEDAZ', ln = 1)

        waluty = ['Albania', 'es']

        for i in range(1, len(waluty)+1):
            pdf.image('Albania.png', 5, (i*45) - 15, h=25)
            pdf.set_font('helvetica', '', 30)
            pdf.text(45, i*45, 'ALL')
            pdf.set_font('helvetica', '', 40)
            pdf.text(80, i*45, '0,0435')
            pdf.text(145, i*45, '0,0485')
        
        pdf.output('ELO.pdf')


