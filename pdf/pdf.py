


def CreerPresentation(Praticien,Medicament1,Medicament2):
    import os



    # ###################################
    # Content


    PDFTitle = "Fiche de présentation"
    fileName = 'GSB Applivisiteur - Fiche de présentation.pdf'
    documentTitle = 'GSB Applivisiteur - Fiche de présentation'
    image = "image/gsb.png"
    footer = "2022 GSB Applivsiteur"

    textPraticien = f'Praticien : Dr. {Praticien}'

    Title = "Médicament(s) :"

    LabelMedicaments1 = Medicament1["NomMedicament"]
    Composition1 = Medicament1["Composition"]
    Effet1 = Medicament1["Effet(s)"]
    CI1 = Medicament1["Contre-indication(s)"]
    Prix1 = Medicament1["Prix"]

    LabelMedicaments2 = Medicament2["NomMedicament"]
    Composition2 = Medicament2["Composition"]
    Effet2 = Medicament2["Effet(s)"]
    CI2 = Medicament2["Contre-indication(s)"]
    Prix2 = Medicament2["Prix"]

    textMedicament1 = [f'Composition : {Composition1}',f'Effet(s) : {Effet1}',f'Contre-indication(s) : {CI1}',f'Prix : {Prix1}']
    textMedicament2 = [f'Composition : {Composition2}',f'Effet(s) : {Effet2}',f'Contre-indication(s) : {CI2}',f'Prix : {Prix2}']



    # ###################################
    # 0) Create document 
    from reportlab.pdfgen import canvas 
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, Image
    from reportlab.lib.styles import getSampleStyleSheet

    
    username = os.environ.get('USERNAME')
    path = f"C:/Users/{username}/Downloads/"
    pdf = canvas.Canvas(path + fileName)
    pdf.setTitle(documentTitle)
    y = 740
    pdf.drawImage(image, 40, y, width=121, height=67)

    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics

    text = pdf.beginText(250, 750)
    text.setFont("Helvetica", 27)
    text.textLine(PDFTitle)
    pdf.drawText(text)

    pdfmetrics.registerFont(
        TTFont('abc', 'arial.ttf')
    )
    pdf.setFont('abc', 36)

    pdf.setFont("Helvetica", 24)

    y-=40
    text = pdf.beginText(40, y)
    text.setFont("Helvetica", 18)
    text.textLine(textPraticien)

    pdf.drawText(text)

    #Médicaments

    y-=50
    text = pdf.beginText(40, y)
    text.setFont("Helvetica-Bold", 24)
    text.textLine(Title)
    pdf.drawText(text)


    #Informations médicaments 1

    text = pdf.beginText(40, 600)
    text.setFont("Helvetica", 18)
    text.textLine(LabelMedicaments1)
    text.moveCursor(14,20)
    pdf.line(40,595,40+float(len(Medicament1["NomMedicament"])*8.5),595)
    for line in textMedicament1:
        text.textLine(line)
    pdf.drawText(text)

    #Informations médicaments 2
    text = pdf.beginText(40, 450)
    text.setFont("Helvetica", 18)
    text.textLine(LabelMedicaments2)
    text.moveCursor(14,20)
    pdf.line(40,445,40+float(len(Medicament2["NomMedicament"])*8.5),445)
    for line in textMedicament2:
        text.textLine(line)
    pdf.drawText(text)

    text = pdf.beginText(250, 50)
    text.setFont("Helvetica", 10)
    text.textLine(footer)
    pdf.drawText(text)

    pdf.showPage()
    pdf.save()
    os.system(path + fileName)

Praticien = f"Thomas Teynier"
Medicament1 = {"NomMedicament" : "doliprane","Composition" : "truc machin", "Effet(s)" : "test","Contre-indication(s)" :"test", "Prix" : "test"}
Medicament2 = {"NomMedicament" : "couille","Composition" : "test2", "Effet(s)" : "test2","Contre-indication(s)" :"test2", "Prix" : "test2"}
CreerPresentation(Praticien,Medicament1,Medicament2)