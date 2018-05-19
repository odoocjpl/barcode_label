from odoo import api, models, _
from reportlab.graphics import barcode 
from base64 import b64encode
from odoo.exceptions import Warning


class product_barcode_report_templete(models.AbstractModel):
    _name = 'report.barcode_label.product_barcode_report_template'

    @api.multi
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('barcode_label.product_barcode_report_template')
        docargs = {
           'doc_ids': self.env["small.barcode.label"].browse(data["ids"]),
           'doc_model': report.model,
           'docs': self,
           'get_label_data': self._get_label_data,
           'draw_style': self._draw_style,
           'data': data
        }
        if 'name' in [x.name for x in self.env['small.barcode.label.line'].browse(data['form']['field_lines'])] \
            and data['form']['barcode_type']:
            for product in self.env['small.product.label.qty'].browse(data['form']['product_lines']):
                if not product.product_id.name:
                    continue
                try:
                    barcode_str = barcode.createBarcodeDrawing(
                                    data['form']['barcode_type'], value=product.product_id.name, format='png', width=2000, height=2000)
                except:
                    raise Warning('Select valid barcode type according product barcode value !')
        return report_obj.render('barcode_label.product_barcode_report_template', docargs)

    def _get_barcode_string(self, ean13, data):
       barcode_str = barcode.createBarcodeDrawing(
                           data['barcode_type'], value=ean13, format='png', width=2000,
                           height=2000)
       encoded_string = b64encode(barcode_str.asString('png'))
       barcode_str = "<img style='width:" + str(data['disp_width']) + "px;height:" + str(data['disp_height']) + "px;' src='data:image/png;base64,{0}'>".format(encoded_string)
       return barcode_str

    def _get_label_data(self, form):
        currency_symbol = ''
        if form['currency_id']:
            currency_symbol = self.env['res.currency'].browse(form['currency_id'][0]).symbol
        line_ids = []
        selected_fields = {}
        for line in self.env['small.barcode.label.line'].browse(form['field_lines']):
            selected_fields.update({line.sequence : line.name})
        for product in self.env['small.product.label.qty'].browse(form['product_lines']):
            product_dict = {}
            if 'name' in selected_fields.values() and not product.product_id.name:
                continue
            product_data = product.product_id.read(selected_fields.values())
            for key, value in selected_fields.iteritems():
                if product_data[0].get(value):
                    if value == 'name':
                        barcode_str = self._get_barcode_string(product_data[0].get(value), form)
                        if barcode_str:
                            product_dict.update({key: barcode_str})
                    elif value == 'lst_price':
                        if form['currency_position'] == 'before':
                            product_dict.update({key: currency_symbol + ' ' + str(product_data[0].get(value))})
                        else:
                            product_dict.update({key: str(product_data[0].get(value)) + ' ' + currency_symbol})
                    else:
                        product_dict.update({key: product_data[0].get(value)})
            for no in range(0, product.qty):
                line_ids.append(product_dict)
        return line_ids

    def _draw_style(self, data, field):
        style = ''
        selected_fields = {}
        for line in self.env['small.barcode.label.line'].browse(data['field_lines']):
            selected_fields.update({line.name: str(line.font_size) + '-' + (line.font_color or 'black')})
        for product in self.env['small.product.label.qty'].browse(data['product_lines']):
            if product.product_id.short_name == field:
                style = 'font-size:' + str(selected_fields.get('short_name').split('-')[0]) + 'px;margin-top:10px;color:' + str(selected_fields.get('name').split('-')[1]) + ';'
            elif product.product_id.default_code == field:
                style = 'font-size:' + str(selected_fields.get('default_code').split('-')[0]) + 'px;margin-top:10px;color:' + str(selected_fields.get('default_code').split('-')[1]) + ';'
            elif str(product.product_id.lst_price) in field:
                style = 'font-size:' + str(selected_fields.get('lst_price').split('-')[0]) + 'px;margin-top:10px;color:' + str(selected_fields.get('lst_price').split('-')[1]) + ';'
        return style

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
