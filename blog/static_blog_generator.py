import os
import yaml
import shutil
import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import re
from markdown.extensions import fenced_code, codehilite

class BlogGenerator:
    def __init__(self, config_path='config.yaml'):
        # 获取脚本所在目录的绝对路径
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Base directory: {self.base_dir}")  # 调试信息
        self.config = self._load_config(config_path)
        self.env = Environment(loader=FileSystemLoader(os.path.join(self.base_dir, 'templates')))
        
    def _load_config(self, config_path):
        config_file = os.path.join(self.base_dir, config_path)
        print(f"Loading config from: {config_file}")  # 调试信息
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _convert_markdown(self, content):
        import sys

        def debug_print(*args, **kwargs):
            print(*args, **kwargs, file=sys.stderr, flush=True)

        debug_print("\n=== Start Markdown Processing ===")
        
        # 解析元数据和内容
        lines = content.split('\n')
        meta_content = []
        main_content = []
        in_meta = False
        
        for line in lines:
            if line.strip() == '---':
                if not in_meta:
                    in_meta = True
                    continue
                else:
                    in_meta = False
                    continue
            if in_meta:
                meta_content.append(line)
            else:
                main_content.append(line)
        
        # 不再自动添加 [TOC]，直接使用原始内容
        content_without_meta = '\n'.join(main_content)
        
        # Markdown 配置
        markdown_extensions = [
            'fenced_code',
            'codehilite',
            'toc',
            'meta',
            'tables',
            'attr_list',
        ]
        
        # Markdown 扩展配置
        extension_configs = {
            'codehilite': {
                'css_class': 'highlight',
                'guess_lang': False,
                'use_pygments': True,
                'noclasses': False,
                'linenums': False
            },
            'fenced_code': {
                'lang_prefix': 'language-'
            },
            'toc': {
                'permalink': True,
                'toc_depth': 3,
                'baselevel': 1,
                'toc_class': 'post-toc'
            }
        }
        
        # 创建 Markdown 实例
        md = markdown.Markdown(
            extensions=markdown_extensions,
            extension_configs=extension_configs
        )
        
        # 转换内容
        html = md.convert(content_without_meta)
        
        # 获取目录
        toc = md.toc
        
        # 从内容中移除目录部分
        html = re.sub(r'<div class="post-toc">.*?</div>', '', html, flags=re.DOTALL)
        
        # 解析元数据
        meta = {}
        for line in meta_content:
            if ':' in line:
                key, value = line.split(':', 1)
                meta[key.strip()] = [value.strip()]
        
        return html, meta, toc
    
    def _get_posts(self):
        posts = []
        posts_dir = os.path.join(self.base_dir, 'posts')
        print(f"\n=== Processing Posts from {posts_dir} ===")
        
        if not os.path.exists(posts_dir):
            print(f"Error: Posts directory not found: {posts_dir}")
            return posts
        
        for filename in os.listdir(posts_dir):
            if filename.endswith('.md'):
                print(f"\nProcessing post: {filename}")
                with open(os.path.join(posts_dir, filename), 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(f"File content length: {len(content)}")
                    html, meta, toc = self._convert_markdown(content)
                    
                    # 计算阅读时间（假设每分钟阅读300字）
                    word_count = len(content)
                    read_time = max(1, round(word_count / 300))
                    
                    # 提取第一张图片作为预览图
                    image_match = re.search(r'!\[.*?\]\((.*?)\)', content)
                    image = image_match.group(1) if image_match else None
                    
                    # 生成摘要（提取第一段文字）
                    # 先移除元数据部分
                    content_without_meta = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
                    # 然后找到第一个非空段落
                    paragraphs = content_without_meta.split('\n\n')
                    excerpt = ''
                    for p in paragraphs:
                        # 跳过标题行和空行
                        if p.strip() and not p.strip().startswith('#'):
                            # 移除 Markdown 标记
                            excerpt = re.sub(r'[#*`_\[\]\(\)]+', '', p.strip())
                            break
                    
                    post = {
                        'title': meta.get('title', [filename])[0],
                        'date': meta.get('date', [datetime.now().strftime('%Y-%m-%d')])[0],
                        'content': html,
                        'toc': toc,
                        'url': filename.replace('.md', '.html'),
                        'image': image,
                        'read_time': read_time,
                        'excerpt': excerpt,
                        'tags': meta.get('tags', ['未分类'])[0].split(',')
                    }
                    print("Post processed successfully")
                    posts.append(post)
        
        return sorted(posts, key=lambda x: x['date'], reverse=True)
    
    def _get_tags(self, posts):
        tags = {}
        for post in posts:
            post_tags = post.get('tags', [])
            for tag in post_tags:
                if tag not in tags:
                    tags[tag] = []
                tags[tag].append(post)
        return dict(sorted(tags.items()))
    
    def generate_site(self):
        """生成整个站点"""
        # 确保public目录存在并清空
        public_dir = os.path.join(self.base_dir, 'public')
        print(f"Creating public directory: {public_dir}")  # 调试信息
        
        if os.path.exists(public_dir):
            print("Removing existing public directory")  # 调试信息
            shutil.rmtree(public_dir)
        os.makedirs(public_dir)
        
        # 复制样式文件
        styles_dir = os.path.join(self.base_dir, 'styles')
        public_styles_dir = os.path.join(public_dir, 'styles')
        print(f"Copying styles from {styles_dir} to {public_styles_dir}")  # 调试信息
        
        if not os.path.exists(styles_dir):
            print(f"Styles directory not found: {styles_dir}")  # 调试信息
            os.makedirs(styles_dir)
            
        shutil.copytree(styles_dir, public_styles_dir)
        
        # 复制图片文件夹
        images_dir = os.path.join(self.base_dir, 'images')
        if os.path.exists(images_dir):
            public_images_dir = os.path.join(public_dir, 'images')
            shutil.copytree(images_dir, public_images_dir)
        
        # 生成文章页面
        posts = self._get_posts()
        print(f"Found {len(posts)} posts")  # 调试信息
        
        post_template = self.env.get_template('post.html')
        
        for i, post in enumerate(posts):
            # 添加上一篇和下一篇文章的信息
            prev_post = posts[i + 1] if i + 1 < len(posts) else None
            next_post = posts[i - 1] if i > 0 else None
            
            output_file = os.path.join(public_dir, post['url'])
            output = post_template.render(
                post=post,
                config=self.config,
                active_page='post',
                prev_post=prev_post,  # 添加上一篇文章
                next_post=next_post   # 添加下一篇文章
            )
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
        
        # 获取所有标签
        tags = self._get_tags(posts)
        tags_count = len(tags)  # 获取标签总数
        
        # 生成首页
        index_template = self.env.get_template('index.html')
        index_file = os.path.join(public_dir, 'index.html')
        output = index_template.render(
            posts=posts,
            config=self.config,
            active_page='home',
            tags=tags,  # 传递标签数据
            tags_count=tags_count  # 传递标签数量
        )
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(output)
        
        # 生成标签页
        tags_template = self.env.get_template('tags.html')
        tags_file = os.path.join(public_dir, 'tags.html')
        output = tags_template.render(
            tags=tags,
            config=self.config,
            active_page='tags'
        )
        with open(tags_file, 'w', encoding='utf-8') as f:
            f.write(output)
        
        # 生成关于页面
        about_template = self.env.get_template('about.html')
        about_file = os.path.join(public_dir, 'about.html')
        about_content = ''
        about_path = os.path.join(self.base_dir, 'posts', 'about.md')
        
        if os.path.exists(about_path):
            with open(about_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 使用 _convert_markdown 方法处理内容
                html_content, _, _ = self._convert_markdown(content)
                about_content = html_content
        
        output = about_template.render(
            content=about_content,
            config=self.config,
            active_page='about',
            posts=posts,  # 为了显示文章数量
            tags=tags     # 为了显示标签数量
        )
        
        with open(about_file, 'w', encoding='utf-8') as f:
            f.write(output)

if __name__ == '__main__':
    try:
        generator = BlogGenerator()
        generator.generate_site()
        print("Site generation completed successfully!")  # 调试信息
    except Exception as e:
        print(f"Error generating site: {str(e)}")  # 错误信息
        import traceback
        traceback.print_exc()  # 打印详细的错误堆栈 