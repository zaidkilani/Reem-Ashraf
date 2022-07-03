from odoo import api, fields, models, _

class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'


    bonus_quantity = fields.Integer("Bonus Quantity", compute='_get_bonus_quantity',readonly='False')


    def create(self, vals_list):
        lines = super().create(vals_list)
        for line in lines:
            if line.bonus_quantity != 0 :
                self.env['account.move.line'].with_context(
                check_move_validity=False).create({
                    'price_unit' : 0,
                    'move_id':line.move_id.id,
                    'name':line.name,
                    'account_id':line.account_id.id,
                    'sequence':line.sequence,
                    'quantity':line.bonus_quantity,
                    'partner_id':line.partner_id.id,
                    'product_uom_id':line.product_uom_id.id,
                    'product_id':line.product_id.id,
                    'tax_ids':False,
                    'exclude_from_invoice_tab': False,      # this to make it appear as video or not as document
                })

    @api.onchange('quantity')
    def _get_bonus_quantity(self):
        '''
        this Function responsible for getting and setting bonus quantity value
        '''
        for rec in self :
            if rec.product_id.product_tmpl_id.has_bonus:
                rec.bonus_quantity = (rec.product_id.product_tmpl_id.bonus_quantity) * int(rec.quantity / rec.product_id.product_tmpl_id.ordered_quantity)
            else:
                rec.bonus_quantity = 0
