# -*- coding = utf-8 -*-
__author__ = 'cannon'
__date__ = '2018/7/2 15:41'

import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader
from xadmin.plugins.utils import get_context_dict

#excel 导入
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    # 这个函数返回true or false。如果为true会加载插件。
    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    def block_top_toolbar(self, context, nodes):
        context = get_context_dict(context or {})  # no error!
        nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html', context=context))


xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)