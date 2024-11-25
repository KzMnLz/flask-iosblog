from app import create_app, db
from app.models import User, Article, Tag, Comment, ViewHistory, Category
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

app = create_app()

def init_db():
    with app.app_context():
        # 清空所有表
        db.drop_all()
        db.create_all()
        
        # 创建管理员用户
        admin = User(
            username='admin',
            email='575732022@qq.com',
            password_hash=generate_password_hash('123456'),
            role='admin'
        )
        db.session.add(admin)
        
        # 创建普通用户
        users = []
        for i in range(5):
            user = User(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password_hash=generate_password_hash(f'user{i}123'),
                role='user'
            )
            users.append(user)
            db.session.add(user)
        
        # 创建标签
        tags = []
        tag_names = ['Python', 'Java', 'C++', ' 数据结构 ', ' 算法 ', ' 人工智能 ', ' 机器学习 ', ' 深度学习 ', ' 数据分析 ', ' 数据挖掘 ', ' 大数据 ', ' 云计算 ', ' 区块链 ', ' 网络安全 ', ' 物联网 ', ' 移动开发 ', 'Android', 'iOS', ' 游戏开发 ', ' 图形图像 ', ' 音视频处理 ', ' 数据库设计 ', 'SQL', 'NoSQL', 'MongoDB', 'Redis', 'Web 框架 ', 'Django', 'Flask', 'Spring', 'Hibernate', ' 前端框架 ', 'Vue.js', 'React', 'Angular', 'HTML5', 'CSS3', 'JavaScript', 'TypeScript', 'Node.js', ' 后端开发 ', ' 服务器 ', ' 运维 ', 'Linux', 'Unix', 'Windows 开发 ', ' 软件测试 ', ' 自动化测试 ', ' 性能测试 ', ' 单元测试 ', ' 集成测试 ', ' 系统测试 ', 'UI 设计 ', 'UX 设计 ', ' 交互设计 ', ' 产品设计 ', ' 项目管理 ', ' 敏捷开发 ', ' 瀑布模型 ', ' 迭代开发 ', ' 版本控制 ', 'Git', 'SVN', ' 代码规范 ', ' 编程思想 ', ' 设计模式 ', ' 软件工程 ', ' 计算机网络 ', 'TCP/IP', 'HTTP', 'HTTPS', ' 网络协议 ', ' 路由交换 ', ' 无线网络 ', ' 云计算平台 ', 'AWS', 'Azure', ' 阿里云 ', ' 腾讯云 ', ' 虚拟化技术 ', 'Docker', 'Kubernetes', ' 微服务架构 ', ' 消息队列 ', 'Kafka', 'RabbitMQ', ' 缓存技术 ', ' 数据存储 ', ' 文件系统 ', ' 分布式系统 ', ' 一致性算法 ', ' 分布式数据库 ', ' 数据仓库 ', ' 数据湖 ', ' 数据可视化 ', 'Echarts', 'Tableau', 'PowerBI', ' 商业智能 ', ' 人工智能算法 ', ' 神经网络 ', ' 卷积神经网络 ', ' 循环神经网络 ', ' 自然语言处理 ', ' 语音识别 ', ' 图像识别 ', ' 计算机视觉 ', ' 机器人技术 ', ' 智能硬件 ', ' 传感器技术 ', ' 嵌入式系统 ', ' 电子电路 ', ' 单片机 ', 'PLC 编程 ', ' 工业自动化 ', ' 增材制造 ', '3D 打印 ', ' 虚拟现实 ', ' 增强现实 ', ' 混合现实 ', ' 元宇宙 ', ' 数字孪生 ', ' 教育科技 ', ' 在线教育 ', ' 教育信息化 ', ' 智慧教育 ', ' 金融科技 ', ' 数字货币 ', ' 区块链金融 ', ' 支付系统 ', ' 风控系统 ', ' 保险科技 ', ' 医疗科技 ', ' 医疗信息化 ', ' 电子病历 ', ' 远程医疗 ', ' 医学影像 ', ' 生物识别 ', ' 基因技术 ', ' 精准医疗 ', ' 农业科技 ', ' 智慧农业 ', ' 农业物联网 ', ' 农业大数据 ', ' 无人机植保 ', ' 智能家居 ', ' 智能家电 ', ' 智能照明 ', ' 智能安防 ', ' 智能门锁 ', ' 智能窗帘 ', ' 智能音箱 ', ' 智能手表 ', ' 智能手环 ', ' 智能交通 ', ' 自动驾驶 ', ' 车联网 ', ' 智能物流 ', ' 物流信息化 ', ' 供应链管理 ', ' 电商平台 ', ' 电商运营 ', ' 电商营销 ', ' 跨境电商 ', ' 社交网络 ', ' 社交媒体 ', ' 短视频 ', ' 直播 ', ' 内容创作 ', ' 数字营销 ', ' 搜索引擎优化 ', ' 搜索引擎营销 ', ' 社交媒体营销 ', ' 电子邮件营销 ', ' 内容管理系统 ', 'WordPress', 'Drupal', 'Joomla']
        for name in tag_names:
            tag = Tag(name=name)
            tags.append(tag)
            db.session.add(tag)
        
        # 创建分类
        categories = []
        default_categories = [
            {'name': '技术教程', 'description': '各类技术教程和指南'},
            {'name': '经验分享', 'description': '个人经验和心得分享'},
            {'name': '项目实战', 'description': '实际项目开发经验'},
            {'name': '技术资讯', 'description': '行业新闻和技术动态'},
            {'name': '其他', 'description': '其他类型的文章'},
        ]
        for category_data in default_categories:
            category = Category(**category_data)
            categories.append(category)
            db.session.add(category)
        
        # 提交以获取ID
        db.session.commit()

        # 文章内容模板
        article_contents = [
            '''FlaksIOS风Blog系统，作者QQ：575732022.Flask是一个轻量级的Python Web框架，它提供了基础的核心功能，同时具有很强的可扩展性。本文将介绍Flask的主要特点和基本使用方法。

Flask的设计理念是"微框架"，这意味着它的核心很简单，但可以通过各种扩展来增加功能。它不会强制你使用特定的项目布局或依赖特定的数据库。

Flask的主要优点包括：
1. 轻量级，易于学习
2. 灵活性强，可以根据需求选择组件
3. 详细的文档和活跃的社区
4. 适合小型到中型项目

如果你正在选择Python Web框架，Flask是一个值得考虑的选择。''',

            '''数据库设计是Web开发中的重要环节，好的数据库设计可以提高系统的性能和可维护性。

在设计数据库时，我们需要注意以下几点：
1. 合理的表结构设计
2. 适当的索引使用
3. 关系的正确处理
4. 数据的完整性约束

同时，我们还需要考虑数据库的性能优化，包括查询优化、索引优化等方面。''',

            '''前端开发技术日新月异，作为开发者需要不断学习和更新知识。目前主流的前端技术包括：

1. 现代JavaScript框架（React、Vue、Angular）
2. CSS预处理器（Sass、Less）
3. 构建工具（Webpack、Vite）
4. 响应式设计
5. 性能优化

前端开发不仅要注重功能实现，还要关注用户体验、页面性能和代码质量。'''
        ]
        
        # 创建文章
        articles = []
        for i in range(1000):
            article = Article(
                title=f'技术探讨：{random.choice(["Web开发实践", "数据库优化", "前端技术", "后端架构", "系统设计"])} {i+1}',
                content=random.choice(article_contents),
                author_id=random.choice(users + [admin]).id,
                category_id=random.choice(categories).id,
                created_at=datetime.now() - timedelta(days=random.randint(0, 30)),
                view_count=random.randint(0, 100),
                sentiment_score=random.uniform(-1, 1)
            )
            # 随机添加2-4个标签
            article.tags = random.sample(tags, random.randint(2, 4))
            articles.append(article)
            db.session.add(article)
        
        # 提交以获取文章ID
        db.session.commit()
        
        # 创建评论
        for _ in range(150):
            comment = Comment(
                content=random.choice([
                    '这篇文章讲解得很清楚，对我帮助很大！',
                    '这篇文章太溜了，技术大师！',
                    '文章内容很实用，期待更多类似的分享。',
                    '写得不错，把复杂的概念解释得很通俗易懂。',
                    '这个观点很有意思，值得深入探讨。',
                    '感谢分享，学到了很多新知识。'
                ]),
                article_id=random.choice(articles).id,
                user_id=random.choice(users + [admin]).id,
                created_at=datetime.now() - timedelta(days=random.randint(0, 30))
            )
            db.session.add(comment)
        
        # 创建浏览历史
        for _ in range(100):
            view = ViewHistory(
                user_id=random.choice(users + [admin]).id,
                article_id=random.choice(articles).id,
                viewed_at=datetime.now() - timedelta(days=random.randint(0, 30))
            )
            db.session.add(view)
        
        # 最终提交
        db.session.commit()
        
        print("数据库初始化完成！作者QQ：575732022")
        print("\n测试账号：")
        print("管理员 - 用户名：admin，密码：admin123")
        print("普通用户 - 用户名：user0-4，密码：user0-4123")

if __name__ == '__main__':
    init_db()