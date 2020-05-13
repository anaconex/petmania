from odoo import models, fields, api
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class ProductProduct(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char('Item ID', index=True)

    def add_product_to_cart(self):
        self.select_products(self._context.get('flag_order'))
        return {
            'type': 'ir.actions.do_nothing'
        }

    def select_products(self, flag_order):
        if flag_order == 'so':
            order_id = self.env['sale.order'].browse(self._context.get('active_id', False))
            if self in order_id.order_line.mapped('product_id'):
                so_line = order_id.order_line.filtered(lambda l: l.product_id.id == self.id)
                if so_line:
                    so_line.write({'product_uom_qty': so_line.product_uom_qty + 1})
            else:
                self.env['sale.order.line'].create({'product_id': self.id, 'product_uom': self.uom_id.id,
                                                    'price_unit': self.lst_price, 'order_id': order_id.id})
        elif flag_order == 'po':
            order_id = self.env['purchase.order'].browse(self._context.get('active_id', False))
            if self in order_id.order_line.mapped('product_id'):
                po_line = order_id.order_line.filtered(lambda l: l.product_id.id == self.id)
                if po_line:
                    po_line.write({'product_qty': po_line.product_qty + 1})
            else:
                self.env['purchase.order.line'].create({'product_id': self.id, 'name': self.name,
                                                        'date_planned': order_id.date_planned or datetime.today().strftime(
                                                            DEFAULT_SERVER_DATETIME_FORMAT),
                                                        'product_uom': self.uom_id.id, 'price_unit': self.lst_price,
                                                        'product_qty': 1.0, 'display_type': False,
                                                        'order_id': order_id.id})
