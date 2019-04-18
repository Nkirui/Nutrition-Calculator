# pos application
from odoo import models, fields, api

#extend the product template model with calories
class forest_hotel(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'
    calories = fields.Integer("Calories")
    serving_size = fields.Float('Serving size')
    date_modified = fields.Date('Date Modified')
    nutrients_ids = fields.One2many('product.template.nutrients','product_id','Nutrients')

    @api.one
    @api.depends('nutrients_ids','nutrients_ids.value')
    def _calcscore(self):
        currentscore = 0
        for nutrient in self.nutrients_ids:
            if nutrient.nutrients_id.name == 'Sodium':
                currentscore = currentscore + (nutrient.value /5)
        self.nutrients_score = currentscore
    nutrients_score = fields.Float(string = "Nutritional Score",compute="_calcscore",store=True)

class Forestdiet_res_users_meal(models.Model):
    _name = 'res.users.meal'
    name = fields.Char("Meal Name")
    meal_date = fields.Datetime("Meal date")
    item_ids = fields.One2many('res.users.mealitem','meal_id')
    user_id = fields.Many2one('res.users','Meal user')
    notes = fields.Text('Meal Notes')

    @api.one
    @api.onchange('totacalories')
    def _check_totalcalories(self):
        if self.totalcalories > 500:
            self.largemeal = True
        else:
            self.largemeal = False
    largemeal = fields.Boolean("Large meal",compute = '_check_totalcalories')

    @api.one
    @api.depends('item_ids','item_ids.servings')
    def _calcalories(self):
        currentcalories = 0
        for mealitem in self.item_ids:
            currentcalories = currentcalories + (mealitem.calories * mealitem.servings)

        self.totalcalories = currentcalories

    totalcalories = fields.Integer(string="Total Meal Calories",store=True,compute="_calcalories")

class Forestdiet_res_users_mealitem(models.Model):
    _name = 'res.users.mealitem'
    meal_id = fields.Many2one('res.users.meal')
    item_id  = fields.Many2one('product.template','Meal Item')
    servings = fields.Float("Servings")
    calories = fields.Integer(related= 'item_id.calories',string= "Calories Per Serving",store=True,readonly=True)
    notes = fields.Text("Meal Item notes")

class Forestdiet_products_nutrients(models.Model):
    _name = 'product.nutrients'
    name = fields.Char("Nutrients Name")
    uom_id = fields.Many2one('product.uom','Unit of Measure')
    description = fields.Text("Description")

class Firestdiet_product_template_nutrients(models.Model):
    _name = 'product.template.nutrients'
    nutrients_id = fields.Many2one('product.nutrients',string='Product Nutrients')
    product_id = fields.Many2one('product.template')
    uom = fields.Char(related='nutrients_id.uom_id.name',string="UOM",readonly=True)
    value = fields.Float('Nutrient Value')
    dailypercent = fields.Float("Daily Recommended Value")


