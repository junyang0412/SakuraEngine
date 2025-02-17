import os

BASE = os.path.dirname(os.path.realpath(__file__).replace("\\", "/"))
class Generator(object):
    def __init__(self):
        pass

    def filter_enum(self, record):
        if not hasattr(record, "target") or not hasattr(record.target, "realized_expr"):
            self.process_type(record)
        if(record.target.realized_expr):
            return True
        return False

    def filter_record(self, record):
        if not hasattr(record, "target") or not hasattr(record.target, "realized_expr"):
            self.process_record(record)
        if(record.target.realized_expr):
            return True
        return False

    def process_type(self, record):
        if hasattr(record.attrs, "inject"):
            record.target = self.db.name_to_record[record.attrs.inject]
        else:
            record.target = record
        record.target.realized_expr = []
        for name, attr in vars(record.attrs).items():
            if name.startswith("StaticCtor"):
                record.target.realized_expr.append(self.realize_record_expr(record.target, attr))

    def process_record(self, record):
        self.process_type(record)
        for fieldname, field in vars(record.target.fields).items():
            for name, attr in vars(field.attrs).items():
                if name.startswith("StaticCtor"):
                    record.target.realized_expr.append(self.realize_field_expr(fieldname, field, record.target, attr))
        for method in record.target.methods:
            for name, attr in vars(method.attrs).items():
                if name.startswith("StaticCtor"):
                    record.target.realized_expr.append(self.realize_method_expr(method.name, record.target, record, attr))

    def realize_common(self, expr : str):
        expr = expr.replace("$module", self.arg.module)
        return expr

    def realize_record_expr(self, record, expr : str): 
        expr = self.realize_common(expr)
        expr = expr.replace("$T", record.name)
        if hasattr(record, "bases") and record.bases:
            expr = expr.replace("$Super", record.bases[0])
        if hasattr(record.attrs, "guid"):
            expr = expr.replace("$guid", "skr_guid_t{%s}"%self.db.guid_constant(record))
        expr = expr.replace("$rtti", "skr::type::type_of<%s>::get()"%record.name)
        return expr

    def realize_field_expr(self, fieldname, field, record, expr):
        expr = self.realize_common(expr)
        expr = expr.replace("$T", field.type)
        expr = expr.replace("$name", "\"%s\""%fieldname)
        expr = expr.replace("$field_ptr", "&{}::{}".format(record.name, fieldname))
        expr = expr.replace("$Owner", record.name)
        expr = expr.replace("$field", "skr_get_field(skr::type::type_of<{}>::get(), \"{}\")".format(record.name, fieldname))
        return expr

    def realize_method_expr(self, methodname, desc, record, expr):
        expr = self.realize_common(expr)
        expr = expr.replace("$name", "\"%s\""%methodname)
        expr = expr.replace("$method_ptr", "({})&{}::{}".format(self.db.signature(desc), record.name, methodname))
        expr = expr.replace("$Owner", record.name)
        #TODO: get method by signature?
        #expr = expr.replace("$method", "skr_get_method(skr::type::type_of<{}>::get(), \"{}\")".format(record.name, methodname))
        return expr
    
    def filter_records(self, records):
        return [record.target for record in records if self.filter_record(record)]

    def filter_enums(self, enums):
        return [enum.target for enum in enums if self.filter_enum(enum)]
    
    def generate_impl(self, db, arg):
        self.db = db
        self.arg = arg
        template = os.path.join(BASE, "static_ctor.cpp.mako")
        if self.filter_enums(db.enums) or self.filter_records(db.records):
            return db.render(template, db=db, generator = self)
        return ""

