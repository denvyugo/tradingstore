from collections import namedtuple

from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm

font_arial = ttfonts.TTFont('Arial', 'arial.ttf')
pdfmetrics.registerFont(font_arial)

HMARGIN = 20 * mm
RMARGIN = 5 * mm
TMARGIN = 10 * mm
BMARGIN = 20 * mm

def get_vertical():
    num = 270
    while True:
        yield num
        num -= 5

Item = namedtuple('Item', 'name, code, unit, quantity, price')


class ReportInvoice:
    def __init__(self):
        self._info = {}
        self._order=namedtuple('Info', 'date, number, payer, address, delivery')
        self._story = []
        self._data = []
        self._styles = getSampleStyleSheet()

    @staticmethod
    def invoice_file(number):
        """
        get invoice file name by the number of invoice
        :param number: order number
        :return path: invoice file name
        """
        return './invoices/invoice{:06}.pdf'.format(number)

    def set_order(self, date, number, payer, address, delivery):
        self._order.date = date
        self._order.number = number
        self._order.payer = payer
        self._order.address = address
        self._order.delivery = delivery

    def add_item(self, name, code, unit, quantity, price):
        item = Item(name= name,
                    code= code,
                    unit= unit,
                    quantity= quantity,
                    price= price)
        self._data.append(item)

    def _first_page(self, canvas, doc):
        """
        make a top of page with company info
        make a footer
        """
        vertical = get_vertical()
        canvas.saveState()
        canvas.setFont('Arial', 16)
        canvas.drawString(HMARGIN, next(vertical) * mm, self._info['name'])
        canvas.setFont('Arial', 12)
        format_text = 'ИНН/КПП: {}/{}'.format(self._info['taxpayerID'],
                                              self._info['registrationID'])
        canvas.drawString(HMARGIN, next(vertical) * mm, format_text)
        format_text = 'Адресс: {}'.format(self._info['address'])
        canvas.drawString(HMARGIN, next(vertical) * mm, format_text)
        format_text = 'Телефон: {}'.format(self._info['phone'])
        canvas.drawString(HMARGIN, next(vertical) * mm, format_text)
        format_text = 'Эл.почта: {}'.format(self._info['email'])
        canvas.drawString(HMARGIN, next(vertical) * mm, format_text)
        format_text = 'Банк: {}'.format(self._info['bank_account']['name'])
        canvas.drawString(HMARGIN, next(vertical) * mm, format_text)
        format_text = 'БИК: {}'.format(self._info['bank_account']['id'])
        canvas.drawString(HMARGIN, next(vertical) * mm, format_text)
        format_text = 'р/с: {}'.format(self._info['bank_account']['account'])
        canvas.drawString(HMARGIN, next(vertical) * mm, format_text)
        format_text = 'к/с: {}'.format(self._info['bank_account']['corr_acc'])
        canvas.drawString(HMARGIN, next(vertical) * mm, format_text)
        canvas.line(HMARGIN, 228 * mm, 205 * mm, 228 * mm)
        format_text = 'Счёт № {:06} от {:%d.%m.%Y}'.format(self._order.number, self._order.date)
        canvas.drawCentredString(210 / 2 * mm, 222 * mm, format_text)
        format_text = 'Получатель: {}'.format(self._order.payer)
        canvas.drawCentredString(210 / 2 * mm, 217 * mm, format_text)
        canvas.line(HMARGIN, 215 * mm, 205 * mm, 215 * mm)
        self._footer(canvas, str(doc.page))
        canvas.restoreState()

    def _later_page(self, canvas, doc):
        """
        make a footer
        """
        canvas.saveState()
        self._footer(canvas, str(doc.page))
        canvas.restoreState()

    def _footer(self, canvas, page):
        canvas.line(HMARGIN, 10 * mm, 205 * mm, 10 * mm)
        canvas.setFont('Arial', 8)
        canvas.drawString(200 * mm, 6 * mm, page)

    def _order_table(self):
        """
        prepare a data and create a Table
        :return Table: Flowable
        """
        style = self._styles['Normal']
        style.wordWrap = 'CJK'
        style.fontName = 'Arial'
        table_data = [['№', 'Наименование', 'Код', 'Кол-во', 'Ед.изм.', 'Цена', 'Сумма']]
        position = 1
        total_cost = 0.0
        for item in self._data:
            cost = item.price * item.quantity
            table_data.append([str(position),
                               item.name,
                               '',
                               str(item.quantity),
                               item.unit,
                               '{:.2f}'.format(item.price).replace('.', ','),
                               '{:.2f}'.format(round(cost, 2)).replace('.', ',')])
            position += 1
            total_cost += cost
        table_data.append(['', '', '', '', '', 'Итого:', '{:.2f}'.format(total_cost).replace('.', ',')])
        table_data.append(['', '', '', '', '', 'Доставка:', '{:.2f}'.format(self._order.delivery).replace('.', ',')])
        return Table([[Paragraph(cell, style) for cell in row] for row in table_data],
                     colWidths=[10 * mm, 50 * mm, 40 * mm, 20 * mm, 20 * mm, 20 * mm, 25 * mm],
                     style=[
                         ('FONT', (0,0), (-1,-1), 'Arial'),
                         ('GRID', (0,0), (-1,-3), 0.5, colors.black),
                            ])

    def company_info(self, info_dict):
        self._info = info_dict

    def make(self):
        path = self.invoice_file(self._order.number)
        doc = SimpleDocTemplate(path,
                              pagesize = A4,
                              rightMargin = RMARGIN,
                              leftMargin = HMARGIN,
                              topMargin = TMARGIN,
                              bottomMargin = BMARGIN,
                              showBoundary = False)
        self._story.append(Spacer(1, 70 * mm))
        self._story.append(self._order_table())
        doc.build(self._story,
                  onFirstPage=self._first_page,
                  onLaterPages=self._later_page)
