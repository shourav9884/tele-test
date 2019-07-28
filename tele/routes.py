class WareHouseRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'bitcoin':
            return 'btc_db'
        if model._meta.app_label == 'warehouse':
            return 'warehouse_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'bitcoin':
            return 'btc_db'
        if model._meta.app_label == 'warehouse':
            return 'warehouse_db'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # print("db:{}, app_label:{}",db, app_label)
        if app_label == 'warehouse':
            return db == 'warehouse_db'
        if app_label == "bitcoin":
            return db == "btc_db"
        return None