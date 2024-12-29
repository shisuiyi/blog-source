# My Blog

这是我的个人博客，使用 Python 静态博客生成器构建。

## 特性

- 支持 Markdown 写作
- 自动代码高亮
- 响应式设计
- 支持明暗主题切换
- 标签分类

## 项目结构

```
blog/
├── templates/          # 模板文件
├── styles/            # CSS 样式文件
├── posts/             # Markdown 文章
├── images/            # 图片资源
│   ├── avatar/        # 头像图片
│   ├── posts/         # 文章图片
│   │   └── default/   # 默认图片
│   └── site/          # 网站通用图片
├── public/            # 生成的静态文件
└── static_blog_generator.py  # 生成器脚本
```

## 初始设置

### 1. 环境准备
```bash
# 安装依赖
pip install pyyaml markdown pygments requests

# 配置 Git
git config --global user.name "shisuiyi"
git config --global user.email "你的邮箱"
```

### 2. 获取代码
```bash
# 克隆源码仓库
git clone git@github.com:shisuiyi/blog-source.git
cd blog-source

# 给部署脚本添加执行权限
chmod +x deploy.sh
```

## 图片管理

图片文件存放在 `blog/images/` 目录下，分为以下类别：

- `avatar/`: 存放头像图片
- `posts/`: 存放文章相关图片
  - `default/`: 默认图片
  - `文章名/`: 每篇文章的图片单独存放
- `site/`: 存放网站通用图片（如 favicon）

### 使用方法

1. 头像：
   - 将头像图片保存为 `blog/images/avatar/avatar.jpg`
   - 在 `config.yaml` 中配置 `avatar` 路径

2. 文章图片：
   - 创建文章同名目录：`blog/images/posts/文章名/`
   - 在文章中使用相对路径引用：`![描述](/images/posts/文章名/图片名)`

3. 默认图片：
   - 默认文章封面：`/images/posts/default/default.jpg`
   - 网站图标：`/images/site/favicon.ico`

## 写作指南

### 1. 创建新文章
- 在 `blog/posts/` 目录下创建 `.md` 文件
- 添加文章元数据：
```yaml
---
title: 文章标题
date: YYYY-MM-DD
tags: [标签1, 标签2]
---
```
- 使用 Markdown 语法编写内容

### 2. 本地预览
```bash
# 生成静态文件
python blog/static_blog_generator.py

# 可以使用 Python 的 http 服务器预览
python -m http.server --directory blog/public 8000
# 然后访问 http://localhost:8000
```

## 部署流程

### 1. 提交源码更新
```bash
# 添加更改
git add .

# 提交更改
git commit -m "更新说明"

# 推送到源码仓库
git push origin main
```

### 2. 部署到 GitHub Pages
```bash
# 执行部署脚本
./deploy.sh
```

## 自动部署

本项目配置了 GitHub Actions：
- 当推送到 main 分支时自动部署
- 配置文件：`.github/workflows/deploy.yml`
- 部署目标：`shisuiyi.github.io`

## 仓库说明

- 源码仓库：`github.com/shisuiyi/blog-source`
  - 存放博客源代码
  - 包含模板、样式、文章等

- 部署仓库：`github.com/shisuiyi/shisuiyi.github.io`
  - 存放生成的静态文件
  - 通过 GitHub Pages 提供访问

## 文件说明

- `deploy.sh`: 部署脚本
- `.gitignore`: Git 忽略文件配置
- `blog/templates/`: 网站模板
- `blog/styles/`: 样式文件
- `blog/posts/`: 博客文章
- `.github/workflows/`: GitHub Actions 配置

## 许可证

MIT 