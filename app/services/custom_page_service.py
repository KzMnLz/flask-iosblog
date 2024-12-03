from app import db
from app.models import CustomPage
from flask import current_app
import os

class CustomPageService:
    @staticmethod
    def get_pages():
        """获取所有自定义页面"""
        try:
            pages = CustomPage.query.order_by(CustomPage.created_at.desc()).all()
            return pages, None
        except Exception as e:
            current_app.logger.error(f"Get custom pages error: {str(e)}")
            return None, str(e)

    @staticmethod
    def get_templates():
        """获取可用的模板文件"""
        try:
            templates = []
            # 检查默认主题的自定义模板目录
            default_template_dir = os.path.join(current_app.template_folder, 'default/custom')
            if os.path.exists(default_template_dir):
                for file in os.listdir(default_template_dir):
                    if file.endswith('.html'):
                        templates.append({
                            'name': file.replace('.html', '').title(),
                            'path': file  # 只保留文件名
                        })
            
            # 检查当前主题的自定义模板目录
            from app.models.site_config import SiteConfig
            current_theme = SiteConfig.get_config('site_theme', 'default')
            if current_theme != 'default':
                theme_custom_path = os.path.join(current_app.template_folder, f'{current_theme}/custom')
                if os.path.exists(theme_custom_path):
                    for file in os.listdir(theme_custom_path):
                        if file.endswith('.html'):
                            templates.append({
                                'name': file.replace('.html', '').title(),
                                'path': file  # 只保留文件名
                            })
            
            if not templates:
                return None, '未找到可用的模板文件,请先在主题的 custom 目录下创建模板'
            
            return templates, None
        except Exception as e:
            current_app.logger.error(f"Get templates error: {str(e)}")
            return None, str(e)

    @staticmethod
    def add_page(data):
        """添加自定义页面"""
        try:
            # 验证key唯一性
            if CustomPage.query.filter_by(key=data['key']).first():
                return False, '页面标识已存在', None
            
            # 如果未指定路由,使用默认规则
            route = data.get('route') or f'/custom/{data["key"]}'
            
            page = CustomPage(
                key=data['key'],
                title=data['title'],
                template=data['template'],
                route=route,
                content=data.get('content', ''),
                fields=data.get('fields', {}),
                require_login=data.get('require_login', False)
            )
            
            db.session.add(page)
            db.session.commit()
            
            # 添加路由
            from app.utils.custom_pages import custom_page_manager
            custom_page_manager.add_page_route(current_app, page)
            
            return True, '添加成功', {
                'id': page.id,
                'key': page.key,
                'title': page.title,
                'route': page.route,
                'content': page.content,
                'fields': page.fields
            }
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Add custom page error: {str(e)}")
            return False, str(e), None

    @staticmethod
    def edit_page(page_id, data):
        """编辑自定义页面"""
        try:
            page = CustomPage.query.get_or_404(page_id)
            
            # 如果修改了key,检查唯一性
            if 'key' in data and data['key'] != page.key:
                if CustomPage.query.filter_by(key=data['key']).first():
                    return False, '页面标识已存在', None
                page.key = data['key']
            
            page.title = data['title']
            page.template = data['template']
            page.route = data.get('route') or f'/custom/{page.key}'
            page.content = data.get('content', '')
            page.fields = data.get('fields', {})
            page.require_login = data.get('require_login', False)
            
            db.session.commit()
            
            # 更新路由
            from app.utils.custom_pages import custom_page_manager
            custom_page_manager.update_page_route(current_app, page)
            
            return True, '更新成功', page
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Edit custom page error: {str(e)}")
            return False, str(e), None

    @staticmethod
    def delete_page(page_id):
        """删除自定义页面"""
        try:
            page = CustomPage.query.get_or_404(page_id)
            db.session.delete(page)
            db.session.commit()
            return True, '删除成功'
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Delete custom page error: {str(e)}")
            return False, str(e)

    @staticmethod
    def get_page(page_id):
        """获取单个页面"""
        try:
            page = CustomPage.query.get_or_404(page_id)
            return True, None, page
        except Exception as e:
            current_app.logger.error(f"Get custom page error: {str(e)}")
            return False, str(e), None 