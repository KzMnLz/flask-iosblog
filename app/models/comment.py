from ..extensions import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # 新增字段
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    reply_to_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    guest_name = db.Column(db.String(50))
    guest_email = db.Column(db.String(120))
    guest_contact = db.Column(db.String(120))
    status = db.Column(db.Enum('pending', 'approved', 'rejected', name='comment_status'), 
                      default='approved')
    
    # 关系定义
    article = db.relationship('Article', backref=db.backref('comments', lazy=True, cascade='all, delete'))
    user = db.relationship('User', back_populates='comments', lazy='joined')
    
    # 评论层级关系
    parent = db.relationship('Comment',
                           backref=db.backref('replies', 
                                            lazy='joined',  # 改为 joined 加载
                                            order_by='Comment.created_at'),  # 添加默认排序
                           remote_side=[id],
                           foreign_keys=[parent_id])
    reply_to = db.relationship('Comment',
                             backref=db.backref('replies_received', lazy=True),
                             remote_side=[id],
                             foreign_keys=[reply_to_id])

    @property
    def display_name(self):
        """显示名称"""
        if self.user_id:
            return self.user.nickname or self.user.username
        return self.guest_name or '游客'

    @property
    def visible_replies(self):
        """获取可见的回复评论"""
        if hasattr(self, 'replies'):
            return [r for r in self.replies if r.status == 'approved']
        return []

    def is_visible(self, user=None):
        """检查评论是否对指定用户可见"""
        if user and user.role == 'admin':
            return True
        return self.status == 'approved'