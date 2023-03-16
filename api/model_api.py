from flask_restx import Api


class ModelApi(Api):
    def init_app(self, app, **kwargs):
        super(ModelApi, self).init_app(app, **kwargs)
        self.namespaces.clear()
